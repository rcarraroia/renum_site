/**
 * Conversation Service - Sprint 09
 * Handles all conversation-related API calls with WebSocket integration
 */

import { apiClient } from './api';

export interface Conversation {
  id: string;
  lead_id: string;
  client_id: string;
  status: 'open' | 'closed';
  last_message_at?: string;
  created_at: string;
  updated_at?: string;
}

export interface Message {
  id: string;
  conversation_id: string;
  user_id?: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  channel: 'whatsapp' | 'sms' | 'email' | 'web';
  metadata?: Record<string, any>;
  timestamp?: string;
  created_at: string;
}

export interface ConversationList {
  items: Conversation[];
  total: number;
  page: number;
  limit: number;
  has_next: boolean;
}

// Message cache for real-time updates
class MessageCache {
  private cache: Map<string, Message[]> = new Map();

  get(conversationId: string): Message[] | undefined {
    return this.cache.get(conversationId);
  }

  set(conversationId: string, messages: Message[]): void {
    this.cache.set(conversationId, messages);
  }

  add(conversationId: string, message: Message): void {
    const messages = this.cache.get(conversationId) || [];
    messages.push(message);
    this.cache.set(conversationId, messages);
  }

  clear(conversationId?: string): void {
    if (conversationId) {
      this.cache.delete(conversationId);
    } else {
      this.cache.clear();
    }
  }
}

const messageCache = new MessageCache();

export const conversationService = {
  /**
   * Get all conversations
   */
  async getAll(params?: {
    page?: number;
    limit?: number;
    status?: string;
  }): Promise<ConversationList> {
    const { data } = await apiClient.get<ConversationList>('/api/conversations/', params);
    return data;
  },

  /**
   * Get conversation by ID
   */
  async getById(id: string): Promise<Conversation> {
    const { data } = await apiClient.get<Conversation>(`/api/conversations/${id}`);
    return data;
  },

  /**
   * Get messages for a conversation
   * Uses cache if available, otherwise fetches from API
   */
  async getMessages(conversationId: string, useCache = true): Promise<Message[]> {
    // Check cache first
    if (useCache) {
      const cached = messageCache.get(conversationId);
      if (cached) {
        return cached;
      }
    }

    // Fetch from API
    const { data } = await apiClient.get<{ items: Message[] }>(`/api/conversations/${conversationId}/messages`);
    const messages = data.items;

    // Update cache
    messageCache.set(conversationId, messages);

    return messages;
  },

  /**
   * Send message via HTTP (fallback)
   * For WebSocket, use WebSocketClient.sendMessage() instead
   */
  async sendMessage(conversationId: string, content: string): Promise<Message> {
    const { data } = await apiClient.post<Message>(`/api/conversations/${conversationId}/messages`, {
      content,
      role: 'user',
      channel: 'web',
    });

    // Update cache
    messageCache.add(conversationId, data);

    return data;
  },

  /**
   * Add message to cache (called by WebSocket handler)
   */
  addMessageToCache(message: Message): void {
    messageCache.add(message.conversation_id, message);
  },

  /**
   * Get messages after a specific message ID
   * Used for syncing missed messages
   */
  async getMessagesAfter(conversationId: string, afterMessageId: string): Promise<Message[]> {
    const { data } = await apiClient.get<{ items: Message[] }>(
      `/api/conversations/${conversationId}/messages`,
      {
        after: afterMessageId,
      }
    );
    return data.items;
  },

  /**
   * Mark message as read
   */
  async markAsRead(conversationId: string, messageId: string): Promise<void> {
    await apiClient.post(`/api/conversations/${conversationId}/messages/${messageId}/read`);
  },

  /**
   * Clear message cache
   */
  clearCache(conversationId?: string): void {
    messageCache.clear(conversationId);
  },

  /**
   * Get cached messages (for real-time updates)
   */
  getCachedMessages(conversationId: string): Message[] | undefined {
    return messageCache.get(conversationId);
  },
};
