"""
Embedding Service - Vector Embeddings for SICC
Sprint 10 - SICC Implementation

Service for generating and managing vector embeddings using GTE-small model.
"""

from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import tiktoken

from src.utils.logger import logger


class EmbeddingService:
    """Service for generating vector embeddings"""
    
    # Model configuration
    PRIMARY_MODEL = "thenlper/gte-small"  # 384 dimensions
    FALLBACK_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # 384 dimensions
    EMBEDDING_DIMENSION = 384
    MAX_TOKENS = 512  # Maximum tokens for GTE-small
    
    def __init__(self):
        """Initialize embedding service with model loading"""
        self.model: Optional[SentenceTransformer] = None
        self.tokenizer = None
        self.model_name = None
        self._load_model()
    
    def _load_model(self) -> None:
        """
        Load embedding model with fallback.
        
        Tries PRIMARY_MODEL first, falls back to FALLBACK_MODEL if needed.
        """
        try:
            logger.info(f"Loading embedding model: {self.PRIMARY_MODEL}")
            self.model = SentenceTransformer(self.PRIMARY_MODEL)
            self.model_name = self.PRIMARY_MODEL
            logger.info(f"Successfully loaded {self.PRIMARY_MODEL}")
            
            # Initialize tokenizer for token counting
            try:
                self.tokenizer = tiktoken.get_encoding("cl100k_base")
            except Exception as e:
                logger.warning(f"Failed to load tiktoken, using approximate counting: {e}")
                self.tokenizer = None
                
        except Exception as e:
            logger.error(f"Failed to load {self.PRIMARY_MODEL}: {e}")
            logger.info(f"Attempting fallback model: {self.FALLBACK_MODEL}")
            
            try:
                self.model = SentenceTransformer(self.FALLBACK_MODEL)
                self.model_name = self.FALLBACK_MODEL
                logger.info(f"Successfully loaded fallback model {self.FALLBACK_MODEL}")
            except Exception as fallback_error:
                logger.error(f"Failed to load fallback model: {fallback_error}")
                raise RuntimeError("Failed to load any embedding model") from fallback_error
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text.
        
        Args:
            text: Text to count tokens for
        
        Returns:
            Number of tokens
        """
        if self.tokenizer:
            try:
                return len(self.tokenizer.encode(text))
            except Exception as e:
                logger.warning(f"Token counting failed, using approximation: {e}")
        
        # Approximate: ~4 characters per token
        return len(text) // 4
    
    def truncate_text(self, text: str, max_tokens: Optional[int] = None) -> str:
        """
        Truncate text to maximum tokens.
        
        Args:
            text: Text to truncate
            max_tokens: Maximum tokens (defaults to MAX_TOKENS)
        
        Returns:
            Truncated text
        """
        max_tokens = max_tokens or self.MAX_TOKENS
        
        if self.count_tokens(text) <= max_tokens:
            return text
        
        # Binary search for optimal truncation point
        left, right = 0, len(text)
        result = text
        
        while left < right:
            mid = (left + right + 1) // 2
            truncated = text[:mid]
            
            if self.count_tokens(truncated) <= max_tokens:
                result = truncated
                left = mid
            else:
                right = mid - 1
        
        logger.warning(f"Text truncated from {len(text)} to {len(result)} characters")
        return result
    
    def generate_embedding(self, text: str, truncate: bool = True) -> List[float]:
        """
        Generate embedding for text.
        
        Args:
            text: Text to embed
            truncate: Whether to truncate text to max tokens
        
        Returns:
            List of floats representing the embedding vector (384 dimensions)
        
        Raises:
            RuntimeError: If model is not loaded
            ValueError: If text is empty
        """
        if not self.model:
            raise RuntimeError("Embedding model not loaded")
        
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        text = text.strip()
        
        # Truncate if needed
        if truncate:
            text = self.truncate_text(text)
        
        try:
            logger.debug(f"Generating embedding for text ({len(text)} chars)")
            
            # Generate embedding
            embedding = self.model.encode(text, convert_to_numpy=True)
            
            # Ensure correct dimensions
            if len(embedding) != self.EMBEDDING_DIMENSION:
                raise ValueError(
                    f"Unexpected embedding dimension: {len(embedding)} "
                    f"(expected {self.EMBEDDING_DIMENSION})"
                )
            
            # Convert to list of floats
            embedding_list = embedding.tolist()
            
            logger.debug(f"Successfully generated embedding with {len(embedding_list)} dimensions")
            return embedding_list
            
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise RuntimeError(f"Embedding generation failed: {e}") from e
    
    def generate_embeddings_batch(
        self,
        texts: List[str],
        truncate: bool = True,
        batch_size: int = 32
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batches.
        
        Args:
            texts: List of texts to embed
            truncate: Whether to truncate texts to max tokens
            batch_size: Batch size for processing
        
        Returns:
            List of embedding vectors
        
        Raises:
            RuntimeError: If model is not loaded
            ValueError: If texts list is empty
        """
        if not self.model:
            raise RuntimeError("Embedding model not loaded")
        
        if not texts:
            raise ValueError("Texts list cannot be empty")
        
        # Filter and truncate texts
        processed_texts = []
        for text in texts:
            if text and text.strip():
                text = text.strip()
                if truncate:
                    text = self.truncate_text(text)
                processed_texts.append(text)
        
        if not processed_texts:
            raise ValueError("No valid texts to embed")
        
        try:
            logger.info(f"Generating embeddings for {len(processed_texts)} texts")
            
            # Generate embeddings in batches
            all_embeddings = []
            
            for i in range(0, len(processed_texts), batch_size):
                batch = processed_texts[i:i + batch_size]
                logger.debug(f"Processing batch {i // batch_size + 1}")
                
                embeddings = self.model.encode(batch, convert_to_numpy=True)
                
                # Convert to list of lists
                batch_embeddings = embeddings.tolist()
                all_embeddings.extend(batch_embeddings)
            
            logger.info(f"Successfully generated {len(all_embeddings)} embeddings")
            return all_embeddings
            
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {e}")
            raise RuntimeError(f"Batch embedding generation failed: {e}") from e
    
    def cosine_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
        
        Returns:
            Similarity score between 0 and 1
        
        Raises:
            ValueError: If embeddings have different dimensions
        """
        if len(embedding1) != len(embedding2):
            raise ValueError("Embeddings must have same dimensions")
        
        # Convert to numpy arrays
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # Calculate cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        
        # Ensure result is between 0 and 1
        similarity = max(0.0, min(1.0, (similarity + 1) / 2))
        
        return float(similarity)
    
    def get_model_info(self) -> dict:
        """
        Get information about loaded model.
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_name": self.model_name,
            "embedding_dimension": self.EMBEDDING_DIMENSION,
            "max_tokens": self.MAX_TOKENS,
            "model_loaded": self.model is not None,
            "tokenizer_available": self.tokenizer is not None
        }


# Singleton instance
_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    """
    Get singleton instance of EmbeddingService.
    
    Returns:
        EmbeddingService instance
    """
    global _embedding_service
    
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    
    return _embedding_service
