/**
 * useWebSocket Hook
 * Manages WebSocket connection for a conversation
 */
import { useState, useEffect, useCallback, useRef } from 'react';
import { websocketService, ConnectionStatus } from '../services/websocketService';
import { MessageResponse } from '../services/messageService';

interface UseWebSocketOptions {
  conversationId: string;
  token: string;
  autoConnect?: boolean;
}

interface TypingUser {
  user_id: string;
  timestamp: number;
}

export function useWebSocket({ conversationId, token, autoConnect = true }: UseWebSocketOptions) {
  const [isConnected, setIsConnected] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('disconnected');
  const [messages, setMessages] = useState<MessageResponse[]>([]);
  const [typingUsers, setTypingUsers] = useState<TypingUser[]>([]);
  
  const typingTimeoutRef = useRef<Map<string, NodeJS.Timeout>>(new Map());
  const lastTypingEventRef = useRef<number>(0);
  const typingDebounceRef = useRef<NodeJS.Timeout | null>(null);

  // Handle connection status changes
  useEffect(() => {
    const unsubscribe = websocketService.onConnectionChange((status) => {
      setConnectionStatus(status);
      setIsConnected(status === 'connected');
    });

    return unsubscribe;
  }, []);

  // Handle incoming messages
  useEffect(() => {
    const unsubscribe = websocketService.onMessage((message: MessageResponse) => {
      setMessages((prev) => {
        // Check if message already exists (prevent duplicates)
        if (prev.some(m => m.id === message.id)) {
          return prev;
        }
        return [...prev, message];
      });
    });

    return unsubscribe;
  }, []);

  // Handle typing indicators
  useEffect(() => {
    const unsubscribe = websocketService.onTyping(({ user_id, isTyping }) => {
      if (isTyping) {
        // Add user to typing list
        setTypingUsers((prev) => {
          if (prev.some(u => u.user_id === user_id)) {
            return prev;
          }
          return [...prev, { user_id, timestamp: Date.now() }];
        });

        // Clear existing timeout for this user
        const existingTimeout = typingTimeoutRef.current.get(user_id);
        if (existingTimeout) {
          clearTimeout(existingTimeout);
        }

        // Set new timeout to remove user after 3 seconds
        const timeout = setTimeout(() => {
          setTypingUsers((prev) => prev.filter(u => u.user_id !== user_id));
          typingTimeoutRef.current.delete(user_id);
        }, 3000);

        typingTimeoutRef.current.set(user_id, timeout);
      } else {
        // Remove user from typing list
        setTypingUsers((prev) => prev.filter(u => u.user_id !== user_id));
        
        const timeout = typingTimeoutRef.current.get(user_id);
        if (timeout) {
          clearTimeout(timeout);
          typingTimeoutRef.current.delete(user_id);
        }
      }
    });

    return unsubscribe;
  }, []);

  // Connect/disconnect on mount/unmount
  useEffect(() => {
    if (autoConnect && conversationId && token) {
      websocketService.connect(conversationId, token);
    }

    return () => {
      if (autoConnect) {
        websocketService.disconnect();
      }
      
      // Clear all typing timeouts
      typingTimeoutRef.current.forEach(timeout => clearTimeout(timeout));
      typingTimeoutRef.current.clear();
      
      if (typingDebounceRef.current) {
        clearTimeout(typingDebounceRef.current);
      }
    };
  }, [conversationId, token, autoConnect]);

  // Send message
  const sendMessage = useCallback((content: string, type: 'text' | 'image' | 'file' = 'text') => {
    websocketService.sendMessage({
      type: 'send_message',
      payload: {
        content,
        type,
      },
    });

    // Stop typing indicator when message is sent
    websocketService.sendTypingStop();
    if (typingDebounceRef.current) {
      clearTimeout(typingDebounceRef.current);
      typingDebounceRef.current = null;
    }
  }, []);

  // Start typing (with debounce - max once per second)
  const startTyping = useCallback(() => {
    const now = Date.now();
    
    // Only send if more than 1 second has passed since last event
    if (now - lastTypingEventRef.current > 1000) {
      websocketService.sendTypingStart();
      lastTypingEventRef.current = now;
    }

    // Clear existing debounce timeout
    if (typingDebounceRef.current) {
      clearTimeout(typingDebounceRef.current);
    }

    // Set new timeout to stop typing after 3 seconds of inactivity
    typingDebounceRef.current = setTimeout(() => {
      websocketService.sendTypingStop();
      typingDebounceRef.current = null;
    }, 3000);
  }, []);

  // Stop typing
  const stopTyping = useCallback(() => {
    websocketService.sendTypingStop();
    
    if (typingDebounceRef.current) {
      clearTimeout(typingDebounceRef.current);
      typingDebounceRef.current = null;
    }
  }, []);

  // Mark messages as read
  const markAsRead = useCallback((messageIds: string[]) => {
    websocketService.markAsRead(messageIds);
  }, []);

  // Manual connect/disconnect
  const connect = useCallback(() => {
    if (conversationId && token) {
      websocketService.connect(conversationId, token);
    }
  }, [conversationId, token]);

  const disconnect = useCallback(() => {
    websocketService.disconnect();
  }, []);

  return {
    isConnected,
    connectionStatus,
    messages,
    typingUsers: typingUsers.map(u => u.user_id),
    sendMessage,
    startTyping,
    stopTyping,
    markAsRead,
    connect,
    disconnect,
  };
}
