import os
import logging
from typing import Dict, List, Optional, Any, Union
import uuid
import json
from pathlib import Path

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from app.core.config import settings

logger = logging.getLogger(__name__)

class ChromaService:
    _instance = None
    _client = None
    _collections = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChromaService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the ChromaDB client."""
        try:
            if settings.CHROMA_SERVER:
                # Connect to remote Chroma server
                self._client = chromadb.HttpClient(
                    host=settings.CHROMA_SERVER,
                    port=8000,
                    ssl=False,
                    headers={"Authorization": f"Bearer {settings.CHROMA_AUTH_TOKEN}"} if hasattr(settings, "CHROMA_AUTH_TOKEN") else None
                )
                logger.info(f"Connected to ChromaDB server at {settings.CHROMA_SERVER}")
            else:
                # Use local persistent storage
                chroma_dir = Path(settings.CHROMA_DIR)
                chroma_dir.mkdir(parents=True, exist_ok=True)
                
                self._client = chromadb.PersistentClient(
                    path=str(chroma_dir),
                    settings=Settings(
                        anonymized_telemetry=False,
                        allow_reset=True,
                    )
                )
                logger.info(f"Initialized ChromaDB with local storage at {chroma_dir.absolute()}")
                
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise
    
    def get_or_create_collection(
        self, 
        name: str, 
        embedding_model: str = "all-MiniLM-L6-v2"
    ) -> chromadb.Collection:
        """
        Get or create a Chroma collection with the specified name and embedding model.
        
        Args:
            name: Name of the collection
            embedding_model: Name of the sentence-transformers model to use for embeddings
            
        Returns:
            chromadb.Collection: The requested collection
        """
        if not self._client:
            self._initialize()
            
        if name not in self._collections:
            try:
                # Use sentence-transformers for local embedding generation
                embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name=embedding_model
                )
                
                self._collections[name] = self._client.get_or_create_collection(
                    name=name,
                    embedding_function=embedding_function,
                    metadata={"hnsw:space": "cosine"}  # Use cosine similarity
                )
                logger.info(f"Initialized collection: {name}")
                
            except Exception as e:
                logger.error(f"Failed to get or create collection {name}: {e}")
                raise
                
        return self._collections[name]
    
    async def add_documents(
        self,
        collection_name: str,
        documents: List[Dict[str, Any]],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add documents to a collection with optional metadata and custom IDs.
        
        Args:
            collection_name: Name of the collection
            documents: List of document dictionaries (must contain 'text' key)
            metadatas: Optional list of metadata dictionaries
            ids: Optional list of document IDs
            
        Returns:
            List of document IDs
        """
        collection = self.get_or_create_collection(collection_name)
        
        # Extract texts for embedding
        texts = [doc["text"] for doc in documents]
        
        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in documents]
        
        # Prepare metadatas if not provided
        if metadatas is None:
            metadatas = [{} for _ in documents]
            
        # Add documents to collection
        collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        return ids
    
    async def query(
        self,
        collection_name: str,
        query_texts: Union[str, List[str]],
        n_results: int = 5,
        filter_conditions: Optional[Dict[str, Any]] = None,
        include: Optional[List[str]] = None
    ) -> Dict[str, List]:
        """
        Query the collection for similar documents.
        
        Args:
            collection_name: Name of the collection
            query_texts: Query text or list of query texts
            n_results: Number of results to return
            filter_conditions: Optional filter conditions
            include: Optional list of fields to include in results
            
        Returns:
            Dictionary containing query results
        """
        collection = self.get_or_create_collection(collection_name)
        
        if isinstance(query_texts, str):
            query_texts = [query_texts]
        
        # Default included fields
        if include is None:
            include = ["documents", "metadatas", "distances"]
            
        results = collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=filter_conditions,
            include=include
        )
        
        return results
    
    async def delete_documents(
        self,
        collection_name: str,
        ids: Optional[List[str]] = None,
        filter_conditions: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Delete documents from a collection by IDs or filter conditions.
        
        Args:
            collection_name: Name of the collection
            ids: Optional list of document IDs to delete
            filter_conditions: Optional filter conditions for deletion
        """
        collection = self.get_or_create_collection(collection_name)
        
        if ids:
            collection.delete(ids=ids)
        elif filter_conditions:
            collection.delete(where=filter_conditions)
        else:
            raise ValueError("Either 'ids' or 'filter_conditions' must be provided")
    
    async def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """
        Get statistics about a collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Dictionary containing collection statistics
        """
        collection = self.get_or_create_collection(collection_name)
        
        # Get collection info
        info = {
            "name": collection.name,
            "count": collection.count(),
            "metadata": collection.metadata
        }
        
        return info
    
    def reset(self) -> None:
        """Reset the ChromaDB instance (for testing)."""
        if self._client:
            if settings.CHROMA_SERVER:
                # For server mode, delete all collections
                for collection in self._client.list_collections():
                    self._client.delete_collection(collection.name)
            else:
                # For local mode, reset the entire client
                self._client.reset()
        
        # Clear cached collections
        self._collections = {}

# Global ChromaDB service instance
chroma_service = ChromaService()

def get_chroma_client() -> ChromaService:
    """Dependency to get ChromaDB client."""
    return chroma_service
