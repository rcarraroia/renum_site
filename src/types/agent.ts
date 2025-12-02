export type AgentStatus = 'Active' | 'Inactive' | 'Draft' | 'Training';
export type AgentChannel = 'Web' | 'WhatsApp' | 'Email' | 'API';

export interface AgentIntegration {
  name: string;
  status: 'Configurado' | 'Parcialmente configurado' | 'Não configurado';
  provider?: string;
  details: Record<string, string | number | boolean>;
  configuredAt?: string;
}

export interface ApiKey {
  key: string;
  name: string;
  createdAt: string;
  lastUsed: string;
}

export interface WebhookConfig {
  url: string;
  events: string[];
  callbackUrl: string;
  status: 'Funcionando' | 'Erro';
  logs: { date: string; event: string; status: string }[];
}

export interface Agent {
  id: string;
  name: string;
  status: AgentStatus;
  channel: AgentChannel;
  description: string;
  version: string;
  lastPublished: string;
  integrations: AgentIntegration[];
  apiKeys: ApiKey[];
  webhookConfig: WebhookConfig;
  widgetConfig: {
    primaryColor: string;
    position: string;
    embedCode: string;
  };
  // Placeholder for configuration tabs data
  instructions: Record<string, string>;
  tools: any[];
  knowledge: any[];
  triggers: any[];
  guardrails: Record<string, any>;
  advancedConfig: Record<string, any>;
}