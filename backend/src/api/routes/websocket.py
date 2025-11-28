"""
WebSocket routes
"""
from fastapi import APIRouter, WebSocket, Query
from src.api.websocket.ws_handler import ws_handler
from src.utils.logger import logger


router = APIRouter()


@router.websocket("/ws/{conversation_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    conversation_id: str,
    token: str = Query(...)
):
    """
    WebSocket endpoint for real-time conversation
    
    Args:
        websocket: WebSocket connection
        conversation_id: Conversation ID
        token: JWT authentication token (query parameter)
    """
    logger.info(f"WebSocket connection attempt: conversation={conversation_id}")
    
    await ws_handler.handle_connection(
        websocket,
        conversation_id,
        token
    )
