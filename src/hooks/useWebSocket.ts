/**
 * useWebSocket Hook - Sprint 09
 * React hook for WebSocket communication
 */

import { useState, useEffect, useRef, useCallback } from 'react';
import { WebSocketClient } from '../services/websocket/WebSocketClient';
import {
  ConnectionStatus,
  WebSocketEventHandlers,
  MessageReceivedData,
  TypingReceivedData,
  PresenceReceivedData,
  ErrorMessage,
} from '../services/websocket/types';

interface UseWebSocketOptions {
  url: string;
  token: string;
  autoConnect?: boolean;
  onMessage?: (data: MessageReceivedData) => void;
  onTyping?: (data: TypingReceivedData) => void;
  onPresence?: (data: PresenceReceivedData) => void;
  onError?: (data: ErrorMessage) => void;
}

interface UseWebSocketReturn {
  // Connection state
  isConnected: boolean;
  connectionStatus: ConnectionStatus;
  lastError: string | null;

  // Methods
  connect: () => void;
  disconnect: () => void;
  sendMessage: (conversationId: string, content: string) => void;
  sendTyping: (conversationId: string, isTyping: boolean) => void;
  markAsRead: (conversationId: string, messageId: string) => void;
  syncMessages: (conversationId: string, lastMessageId?: string) => void;
  updatePresence: (status: 'online' | 'away' | 'offline') => void;
  joinConversation: (conversationId: string) => void;
  leaveConversation: (conversationId: string) => void;
}

export function useWebSocket(options: UseWebSocketOptions): UseWebSocketReturn {
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('disconnected');
  const [lastError, setLastError] = useState<string | null>(null);
  const clientRef = useRef<WebSocketClient | null>(null);

  // Initialize WebSocket client
  useEffect(() => {
    const handlers: WebSocketEventHandlers = {
      onConnected: () => {
        console.log('WebSocket connected');
        setConnectionStatus('connected');
        setLastError(null);
      },

      onMessage: (data) => {
        console.log('Message received:', data);
        options.onMessage?.(data);
      },

      onTyping: (data) => {
        console.log('Typing indicator:', data);
        options.onTyping?.(data);
      },

      onPresence: (data) => {
        console.log('Presence update:', data);
        options.onPresence?.(data);
      },

      onError: (data) => {
        console.error('WebSocket error:', data.error);
        setLastError(data.error);
        options.onError?.(data);
      },

      onDisconnect: () => {
        console.log('WebSocket disconnected');
        setConnectionStatus('disconnected');
      },

      onReconnect: () => {
        console.log('WebSocket reconnected');
        setConnectionStatus('connected');
        setLastError(null);
      },
    };

    clientRef.current = new WebSocketClient(
      {
        url: options.url,
        token: options.token,
      },
      handlers
    );

    // Auto-connect if enabled
    if (options.autoConnect !== false) {
      clientRef.current.connect();
    }

    // Cleanup on unmount
    return () => {
      if (clientRef.current) {
        clientRef.current.disconnect();
        clientRef.current = null;
      }
    };
  }, [options.url, options.token, options.autoConnect]);

  // Update connection status periodically
  useEffect(() => {
    const interval = setInterval(() => {
      if (clientRef.current) {
        const status = clientRef.current.getStatus();
        setConnectionStatus(status);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  // Methods
  const connect = useCallback(() => {
    clientRef.current?.connect();
  }, []);

  const disconnect = useCallback(() => {
    clientRef.current?.disconnect();
  }, []);

  const sendMessage = useCallback((conversationId: string, content: string) => {
    clientRef.current?.sendMessage(conversationId, content);
  }, []);

  const sendTyping = useCallback((conversationId: string, isTyping: boolean) => {
    clientRef.current?.sendTyping(conversationId, isTyping);
  }, []);

  const markAsRead = useCallback((conversationId: string, messageId: string) => {
    clientRef.current?.markAsRead(conversationId, messageId);
  }, []);

  const syncMessages = useCallback((conversationId: string, lastMessageId?: string) => {
    clientRef.current?.syncMessages(conversationId, lastMessageId);
  }, []);

  const updatePresence = useCallback((status: 'online' | 'away' | 'offline') => {
    clientRef.current?.updatePresence(status);
  }, []);

  const joinConversation = useCallback((conversationId: string) => {
    clientRef.current?.joinConversation(conversationId);
  }, []);

  const leaveConversation = useCallback((conversationId: string) => {
    clientRef.current?.leaveConversation(conversationId);
  }, []);

  return {
    // State
    isConnected: connectionStatus === 'connected',
    connectionStatus,
    lastError,

    // Methods
    connect,
    disconnect,
    sendMessage,
    sendTyping,
    markAsRead,
    syncMessages,
    updatePresence,
    joinConversation,
    leaveConversation,
  };
}
