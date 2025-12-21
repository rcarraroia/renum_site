
/**
 * Integration Service - Sprint 07A
 * Service for managing integrations (WhatsApp, Email, Database)
 */

import { apiClient } from './api';

export interface Integration {
  id: string
  client_id: string
  provider: string // Changed from type to provider to match backend
  name?: string
  status: 'connected' | 'disconnected' | 'error'
  config: Record<string, any>
  created_at: string
  updated_at: string
  agent_id?: string | null
}

export interface IntegrationTestResult {
  success: boolean
  message: string
  latency_ms?: number
  details?: Record<string, any>
}

class IntegrationService {
  /**
   * Get all integrations for current client
   */
  async listIntegrations(provider?: string, agentId?: string): Promise<Integration[]> {
    const params: any = {};
    if (provider) params.provider = provider;
    if (agentId) params.agent_id = agentId;

    const response = await apiClient.get<Integration[]>('/api/integrations/', { params });
    return response.data;
  }

  /**
   * Save (Create/Update) integration
   */
  async saveIntegration(
    provider: string,
    config: Record<string, any>,
    agent_id?: string
  ): Promise<Integration> {
    const payload = { config, agent_id };
    const response = await apiClient.post<Integration>(`/api/integrations/${provider}`, payload);
    return response.data;
  }

  /**
   * Test integration connection
   */
  async testIntegration(
    provider: string,
    config: Record<string, any>
  ): Promise<IntegrationTestResult> {
    const payload = { config };
    const response = await apiClient.post<IntegrationTestResult>(`/api/integrations/${provider}/test`, payload);
    return response.data;
  }
  /**
   * Get aggregated status for Radar
   */
  async getIntegrationsStatus(): Promise<any[]> {
    const response = await apiClient.get<any[]>('/api/integrations/status');
    return response.data;
  }
}

export const integrationService = new IntegrationService();
