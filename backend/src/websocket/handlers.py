"""
WebSocket Message Handlers - Sprint 09
Handles different types of WebSocket messages
"""

from typing import Dict, Any, Optional
from datetime import datetime
from src.websocket.connection_manager import get_connection_manager
from src.services.conversation_service import ConversationService
from src.utils.logger import logger


class WebSocketHandlers:
    """
    Handles WebSocket message types
    
    Message Types:
    - message: Send/receive chat messages
    - typing: Typing indicator
    - read: Mark messages as read
    - sync: Sync missed messages
    - ping/pong: Keep-alive
    """
    
    def __init__(self):
        self.manager = get_connection_manager()
        self.conversation_service = ConversationService()
    
    async def handle_message(
        self, 
        user_id: str, 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle incoming chat message
        
        Args:
            user_id: Sender user ID
            data: Message data
                {
                    "type": "message",
                    "conversation_id": "uuid",
                    "content": "Hello world"
                }
        
        Returns:
            Response message
        """
        try:
            conversation_id = data.get("conversation_id")
            content = data.get("content")
            
            if not conversation_id or not content:
                return {
                    "type": "error",
                    "error": "Missing conversation_id or content",
                    "code": "VALIDATION_ERROR"
                }
            
            # Save message to database
            message = await self.conversation_service.create_message(
                conversation_id=conversation_id,
                user_id=user_id,
                content=content,
                role="user"
            )
            
            # Broadcast to all participants
            broadcast_data = {
                "type": "message",
                "message": {
                    "id": str(message.id),
                    "conversation_id": str(message.conversation_id),
                    "user_id": str(message.user_id),
                    "content": message.content,
                    "role": message.role,
                    "created_at": message.created_at.isoformat(),
                }
            }
            
            await self.manager.broadcast_to_conversation(
                conversation_id=conversation_id,
                message=broadcast_data,
                exclude=user_id  # Don't send back to sender
            )
            
            logger.info(f"Message sent: user={user_id}, conversation={conversation_id}")
            
            # Return confirmation to sender
            return {
                "type": "message_sent",
                "message_id": str(message.id),
                "timestamp": message.created_at.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            return {
                "type": "error",
                "error": str(e),
                "code": "MESSAGE_ERROR"
            }
    
    async def handle_typing(
        self, 
        user_id: str, 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle typing indicator
        
        Args:
            user_id: User who is typing
            data: Typing data
                {
                    "type": "typing",
                    "conversation_id": "uuid",
                    "is_typing": true
                }
        
        Returns:
            Response message
        """
        try:
            conversation_id = data.get("conversation_id")
            is_typing = data.get("is_typing", False)
            
            if not conversation_id:
                return {
                    "type": "error",
                    "error": "Missing conversation_id",
                    "code": "VALIDATION_ERROR"
                }
            
            # Broadcast typing indicator to participants
            broadcast_data = {
                "type": "typing",
                "user_id": user_id,
                "conversation_id": conversation_id,
                "is_typing": is_typing
            }
            
            await self.manager.broadcast_to_conversation(
                conversation_id=conversation_id,
                message=broadcast_data,
                exclude=user_id  # Don't send back to sender
            )
            
            logger.debug(f"Typing indicator: user={user_id}, typing={is_typing}")
            
            return {
                "type": "typing_sent",
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error handling typing: {e}")
            return {
                "type": "error",
                "error": str(e),
                "code": "TYPING_ERROR"
            }
    
    async def handle_read(
        self, 
        user_id: str, 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle mark as read
        
        Args:
            user_id: User who read the message
            data: Read data
                {
                    "type": "read",
                    "conversation_id": "uuid",
                    "message_id": "uuid"
                }
        
        Returns:
            Response message
        """
        try:
            conversation_id = data.get("conversation_id")
            message_id = data.get("message_id")
            
            if not conversation_id or not message_id:
                return {
                    "type": "error",
                    "error": "Missing conversation_id or message_id",
                    "code": "VALIDATION_ERROR"
                }
            
            # Mark message as read in database
            await self.conversation_service.mark_as_read(
                message_id=message_id,
                user_id=user_id
            )
            
            # Broadcast read status to participants
            broadcast_data = {
                "type": "read",
                "user_id": user_id,
                "conversation_id": conversation_id,
                "message_id": message_id,
                "read_at": datetime.utcnow().isoformat()
            }
            
            await self.manager.broadcast_to_conversation(
                conversation_id=conversation_id,
                message=broadcast_data,
                exclude=user_id  # Don't send back to sender
            )
            
            logger.debug(f"Message marked as read: user={user_id}, message={message_id}")
            
            return {
                "type": "read_sent",
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error handling read: {e}")
            return {
                "type": "error",
                "error": str(e),
                "code": "READ_ERROR"
            }
    
    async def handle_sync(
        self, 
        user_id: str, 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle sync request for missed messages
        
        Args:
            user_id: User requesting sync
            data: Sync data
                {
                    "type": "sync",
                    "conversation_id": "uuid",
                    "last_message_id": "uuid"
                }
        
        Returns:
            Response with missed messages
        """
        try:
            conversation_id = data.get("conversation_id")
            last_message_id = data.get("last_message_id")
            
            if not conversation_id:
                return {
                    "type": "error",
                    "error": "Missing conversation_id",
                    "code": "VALIDATION_ERROR"
                }
            
            # Get messages after last_message_id
            messages = await self.conversation_service.get_messages_after(
                conversation_id=conversation_id,
                after_message_id=last_message_id
            )
            
            # Format messages
            messages_data = [
                {
                    "id": str(msg.id),
                    "conversation_id": str(msg.conversation_id),
                    "user_id": str(msg.user_id),
                    "content": msg.content,
                    "role": msg.role,
                    "created_at": msg.created_at.isoformat(),
                }
                for msg in messages
            ]
            
            logger.info(f"Sync: user={user_id}, messages={len(messages_data)}")
            
            return {
                "type": "sync_data",
                "conversation_id": conversation_id,
                "messages": messages_data,
                "count": len(messages_data)
            }
            
        except Exception as e:
            logger.error(f"Error handling sync: {e}")
            return {
                "type": "error",
                "error": str(e),
                "code": "SYNC_ERROR"
            }
    
    async def handle_ping(
        self, 
        user_id: str, 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle ping (keep-alive)
        
        Args:
            user_id: User ID
            data: Ping data
                {
                    "type": "ping"
                }
        
        Returns:
            Pong response
        """
        # Update last activity
        self.manager.update_presence(user_id, "online")
        
        return {
            "type": "pong",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def handle_presence(
        self, 
        user_id: str, 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle presence update
        
        Args:
            user_id: User ID
            data: Presence data
                {
                    "type": "presence",
                    "status": "online" | "away" | "offline"
                }
        
        Returns:
            Response message
        """
        try:
            status = data.get("status", "online")
            
            # Update presence
            self.manager.update_presence(user_id, status)
            
            # Broadcast presence to all active conversations
            # (In a real app, you'd get user's active conversations from DB)
            broadcast_data = {
                "type": "presence",
                "user_id": user_id,
                "status": status,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # For now, just log it
            # In production, broadcast to relevant users
            logger.debug(f"Presence updated: user={user_id}, status={status}")
            
            return {
                "type": "presence_updated",
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error handling presence: {e}")
            return {
                "type": "error",
                "error": str(e),
                "code": "PRESENCE_ERROR"
            }
    
    async def handle_join_conversation(
        self, 
        user_id: str, 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle user joining a conversation
        
        Args:
            user_id: User ID
            data: Join data
                {
                    "type": "join",
                    "conversation_id": "uuid"
                }
        
        Returns:
            Response message
        """
        try:
            conversation_id = data.get("conversation_id")
            
            if not conversation_id:
                return {
                    "type": "error",
                    "error": "Missing conversation_id",
                    "code": "VALIDATION_ERROR"
                }
            
            # Add user to conversation participants
            self.manager.join_conversation(user_id, conversation_id)
            
            logger.info(f"User joined conversation: user={user_id}, conversation={conversation_id}")
            
            return {
                "type": "joined",
                "conversation_id": conversation_id,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error handling join: {e}")
            return {
                "type": "error",
                "error": str(e),
                "code": "JOIN_ERROR"
            }
    
    async def handle_leave_conversation(
        self, 
        user_id: str, 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle user leaving a conversation
        
        Args:
            user_id: User ID
            data: Leave data
                {
                    "type": "leave",
                    "conversation_id": "uuid"
                }
        
        Returns:
            Response message
        """
        try:
            conversation_id = data.get("conversation_id")
            
            if not conversation_id:
                return {
                    "type": "error",
                    "error": "Missing conversation_id",
                    "code": "VALIDATION_ERROR"
                }
            
            # Remove user from conversation participants
            self.manager.leave_conversation(user_id, conversation_id)
            
            logger.info(f"User left conversation: user={user_id}, conversation={conversation_id}")
            
            return {
                "type": "left",
                "conversation_id": conversation_id,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error handling leave: {e}")
            return {
                "type": "error",
                "error": str(e),
                "code": "LEAVE_ERROR"
            }


# Singleton instance
_handlers = None

def get_handlers() -> WebSocketHandlers:
    """Get singleton instance of WebSocketHandlers"""
    global _handlers
    if _handlers is None:
        _handlers = WebSocketHandlers()
    return _handlers
