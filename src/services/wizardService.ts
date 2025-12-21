/**
 * Wizard Service - Sprint 06
 * API service for agent creation wizard
 */

import { apiClient } from './api';

export interface WizardSession {
  id: string;
  client_id: string;
  current_step: number;
  step_1_data?: any;
  step_2_data?: any;
  step_3_data?: any;
  step_4_data?: any;
  step_5_data?: any;
  step_6_data?: any;
  created_at: string;
  updated_at: string;
}

export interface PublicationResult {
  agent_id: string;
  slug: string;
  public_url: string;
  embed_code: string;
  qr_code_url: string;
  status: string;
}

class WizardService {
  async startWizard(clientId?: string, category?: string): Promise<WizardSession> {
    const { data } = await apiClient.post<WizardSession>('/api/agents/wizard/start', {
      client_id: clientId,
      category: category
    });
    return data;
  }

  async saveStep(wizardId: string, stepNumber: number, data: any): Promise<WizardSession> {
    const { data: responseData } = await apiClient.put<WizardSession>(`/api/agents/wizard/${wizardId}/step/${stepNumber}`, {
      step_number: stepNumber,
      data
    });
    return responseData;
  }

  async getWizard(wizardId: string): Promise<WizardSession> {
    const { data } = await apiClient.get<WizardSession>(`/api/agents/wizard/${wizardId}`);
    return data;
  }

  async deleteWizard(wizardId: string): Promise<void> {
    await apiClient.delete(`/api/agents/wizard/${wizardId}`);
  }

  async listTemplates(): Promise<any[]> {
    const { data } = await apiClient.get<any[]>('/api/agents/wizard/templates/list');
    return data;
  }

  async getTemplate(templateType: string): Promise<any> {
    const { data } = await apiClient.get(`/api/agents/wizard/templates/${templateType}`);
    return data;
  }

  // Sandbox methods

  async startSandbox(wizardId: string): Promise<any> {
    const { data } = await apiClient.post(`/api/agents/wizard/${wizardId}/sandbox/start`);
    return data;
  }

  async sendSandboxMessage(wizardId: string, message: string): Promise<any> {
    const { data } = await apiClient.post(`/api/agents/wizard/${wizardId}/sandbox/message`, { message });
    return data;
  }

  async getSandboxHistory(wizardId: string): Promise<any[]> {
    const { data } = await apiClient.get<any[]>(`/api/agents/wizard/${wizardId}/sandbox/history`);
    return data;
  }

  async getSandboxData(wizardId: string): Promise<any> {
    const { data } = await apiClient.get(`/api/agents/wizard/${wizardId}/sandbox/data`);
    return data;
  }

  async cleanupSandbox(wizardId: string): Promise<void> {
    await apiClient.delete(`/api/agents/wizard/${wizardId}/sandbox`);
  }

  // Publication

  async publishAgent(wizardId: string): Promise<PublicationResult> {
    const { data } = await apiClient.post<PublicationResult>(`/api/agents/wizard/${wizardId}/publish`);
    return data;
  }

  // Utility
  async convertN8n(workflow: any): Promise<{ name: string; description: string; system_prompt_hint: string; node_count: number }> {
    const { data } = await apiClient.post<{ name: string; description: string; system_prompt_hint: string; node_count: number }>('/api/agents/wizard/n8n-convert', workflow);
    return data;
  }
}

export const wizardService = new WizardService();
export default wizardService;
