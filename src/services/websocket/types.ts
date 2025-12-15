/**
 * WebSocket Types - Sprint 09
 * Type definitions for WebSocket communication
 */

// Connection status
export type ConnectionStatus = 
  | 'disconnected'
  | 'connecting'
  | 'connected'
  | 'reconnecting'
  | 'error';

// Message types (Client → Server)
export type ClientMessageType =
  | 'message'
  | 'typing'
  | 'read'
  | 'sync'
  | 'ping'
  | 'presence'
  | 'join'
  | 'leave';

// Message types (Server → Client)
export type ServerMessageType =
  | 'connected'
  | 'message'
  | 'message_sent'
  | 'typing'
  | 'typing_sent'
  | 'read'
  | 'read_sent'
  | 'presence'
  | 'presence_updated'
  | 'sync_data'
  | 'pong'
  | 'joined'
  | 'left'
  | 'error';

// Presence status
export type PresenceStatus = 'online' | 'offline' | 'away';

// Base message interface
export interface BaseMessage {
  type: string;
}

// Client messages
export interface SendMessageData extends BaseMessage {
  type: 'message';
  conversation_id: string;
  content: string;
}

export interface TypingData extends BaseMessage {
  type: 'typing';
  conversation_id: string;
  is_typing: boolean;
}

export interface ReadData extends BaseMessage {
  type: 'read';
  conversation_id: string;
  message_id: string;
}

export interface SyncData extends BaseMessage {
  type: 'sync';
  conversation_id: string;
  last_message_id?: string;
}

export interface PingData extends BaseMessage {
  type: 'ping';
}

export interface PresenceData extends BaseMessage {
  type: 'presence';
  status: PresenceStatus;
}

export interface JoinData extends BaseMessage {
  type: 'join';
  conversation_id: string;
}

export interface LeaveData extends BaseMessage {
  type: 'leave';
  conversation_id: string;
}

export type ClientMessage =
  | SendMessageData
  | TypingData
  | ReadData
  | SyncData
  | PingData
  | PresenceData
  | JoinData
  | LeaveData;

// Server messages
export interface ConnectedMessage extends BaseMessage {
  type: 'connected';
  user_id: string;
  timestamp: string;
}

export interface MessageReceivedData extends BaseMessage {
  type: 'message';
  message: {
    id: string;
    conversation_id: string;
    user_id: string;
    content: string;
    role: string;
    created_at: string;
  };
}

export interface MessageSentData extends BaseMessage {
  type: 'message_sent';
  message_id: string;
  timestamp: string;
}

export interface TypingReceivedData extends BaseMessage {
  type: 'typing';
  user_id: string;
  conversation_id: string;
  is_typing: boolean;
}

export interface ReadReceivedData extends BaseMessage {
  type: 'read';
  user_id: string;
  conversation_id: string;
  message_id: string;
  read_at: string;
}

export interface PresenceReceivedData extends BaseMessage {
  type: 'presence';
  user_id: string;
  status: PresenceStatus;
  timestamp: string;
}

export interface SyncDataMessage extends BaseMessage {
  type: 'sync_data';
  conversation_id: string;
  messages: Array<{
    id: string;
    conversation_id: string;
    user_id: string;
    content: string;
    role: string;
    created_at: string;
  }>;
  count: number;
}

export interface PongMessage extends BaseMessage {
  type: 'pong';
  timestamp: string;
}

export interface ErrorMessage extends BaseMessage {
  type: 'error';
  error: string;
  code: string;
}

export type ServerMessage =
  | ConnectedMessage
  | MessageReceivedData
  | MessageSentData
  | TypingReceivedData
  | ReadReceivedData
  | PresenceReceivedData
  | SyncDataMessage
  | PongMessage
  | ErrorMessage;

// Event handlers
export interface WebSocketEventHandlers {
  onConnected?: (data: ConnectedMessage) => void;
  onMessage?: (data: MessageReceivedData) => void;
  onMessageSent?: (data: MessageSentData) => void;
  onTyping?: (data: TypingReceivedData) => void;
  onRead?: (data: ReadReceivedData) => void;
  onPresence?: (data: PresenceReceivedData) => void;
  onSyncData?: (data: SyncDataMessage) => void;
  onError?: (data: ErrorMessage) => void;
  onDisconnect?: () => void;
  onReconnect?: () => void;
}

// WebSocket client config
export interface WebSocketConfig {
  url: string;
  token: string;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  pingInterval?: number;
}

// Queued message (for offline sending)
export interface QueuedMessage {
  id: string;
  data: ClientMessage;
  timestamp: number;
  attempts: number;
}
