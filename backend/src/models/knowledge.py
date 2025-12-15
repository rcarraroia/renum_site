from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID

class KnowledgeDocumentBase(BaseModel):
    title: str = Field(..., description="Document title or filename")
    description: Optional[str] = Field(None, description="Optional description")
    file_type: str = Field(..., description="File extension/type (pdf, txt, md)")

class KnowledgeDocumentCreate(KnowledgeDocumentBase):
    pass

class KnowledgeDocumentResponse(KnowledgeDocumentBase):
    id: UUID
    agent_id: UUID
    file_path: Optional[str]
    status: str = Field(..., description="indexing, ready, error")
    chunk_count: int
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]

class KnowledgeSearchRequest(BaseModel):
    query: str
    limit: int = 5
    threshold: float = 0.7

class KnowledgeSearchResult(BaseModel):
    content: str
    metadata: Dict[str, Any]
    similarity: float
