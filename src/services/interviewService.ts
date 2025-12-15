/**
 * Interview Service
 * Handles all interview-related API calls
 */

import { apiClient } from './api';

export interface Interview {
  id: string;
  lead_id: string;
  project_id: string;
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  metadata: Record<string, any>;
  started_at?: string;
  completed_at?: string;
  created_at: string;
  updated_at?: string;
}

export interface InterviewMessage {
  id: string;
  interview_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  metadata: Record<string, any>;
  timestamp: string;
  created_at: string;
}

export interface InterviewDetail extends Interview {
  messages: InterviewMessage[];
  lead: any;
  project: any;
}

export interface InterviewResults {
  interview: Interview;
  analysis: Record<string, any>;
  summary: string;
  insights: string[];
}

export interface InterviewList {
  items: Interview[];
  total: number;
  page: number;
  limit: number;
  has_next: boolean;
}

export const interviewService = {
  /**
   * Get all interviews
   */
  async getAll(params?: {
    page?: number;
    limit?: number;
    status?: string;
  }): Promise<InterviewList> {
    const { data } = await apiClient.get<InterviewList>('/api/interviews', params);
    return data;
  },

  /**
   * Get interview by ID with details
   */
  async getById(id: string): Promise<InterviewDetail> {
    const { data } = await apiClient.get<InterviewDetail>(`/api/interviews/${id}`);
    return data;
  },

  /**
   * Get interview results with AI analysis
   */
  async getResults(id: string): Promise<InterviewResults> {
    const { data } = await apiClient.get<InterviewResults>(`/api/interviews/${id}/results`);
    return data;
  },

  /**
   * Get analytics data for interviews
   */
  async getAnalytics(params?: {
    start_date?: string;
    end_date?: string;
    project_id?: string;
  }): Promise<any> {
    const { data } = await apiClient.get('/api/interviews/analytics', params);
    return data;
  },

  /**
   * Get interviews for analysis page
   */
  async getInterviews(params?: {
    page?: number;
    limit?: number;
    status?: string;
    project_id?: string;
  }): Promise<InterviewList> {
    return this.getAll(params);
  },

  /**
   * Get interview detail for analysis
   */
  async getInterviewDetail(id: string): Promise<InterviewDetail> {
    return this.getById(id);
  },
};
