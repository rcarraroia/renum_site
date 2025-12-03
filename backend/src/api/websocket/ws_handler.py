"""
WebSocket Handler
Handles WebSocket connections and message routing
"""
import asyncio
import json
from typing import Optional, Dict
from datetime import datetime, timedelta
from fastapi import WebSocket, WebSocketDisconnect
from jose import jwt, JWTError
from src.config.settings import settings
from src.utils.websocket_manager import connection_manager
from src.utils.logger import logger
from src.models.websocket import WSMessageType, WSMessage
from src.models.message import MessageCreate
from src.services.message_service import message_service
from src.services.conversation_service import conversation_service


class WebSocketHandler:
    """Handles WebSocket connections and message routing"""
    
    def __init__(self):
        self.heartbeat_interval = 30  # seconds
        self.rate_limits: Dict[str, Dict] = {}  # {user_id: {messages: count, typing: count, reset_time}}
        self.typing_timers: Dict[str, asyncio.Task] = {}  # {conversation_id: timer_task}
    
    async def handle_connection(
        self,
        websocket: WebSocket,
        conversation_id: str,
        token: str
    ) -> None:
        """
        Main WebSocket connection handler
        
        Args:
            websocket: WebSocket connection
            conversation_id: Conversation ID
            token: JWT authentication token
        """
        user_id = None
        
        try:
            # Authenticate connection BEFORE accepting
            user_id = await self.authenticate_connection(token)
            
            if not user_id:
                # Must accept before closing
                await websocket.accept()
                await websocket.close(code=4001, reason="Unauthorized")
                return
            
            # Verify conversation exists (DISABLED FOR TESTING)
            # TODO: Re-enable after creating test conversation
            # try:
            #     await conversation_service.get_conversation_by_id(conversation_id)
            # except Exception:
            #     # Must accept before closing
            #     await websocket.accept()
            #     await websocket.close(code=4004, reason="Conversation not found")
            #     return
            
            # Accept connection AFTER authentication succeeds
            await websocket.accept()
            
            # Register connection
            await connection_manager.connect(websocket, conversation_id, user_id)
            
            # Send connected confirmation
            await self.send_message(websocket, {
                "type": WSMessageType.CONNECTED,
                "payload": {
                    "conversation_id": conversation_id,
                    "user_id": user_id,
                    "timestamp": datetime.utcnow().isoformat()
                }
            })
            
            # Broadcast presence update
            await connection_manager.broadcast_to_conversation(
                conversation_id,
                {
                    "type": WSMessageType.PRESENCE_UPDATE,
                    "payload": {
                        "user_id": user_id,
                        "status": "online",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )
            
            # Start heartbeat
            heartbeat_task = asyncio.create_task(
                self.heartbeat(websocket, conversation_id, user_id)
            )
            
            # Listen for messages
            while True:
                try:
                    data = await websocket.receive_text()
                    message = json.loads(data)
                    
                    # Handle message
                    await self.handle_message(
                        websocket,
                        message,
                        conversation_id,
                        user_id
                    )
                    
                except WebSocketDisconnect:
                    logger.info(f"WebSocket disconnected: {user_id}")
                    break
                except json.JSONDecodeError:
                    await self.send_error(websocket, "Invalid JSON format")
                except Exception as e:
                    logger.error(f"Error handling message: {str(e)}")
                    await self.send_error(websocket, str(e))
        
        except Exception as e:
            logger.error(f"WebSocket connection error: {str(e)}")
        
        finally:
            # Cleanup
            if user_id:
                # Cancel heartbeat
                if 'heartbeat_task' in locals():
                    heartbeat_task.cancel()
                
                # Disconnect
                await connection_manager.disconnect(websocket, conversation_id, user_id)
                
                # Broadcast offline status after 30 seconds
                await asyncio.sleep(30)
                
                # Check if user is still offline
                if not connection_manager.is_user_connected(user_id, conversation_id):
                    await connection_manager.broadcast_to_conversation(
                        conversation_id,
                        {
                            "type": WSMessageType.PRESENCE_UPDATE,
                            "payload": {
                                "user_id": user_id,
                                "status": "offline",
                                "timestamp": datetime.utcnow().isoformat()
                            }
                        }
                    )
    
    async def authenticate_connection(
        self,
        token: str
    ) -> Optional[str]:
        """
        Authenticate WebSocket connection using JWT token
        
        Args:
            token: JWT token
            
        Returns:
            User ID if authenticated, None otherwise
        """
        try:
            logger.info(f"Attempting to authenticate WebSocket...")
            logger.info(f"Token (first 50 chars): {token[:50]}...")
            
            # Decode JWT token (Supabase token)
            # Use Supabase JWT secret, not application secret
            # Disable audience verification for Supabase tokens
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                options={"verify_aud": False}
            )
            
            logger.info(f"Token decoded successfully. Payload: {payload}")
            
            user_id = payload.get("sub")
            
            # Token is valid if it has a user_id
            # Role verification is done at the profile level, not JWT level
            # Supabase tokens have role="authenticated", not "admin"
            if not user_id:
                logger.warning(f"Token without user_id")
                return None
            
            logger.info(f"WebSocket authenticated: {user_id}")
            return user_id
            
        except JWTError as e:
            logger.error(f"JWT authentication failed: {str(e)}")
            logger.error(f"JWT_SECRET used: {settings.SUPABASE_JWT_SECRET[:20]}...")
            return None
    
    async def handle_message(
        self,
        websocket: WebSocket,
        message: dict,
        conversation_id: str,
        user_id: str
    ) -> None:
        """
        Process incoming WebSocket message
        
        Args:
            websocket: WebSocket connection
            message: Message data
            conversation_id: Conversation ID
            user_id: User ID
        """
        try:
            # Validate message format
            if "type" not in message:
                await self.send_error(websocket, "Missing message type")
                return
            
            message_type = message["type"]
            payload = message.get("payload", {})
            
            # Check rate limits
            if not await self.check_rate_limit(user_id, message_type):
                await self.send_error(websocket, "Rate limit exceeded")
                return
            
            # Route message
            if message_type == WSMessageType.SEND_MESSAGE:
                await self.handle_send_message(websocket, payload, conversation_id, user_id)
            
            elif message_type == WSMessageType.TYPING_START:
                await self.handle_typing_start(conversation_id, user_id)
            
            elif message_type == WSMessageType.TYPING_STOP:
                await self.handle_typing_stop(conversation_id, user_id)
            
            elif message_type == WSMessageType.MARK_READ:
                await self.handle_mark_read(payload, conversation_id)
            
            else:
                await self.send_error(websocket, f"Unknown message type: {message_type}")
        
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            await self.send_error(websocket, str(e))
    
    async def handle_send_message(
        self,
        websocket: WebSocket,
        payload: dict,
        conversation_id: str,
        user_id: str
    ) -> None:
        """
        Handle SEND_MESSAGE type
        
        Args:
            websocket: WebSocket connection
            payload: Message payload
            conversation_id: Conversation ID
            user_id: User ID
        """
        try:
            # Verify conversation is not closed
            conversation = await conversation_service.get_conversation_by_id(conversation_id)
            
            if conversation.status == 'closed':
                await self.send_error(websocket, "Cannot send message to closed conversation")
                return
            
            # Create message
            message_data = MessageCreate(
                conversation_id=conversation_id,
                sender='admin',
                type=payload.get('type', 'text'),
                content=payload.get('content', ''),
                metadata=payload.get('metadata')
            )
            
            # Save message
            saved_message = await message_service.send_message(message_data)
            
            # Broadcast to all connections in conversation
            await connection_manager.broadcast_to_conversation(
                conversation_id,
                {
                    "type": WSMessageType.NEW_MESSAGE,
                    "payload": saved_message.model_dump(mode='json'),
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
            logger.info(f"Message sent: {saved_message.id}")
            
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            await self.send_error(websocket, str(e))
    
    async def handle_typing_start(
        self,
        conversation_id: str,
        user_id: str
    ) -> None:
        """
        Handle TYPING_START event
        
        Args:
            conversation_id: Conversation ID
            user_id: User ID
        """
        # Broadcast typing indicator
        await connection_manager.broadcast_to_conversation(
            conversation_id,
            {
                "type": WSMessageType.USER_TYPING,
                "payload": {
                    "user_id": user_id,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )
        
        # Set auto-clear timer (3 seconds)
        timer_key = f"{conversation_id}:{user_id}"
        
        # Cancel existing timer
        if timer_key in self.typing_timers:
            self.typing_timers[timer_key].cancel()
        
        # Create new timer
        self.typing_timers[timer_key] = asyncio.create_task(
            self.auto_clear_typing(conversation_id, user_id)
        )
    
    async def handle_typing_stop(
        self,
        conversation_id: str,
        user_id: str
    ) -> None:
        """
        Handle TYPING_STOP event
        
        Args:
            conversation_id: Conversation ID
            user_id: User ID
        """
        # Cancel timer
        timer_key = f"{conversation_id}:{user_id}"
        if timer_key in self.typing_timers:
            self.typing_timers[timer_key].cancel()
            del self.typing_timers[timer_key]
        
        # Broadcast stop typing
        await connection_manager.broadcast_to_conversation(
            conversation_id,
            {
                "type": WSMessageType.USER_STOPPED_TYPING,
                "payload": {
                    "user_id": user_id,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )
    
    async def auto_clear_typing(
        self,
        conversation_id: str,
        user_id: str
    ) -> None:
        """
        Auto-clear typing indicator after 3 seconds
        
        Args:
            conversation_id: Conversation ID
            user_id: User ID
        """
        await asyncio.sleep(3)
        await self.handle_typing_stop(conversation_id, user_id)
    
    async def handle_mark_read(
        self,
        payload: dict,
        conversation_id: str
    ) -> None:
        """
        Handle MARK_READ event
        
        Args:
            payload: Message payload with message_ids
            conversation_id: Conversation ID
        """
        try:
            message_ids = payload.get('message_ids', [])
            
            if message_ids:
                await message_service.mark_messages_as_read(message_ids)
                logger.info(f"Marked {len(message_ids)} messages as read")
            
        except Exception as e:
            logger.error(f"Error marking messages as read: {str(e)}")
    
    async def heartbeat(
        self,
        websocket: WebSocket,
        conversation_id: str,
        user_id: str
    ) -> None:
        """
        Send periodic heartbeat to keep connection alive
        
        Args:
            websocket: WebSocket connection
            conversation_id: Conversation ID
            user_id: User ID
        """
        try:
            while True:
                await asyncio.sleep(self.heartbeat_interval)
                
                # Send ping
                await websocket.send_json({
                    "type": "ping",
                    "timestamp": datetime.utcnow().isoformat()
                })
                
        except Exception as e:
            logger.debug(f"Heartbeat stopped: {str(e)}")
    
    async def check_rate_limit(
        self,
        user_id: str,
        message_type: str
    ) -> bool:
        """
        Check rate limits for user
        
        Args:
            user_id: User ID
            message_type: Message type
            
        Returns:
            True if within limits, False otherwise
        """
        now = datetime.utcnow()
        
        # Initialize rate limit tracking
        if user_id not in self.rate_limits:
            self.rate_limits[user_id] = {
                "messages": 0,
                "typing": 0,
                "reset_time": now + timedelta(minutes=1)
            }
        
        limits = self.rate_limits[user_id]
        
        # Reset if time window passed
        if now >= limits["reset_time"]:
            limits["messages"] = 0
            limits["typing"] = 0
            limits["reset_time"] = now + timedelta(minutes=1)
        
        # Check limits
        if message_type == WSMessageType.SEND_MESSAGE:
            if limits["messages"] >= 100:
                return False
            limits["messages"] += 1
        
        elif message_type in [WSMessageType.TYPING_START, WSMessageType.TYPING_STOP]:
            if limits["typing"] >= 10:
                return False
            limits["typing"] += 1
        
        return True
    
    async def send_message(
        self,
        websocket: WebSocket,
        message: dict
    ) -> None:
        """
        Send message to WebSocket
        
        Args:
            websocket: WebSocket connection
            message: Message to send
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {str(e)}")
    
    async def send_error(
        self,
        websocket: WebSocket,
        error: str
    ) -> None:
        """
        Send error message to WebSocket
        
        Args:
            websocket: WebSocket connection
            error: Error message
        """
        await self.send_message(websocket, {
            "type": WSMessageType.ERROR,
            "payload": {
                "error": error,
                "timestamp": datetime.utcnow().isoformat()
            }
        })


# Global instance
ws_handler = WebSocketHandler()
