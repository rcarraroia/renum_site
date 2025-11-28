/**
 * WebSocket Service
 * Manages WebSocket connections with reconnection logic
 */

type ConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'reconnecting';

type MessageCallback = (message: any) => void;
type ConnectionCallback = (status: ConnectionStatus) => void;
type TypingCallback = (data: { user_id: string; isTyping: boolean }) => void;

interface QueuedMessage {
  type: string;
  payload: any;
  timestamp: number;
}

class WebSocketService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000; // Start with 1 second
  private messageQueue: QueuedMessage[] = [];
  private messageCallbacks: MessageCallback[] = [];
  private connectionCallbacks: ConnectionCallback[] = [];
  private typingCallbacks: TypingCallback[] = [];
  private connectionStatus: ConnectionStatus = 'disconnected';
  private conversationId: string | null = null;
  private token: string | null = null;
  private heartbeatInterval: NodeJS.Timeout | null = null;
  private reconnectTimeout: NodeJS.Timeout | null = null;

  /**
   * Connect to WebSocket server
   */
  connect(conversationId: string, token: string): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected');
      return;
    }

    this.conversationId = conversationId;
    this.token = token;
    this.setConnectionStatus('connecting');

    const wsUrl = `${import.meta.env.VITE_WS_URL || 'ws://localhost:8000'}/ws/${conversationId}?token=${token}`;

    try {
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.setConnectionStatus('connected');
        this.reconnectAttempts = 0;
        this.reconnectDelay = 1000;
        
        // Send queued messages
        this.flushMessageQueue();
        
        // Start heartbeat
        this.startHeartbeat();
      };

      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          this.handleMessage(message);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        this.setConnectionStatus('disconnected');
        this.stopHeartbeat();
        
        // Attempt reconnection
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.attemptReconnect();
        }
      };

    } catch (error) {
      console.error('Error creating WebSocket:', error);
      this.setConnectionStatus('disconnected');
    }
  }

  /**
   * Disconnect from WebSocket server
   */
  disconnect(): void {
    this.stopHeartbeat();
    
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }

    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }

    this.setConnectionStatus('disconnected');
    this.conversationId = null;
    this.token = null;
    this.reconnectAttempts = 0;
  }

  /**
   * Send message via WebSocket
   */
  sendMessage(message: { type: string; payload: any }): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      // Queue message for later
      this.messageQueue.push({
        ...message,
        timestamp: Date.now()
      });
      console.log('Message queued (WebSocket not connected)');
    }
  }

  /**
   * Send typing start event
   */
  sendTypingStart(): void {
    this.sendMessage({
      type: 'typing_start',
      payload: {}
    });
  }

  /**
   * Send typing stop event
   */
  sendTypingStop(): void {
    this.sendMessage({
      type: 'typing_stop',
      payload: {}
    });
  }

  /**
   * Mark messages as read
   */
  markAsRead(messageIds: string[]): void {
    this.sendMessage({
      type: 'mark_read',
      payload: { message_ids: messageIds }
    });
  }

  /**
   * Register callback for incoming messages
   */
  onMessage(callback: MessageCallback): () => void {
    this.messageCallbacks.push(callback);
    
    // Return unsubscribe function
    return () => {
      this.messageCallbacks = this.messageCallbacks.filter(cb => cb !== callback);
    };
  }

  /**
   * Register callback for connection status changes
   */
  onConnectionChange(callback: ConnectionCallback): () => void {
    this.connectionCallbacks.push(callback);
    
    // Immediately call with current status
    callback(this.connectionStatus);
    
    // Return unsubscribe function
    return () => {
      this.connectionCallbacks = this.connectionCallbacks.filter(cb => cb !== callback);
    };
  }

  /**
   * Register callback for typing events
   */
  onTyping(callback: TypingCallback): () => void {
    this.typingCallbacks.push(callback);
    
    // Return unsubscribe function
    return () => {
      this.typingCallbacks = this.typingCallbacks.filter(cb => cb !== callback);
    };
  }

  /**
   * Get current connection status
   */
  getConnectionStatus(): ConnectionStatus {
    return this.connectionStatus;
  }

  /**
   * Handle incoming WebSocket message
   */
  private handleMessage(message: any): void {
    const { type, payload } = message;

    switch (type) {
      case 'connected':
        console.log('WebSocket connection confirmed');
        break;

      case 'new_message':
        this.messageCallbacks.forEach(cb => cb(payload));
        break;

      case 'user_typing':
        this.typingCallbacks.forEach(cb => cb({
          user_id: payload.user_id,
          isTyping: true
        }));
        break;

      case 'user_stopped_typing':
        this.typingCallbacks.forEach(cb => cb({
          user_id: payload.user_id,
          isTyping: false
        }));
        break;

      case 'presence_update':
        console.log('Presence update:', payload);
        break;

      case 'error':
        console.error('WebSocket error:', payload.error);
        break;

      case 'ping':
        // Respond to ping with pong
        this.sendMessage({ type: 'pong', payload: {} });
        break;

      default:
        console.log('Unknown message type:', type);
    }
  }

  /**
   * Set connection status and notify callbacks
   */
  private setConnectionStatus(status: ConnectionStatus): void {
    this.connectionStatus = status;
    this.connectionCallbacks.forEach(cb => cb(status));
  }

  /**
   * Flush queued messages
   */
  private flushMessageQueue(): void {
    if (this.messageQueue.length === 0) return;

    console.log(`Flushing ${this.messageQueue.length} queued messages`);

    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift();
      if (message) {
        this.sendMessage({
          type: message.type,
          payload: message.payload
        });
      }
    }
  }

  /**
   * Attempt to reconnect with exponential backoff
   */
  private attemptReconnect(): void {
    this.reconnectAttempts++;
    this.setConnectionStatus('reconnecting');

    const delay = Math.min(
      this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1),
      16000 // Max 16 seconds
    );

    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

    this.reconnectTimeout = setTimeout(() => {
      if (this.conversationId && this.token) {
        this.connect(this.conversationId, this.token);
      }
    }, delay);
  }

  /**
   * Start heartbeat to keep connection alive
   */
  private startHeartbeat(): void {
    this.stopHeartbeat();
    
    this.heartbeatInterval = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.sendMessage({ type: 'ping', payload: {} });
      }
    }, 30000); // Every 30 seconds
  }

  /**
   * Stop heartbeat
   */
  private stopHeartbeat(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }
}

// Export singleton instance
export const websocketService = new WebSocketService();
export type { ConnectionStatus };
