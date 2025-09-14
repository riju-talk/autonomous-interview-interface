import os
from typing import List, Optional
import logging
from groq import Groq
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class EmbeddingResponse(BaseModel):
    """Schema for embedding response."""
    embedding: List[float]
    model: str
    usage: dict

class GroqEmbeddings:
    """Service for generating embeddings using Groq."""
    
    def __init__(self, model_name: str = "llama3-70b-8192"):
        """Initialize the Groq embeddings service.
        
        Args:
            model_name: The name of the Groq model to use for embeddings
        """
        self.model_name = model_name
        self.client = self._initialize_client()
    
    def _initialize_client(self) -> Optional[Groq]:
        """Initialize the Groq client."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.warning(
                "GROQ_API_KEY not set. Embeddings functionality will be limited. "
                "Using mock embeddings."
            )
            return None
            
        try:
            client = Groq(api_key=api_key)
            logger.info("Successfully initialized Groq client for embeddings")
            return client
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            return None
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """Get embedding for a single text.
        
        Args:
            text: The text to generate embedding for
            
        Returns:
            List of floats representing the embedding, or None if failed
        """
        if not self.client:
            logger.warning("Groq client not initialized. Using mock embedding.")
            return self._get_mock_embedding()
            
        try:
            response = self.client.embeddings.create(
                model=self.model_name,
                input=text,
                encoding_format="float"
            )
            
            if hasattr(response, 'data') and len(response.data) > 0:
                return response.data[0].embedding
            return None
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None
    
    def get_embeddings(self, texts: List[str]) -> List[Optional[List[float]]]:
        """Get embeddings for multiple texts.
        
        Args:
            texts: List of texts to generate embeddings for
            
        Returns:
            List of embeddings (each is a list of floats or None if failed)
        """
        if not self.client:
            logger.warning("Groq client not initialized. Using mock embeddings.")
            return [self._get_mock_embedding() for _ in texts]
            
        try:
            # Process in batches to handle rate limits
            batch_size = 32  # Adjust based on Groq's rate limits
            all_embeddings = []
            
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                response = self.client.embeddings.create(
                    model=self.model_name,
                    input=batch,
                    encoding_format="float"
                )
                
                if hasattr(response, 'data') and len(response.data) > 0:
                    batch_embeddings = [item.embedding for item in response.data]
                    all_embeddings.extend(batch_embeddings)
                else:
                    all_embeddings.extend([None] * len(batch))
            
            return all_embeddings
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return [None] * len(texts)
    
    def _get_mock_embedding(self, dimension: int = 768) -> List[float]:
        """Generate a mock embedding for testing purposes."""
        return [0.0] * dimension

# Global instance
groq_embeddings = GroqEmbeddings()
