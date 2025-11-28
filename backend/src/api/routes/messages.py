"""
REST endpoints for Messages
"""
from fastapi import APIRouter, Depends, Query, status, HTTPException, Body
from typing import Optional, List
from src.models.message import MessageCreate, MessageResponse
from src.models.user import UserProfile
from src.services.message_service import message_service
from src.api.middleware.auth_middleware import get_current_user
from src.utils.exceptions import NotFoundError, ValidationError
from src.utils.logger import logger


router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get("", response_model=List[MessageResponse])
async def list_messages(
    conversation_id: str = Query(..., description="Conversation ID"),
    limit: int = Query(50, ge=1, le=100, description="Number of messages to retrieve"),
    before_id: Optional[str] = Query(None, description="Get messages before this message ID"),
    current_user: UserProfile = Depends(get_current_user)
):
    """
    List messages for a conversation with pagination
    
    Query params:
    - conversation_id: Conversation ID (required)
    - limit: Number of messages (default: 50, max: 100)
    - before_id: Get messages before this message ID (for pagination)
    """
    try:
        return await message_service.get_messages(
            conversation_id=conversation_id,
            limit=limit,
            before_id=before_id
        )
    except Exception as e:
        logger.error(f"Error in list_messages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    data: MessageCreate,
    current_user: UserProfile = Depends(get_current_user)
):
    """
    Send message via REST (fallback when WebSocket is not available)
    """
    try:
        return await message_service.send_message(data)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/mark-read", status_code=status.HTTP_200_OK)
async def mark_messages_as_read(
    message_ids: List[str] = Body(..., description="List of message IDs to mark as read"),
    current_user: UserProfile = Depends(get_current_user)
):
    """
    Mark multiple messages as read
    
    Body:
    - message_ids: List of message IDs
    """
    try:
        count = await message_service.mark_messages_as_read(message_ids)
        return {
            "success": True,
            "marked_count": count,
            "message": f"Marked {count} messages as read"
        }
    except Exception as e:
        logger.error(f"Error in mark_messages_as_read: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
