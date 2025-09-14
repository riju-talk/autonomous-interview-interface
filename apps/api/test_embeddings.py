import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.services.embeddings_service import groq_embeddings

def test_embeddings():
    # Test with a sample text
    sample_text = "This is a test sentence for generating embeddings."
    
    print("Testing Groq embeddings...")
    embedding = groq_embeddings.get_embedding(sample_text)
    
    if embedding is None:
        print("Failed to get embedding. Check if GROQ_API_KEY is set in your environment variables.")
        return
    
    print(f"Successfully generated embedding with dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}...")
    
    # Test batch embeddings
    print("\nTesting batch embeddings...")
    texts = [
        "First test sentence",
        "Second test sentence",
        "Third test sentence"
    ]
    
    embeddings = groq_embeddings.get_embeddings(texts)
    if embeddings and all(emb is not None for emb in embeddings):
        print(f"Successfully generated {len(embeddings)} embeddings")
        for i, emb in enumerate(embeddings):
            print(f"Text {i+1} embedding dimension: {len(emb) if emb else 'None'}")
    else:
        print("Failed to generate batch embeddings")

if __name__ == "__main__":
    test_embeddings()
