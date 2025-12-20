/**
 * Agent Service - Sprint 09 (Task F.6, F.7)
 * Service for managing agents and sub-agents
 * 
 * NO MOCKS - All data comes from real API
 */

import { apiClient } from './api';
import type { Agent, AgentCreate, AgentUpdate, SubAgent, SubAgentCreate, SubAgentUpdate } from '@/types/agent';

/**
 * List agents with optional filters
 */
export async function listAgents(params: any = {}): Promise<Agent[]> {
  const response = await apiClient.get<Agent[]>('/api/agents/', params);
  return response.data;
}

/**
 * Get agent by ID
 */
export async function getAgent(id: string): Promise<Agent> {
  const response = await apiClient.get<Agent>(`/api/agents/${id}`);
  return response.data;
}

/**
 * Get agent by slug
 */
export async function getAgentBySlug(slug: string): Promise<Agent> {
  const response = await apiClient.get<Agent>(`/api/agents/slug/${slug}`);
  return response.data;
}

/**
 * Create new agent
 */
export async function createAgent(data: Partial<Agent>): Promise<Agent> {
  const response = await apiClient.post<Agent>('/api/agents/', data);
  return response.data;
}

/**
 * Update agent
 */
export async function updateAgent(id: string, data: Partial<Agent>): Promise<Agent> {
  const response = await apiClient.put<Agent>(`/api/agents/${id}`, data);
  return response.data;
}

/**
 * Get system agent (orchestrator or supervisor)
 */
export async function getSystemAgent(
  role: 'system_orchestrator' | 'system_supervisor' = 'system_orchestrator'
): Promise<Agent | undefined> {
  const response = await apiClient.get<Agent[]>('/api/agents/', { role, limit: 1 });
  return response.data[0];
}

/**
 * Delete agent
 */
export async function deleteAgent(agentId: string): Promise<void> {
  await apiClient.delete(`/api/agents/${agentId}`);
}

/**
 * Change agent status
 */
export async function changeAgentStatus(id: string, status: string): Promise<Agent> {
  const response = await apiClient.patch<Agent>(`/api/agents/${id}/status`, { new_status: status });
  return response.data;
}

/**
 * Get agent statistics
 */
export async function getAgentStats(agentId: string): Promise<{
  agent_id: string;
  sub_agents_count: number;
  total_conversations: number;
  active_conversations: number;
  total_messages: number;
  access_count: number;
  last_used_at: string | null;
}> {
  const response = await apiClient.get<{
    agent_id: string;
    sub_agents_count: number;
    total_conversations: number;
    active_conversations: number;
    total_messages: number;
    access_count: number;
    last_used_at: string | null;
  }>(`/api/agents/${agentId}/stats`);
  return response.data;
}

// ============================================================================
// SUB-AGENTS (Nested routes)
// ============================================================================

/**
 * List sub-agents of an agent
 */
export async function listSubAgents(agentId: string, params: any = {}): Promise<SubAgent[]> {
  const response = await apiClient.get<SubAgent[]>(`/api/agents/${agentId}/sub-agents`, params);
  return response.data;
}

/**
 * Create sub-agent for an agent
 */
export async function createSubAgent(agentId: string, data: Partial<SubAgent>): Promise<SubAgent> {
  const response = await apiClient.post<SubAgent>(`/api/agents/${agentId}/sub-agents`, data);
  return response.data;
}

/**
 * Update sub-agent
 */
export async function updateSubAgent(agentId: string, subAgentId: string, data: Partial<SubAgent>): Promise<SubAgent> {
  const response = await apiClient.put<SubAgent>(`/api/agents/${agentId}/sub-agents/${subAgentId}`, data);
  return response.data;
}

/**
 * Delete sub-agent
 */
export async function deleteSubAgent(agentId: string, subAgentId: string): Promise<void> {
  await apiClient.delete(`/api/agents/${agentId}/sub-agents/${subAgentId}`);
}

/**
 * Toggle sub-agent active status
 */
export async function toggleSubAgentActive(
  agentId: string,
  subAgentId: string
): Promise<SubAgent> {
  // Get current sub-agent
  const subAgents = await listSubAgents(agentId);
  const subAgent = subAgents.find(sa => sa.id === subAgentId);

  if (!subAgent) {
    throw new Error('Sub-agent not found');
  }

  // Toggle is_active
  return updateSubAgent(agentId, subAgentId, {
    is_active: !subAgent.is_active
  });
}

/**
 * List templates from marketplace
 */
export async function listTemplates(params: { niche?: string } = {}): Promise<Agent[]> {
  const response = await apiClient.get<Agent[]>('/api/agents/', {
    ...params,
    is_template: true
  });
  return response.data;
}

/**
 * Clone template for client
 */
export async function cloneTemplate(templateId: string, customName?: string): Promise<Agent> {
  const response = await apiClient.post<Agent>(`/api/marketplace/templates/${templateId}/clone`, {
    custom_name: customName
  });
  return response.data;
}

export const agentService = {
  // Agents
  listAgents,
  getAgent,
  getAgentBySlug,
  createAgent,
  updateAgent,
  deleteAgent,
  changeAgentStatus,
  getAgentStats,
  getSystemAgent,

  // Sub-agents
  listSubAgents,
  createSubAgent,
  updateSubAgent,
  deleteSubAgent,
  toggleSubAgentActive,

  // Templates
  listTemplates,
  cloneTemplate,
};

export default agentService;
