# Implementation Plan - Sprint 03: Conversações e WebSocket

## Overview

Este plano de implementação detalha as tarefas necessárias para construir um sistema completo de conversações em tempo real com WebSocket. As tarefas estão organizadas em ordem de dependência, começando pela infraestrutura base (models e services), seguindo para a camada de WebSocket, e finalizando com a interface do usuário.

---

## Backend Implementation

### Phase 1: Foundation

- [x] 1. Create data models and validation schemas


  - Create Pydantic models for Conversation (ConversationBase, ConversationCreate, ConversationUpdate, ConversationResponse)
  - Create Pydantic models for Message (MessageBase, MessageCreate, MessageResponse)
  - Create WebSocket message types enum (WSMessageType)
  - Create WebSocket message wrapper (WSMessage)
  - Add validation for status field (must be 'active', 'closed', or 'pending')
  - Add validation for channel field (must be 'whatsapp', 'email', or 'web')
  - Add validation for priority field (must be 'Low', 'Medium', or 'High')
  - Add validation for sender field (must be 'admin', 'client', or 'system')
  - Add validation for message type field (must be 'text', 'image', or 'file')
  - _Requirements: 2.1, 2.3, 4.2, 9.1_

- [ ]* 1.1 Write property test for status validation
  - **Property 8: Status Transition Validity**
  - **Validates: Requirements 9.1**

- [x] 2. Implement Conversation Service



  - Create ConversationService class with Supabase client injection
  - Implement create_conversation method (insert into conversations table)
  - Implement list_conversations method with filters (status, priority, client_id)
  - Implement get_conversation_by_id method
  - Implement update_status method with validation
  - Implement update_conversation method for other fields
  - Implement delete_conversation method (soft delete by setting status)
  - Implement mark_as_read method (set unread_count to 0)
  - Add error handling for database operations
  - Add logging for all operations
  - _Requirements: 2.1, 2.2, 2.3, 3.1, 9.1, 9.2_

- [ ]* 2.1 Write unit tests for ConversationService
  - Test create_conversation with valid data
  - Test create_conversation with invalid status
  - Test list_conversations with filters
  - Test update_status with valid transitions
  - Test update_status with invalid status
  - Test mark_as_read updates unread_count
  - _Requirements: 2.1, 9.1_


- [x] 3. Implement Message Service


  - Create MessageService class with Supabase client injection
  - Implement send_message method (insert into messages table)
  - Implement get_messages method with pagination (limit, before_id)
  - Implement mark_messages_as_read method (update is_read field)
  - Implement update_conversation_timestamp method (update last_update)
  - Implement increment_unread_count method
  - Implement decrement_unread_count method
  - Add validation for message content (max length, not empty)
  - Add error handling for database operations
  - Add logging for all operations
  - _Requirements: 4.2, 4.4, 5.5, 6.1, 6.2_

- [ ]* 3.1 Write property test for message ordering
  - **Property 3: Message Ordering**
  - **Validates: Requirements 6.1, 6.2**

- [ ]* 3.2 Write property test for unread count accuracy
  - **Property 5: Unread Count Accuracy**
  - **Validates: Requirements 5.3**

- [ ]* 3.3 Write unit tests for MessageService
  - Test send_message creates message
  - Test send_message updates conversation timestamp
  - Test get_messages returns ordered by timestamp
  - Test get_messages pagination works correctly
  - Test mark_as_read updates is_read field
  - Test mark_as_read decrements unread_count
  - _Requirements: 4.2, 5.5, 6.1_

### Phase 2: WebSocket Infrastructure

- [x] 4. Create Connection Manager


  - Create ConnectionManager class with active_connections dictionary
  - Implement connect method (add WebSocket to active_connections)
  - Implement disconnect method (remove WebSocket from active_connections)
  - Implement broadcast_to_conversation method (send to all in conversation)
  - Implement broadcast_to_all method (send to all connections)
  - Implement get_connections_count method
  - Implement is_user_connected method
  - Add connection tracking by user_id and conversation_id
  - Add error handling for failed broadcasts
  - Add logging for connection events
  - _Requirements: 1.1, 4.3, 5.1, 8.1_

- [ ]* 4.1 Write unit tests for ConnectionManager
  - Test connect adds connection
  - Test disconnect removes connection
  - Test broadcast_to_conversation sends to correct clients
  - Test broadcast_to_all sends to all clients
  - Test failed broadcast doesn't crash
  - _Requirements: 1.1, 4.3_

- [x] 5. Implement WebSocket Handler


  - Create WebSocketHandler class
  - Implement handle_connection method (main connection lifecycle)
  - Implement authenticate_connection method (validate JWT token)
  - Implement handle_message method (route incoming messages)
  - Implement handle_send_message (process SEND_MESSAGE type)
  - Implement handle_typing_start (process TYPING_START type)
  - Implement handle_typing_stop (process TYPING_STOP type)
  - Implement handle_mark_read (process MARK_READ type)
  - Implement send_error method (send error to client)
  - Implement heartbeat mechanism (ping/pong every 30s)
  - Add message validation before processing
  - Add rate limiting (100 messages/min, 10 typing events/min)
  - Add error handling for all message types
  - Add logging for all events
  - _Requirements: 1.2, 1.3, 4.1, 5.1, 7.1, 11.1, 11.4_

- [ ]* 5.1 Write property test for closed conversation immutability
  - **Property 9: Closed Conversation Immutability**
  - **Validates: Requirements 9.3, 9.4**

- [ ]* 5.2 Write integration tests for WebSocket Handler
  - Test connection with valid token succeeds
  - Test connection with invalid token fails
  - Test send_message persists and broadcasts
  - Test typing events broadcast correctly
  - Test rate limiting blocks excess messages
  - Test heartbeat keeps connection alive
  - _Requirements: 1.2, 4.1, 7.1_

- [x] 6. Create WebSocket endpoint



  - Create /ws/{conversation_id} endpoint in FastAPI
  - Extract JWT token from query parameters
  - Call WebSocketHandler.handle_connection
  - Handle WebSocket exceptions
  - Add CORS configuration for WebSocket
  - Add endpoint to main.py router
  - _Requirements: 1.1, 1.2_

### Phase 3: REST API Endpoints

- [x] 7. Create Conversations REST endpoints


  - Create /api/conversations router
  - Implement POST /api/conversations (create conversation)
  - Implement GET /api/conversations (list with filters and pagination)
  - Implement GET /api/conversations/{id} (get single conversation)
  - Implement PUT /api/conversations/{id} (update conversation)
  - Implement PATCH /api/conversations/{id}/status (update status)
  - Implement DELETE /api/conversations/{id} (soft delete)
  - Implement POST /api/conversations/{id}/mark-read (mark as read)
  - Add authentication middleware (require admin role)
  - Add request validation using Pydantic models
  - Add error handling and appropriate HTTP status codes
  - Add logging for all operations
  - Register router in main.py
  - _Requirements: 2.1, 2.2, 3.1, 3.4, 9.1, 9.2_

- [ ]* 7.1 Write unit tests for Conversations endpoints
  - Test POST creates conversation
  - Test GET lists conversations with filters
  - Test GET by id returns conversation
  - Test PUT updates conversation
  - Test PATCH updates status
  - Test DELETE soft deletes
  - Test mark-read updates unread_count
  - Test authentication required
  - _Requirements: 2.1, 3.1, 9.1_

- [x] 8. Create Messages REST endpoints



  - Create /api/messages router
  - Implement GET /api/messages (list messages for conversation with pagination)
  - Implement POST /api/messages (send message via REST as fallback)
  - Implement PATCH /api/messages/mark-read (mark multiple messages as read)
  - Add authentication middleware (require admin role)
  - Add request validation using Pydantic models
  - Add error handling and appropriate HTTP status codes
  - Add logging for all operations
  - Register router in main.py
  - _Requirements: 4.2, 5.5, 6.1, 6.2_

- [ ]* 8.1 Write unit tests for Messages endpoints
  - Test GET returns messages ordered by timestamp
  - Test GET pagination works correctly
  - Test POST creates message
  - Test PATCH marks messages as read
  - Test authentication required
  - _Requirements: 4.2, 6.1_

### Phase 4: Backend Checkpoint

- [x] 9. Backend integration checkpoint



  - Ensure all tests pass
  - Verify WebSocket connection works with test client
  - Verify messages persist to database
  - Verify broadcast works to multiple connections
  - Test reconnection behavior
  - Test rate limiting
  - Ask user if questions arise
  - _Requirements: All backend requirements_

---

## Frontend Implementation

### Phase 5: Services Layer

- [x] 10. Create WebSocket Service


  - Create WebSocketService class in src/services/websocketService.ts
  - Implement connect method (establish WebSocket connection)
  - Implement disconnect method (close connection gracefully)
  - Implement sendMessage method (send message via WebSocket)
  - Implement sendTypingStart method (send typing indicator)
  - Implement sendTypingStop method (send typing stop)
  - Implement markAsRead method (send mark read event)
  - Implement onMessage callback registration
  - Implement onConnectionChange callback registration
  - Implement onTyping callback registration
  - Implement reconnection logic with exponential backoff
  - Implement message queue for offline messages
  - Implement heartbeat/ping mechanism
  - Add connection state management (connecting, connected, disconnected, reconnecting)
  - Add error handling and logging
  - _Requirements: 1.1, 1.3, 1.4, 4.1, 7.1, 10.1, 10.2_



- [ ] 11. Create Conversation Service
  - Create conversationService.ts with API client
  - Implement createConversation method (POST /api/conversations)
  - Implement getConversations method (GET /api/conversations with filters)
  - Implement getConversationById method (GET /api/conversations/{id})
  - Implement updateConversation method (PUT /api/conversations/{id})
  - Implement updateStatus method (PATCH /api/conversations/{id}/status)
  - Implement deleteConversation method (DELETE /api/conversations/{id})
  - Implement markAsRead method (POST /api/conversations/{id}/mark-read)
  - Add error handling and retry logic
  - Add TypeScript types for all methods
  - _Requirements: 2.1, 3.1, 9.1_




- [ ] 12. Create Message Service
  - Create messageService.ts with API client
  - Implement getMessages method (GET /api/messages with pagination)
  - Implement sendMessage method (POST /api/messages as fallback)
  - Implement markMessagesAsRead method (PATCH /api/messages/mark-read)
  - Add error handling and retry logic
  - Add TypeScript types for all methods


  - _Requirements: 4.2, 6.1, 6.2_

### Phase 6: React Hooks

- [ ] 13. Create useWebSocket hook
  - Create useWebSocket.ts custom hook
  - Manage WebSocket connection state (isConnected, connectionStatus)
  - Manage messages state (messages array)
  - Manage typing indicators state (typingUsers array)
  - Implement sendMessage function
  - Implement startTyping function
  - Implement stopTyping function
  - Implement markAsRead function
  - Handle incoming messages (add to messages array)
  - Handle typing events (update typingUsers array)


  - Handle connection status changes
  - Auto-connect on mount, disconnect on unmount
  - Add debouncing for typing events (send max once per second)
  - Add auto-clear for typing indicators (3 seconds)
  - _Requirements: 1.1, 4.1, 5.1, 7.1, 7.2, 7.3_

- [ ] 14. Create useConversations hook
  - Create useConversations.ts custom hook using TanStack Query
  - Implement useConversations query (fetch conversations list)
  - Implement useConversation query (fetch single conversation)
  - Implement useCreateConversation mutation
  - Implement useUpdateConversation mutation



  - Implement useUpdateStatus mutation
  - Implement useDeleteConversation mutation
  - Implement useMarkAsRead mutation
  - Add optimistic updates for mutations
  - Add cache invalidation on mutations
  - Add error handling
  - _Requirements: 2.1, 3.1, 9.1_

- [ ] 15. Create useMessages hook
  - Create useMessages.ts custom hook using TanStack Query
  - Implement useMessages query (fetch messages with pagination)
  - Implement useInfiniteMessages for infinite scroll
  - Implement useSendMessage mutation
  - Implement useMarkAsRead mutation
  - Add optimistic updates for sending messages
  - Add cache invalidation on mutations
  - Add error handling
  - _Requirements: 4.2, 6.1, 6.2_

### Phase 7: UI Components

- [x] 16. Create ConversationsPage component

  - Create ConversationsPage.tsx main page component
  - Display list of conversations using useConversations hook
  - Implement search/filter UI (by status, priority, client name)
  - Implement pagination controls
  - Display conversation cards with: client name, status, unread count, last update
  - Highlight conversations with unread messages
  - Add "New Conversation" button
  - Add click handler to open conversation in ChatWindow
  - Add loading states
  - Add empty state when no conversations
  - Add error handling UI
  - Style with Tailwind CSS
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 12.1, 12.2_


- [ ] 17. Create ChatWindow component
  - Create ChatWindow.tsx component
  - Display conversation header (client name, status, actions)
  - Integrate MessageList component
  - Integrate MessageInput component
  - Integrate TypingIndicator component
  - Display connection status indicator
  - Add "Close Conversation" button
  - Add "Reopen Conversation" button (if closed)
  - Handle conversation status changes
  - Add loading states
  - Add error handling UI
  - Style with Tailwind CSS
  - _Requirements: 1.4, 5.1, 9.1, 9.3_

- [x] 18. Create MessageList component


  - Create MessageList.tsx component
  - Display messages using useMessages hook

  - Implement infinite scroll for loading older messages
  - Display MessageBubble for each message
  - Auto-scroll to bottom on new message
  - Scroll to first unread message on load
  - Group messages by date
  - Display timestamps
  - Add loading indicator for pagination
  - Add empty state when no messages
  - Style with Tailwind CSS
  - _Requirements: 5.1, 6.1, 6.2, 6.3, 6.4_

- [x] 19. Create MessageBubble component

  - Create MessageBubble.tsx component
  - Display message content with proper escaping (prevent XSS)
  - Display sender name
  - Display timestamp
  - Display read status indicator
  - Style differently for admin vs client messages
  - Support different message types (text, image, file)
  - Add hover effects
  - Style with Tailwind CSS
  - _Requirements: 5.1, 6.3_

- [x] 20. Create MessageInput component


  - Create MessageInput.tsx component
  - Implement textarea for message input


  - Implement "Send" button
  - Handle Enter key to send (Shift+Enter for new line)
  - Trigger typing indicator on input change
  - Clear input after sending
  - Disable input when conversation is closed
  - Add character count indicator
  - Add loading state while sending
  - Add error handling UI
  - Style with Tailwind CSS
  - _Requirements: 4.1, 7.1, 9.3_


- [x] 21. Create TypingIndicator component

  - Create TypingIndicator.tsx component
  - Display "X is typing..." message
  - Support multiple users typing
  - Animate typing dots
  - Auto-hide after 3 seconds of no typing events
  - Style with Tailwind CSS
  - _Requirements: 7.2, 7.3, 7.4_


- [ ] 22. Create ConversationCreationModal component
  - Create ConversationCreationModal.tsx component
  - Display modal dialog
  - Add client selection dropdown
  - Add channel selection (whatsapp, email, web)
  - Add priority selection (Low, Medium, High)
  - Add optional summary textarea
  - Implement form validation
  - Call useCreateConversation mutation on submit
  - Close modal on success
  - Display error messages
  - Style with Tailwind CSS
  - _Requirements: 2.1, 2.2, 2.3_

### Phase 8: Integration and Polish

- [x] 23. Integrate WebSocket with UI

  - Connect useWebSocket hook in ChatWindow
  - Update MessageList when new messages arrive via WebSocket
  - Update conversation list when conversations change
  - Update unread counts in real-time
  - Display connection status in UI
  - Handle reconnection gracefully
  - Test with multiple browser tabs
  - _Requirements: 1.1, 4.3, 5.1, 5.2_

- [x] 24. Implement connection status indicator

  - Create ConnectionStatus.tsx component
  - Display "Connected" (green), "Connecting" (yellow), "Disconnected" (red)
  - Show reconnection attempts
  - Add manual reconnect button
  - Position in top-right corner
  - Style with Tailwind CSS
  - _Requirements: 1.4, 10.3_

- [x] 25. Add notification sounds

  - Add notification sound file to public/sounds/
  - Play sound when new message arrives (if conversation not in focus)
  - Add user preference to enable/disable sounds
  - Store preference in localStorage
  - _Requirements: 5.2_

- [ ]* 26. Write property test for message read propagation
  - **Property 10: Message Read Propagation**
  - **Validates: Requirements 5.5, 6.4**

- [ ]* 27. Write E2E tests for conversation flow
  - Test creating conversation
  - Test sending message via WebSocket
  - Test receiving message in real-time
  - Test typing indicators
  - Test marking as read
  - Test closing conversation
  - _Requirements: 2.1, 4.1, 5.1, 7.1, 9.1_

### Phase 9: Final Checkpoint

- [x] 28. Final integration checkpoint


  - Ensure all tests pass (backend + frontend)
  - Test complete user flow: create conversation → send messages → receive messages → close
  - Test with multiple users simultaneously
  - Test reconnection after network interruption
  - Test rate limiting behavior
  - Verify no console errors
  - Verify no memory leaks
  - Test on different browsers (Chrome, Firefox, Safari)
  - Ask user if questions arise
  - _Requirements: All requirements_

---

## Summary

**Total Tasks:** 28 main tasks  
**Optional Tasks:** 11 (marked with *)  
**Estimated Complexity:** High  
**Key Dependencies:**
- Sprint 01 (Authentication) must be complete
- Sprint 02 (CRUD Core) must be complete
- Supabase tables must exist and have correct structure

**Critical Path:**
1. Models → Services → WebSocket Infrastructure → REST API → Frontend Services → Hooks → UI Components → Integration

**Testing Strategy:**
- Unit tests for services and utilities
- Property-based tests for correctness properties
- Integration tests for WebSocket flow
- E2E tests for complete user journeys
- Manual testing for UX and edge cases
