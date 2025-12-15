/**
 * WebSocket Client - Sprint 09
 * Manages WebSocket connection with auto-reconnect and message queue
 */

import {
  ConnectionStatus,
  ClientMessage,
  ServerMessage,
  WebSocketConfig,
  WebSocketEventHandlers,
  QueuedMessage,
} from './types';

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private config: WebSocketConfig;
  private handlers: WebSocketEventHandlers;
  private status: ConnectionStatus = 'disconnected';
  private reconnectAttempts = 0;
  private reconnectTimeout: NodeJS.Timeout | null = null;
  private pingInterval: NodeJS.Timeout | null = null;
  private messageQueue: QueuedMessage[] = [];
  private isIntentionalClose = false;

  constructor(config: WebSocketConfig, handlers: WebSocketEventHandlers = {}) {
    this.config = {
      reconnectInterval: 1000, // Start with 1 second
      maxReconnectAttempts: 10,
      pingInterval: 30000, // 30 seconds
      ...config,
    };
    this.handlers = handlers;
  }

  /**
   * Connect to WebSocket server
   */
  public connect(): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected');
      return;
    }

    this.isIntentionalClose = false;
    this.setStatus('connecting');

    const wsUrl = `${this.config.url}?token=${this.config.token}`;
    console.log('Connecting to WebSocket:', wsUrl);

    try {
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = this.handleOpen.bind(this);
      this.ws.onmessage = this.handleMessage.bind(this);
      this.ws.onerror = this.handleError.bind(this);
      this.ws.onclose = this.handleClose.bind(this);
    } catch (error) {
      console.error('Error creating WebSocket:', error);
      this.setStatus('error');
      this.scheduleReconnect();
    }
  }

  /**
   * Disconnect from WebSocket server
   */
  public disconnect(): void {
    this.isIntentionalClose = true;
    this.clearReconnectTimeout();
    this.clearPingInterval();

    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }

    this.setStatus('disconnected');
  }

  /**
   * Send message to server
   */
  public send(message: ClientMessage): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      try {
        this.ws.send(JSON.stringify(message));
        console.log('Message sent:', message.type);
      } catch (error) {
        console.error('Error sending message:', error);
        this.queueMessage(message);
      }
    } else {
      console.log('WebSocket not connected, queueing message');
      this.queueMessage(message);
    }
  }

  /**
   * Send chat message
   */
  public sendMessage(conversationId: string, content: string): void {
    this.send({
      type: 'message',
      conversation_id: conversationId,
      content,
    });
  }

  /**
   * Send typing indicator
   */
  public sendTyping(conversationId: string, isTyping: boolean): void {
    this.send({
      type: 'typing',
      conversation_id: conversationId,
      is_typing: isTyping,
    });
  }

  /**
   * Mark message as read
   */
  public markAsRead(conversationId: string, messageId: string): void {
    this.send({
      type: 'read',
      conversation_id: conversationId,
      message_id: messageId,
    });
  }

  /**
   * Sync missed messages
   */
  public syncMessages(conversationId: string, lastMessageId?: string): void {
    this.send({
      type: 'sync',
      conversation_id: conversationId,
      last_message_id: lastMessageId,
    });
  }

  /**
   * Update presence status
   */
  public updatePresence(status: 'online' | 'away' | 'offline'): void {
    this.send({
      type: 'presence',
      status,
    });
  }

  /**
   * Join conversation
   */
  public joinConversation(conversationId: string): void {
    this.send({
      type: 'join',
      conversation_id: conversationId,
    });
  }

  /**
   * Leave conversation
   */
  public leaveConversation(conversationId: string): void {
    this.send({
      type: 'leave',
      conversation_id: conversationId,
    });
  }

  /**
   * Get current connection status
   */
  public getStatus(): ConnectionStatus {
    return this.status;
  }

  /**
   * Check if connected
   */
  public isConnected(): boolean {
    return this.status === 'connected';
  }

  // Private methods

  private handleOpen(): void {
    console.log('WebSocket connected');
    this.setStatus('connected');
    this.reconnectAttempts = 0;
    this.startPingInterval();
    this.processMessageQueue();

    if (this.handlers.onReconnect && this.reconnectAttempts > 0) {
      this.handlers.onReconnect();
    }
  }

  private handleMessage(event: MessageEvent): void {
    try {
      const message: ServerMessage = JSON.parse(event.data);
      console.log('Message received:', message.type);

      // Route to appropriate handler
      switch (message.type) {
        case 'connected':
          this.handlers.onConnected?.(message);
          break;
        case 'message':
          this.handlers.onMessage?.(message);
          break;
        case 'message_sent':
          this.handlers.onMessageSent?.(message);
          break;
        case 'typing':
          this.handlers.onTyping?.(message);
          break;
        case 'read':
          this.handlers.onRead?.(message);
          break;
        case 'presence':
          this.handlers.onPresence?.(message);
          break;
        case 'sync_data':
          this.handlers.onSyncData?.(message);
          break;
        case 'error':
          console.error('Server error:', message.error);
          this.handlers.onError?.(message);
          break;
        case 'pong':
          // Keep-alive response
          break;
        default:
          console.warn('Unknown message type:', message.type);
      }
    } catch (error) {
      console.error('Error parsing message:', error);
    }
  }

  private handleError(event: Event): void {
    console.error('WebSocket error:', event);
    this.setStatus('error');
  }

  private handleClose(event: CloseEvent): void {
    console.log('WebSocket closed:', event.code, event.reason);
    this.clearPingInterval();

    if (this.handlers.onDisconnect) {
      this.handlers.onDisconnect();
    }

    if (!this.isIntentionalClose) {
      this.setStatus('reconnecting');
      this.scheduleReconnect();
    } else {
      this.setStatus('disconnected');
    }
  }

  private scheduleReconnect(): void {
    if (this.reconnectAttempts >= (this.config.maxReconnectAttempts || 10)) {
      console.error('Max reconnect attempts reached');
      this.setStatus('error');
      return;
    }

    this.clearReconnectTimeout();

    // Exponential backoff: 1s, 2s, 4s, 8s, 16s, 32s (max)
    const delay = Math.min(
      (this.config.reconnectInterval || 1000) * Math.pow(2, this.reconnectAttempts),
      32000
    );

    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts + 1})`);

    this.reconnectTimeout = setTimeout(() => {
      this.reconnectAttempts++;
      this.connect();
    }, delay);
  }

  private clearReconnectTimeout(): void {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }
  }

  private startPingInterval(): void {
    this.clearPingInterval();

    this.pingInterval = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.send({ type: 'ping' });
      }
    }, this.config.pingInterval || 30000);
  }

  private clearPingInterval(): void {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }

  private queueMessage(message: ClientMessage): void {
    const queuedMessage: QueuedMessage = {
      id: Math.random().toString(36).substring(7),
      data: message,
      timestamp: Date.now(),
      attempts: 0,
    };

    this.messageQueue.push(queuedMessage);
    console.log('Message queued:', queuedMessage.id);

    // Limit queue size
    if (this.messageQueue.length > 100) {
      this.messageQueue.shift();
    }
  }

  private processMessageQueue(): void {
    if (this.messageQueue.length === 0) {
      return;
    }

    console.log(`Processing ${this.messageQueue.length} queued messages`);

    const queue = [...this.messageQueue];
    this.messageQueue = [];

    for (const queuedMessage of queue) {
      try {
        this.send(queuedMessage.data);
      } catch (error) {
        console.error('Error sending queued message:', error);
        // Re-queue if failed
        if (queuedMessage.attempts < 3) {
          queuedMessage.attempts++;
          this.messageQueue.push(queuedMessage);
        }
      }
    }
  }

  private setStatus(status: ConnectionStatus): void {
    if (this.status !== status) {
      console.log('Status changed:', this.status, '->', status);
      this.status = status;
    }
  }
}
