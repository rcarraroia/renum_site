/**
 * Agent Types - Sprint 09
 * Type definitions for agents and sub-agents
 */

/**
 * Agent status
 */
export type AgentStatus = 'draft' | 'active' | 'paused' | 'archived';

/**
 * Communication channel
 */
export type Channel = 'whatsapp' | 'web' | 'sms' | 'email';

/**
 * Template type
 */
export type TemplateType = 'custom' | 'mmn' | 'vereador' | 'clinica' | 'pesquisa';

/**
 * Agent Categories
 */
export type AgentCategory = 'discovery' | 'vendas' | 'suporte' | 'mmn' | 'clinica' | 'vereador' | 'custom';

export interface CategoryMock {
  id: AgentCategory;
  name: string;
  icon: string;
}

/**
 * LLM model
 */
export type Model = 'gpt-4' | 'gpt-4-turbo-preview' | 'gpt-4o-mini' | 'claude-3-5-sonnet-20241022' | 'claude-3-opus';

/**
 * Agent (main agent in hierarchy: clients → agents → sub_agents)
 */
export interface Agent {
  id: string;
  client_id: string;
  name: string;
  description: string | null;
  slug: string | null;
  model: Model;
  system_prompt: string;
  channel: Channel;
  template_type: TemplateType;
  status: AgentStatus;
  is_public: boolean;
  public_url: string | null;
  config: Record<string, any>;
  access_count: number;
  created_at: string;
  updated_at: string;
}

/**
 * Agent create payload
 */
export interface AgentCreate {
  client_id: string;
  name: string;
  description?: string | null;
  slug?: string | null;
  model?: Model;
  system_prompt: string;
  channel: Channel;
  template_type?: TemplateType;
  status?: AgentStatus;
  is_public?: boolean;
  public_url?: string | null;
  config?: Record<string, any>;
}

/**
 * Agent update payload
 */
export interface AgentUpdate {
  name?: string;
  description?: string | null;
  slug?: string | null;
  model?: Model;
  system_prompt?: string;
  channel?: Channel;
  template_type?: TemplateType;
  status?: AgentStatus;
  is_public?: boolean;
  public_url?: string | null;
  config?: Record<string, any>;
}

/**
 * Agent list item (lightweight)
 */
export interface AgentListItem {
  id: string;
  client_id: string;
  name: string;
  description: string | null;
  channel: Channel;
  template_type: TemplateType;
  status: AgentStatus;
  is_public: boolean;
  model: Model;
  created_at: string;
  updated_at: string;
  sub_agents_count?: number;
  access_count?: number;
}

/**
 * Agent statistics
 */
export interface AgentStats {
  agent_id: string;
  sub_agents_count: number;
  total_conversations: number;
  active_conversations: number;
  total_messages: number;
  access_count: number;
  last_used_at: string | null;
}

// ============================================================================
// SUB-AGENTS
// ============================================================================

/**
 * Sub-agent (specialized agent under main agent)
 */
export interface SubAgent {
  id: string;
  agent_id: string | null;
  name: string;
  description: string | null;
  channel: Channel;
  system_prompt: string;
  topics: string[] | null;
  model: Model;
  is_active: boolean;
  fine_tuning_config: Record<string, any> | null;
  config_id: number | null;
  slug: string | null;
  public_url: string | null;
  access_count: number;
  is_public: boolean;
  knowledge_base: Record<string, any> | null;
  created_at: string;
  updated_at: string;
}

/**
 * Sub-agent create payload
 */
export interface SubAgentCreate {
  name: string;
  description?: string | null;
  channel: Channel;
  system_prompt: string;
  topics?: string[] | null;
  model?: Model;
  is_active?: boolean;
  fine_tuning_config?: Record<string, any> | null;
  config_id?: number | null;
}

/**
 * Sub-agent update payload
 */
export interface SubAgentUpdate {
  name?: string;
  description?: string | null;
  channel?: Channel;
  system_prompt?: string;
  topics?: string[] | null;
  model?: Model;
  is_active?: boolean;
  fine_tuning_config?: Record<string, any> | null;
}

/**
 * Sub-agent list item (lightweight)
 */
export interface SubAgentListItem {
  id: string;
  name: string;
  description: string | null;
  channel: Channel;
  model: Model;
  is_active: boolean;
  topics: string[] | null;
  created_at: string;
  updated_at: string;
  total_interviews?: number;
  completion_rate?: number;
}

/**
 * Agent with sub-agents count
 */
export interface AgentWithStats extends Agent {
  sub_agents_count: number;
}

/**
 * Sub-agent with parent agent info
 */
export interface SubAgentWithAgent extends SubAgent {
  agent_name?: string;
  agent_slug?: string;
}
