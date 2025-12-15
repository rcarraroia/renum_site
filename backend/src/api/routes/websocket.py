"""
WebSocket routes - Sprint 09
Real-time communication via WebSocket
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from jose import JWTError, jwt
from datetime import datetime
from src.websocket.connection_manager import get_connection_manager
from src.websocket.handlers import get_handlers
from src.config.settings import settings
from src.utils.logger import logger


router = APIRouter()


async def validate_token(token: str) -> str:
    """
    Validate JWT token and extract user_id
    
    Args:
        token: JWT token
        
    Returns:
        user_id if valid
        
    Raises:
        JWTError if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise JWTError("Invalid token: missing sub")
        return user_id
    except JWTError as e:
        logger.error(f"JWT validation error: {e}")
        raise


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...)
):
    """
    WebSocket endpoint for real-time communication
    
    Connection URL: ws://api/ws?token=JWT_TOKEN
    
    Args:
        websocket: WebSocket connection
        token: JWT authentication token (query parameter)
        
    Message Types (Client → Server):
        - message: Send chat message
        - typing: Typing indicator
        - read: Mark message as read
        - sync: Sync missed messages
        - ping: Keep-alive
        - presence: Update presence status
        - join: Join conversation
        - leave: Leave conversation
        
    Message Types (Server → Client):
        - connected: Connection established
        - message: New message received
        - message_sent: Message sent confirmation
        - typing: Typing indicator
        - read: Message read status
        - presence: User presence update
        - sync_data: Missed messages
        - pong: Keep-alive response
        - error: Error message
    """
    manager = get_connection_manager()
    handlers = get_handlers()
    user_id = None
    
    try:
        # Validate JWT token
        user_id = await validate_token(token)
        
        # Accept connection
        await manager.connect(websocket, user_id)
        
        # Send connected confirmation
        await websocket.send_json({
            "type": "connected",
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        logger.info(f"WebSocket connected: user_id={user_id}")
        
        # Message loop
        while True:
            # Receive message
            data = await websocket.receive_json()
            
            # Get message type
            message_type = data.get("type")
            
            if not message_type:
                await websocket.send_json({
                    "type": "error",
                    "error": "Missing message type",
                    "code": "VALIDATION_ERROR"
                })
                continue
            
            # Route to appropriate handler
            response = None
            
            if message_type == "message":
                response = await handlers.handle_message(user_id, data)
            
            elif message_type == "typing":
                response = await handlers.handle_typing(user_id, data)
            
            elif message_type == "read":
                response = await handlers.handle_read(user_id, data)
            
            elif message_type == "sync":
                response = await handlers.handle_sync(user_id, data)
            
            elif message_type == "ping":
                response = await handlers.handle_ping(user_id, data)
            
            elif message_type == "presence":
                response = await handlers.handle_presence(user_id, data)
            
            elif message_type == "join":
                response = await handlers.handle_join_conversation(user_id, data)
            
            elif message_type == "leave":
                response = await handlers.handle_leave_conversation(user_id, data)
            
            else:
                response = {
                    "type": "error",
                    "error": f"Unknown message type: {message_type}",
                    "code": "UNKNOWN_TYPE"
                }
            
            # Send response
            if response:
                await websocket.send_json(response)
    
    except JWTError:
        # Invalid token - reject connection
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token")
        logger.warning(f"WebSocket rejected: invalid token")
    
    except WebSocketDisconnect:
        # Client disconnected
        if user_id:
            manager.disconnect(user_id)
        logger.info(f"WebSocket disconnected: user_id={user_id}")
    
    except Exception as e:
        # Unexpected error
        logger.error(f"WebSocket error: {e}")
        if user_id:
            manager.disconnect(user_id)
        try:
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR, reason="Internal error")
        except:
            pass
