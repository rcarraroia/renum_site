export type AgentStatus = 'ativo' | 'inativo' | 'pausado' | 'erro';
export type AgentType = 'b2b_empresa' | 'b2c_marketplace' | 'b2c_individual';
export type AgentChannel = 'whatsapp' | 'web' | 'telegram' | 'sms';
export type AgentCategory = 'discovery' | 'vendas' | 'suporte' | 'mmn' | 'clinica' | 'vereador' | 'custom';

export interface Agent {
  id: string;
  name: string;
  description: string;
  client_id: string;
  project_id: string;
  type: AgentType;
  category: AgentCategory;
  slug: string;
  domain: string;
  channel: AgentChannel[];
  model: string;
  status: AgentStatus;
  instances_count: number;
  conversations_today: number;
  created_at: string; // Date string
  version: string; // Added version property
}

export interface ProjectMock {
  id: string;
  name: string;
  client_id: string;
  agents_limit: number;
}

export interface ClientMock {
  id: string;
  name: string;
  type: AgentType;
  slug: string;
}

export interface ChannelMock {
  id: AgentChannel;
  name: string;
  icon: string;
}

export interface ModelMock {
  id: string;
  name: string;
  provider: string;
  cost: string;
  description: string;
}

export interface CategoryMock {
  id: AgentCategory; // Changed type to AgentCategory
  name: string;
  icon: string;
}