"""
API Routes for Discovery Agent Interviews
Sprint 04 - Discovery Agent MVP
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import Optional, Dict, Any, List

from ...models.interview import (
    InterviewCreate,
    Interview,
    InterviewDetail,
    InterviewListResponse,
    MessageRequest,
    MessageResponse
)
from ...services.interview_service import InterviewService
from ...utils.logger import logger


router = APIRouter(prefix="/interviews", tags=["Interviews"])


def get_interview_service() -> InterviewService:
    """Dependency to get InterviewService instance"""
    return InterviewService()


@router.post("", response_model=Interview, status_code=status.HTTP_201_CREATED)
async def create_interview(
    service: InterviewService = Depends(get_interview_service)
):
    """
    Create new interview
    
    Creates a new interview with status 'in_progress' and returns the interview object.
    The Discovery Agent will start collecting data through conversation.
    
    Returns:
        Interview: Created interview with id and initial state
    """
    try:
        interview = await service.create_interview()
        logger.info(f"Interview created via API: {interview.id}")
        return interview
    except Exception as e:
        logger.error(f"Error creating interview: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create interview: {str(e)}"
        )


@router.get("", response_model=InterviewListResponse)
async def list_interviews(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    service: InterviewService = Depends(get_interview_service)
):
    """
    List interviews with pagination and filtering
    
    Query params:
    - status: Filter by status (in_progress, completed, abandoned)
    - limit: Number of results per page (default: 50, max: 100)
    - offset: Offset for pagination (default: 0)
    
    Returns:
        InterviewListResponse: List of interviews with pagination info
    """
    try:
        return await service.list_interviews(
            status=status_filter,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        logger.error(f"Error listing interviews: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list interviews: {str(e)}"
        )


@router.get("/{interview_id}", response_model=InterviewDetail)
async def get_interview_details(
    interview_id: str,
    service: InterviewService = Depends(get_interview_service)
):
    """
    Get interview details with messages and progress
    
    Args:
        interview_id: UUID of the interview
    
    Returns:
        InterviewDetail: Interview with all messages and progress tracking
    
    Raises:
        404: If interview not found
    """
    try:
        details = await service.get_interview_details(interview_id)
        
        if not details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Interview {interview_id} not found"
            )
        
        return details
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting interview details: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get interview details: {str(e)}"
        )


@router.post("/{interview_id}/messages", response_model=MessageResponse)
async def send_message(
    interview_id: str,
    message: MessageRequest,
    service: InterviewService = Depends(get_interview_service)
):
    """
    Send message to interview and get agent response
    
    This endpoint:
    1. Saves the user's message
    2. Processes it through the Discovery Agent
    3. Extracts any data fields from the conversation
    4. Updates the interview with extracted data
    5. Returns the agent's response
    
    Args:
        interview_id: UUID of the interview
        message: MessageRequest with user's message content
    
    Returns:
        MessageResponse: Contains user message, agent response, extracted fields, and progress
    
    Raises:
        404: If interview not found
        400: If interview is already completed
    """
    try:
        response = await service.process_user_message(
            interview_id=interview_id,
            user_message=message.content
        )
        
        return response
    except Exception as e:
        error_msg = str(e)
        
        # Handle specific errors
        if "not found" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_msg
            )
        elif "already completed" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        
        logger.error(f"Error processing message for interview {interview_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )


@router.post("/{interview_id}/complete", response_model=Interview)
async def complete_interview(
    interview_id: str,
    service: InterviewService = Depends(get_interview_service)
):
    """
    Mark interview as complete and generate AI analysis
    
    This endpoint:
    1. Marks the interview as completed
    2. Generates AI analysis of the conversation
    3. Saves the analysis to the interview
    4. Returns the updated interview
    
    Args:
        interview_id: UUID of the interview
    
    Returns:
        Interview: Updated interview with status 'completed' and ai_analysis
    
    Raises:
        404: If interview not found
    """
    try:
        interview = await service.complete_interview(interview_id)
        logger.info(f"Interview {interview_id} completed via API")
        return interview
    except Exception as e:
        error_msg = str(e)
        
        if "not found" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_msg
            )
        
        logger.error(f"Error completing interview {interview_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete interview: {str(e)}"
        )



@router.put("/{interview_id}", response_model=Interview)
async def update_interview(
    interview_id: str,
    update_data: Dict[str, Any],
    service: InterviewService = Depends(get_interview_service)
):
    """
    Update interview data.
    
    Args:
        interview_id: Interview ID
        update_data: Fields to update
        service: Interview service dependency
    
    Returns:
        Updated interview
    
    Raises:
        404: If interview not found
    """
    try:
        # Buscar entrevista
        interview = service.get_interview(interview_id)
        if not interview:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Interview {interview_id} not found"
            )
        
        # Atualizar no Supabase
        from src.config.supabase import supabase_admin
        from datetime import datetime
        
        update_data['updated_at'] = datetime.now().isoformat()
        
        response = supabase_admin.table('interviews')\
            .update(update_data)\
            .eq('id', interview_id)\
            .execute()
        
        if not response.data:
            raise Exception("Failed to update interview")
        
        logger.info(f"Interview {interview_id} updated via API")
        return response.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating interview {interview_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update interview: {str(e)}"
        )


@router.get("/{interview_id}/messages")
async def get_interview_messages(
    interview_id: str,
    limit: int = Query(50, ge=1, le=200, description="Number of messages to return"),
    offset: int = Query(0, ge=0, description="Number of messages to skip"),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Get paginated messages for an interview.
    
    Args:
        interview_id: Interview ID
        limit: Maximum number of messages to return (default: 50, max: 200)
        offset: Number of messages to skip for pagination
        service: Interview service dependency
    
    Returns:
        Paginated list of messages
    
    Raises:
        404: If interview not found
    """
    try:
        # Verificar se entrevista existe
        interview = service.get_interview(interview_id)
        if not interview:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Interview {interview_id} not found"
            )
        
        # Buscar mensagens paginadas
        messages = service.get_messages(interview_id)
        
        # Aplicar paginação
        total = len(messages)
        paginated_messages = messages[offset:offset + limit]
        
        return {
            "interview_id": interview_id,
            "messages": paginated_messages,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting messages for interview {interview_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get messages: {str(e)}"
        )
