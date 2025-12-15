/**
 * Integration Service - Sprint 07A
 * Service for managing integrations (WhatsApp, Email, Database)
 */

import { apiClient } from './api';

export interface Integration {
  id: string
  client_id: string
  type: 'whatsapp' | 'email_smtp' | 'email_sendgrid' | 'database'
  name: string
  status: 'connected' | 'disconnected' | 'error'
  config: Record<string, any>
  last_tested_at?: string
  last_error?: string
  created_at: string
  updated_at: string
}

export interface IntegrationCreate {
  type: 'whatsapp' | 'email_smtp' | 'email_sendgrid' | 'database'
  name: string
  config: Record<string, any>
}

export interface IntegrationTestResult {
  success: boolean
  message: string
  latency_ms?: number
  details?: Record<string, any>
}


  /**
   * Get all integrations for current client
   */
  async listIntegrations(provider ?: string): Promise < Integration[] > {
  const params = provider ? { provider } : undefined;
  const response = await apiClient.get<Integration[]>('/api/integrations', { params });
  return response.data;
}

  /**
   * Save (Create/Update) integration
   */
  async saveIntegration(
  provider: string,
  config: Record<string, any>,
  agent_id ?: string
): Promise < Integration > {
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
): Promise < IntegrationTestResult > {
  const payload = { config };
  const response = await apiClient.post<IntegrationTestResult>(`/api/integrations/${provider}/test`, payload);
  return response.data;
}
}

export const integrationService = new IntegrationService()
