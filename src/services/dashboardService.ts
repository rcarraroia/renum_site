/**
 * Dashboard Service
 * Handles dashboard statistics API calls
 */

import { apiClient } from './api';

export interface DashboardStats {
  total_clients: number;
  total_leads: number;
  total_conversations: number;
  active_interviews: number;
  completed_interviews: number;
  completion_rate: number;
  recent_activities: RecentActivity[];
  project_status_distribution: { name: string; value: number }[];
}

export interface RecentActivity {
  type: string;
  action: string;
  timestamp: string;
  details: string;
}

class DashboardService {
  /**
   * Get dashboard statistics
   */
  async getStats(): Promise<DashboardStats> {
    const response = await apiClient.get<DashboardStats>('/api/dashboard/stats');
    return response.data;
  }

  /**
   * Get client-specific metrics
   */
  async getClientMetrics(clientId?: string): Promise<DashboardStats> {
    const params = clientId ? { clientId } : {};
    const response = await apiClient.get<DashboardStats>('/api/dashboard/client-metrics', params);
    return response.data;
  }
}

export const dashboardService = new DashboardService();
