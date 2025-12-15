"""
Memory Models - Agent Memory Chunks
Sprint 10 - SICC Implementation

Models for agent adaptive memory system with vector embeddings.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID
from enum import Enum


class ChunkType(str, Enum):
    """Types of memory chunks - matches DB constraint"""
    BUSINESS_TERM = "business_term"
    PROCESS = "process"
    FAQ = "faq"
    PRODUCT = "product"
    OBJECTION = "objection"
    PATTERN = "pattern"
    INSIGHT = "insight"


class MemoryChunkBase(BaseModel):
    """Base memory chunk model"""
    
    content: str = Field(..., min_length=1, max_length=10000, description="Memory content text")
    chunk_type: ChunkType = Field(..., description="Type of memory chunk")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")
    source: Optional[str] = Field(None, max_length=500, description="Source of this memory")
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score (0-1)")
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Validate content is not empty"""
        if not v or not v.strip():
            raise ValueError("Content cannot be empty")
        return v.strip()


class MemoryChunkCreate(MemoryChunkBase):
    """Model for creating a new memory chunk"""
    
    agent_id: UUID = Field(..., description="Agent ID that owns this memory")
    client_id: UUID = Field(..., description="Client ID that owns this memory")
    embedding: List[float] = Field(..., description="Vector embedding of the content")
    
    @field_validator('embedding')
    @classmethod
    def validate_embedding(cls, v: List[float]) -> List[float]:
        """Validate embedding has correct dimensions (384 for GTE-small)"""
        if len(v) != 384:
            raise ValueError("Embedding must have 384 dimensions for GTE-small model")
        return v


class MemoryChunkUpdate(BaseModel):
    """Model for updating a memory chunk"""
    
    content: Optional[str] = Field(None, min_length=1, max_length=10000)
    chunk_type: Optional[ChunkType] = None
    metadata: Optional[Dict[str, Any]] = None
    source: Optional[str] = Field(None, max_length=500)
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    embedding: Optional[List[float]] = None
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v: Optional[str]) -> Optional[str]:
        """Validate content if provided"""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Content cannot be empty")
        return v.strip() if v else None
    
    @field_validator('embedding')
    @classmethod
    def validate_embedding(cls, v: Optional[List[float]]) -> Optional[List[float]]:
        """Validate embedding dimensions if provided"""
        if v is not None and len(v) != 384:
            raise ValueError("Embedding must have 384 dimensions for GTE-small model")
        return v


class MemoryChunkResponse(MemoryChunkBase):
    """Model for memory chunk responses"""
    
    id: UUID = Field(..., description="Unique identifier")
    agent_id: UUID = Field(..., description="Agent ID that owns this memory")
    version: int = Field(..., description="Version number for tracking changes")
    usage_count: int = Field(default=0, description="Number of times this memory was accessed")
    last_accessed_at: Optional[datetime] = Field(None, description="Last access timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True


class MemorySearchQuery(BaseModel):
    """Model for memory search queries"""
    
    query_text: str = Field(..., min_length=1, max_length=1000, description="Search query text")
    agent_id: UUID = Field(..., description="Agent ID to search memories for")
    chunk_types: Optional[List[ChunkType]] = Field(None, description="Filter by memory types")
    min_confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Minimum confidence threshold")
    min_importance: float = Field(default=0.0, ge=0.0, le=1.0, description="Minimum importance threshold")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum number of results")
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0, description="Minimum similarity score")
    
    @field_validator('query_text')
    @classmethod
    def validate_query_text(cls, v: str) -> str:
        """Validate query text is not empty"""
        if not v or not v.strip():
            raise ValueError("Query text cannot be empty")
        return v.strip()


class MemorySearchResult(BaseModel):
    """Model for memory search results"""
    
    memory: MemoryChunkResponse = Field(..., description="The memory chunk")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Similarity score (0-1)")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Combined relevance score")
    
    class Config:
        from_attributes = True
