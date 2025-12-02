import { Agent, AgentStatus, AgentChannel } from "@/types/agent";

export const MOCK_SLIM_AGENT: Agent = {
  id: 'a1',
  name: 'Agente de Vendas Slim',
  status: 'Active',
  channel: 'WhatsApp',
  description: 'Agente especializado em qualificação e vendas para a Slim Quality.',
  version: 'V2.1',
  lastPublished: '2025-01-20 14:30',
  
  // --- Integrações Mock ---
  integrations: [
    {
      name: 'WhatsApp Business',
      status: 'Configurado',
      provider: 'Uazapi',
      configuredAt: '14/11/2025',
      details: {
        phone: '+55 11 99999-9999',
      },
    },
    {
      name: 'Gmail',
      status: 'Configurado',
      details: {
        email: 'vendas@slim.com',
      },
    },
    {
      name: 'Google Workspace',
      status: 'Parcialmente configurado',
      details: {
        apps: 'Docs, Sheets, Calendar',
      },
    },
    {
      name: 'Composio',
      status: 'Não configurado',
      details: {},
    },
    {
      name: 'SMTP Custom',
      status: 'Não configurado',
      details: {},
    },
  ],

  // --- API & Webhooks Mock ---
  apiKeys: [
    {
      key: 'sk-slim-abc123',
      name: 'Site Slim Quality',
      createdAt: '15/11/2025',
      lastUsed: '2 min atrás',
    },
    {
      key: 'sk-slim-xyz789',
      name: 'WhatsApp Bot',
      createdAt: '10/11/2025',
      lastUsed: '1 hora atrás',
    },
  ],
  webhookConfig: {
    url: 'https://api.renum.com.br/webhook/slim/abc123',
    events: ['message.received', 'conversation.started'],
    callbackUrl: 'https://slim.com.br/webhook/renum',
    status: 'Funcionando',
    logs: [
      { date: '01/12 10:23', event: 'message.received', status: '200 OK' },
      { date: '01/12 10:15', event: 'conversation.started', status: '200 OK' },
      { date: '01/12 09:47', event: 'message.received', status: '500 Error' },
    ],
  },
  widgetConfig: {
    primaryColor: '#6366F1',
    position: 'bottom-right',
    embedCode: '<script src="renum-widget.js" data-agent="slim-vendas"></script>',
  },
  
  // --- Placeholder for other config tabs (reusing existing mock structures) ---
  instructions: {},
  tools: [],
  knowledge: [],
  triggers: [],
  guardrails: {},
  advancedConfig: {},
};

export const getAgentById = (id: string): Agent | undefined => {
    if (id === MOCK_SLIM_AGENT.id) return MOCK_SLIM_AGENT;
    // Mock other agents if needed
    return MOCK_SLIM_AGENT; // Default to Slim Agent for now
};