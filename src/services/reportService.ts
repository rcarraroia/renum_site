/**
 * Report Service
 * Handles all report and analytics-related API calls
 */

import { apiClient } from './api';

export interface ReportOverview {
  totalLeads: number;
  totalClients: number;
  totalConversations: number;
  totalInterviews: number;
  activeProjects: number;
  conversionRate: number;
}

export interface AgentPerformance {
  agentId: string;
  agentName: string;
  totalConversations: number;
  avgResponseTime: number;
  satisfactionScore: number;
}

export interface ConversionFunnel {
  stage: string;
  count: number;
  conversionRate: number;
}

export interface ReportFilters extends Record<string, string | undefined> {
  startDate?: string;
  endDate?: string;
  clientId?: string;
  projectId?: string;
  agentType?: string;
}

export const reportService = {
  /**
   * Get overview metrics
   */
  async getOverview(filters?: ReportFilters): Promise<ReportOverview> {
    const { data } = await apiClient.get<ReportOverview>('/api/reports/overview', filters);
    return data;
  },

  /**
   * Get metrics (alias for getOverview)
   */
  async getMetrics(filters?: ReportFilters): Promise<ReportOverview> {
    return this.getOverview(filters);
  },

  /**
   * Get agent performance metrics
   */
  async getAgentPerformance(filters?: ReportFilters): Promise<AgentPerformance[]> {
    const { data } = await apiClient.get<AgentPerformance[]>('/api/reports/agents', filters);
    return data;
  },

  /**
   * Get conversion funnel data
   */
  async getConversionFunnel(filters?: ReportFilters): Promise<ConversionFunnel[]> {
    const { data } = await apiClient.get<ConversionFunnel[]>('/api/reports/conversions', filters);
    return data;
  },

  /**
   * Export report data
   */
  async exportData(format: 'csv' | 'excel' = 'csv', filters?: ReportFilters): Promise<Blob> {
    const params = new URLSearchParams({ format });
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });
    }
    
    const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/reports/export?${params}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    });
    
    if (!response.ok) {
      throw new Error('Failed to export data');
    }
    
    return await response.blob();
  },
};
