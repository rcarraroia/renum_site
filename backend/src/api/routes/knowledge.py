from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Query
from typing import List, Optional
from uuid import UUID

from src.models.knowledge import KnowledgeDocumentResponse, KnowledgeSearchRequest, KnowledgeSearchResult
from src.services.knowledge_service import KnowledgeService
from src.api.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

@router.get("/documents", response_model=List[KnowledgeDocumentResponse])
async def list_documents(
    agent_id: str = Query(..., description="Agent ID (UUID)"),
    current_user: dict = Depends(get_current_user)
):
    """List knowledge documents for an agent"""
    service = KnowledgeService()
    return await service.list_documents(agent_id)

@router.post("/upload", response_model=KnowledgeDocumentResponse)
async def upload_document(
    agent_id: str = Form(...),
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload and index a PDF/TXT document"""
    service = KnowledgeService()
    try:
        return await service.upload_document(agent_id, file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    agent_id: str = Query(...),
    current_user: dict = Depends(get_current_user)
):
    """Delete a document"""
    service = KnowledgeService()
    try:
        await service.delete_document(agent_id, document_id)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=List[KnowledgeSearchResult])
async def search_knowledge(
    request: KnowledgeSearchRequest,
    agent_id: str = Query(...),
    current_user: dict = Depends(get_current_user)
):
    """Test search in knowledge base"""
    service = KnowledgeService()
    return await service.query_knowledge(
        agent_id=agent_id, 
        query=request.query,
        limit=request.limit,
        threshold=request.threshold
    )
