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
export async function listAgents(params?: {
  clientId?: string;
  role?: 'system_orchestrator' | 'system_supervisor' | 'client_agent';
  status?: 'draft' | 'active' | 'paused' | 'archived';
  isPublic?: boolean;
  limit?: number;
  offset?: number;
}): Promise<Agent[]> {
  /* listAgents URL fixed - params passed directly */
  const response = await apiClient.get('/api/agents/', params);
  return response.data;
}

/**
 * Get agent by ID
 */
export async function getAgent(agentId: string): Promise<Agent> {
  const response = await apiClient.get(`/api/agents/${agentId}`);
  return response.data;
}

/**
 * Get agent by slug
 */
export async function getAgentBySlug(slug: string): Promise<Agent> {
  const response = await apiClient.get(`/api/agents/slug/${slug}`);
  return response.data;
}

/**
 * Create new agent
 */
export async function createAgent(data: AgentCreate): Promise<Agent> {
  const response = await apiClient.post('/api/agents/', data);
  return response.data;
}

/**
 * Update agent
 */
export async function updateAgent(agentId: string, data: AgentUpdate): Promise<Agent> {
  const response = await apiClient.put(`/api/agents/${agentId}`, data);
  return response.data;
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
export async function changeAgentStatus(
  agentId: string,
  newStatus: 'draft' | 'active' | 'paused' | 'archived'
): Promise<Agent> {
  const response = await apiClient.patch(`/api/agents/${agentId}/status`, null);
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
  const response = await apiClient.get(`/api/agents/${agentId}/stats`);
  return response.data;
}

// ============================================================================
// SUB-AGENTS (Nested routes)
// ============================================================================

/**
 * List sub-agents of an agent
 */
export async function listSubAgents(
  agentId: string,
  params?: {
    isActive?: boolean;
    limit?: number;
    offset?: number;
  }
): Promise<SubAgent[]> {
  const response = await apiClient.get(`/api/agents/${agentId}/sub-agents`, { params });
  return response.data;
}

/**
 * Create sub-agent for an agent
 */
export async function createSubAgent(agentId: string, data: SubAgentCreate): Promise<SubAgent> {
  const response = await apiClient.post(`/api/agents/${agentId}/sub-agents`, data);
  return response.data;
}

/**
 * Update sub-agent
 */
export async function updateSubAgent(
  agentId: string,
  subAgentId: string,
  data: SubAgentUpdate
): Promise<SubAgent> {
  const response = await apiClient.put(`/api/agents/${agentId}/sub-agents/${subAgentId}`, data);
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

export default {
  // Agents
  listAgents,
  getAgent,
  getAgentBySlug,
  createAgent,
  updateAgent,
  deleteAgent,
  changeAgentStatus,
  getAgentStats,

  // Sub-agents
  listSubAgents,
  createSubAgent,
  updateSubAgent,
  deleteSubAgent,
  toggleSubAgentActive,
};
