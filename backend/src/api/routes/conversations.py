"""
REST endpoints for Conversations
"""
from fastapi import APIRouter, Depends, Query, status, HTTPException
from typing import Optional
from src.models.conversation import ConversationCreate, ConversationUpdate, ConversationResponse
from src.models.user import UserProfile
from src.services.conversation_service import conversation_service
from src.api.middleware.auth_middleware import get_current_user
from src.utils.exceptions import NotFoundError, ValidationError
from src.utils.logger import logger


router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.get("")
async def list_conversations(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    client_id: Optional[str] = Query(None, description="Filter by client ID"),
    status: Optional[str] = Query(None, description="Filter by status (active, closed, pending)"),
    priority: Optional[str] = Query(None, description="Filter by priority (Low, Medium, High)"),
    search: Optional[str] = Query(None, description="Search in summary"),
    current_user: UserProfile = Depends(get_current_user)
):
    """
    List conversations with filters and pagination
    
    Query params:
    - page: Page number (default: 1)
    - limit: Items per page (default: 20, max: 100)
    - client_id: Filter by client
    - status: Filter by status (active, closed, pending)
    - priority: Filter by priority (Low, Medium, High)
    - search: Search in summary
    """
    try:
        return await conversation_service.list_conversations(
            page=page,
            limit=limit,
            client_id=client_id,
            status=status,
            priority=priority,
            search=search
        )
    except Exception as e:
        logger.error(f"Error in list_conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Get conversation by ID"""
    try:
        return await conversation_service.get_conversation_by_id(conversation_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error in get_conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    data: ConversationCreate,
    current_user: UserProfile = Depends(get_current_user)
):
    """Create new conversation"""
    try:
        return await conversation_service.create_conversation(data)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in create_conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: str,
    data: ConversationUpdate,
    current_user: UserProfile = Depends(get_current_user)
):
    """Update conversation"""
    try:
        return await conversation_service.update_conversation(conversation_id, data)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in update_conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{conversation_id}/status", response_model=ConversationResponse)
async def update_conversation_status(
    conversation_id: str,
    status: str = Query(..., description="New status (active, closed, pending)"),
    current_user: UserProfile = Depends(get_current_user)
):
    """Update conversation status"""
    try:
        return await conversation_service.update_status(conversation_id, status)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in update_conversation_status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Delete conversation (soft delete by setting status to closed)"""
    try:
        await conversation_service.delete_conversation(conversation_id)
        return None
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error in delete_conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{conversation_id}/mark-read", response_model=ConversationResponse)
async def mark_conversation_as_read(
    conversation_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Mark all messages in conversation as read"""
    try:
        return await conversation_service.mark_as_read(conversation_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error in mark_conversation_as_read: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
