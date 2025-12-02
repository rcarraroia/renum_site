# Requirements Document - Sprint 03: Conversações e WebSocket

## Introduction

Este documento especifica os requisitos para implementação de um sistema completo de conversações em tempo real utilizando WebSocket. O sistema permitirá que administradores gerenciem conversas com clientes, troquem mensagens instantaneamente, visualizem histórico completo e recebam notificações em tempo real. A arquitetura suporta múltiplas conversas simultâneas com persistência de dados e reconexão automática.

## Glossary

- **System**: O sistema RENUM de conversações em tempo real
- **Admin**: Usuário autenticado com role='admin' no sistema
- **Client**: Empresa cliente cadastrada na tabela clients
- **Conversation**: Sessão de conversa entre admin e client
- **Message**: Mensagem individual dentro de uma conversation
- **WebSocket**: Protocolo de comunicação bidirecional em tempo real
- **Connection Manager**: Componente que gerencia conexões WebSocket ativas
- **Broadcast**: Envio de mensagem para múltiplos destinatários conectados
- **Typing Indicator**: Indicador visual de que alguém está digitando
- **Presence**: Estado de conexão online/offline de um usuário
- **Reconnection**: Processo de restabelecer conexão WebSocket após desconexão

## Requirements

### Requirement 1

**User Story:** As an admin, I want to establish WebSocket connections to the backend, so that I can receive real-time updates without polling.

#### Acceptance Criteria

1. WHEN an authenticated admin opens the conversations page THEN the system SHALL establish a WebSocket connection to the backend
2. WHEN the WebSocket connection is established THEN the system SHALL authenticate the connection using the JWT token
3. WHEN the WebSocket connection fails THEN the system SHALL attempt automatic reconnection with exponential backoff
4. WHEN the WebSocket connection is lost THEN the system SHALL display a connection status indicator to the admin
5. WHEN the admin closes the conversations page THEN the system SHALL gracefully close the WebSocket connection

### Requirement 2

**User Story:** As an admin, I want to create new conversations with clients, so that I can initiate communication.

#### Acceptance Criteria

1. WHEN an admin selects a client and clicks "New Conversation" THEN the system SHALL create a new conversation record with status='active'
2. WHEN a conversation is created THEN the system SHALL assign the conversation to the requesting admin
3. WHEN a conversation is created THEN the system SHALL set the channel field to the selected communication channel
4. WHEN a conversation is created THEN the system SHALL initialize unread_count to 0
5. WHEN a conversation is created THEN the system SHALL broadcast the new conversation to all connected admins

### Requirement 3

**User Story:** As an admin, I want to view a list of all conversations, so that I can see ongoing and past communications.

#### Acceptance Criteria

1. WHEN an admin accesses the conversations page THEN the system SHALL display all conversations ordered by last_update descending
2. WHEN displaying conversations THEN the system SHALL show client name, status, channel, unread count, and last update time
3. WHEN a conversation has unread messages THEN the system SHALL highlight it with a visual indicator
4. WHEN an admin searches for conversations THEN the system SHALL filter by client name, status, or tags
5. WHEN conversations are loaded THEN the system SHALL paginate results with 20 conversations per page

### Requirement 4

**User Story:** As an admin, I want to send messages in real-time, so that I can communicate instantly with clients.

#### Acceptance Criteria

1. WHEN an admin types a message and presses send THEN the system SHALL transmit the message via WebSocket
2. WHEN a message is sent THEN the system SHALL save it to the messages table with sender='admin'
3. WHEN a message is sent THEN the system SHALL broadcast it to all admins viewing that conversation
4. WHEN a message is sent THEN the system SHALL update the conversation's last_update timestamp
5. WHEN a message fails to send THEN the system SHALL retry transmission up to 3 times before showing an error

### Requirement 5

**User Story:** As an admin, I want to receive messages in real-time, so that I can respond promptly to client communications.

#### Acceptance Criteria

1. WHEN a new message arrives via WebSocket THEN the system SHALL display it immediately in the conversation view
2. WHEN a message is received THEN the system SHALL play a notification sound if the conversation is not in focus
3. WHEN a message is received THEN the system SHALL increment the unread_count for that conversation
4. WHEN an admin views a conversation with unread messages THEN the system SHALL mark all messages as read
5. WHEN messages are marked as read THEN the system SHALL update the is_read field in the database

### Requirement 6

**User Story:** As an admin, I want to see message history, so that I can review past communications.

#### Acceptance Criteria

1. WHEN an admin opens a conversation THEN the system SHALL load the most recent 50 messages
2. WHEN an admin scrolls to the top of the message list THEN the system SHALL load the next 50 older messages
3. WHEN displaying messages THEN the system SHALL show sender, content, timestamp, and read status
4. WHEN messages are loaded THEN the system SHALL scroll to the most recent unread message
5. WHEN no messages exist THEN the system SHALL display an empty state with instructions

### Requirement 7

**User Story:** As an admin, I want to see typing indicators, so that I know when someone is composing a message.

#### Acceptance Criteria

1. WHEN an admin types in the message input THEN the system SHALL broadcast a typing event via WebSocket
2. WHEN a typing event is received THEN the system SHALL display a typing indicator for that sender
3. WHEN typing stops for 3 seconds THEN the system SHALL remove the typing indicator
4. WHEN multiple users are typing THEN the system SHALL display all their names in the typing indicator
5. WHEN a message is sent THEN the system SHALL immediately clear the typing indicator for that sender

### Requirement 8

**User Story:** As an admin, I want to see online presence status, so that I know who is available.

#### Acceptance Criteria

1. WHEN an admin connects via WebSocket THEN the system SHALL broadcast their online status to all connected users
2. WHEN an admin disconnects THEN the system SHALL broadcast their offline status after 30 seconds
3. WHEN displaying conversations THEN the system SHALL show online/offline status for assigned agents
4. WHEN an admin's presence changes THEN the system SHALL update the UI in real-time
5. WHEN the system detects a stale connection THEN the system SHALL mark the user as offline

### Requirement 9

**User Story:** As an admin, I want to update conversation status, so that I can manage conversation lifecycle.

#### Acceptance Criteria

1. WHEN an admin changes conversation status THEN the system SHALL update the status field in the database
2. WHEN conversation status changes THEN the system SHALL broadcast the update to all connected admins
3. WHEN a conversation is marked as closed THEN the system SHALL prevent new messages from being sent
4. WHEN a closed conversation receives a message attempt THEN the system SHALL display an error message
5. WHEN conversation status changes THEN the system SHALL log the change with timestamp and admin ID

### Requirement 10

**User Story:** As an admin, I want the system to handle connection errors gracefully, so that I don't lose data or context.

#### Acceptance Criteria

1. WHEN the WebSocket connection is interrupted THEN the system SHALL queue outgoing messages locally
2. WHEN the connection is restored THEN the system SHALL send all queued messages in order
3. WHEN reconnection fails after 5 attempts THEN the system SHALL prompt the admin to refresh the page
4. WHEN the system detects duplicate messages THEN the system SHALL deduplicate based on message ID
5. WHEN connection state changes THEN the system SHALL persist the last known state to localStorage

### Requirement 11

**User Story:** As a developer, I want comprehensive error handling, so that the system remains stable under failure conditions.

#### Acceptance Criteria

1. WHEN a WebSocket error occurs THEN the system SHALL log the error with full context
2. WHEN message validation fails THEN the system SHALL reject the message and return a descriptive error
3. WHEN database operations fail THEN the system SHALL rollback transactions and notify the user
4. WHEN rate limits are exceeded THEN the system SHALL throttle requests and display a warning
5. WHEN critical errors occur THEN the system SHALL capture error details for debugging

### Requirement 12

**User Story:** As an admin, I want to filter and search conversations, so that I can quickly find specific communications.

#### Acceptance Criteria

1. WHEN an admin enters a search query THEN the system SHALL filter conversations by client name or summary
2. WHEN an admin selects a status filter THEN the system SHALL show only conversations with that status
3. WHEN an admin selects a priority filter THEN the system SHALL show only conversations with that priority
4. WHEN multiple filters are applied THEN the system SHALL combine them with AND logic
5. WHEN filters are cleared THEN the system SHALL restore the full conversation list
