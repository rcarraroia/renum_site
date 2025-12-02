# Design Document - Sprint 03: Conversações e WebSocket

## Overview

This design document outlines the architecture for implementing a real-time conversation system using WebSocket technology. The system enables bidirectional communication between admins and clients with features including instant messaging, typing indicators, presence tracking, and automatic reconnection. The architecture follows a layered approach with clear separation between transport (WebSocket), business logic (services), and data persistence (Supabase).

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                          │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Conversations│  │  ChatWindow  │  │ MessageList  │     │
│  │     Page     │  │              │  │              │     │
│  │              │  │  - Messages  │  │  - History   │     │
│  │  - List      │  │  - Input     │  │  - Scroll    │     │
│  │  - Search    │  │  - Typing    │  │  - Pagination│     │
│  │  - Filter    │  │  - Presence  │  │              │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
│         ┌──────────────────▼──────────────────┐             │
│         │    WebSocket Service (Client)       │             │
│         │  - Connection management            │             │
│         │  - Message queue                    │             │
│         │  - Reconnection logic               │             │
│         │  - Event handlers                   │             │
│         └──────────────────┬──────────────────┘             │
└────────────────────────────┼──────────────────────────────┘
                             │
                    WSS (WebSocket Secure)
                             │
┌────────────────────────────▼──────────────────────────────┐
│                  BACKEND (FastAPI)                         │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │         WebSocket Handler (/ws/{conversation_id})    │ │
│  │  - Authentication                                    │ │
│  │  - Connection lifecycle                             │ │
│  │  - Message routing                                  │ │
│  └──────────────────┬───────────────────────────────────┘ │
│                     │                                      │
│  ┌──────────────────▼───────────────────────────────────┐ │
│  │           Connection Manager                         │ │
│  │  - Active connections: Dict[str, WebSocket]         │ │
│  │  - Broadcast to conversation                        │ │
│  │  - Broadcast to all                                 │ │
│  │  - Presence tracking                                │ │
│  └──────────────────┬───────────────────────────────────┘ │
│                     │                                      │
│  ┌──────────────────▼───────────────────────────────────┐ │
│  │              Services Layer                          │ │
│  │  ┌────────────────┐  ┌────────────────┐             │ │
│  │  │ Conversation   │  │   Message      │             │ │
│  │  │   Service      │  │   Service      │             │ │
│  │  │                │  │                │             │ │
│  │  │ - Create       │  │ - Send         │             │ │
│  │  │ - List         │  │ - Receive      │             │ │
│  │  │ - Update       │  │ - Mark read    │             │ │
│  │  │ - Delete       │  │ - History      │             │ │
│  │  └────────────────┘  └────────────────┘             │ │
│  └──────────────────┬───────────────────────────────────┘ │
└─────────────────────┼──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│              SUPABASE (PostgreSQL)                          │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │  conversations   │  │    messages      │               │
│  │                  │  │                  │               │
│  │  - id            │  │  - id            │               │
│  │  - client_id     │  │  - conversation_id│              │
│  │  - status        │  │  - sender        │               │
│  │  - channel       │  │  - content       │               │
│  │  - assigned_agent│  │  - timestamp     │               │
│  │  - unread_count  │  │  - is_read       │               │
│  │  - priority      │  │  - metadata      │               │
│  │  - last_update   │  │                  │               │
│  └──────────────────┘  └──────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

### Message Flow

```
1. Admin sends message:
   Frontend → WebSocket → Backend Handler → Validate → Save to DB → 
   Broadcast to all connected → Update UI

2. Admin receives message:
   External source → Backend → Save to DB → Broadcast via WebSocket → 
   Frontend receives → Update UI → Mark as read

3. Typing indicator:
   Frontend (typing) → WebSocket → Backend → Broadcast to conversation → 
   Other clients receive → Show indicator → Auto-clear after 3s

4. Reconnection:
   Connection lost → Frontend detects → Wait backoff → Attempt reconnect → 
   Success → Sync state → Resume normal operation
```

## Components and Interfaces

### Backend Components

#### 1. WebSocket Handler (`src/api/websocket/ws_handler.py`)

```python
class WebSocketHandler:
    """Handles WebSocket connections and message routing"""
    
    async def handle_connection(
        websocket: WebSocket,
        conversation_id: str,
        token: str
    ) -> None:
        """
        Main WebSocket connection handler
        - Authenticates user
        - Registers connection
        - Listens for messages
        - Handles disconnection
        """
    
    async def handle_message(
        websocket: WebSocket,
        message: dict,
        conversation_id: str
    ) -> None:
        """
        Processes incoming WebSocket messages
        - Validates message format
        - Routes to appropriate handler
        - Sends response
        """
```

#### 2. Connection Manager (`src/utils/websocket_manager.py`)

```python
class ConnectionManager:
    """Manages active WebSocket connections"""
    
    active_connections: Dict[str, List[WebSocket]]
    
    async def connect(
        self,
        websocket: WebSocket,
        conversation_id: str
    ) -> None:
        """Register new connection"""
    
    async def disconnect(
        self,
        websocket: WebSocket,
        conversation_id: str
    ) -> None:
        """Remove connection"""
    
    async def broadcast_to_conversation(
        self,
        conversation_id: str,
        message: dict
    ) -> None:
        """Send message to all connections in a conversation"""
    
    async def broadcast_to_all(
        self,
        message: dict
    ) -> None:
        """Send message to all active connections"""
```

#### 3. Conversation Service (`src/services/conversation_service.py`)

```python
class ConversationService:
    """Business logic for conversations"""
    
    def create_conversation(
        self,
        client_id: str,
        channel: str,
        assigned_agent_id: str
    ) -> Conversation:
        """Create new conversation"""
    
    def list_conversations(
        self,
        filters: ConversationFilters,
        page: int,
        page_size: int
    ) -> List[Conversation]:
        """List conversations with filters and pagination"""
    
    def update_status(
        self,
        conversation_id: str,
        status: str
    ) -> Conversation:
        """Update conversation status"""
    
    def mark_as_read(
        self,
        conversation_id: str,
        admin_id: str
    ) -> None:
        """Mark all messages in conversation as read"""
```

#### 4. Message Service (`src/services/message_service.py`)

```python
class MessageService:
    """Business logic for messages"""
    
    def send_message(
        self,
        conversation_id: str,
        sender: str,
        content: str,
        metadata: dict
    ) -> Message:
        """Send and persist message"""
    
    def get_messages(
        self,
        conversation_id: str,
        limit: int,
        before_id: Optional[str]
    ) -> List[Message]:
        """Get message history with pagination"""
    
    def mark_as_read(
        self,
        message_ids: List[str]
    ) -> None:
        """Mark messages as read"""
```

### Frontend Components

#### 1. WebSocket Service (`src/services/websocketService.ts`)

```typescript
class WebSocketService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private messageQueue: Message[] = [];
  
  connect(conversationId: string, token: string): void
  disconnect(): void
  sendMessage(message: Message): void
  onMessage(callback: (message: Message) => void): void
  onConnectionChange(callback: (status: ConnectionStatus) => void): void
}
```

#### 2. useWebSocket Hook (`src/hooks/useWebSocket.ts`)

```typescript
function useWebSocket(conversationId: string) {
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  
  useEffect(() => {
    // Connect on mount
    // Cleanup on unmount
  }, [conversationId]);
  
  const sendMessage = (content: string) => {
    // Send via WebSocket
  };
  
  return { isConnected, messages, sendMessage };
}
```

## Data Models

### Backend Models

#### Conversation Model (`src/models/conversation.py`)

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class ConversationBase(BaseModel):
    client_id: UUID
    status: str  # 'active', 'closed', 'pending'
    channel: str  # 'whatsapp', 'email', 'web'
    assigned_agent_id: Optional[UUID] = None
    priority: str = 'Low'  # 'Low', 'Medium', 'High'
    summary: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(BaseModel):
    status: Optional[str] = None
    assigned_agent_id: Optional[UUID] = None
    priority: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[List[str]] = None

class ConversationResponse(ConversationBase):
    id: UUID
    unread_count: int
    start_date: datetime
    last_update: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

#### Message Model (`src/models/message.py`)

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class MessageBase(BaseModel):
    conversation_id: UUID
    sender: str  # 'admin', 'client', 'system'
    type: str  # 'text', 'image', 'file'
    content: str
    metadata: Optional[dict] = None

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: UUID
    timestamp: datetime
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
```

### WebSocket Message Types

```python
class WSMessageType(str, Enum):
    # Client → Server
    SEND_MESSAGE = "send_message"
    TYPING_START = "typing_start"
    TYPING_STOP = "typing_stop"
    MARK_READ = "mark_read"
    
    # Server → Client
    NEW_MESSAGE = "new_message"
    USER_TYPING = "user_typing"
    USER_STOPPED_TYPING = "user_stopped_typing"
    PRESENCE_UPDATE = "presence_update"
    ERROR = "error"
    CONNECTED = "connected"

class WSMessage(BaseModel):
    type: WSMessageType
    payload: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: WebSocket Authentication

*For any* WebSocket connection attempt, the connection SHALL only be established if a valid JWT token is provided and the user has admin role.

**Validates: Requirements 1.2**

### Property 2: Message Persistence

*For any* message sent via WebSocket, the message SHALL be persisted to the database before being broadcast to other clients.

**Validates: Requirements 4.2**

### Property 3: Message Ordering

*For any* sequence of messages in a conversation, when retrieved from the database, they SHALL be ordered by timestamp in ascending order.

**Validates: Requirements 6.1, 6.2**

### Property 4: Broadcast Consistency

*For any* message broadcast to a conversation, all connected WebSocket clients for that conversation SHALL receive the message exactly once.

**Validates: Requirements 4.3, 5.1**

### Property 5: Unread Count Accuracy

*For any* conversation, the unread_count field SHALL equal the number of messages where is_read=false for that conversation.

**Validates: Requirements 5.3**

### Property 6: Typing Indicator Timeout

*For any* typing indicator event, if no subsequent typing event or message is received within 3 seconds, the typing indicator SHALL be automatically cleared.

**Validates: Requirements 7.3**

### Property 7: Reconnection Idempotency

*For any* WebSocket reconnection, messages sent during disconnection SHALL be delivered exactly once when connection is restored, with no duplicates.

**Validates: Requirements 10.1, 10.2, 10.4**

### Property 8: Status Transition Validity

*For any* conversation status update, the new status SHALL be one of the valid values ('active', 'closed', 'pending') and the transition SHALL be logged.

**Validates: Requirements 9.1, 9.5**

### Property 9: Closed Conversation Immutability

*For any* conversation with status='closed', attempts to send new messages SHALL be rejected with an error.

**Validates: Requirements 9.3, 9.4**

### Property 10: Message Read Propagation

*For any* set of messages marked as read, the is_read field SHALL be updated in the database and the conversation's unread_count SHALL be decremented accordingly.

**Validates: Requirements 5.5, 6.4**

### Property 11: Presence Staleness Detection

*For any* WebSocket connection, if no heartbeat is received within 30 seconds, the user SHALL be marked as offline.

**Validates: Requirements 8.2, 8.5**

### Property 12: Error Recovery

*For any* WebSocket error that occurs, the system SHALL log the error with full context and attempt recovery without data loss.

**Validates: Requirements 11.1, 11.5**

## Error Handling

### WebSocket Errors

1. **Connection Refused**: Invalid token or unauthorized user
   - Response: Close connection with code 4001
   - Action: Redirect to login

2. **Message Validation Failed**: Invalid message format
   - Response: Send error message via WebSocket
   - Action: Log error, don't persist message

3. **Database Error**: Failed to save message
   - Response: Send error to sender
   - Action: Retry up to 3 times, then fail gracefully

4. **Broadcast Failed**: Unable to send to some clients
   - Response: Log failed deliveries
   - Action: Continue with successful deliveries

### Reconnection Strategy

```python
def calculate_backoff(attempt: int) -> int:
    """Exponential backoff: 1s, 2s, 4s, 8s, 16s (max)"""
    return min(2 ** attempt, 16)
```

### Rate Limiting

- Max 100 messages per minute per user
- Max 10 typing events per minute per user
- Exceeded: Return 429 error, throttle for 60 seconds

## Testing Strategy

### Unit Tests

1. **Connection Manager Tests**
   - Test connection registration
   - Test disconnection cleanup
   - Test broadcast to conversation
   - Test broadcast to all

2. **Service Tests**
   - Test conversation CRUD operations
   - Test message persistence
   - Test unread count updates
   - Test status transitions

3. **Model Validation Tests**
   - Test Pydantic model validation
   - Test invalid data rejection
   - Test enum constraints

### Property-Based Tests

Property-based tests will use **Hypothesis** library for Python and **fast-check** for TypeScript. Each test will run a minimum of 100 iterations.

1. **Property Test: Message Ordering**
   - Generate random sequences of messages
   - Insert into database
   - Verify retrieval order matches timestamp order
   - **Feature: sprint-03-conversations-websocket, Property 3: Message Ordering**

2. **Property Test: Unread Count Accuracy**
   - Generate random conversations with messages
   - Randomly mark some as read
   - Verify unread_count equals count of is_read=false
   - **Feature: sprint-03-conversations-websocket, Property 5: Unread Count Accuracy**

3. **Property Test: Status Transition Validity**
   - Generate random status transitions
   - Verify only valid statuses are accepted
   - Verify invalid statuses are rejected
   - **Feature: sprint-03-conversations-websocket, Property 8: Status Transition Validity**

4. **Property Test: Closed Conversation Immutability**
   - Generate conversations with status='closed'
   - Attempt to send messages
   - Verify all attempts are rejected
   - **Feature: sprint-03-conversations-websocket, Property 9: Closed Conversation Immutability**

5. **Property Test: Message Read Propagation**
   - Generate conversations with unread messages
   - Mark random subsets as read
   - Verify unread_count decrements correctly
   - **Feature: sprint-03-conversations-websocket, Property 10: Message Read Propagation**

### Integration Tests

1. **WebSocket Connection Test**
   - Establish connection with valid token
   - Verify connection accepted
   - Send test message
   - Verify message received

2. **End-to-End Message Flow**
   - Create conversation
   - Connect two clients
   - Send message from client 1
   - Verify client 2 receives message
   - Verify message persisted in database

3. **Reconnection Test**
   - Establish connection
   - Force disconnect
   - Verify automatic reconnection
   - Verify queued messages delivered

### Manual Testing Checklist

1. Open conversations page → WebSocket connects
2. Create new conversation → Appears in list
3. Send message → Appears immediately
4. Open same conversation in another tab → Both receive messages
5. Close one tab → Other tab still works
6. Disconnect internet → Shows offline indicator
7. Reconnect internet → Automatically reconnects
8. Type in input → Other users see typing indicator
9. Stop typing → Indicator disappears after 3s
10. Mark conversation as closed → Cannot send new messages

## Performance Considerations

### Scalability Targets

- Support 1000+ concurrent WebSocket connections
- Message latency < 100ms
- Database query time < 50ms
- Memory usage < 512MB per 1000 connections

### Optimization Strategies

1. **Connection Pooling**: Reuse database connections
2. **Message Batching**: Batch database writes when possible
3. **Lazy Loading**: Load messages on demand, not all at once
4. **Indexing**: Ensure proper indexes on conversation_id and timestamp
5. **Caching**: Cache conversation metadata in Redis (future)

## Security Considerations

1. **Authentication**: All WebSocket connections must provide valid JWT
2. **Authorization**: Verify user has access to conversation
3. **Input Validation**: Sanitize all message content
4. **Rate Limiting**: Prevent spam and DoS attacks
5. **XSS Prevention**: Escape HTML in message content
6. **SQL Injection**: Use parameterized queries
7. **CORS**: Configure allowed origins

## Deployment Notes

### Environment Variables

```bash
# WebSocket Configuration
WS_HEARTBEAT_INTERVAL=30  # seconds
WS_MAX_CONNECTIONS=1000
WS_MESSAGE_MAX_SIZE=10240  # bytes

# Reconnection
WS_RECONNECT_MAX_ATTEMPTS=5
WS_RECONNECT_BACKOFF_BASE=2

# Rate Limiting
WS_RATE_LIMIT_MESSAGES=100  # per minute
WS_RATE_LIMIT_TYPING=10  # per minute
```

### Infrastructure Requirements

- WebSocket support in reverse proxy (Nginx)
- Sticky sessions for load balancing
- Health check endpoint for monitoring
- Logging infrastructure for debugging

## Future Enhancements

1. **File Attachments**: Support sending images and files
2. **Message Reactions**: Add emoji reactions to messages
3. **Message Editing**: Allow editing sent messages
4. **Message Deletion**: Soft delete messages
5. **Read Receipts**: Show who read each message
6. **Push Notifications**: Mobile push when offline
7. **Voice Messages**: Record and send audio
8. **Video Calls**: Integrate WebRTC for video
