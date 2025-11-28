/**
 * Conversation Service
 * API client for conversation operations
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface ConversationFilters {
  client_id?: string;
  status?: 'active' | 'closed' | 'pending';
  priority?: 'Low' | 'Medium' | 'High';
  search?: string;
}

export interface ConversationCreate {
  client_id: string;
  status: 'active' | 'closed' | 'pending';
  channel: 'whatsapp' | 'email' | 'web';
  assigned_agent_id?: string;
  priority?: 'Low' | 'Medium' | 'High';
  summary?: string;
  tags?: string[];
}

export interface ConversationUpdate {
  status?: 'active' | 'closed' | 'pending';
  assigned_agent_id?: string;
  priority?: 'Low' | 'Medium' | 'High';
  summary?: string;
  tags?: string[];
}

export interface ConversationResponse {
  id: string;
  client_id: string;
  status: 'active' | 'closed' | 'pending';
  channel: 'whatsapp' | 'email' | 'web';
  assigned_agent_id: string | null;
  unread_count: number;
  priority: 'Low' | 'Medium' | 'High';
  start_date: string;
  last_update: string;
  summary: string | null;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface ConversationListResponse {
  items: ConversationResponse[];
  total: number;
  page: number;
  limit: number;
  has_next: boolean;
}

class ConversationService {
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
   * Create new conversation
   */
  async createConversation(data: ConversationCreate): Promise<ConversationResponse> {
    return this.request<ConversationResponse>('/api/conversations', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * Get conversations with filters and pagination
   */
  async getConversations(
    page: number = 1,
    limit: number = 20,
    filters?: ConversationFilters
  ): Promise<ConversationListResponse> {
    const params = new URLSearchParams({
      page: page.toString(),
      limit: limit.toString(),
    });

    if (filters?.client_id) params.append('client_id', filters.client_id);
    if (filters?.status) params.append('status', filters.status);
    if (filters?.priority) params.append('priority', filters.priority);
    if (filters?.search) params.append('search', filters.search);

    return this.request<ConversationListResponse>(
      `/api/conversations?${params.toString()}`
    );
  }

  /**
   * Get conversation by ID
   */
  async getConversationById(id: string): Promise<ConversationResponse> {
    return this.request<ConversationResponse>(`/api/conversations/${id}`);
  }

  /**
   * Update conversation
   */
  async updateConversation(
    id: string,
    data: ConversationUpdate
  ): Promise<ConversationResponse> {
    return this.request<ConversationResponse>(`/api/conversations/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  /**
   * Update conversation status
   */
  async updateStatus(
    id: string,
    status: 'active' | 'closed' | 'pending'
  ): Promise<ConversationResponse> {
    return this.request<ConversationResponse>(
      `/api/conversations/${id}/status?status=${status}`,
      {
        method: 'PATCH',
      }
    );
  }

  /**
   * Delete conversation (soft delete)
   */
  async deleteConversation(id: string): Promise<void> {
    await this.request<void>(`/api/conversations/${id}`, {
      method: 'DELETE',
    });
  }

  /**
   * Mark conversation as read
   */
  async markAsRead(id: string): Promise<ConversationResponse> {
    return this.request<ConversationResponse>(
      `/api/conversations/${id}/mark-read`,
      {
        method: 'POST',
      }
    );
  }
}

// Export singleton instance
export const conversationService = new ConversationService();
