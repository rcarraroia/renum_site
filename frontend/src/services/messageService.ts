/**
 * Message Service
 * API client for message operations
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface MessageCreate {
  conversation_id: string;
  sender: 'admin' | 'client' | 'system';
  type: 'text' | 'image' | 'file';
  content: string;
  metadata?: Record<string, any>;
}

export interface MessageResponse {
  id: string;
  conversation_id: string;
  sender: 'admin' | 'client' | 'system';
  type: 'text' | 'image' | 'file';
  content: string;
  timestamp: string;
  is_read: boolean;
  metadata: Record<string, any> | null;
  created_at: string;
}

class MessageService {
  private getAuthToken(): string {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('No authentication token found');
    }
    return token;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getAuthToken();

    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  /**
   * Get messages for a conversation with pagination
   */
  async getMessages(
    conversationId: string,
    limit: number = 50,
    beforeId?: string
  ): Promise<MessageResponse[]> {
    const params = new URLSearchParams({
      conversation_id: conversationId,
      limit: limit.toString(),
    });

    if (beforeId) {
      params.append('before_id', beforeId);
    }

    return this.request<MessageResponse[]>(
      `/api/messages?${params.toString()}`
    );
  }

  /**
   * Send message via REST (fallback when WebSocket is not available)
   */
  async sendMessage(data: MessageCreate): Promise<MessageResponse> {
    return this.request<MessageResponse>('/api/messages', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * Mark messages as read
   */
  async markMessagesAsRead(messageIds: string[]): Promise<{
    success: boolean;
    marked_count: number;
    message: string;
  }> {
    return this.request('/api/messages/mark-read', {
      method: 'PATCH',
      body: JSON.stringify(messageIds),
    });
  }
}

// Export singleton instance
export const messageService = new MessageService();
