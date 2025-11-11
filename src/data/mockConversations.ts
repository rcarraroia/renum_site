import { Conversation, ConversationMessage, ConversationStatus, ConversationChannel, MessageSender } from "@/types/conversation";
import { MOCK_CLIENTS_DATA } from "./mockClients";
import { getMockTeam } from "./mockProjects";

const MOCK_ADMIN = getMockTeam()[0];
const MOCK_CLIENT_ALPHA = MOCK_CLIENTS_DATA[0];
const MOCK_CLIENT_HEALTH = MOCK_CLIENTS_DATA[1];

const generateMockMessages = (clientId: string): ConversationMessage[] => {
    const now = new Date();
    const messages: ConversationMessage[] = [
        {
            id: 'm1', sender: 'system', type: 'text', content: 'Conversa iniciada via Web Chat.',
            timestamp: new Date(now.getTime() - 120000), read: true,
        },
        {
            id: 'm2', sender: 'client', type: 'text', content: 'Olá, estou com um problema na qualificação dos meus leads. O Renus pode ajudar?',
            timestamp: new Date(now.getTime() - 110000), read: true,
            metadata: { intent: 'Desafio de Negócio', sentiment: 'neutral' }
        },
        {
            id: 'm3', sender: 'renus', type: 'text', content: 'Olá! Eu sou Renus, seu assistente de descoberta. Com certeza! Para mapear a solução ideal, preciso entender seu funil atual. Qual é o seu principal gargalo hoje?',
            timestamp: new Date(now.getTime() - 90000), read: true,
            metadata: { intent: 'Discovery', sentiment: 'positive' }
        },
        {
            id: 'm4', sender: 'client', type: 'text', content: 'O gargalo é a demora em responder no WhatsApp. Perdemos muitos leads por isso.',
            timestamp: new Date(now.getTime() - 60000), read: false,
            metadata: { intent: 'Problema Operacional', sentiment: 'negative' }
        },
    ];

    if (clientId === MOCK_CLIENT_ALPHA.id) {
        messages.push({
            id: 'm5', sender: 'renus', type: 'text', content: 'Entendido. Isso é um caso clássico para um Agente Solo de Resposta Imediata. Vou gerar um resumo de viabilidade.',
            timestamp: new Date(now.getTime() - 30000), read: false,
            metadata: { intent: 'Sugestão de Solução', sentiment: 'positive', tool_call: 'generate_viability_report' }
        });
    }
    
    return messages;
};

export const MOCK_CONVERSATIONS: Conversation[] = [
  {
    id: 'conv1',
    client: {
        id: MOCK_CLIENT_ALPHA.id,
        companyName: MOCK_CLIENT_ALPHA.companyName,
        contact: MOCK_CLIENT_ALPHA.contact,
        segment: MOCK_CLIENT_ALPHA.segment,
    },
    status: 'Em Andamento',
    channel: 'Web',
    assignedAgent: MOCK_ADMIN,
    messages: generateMockMessages(MOCK_CLIENT_ALPHA.id),
    unreadCount: 2,
    priority: 'High',
    startDate: new Date(new Date().getTime() - 120000),
    lastUpdate: new Date(new Date().getTime() - 30000),
    summary: 'Discussão inicial sobre gargalo de leads no WhatsApp. Sugestão de Agente Solo.',
    tags: ['Vendas', 'Agente Solo', 'Lead Qualificado'],
  },
  {
    id: 'conv2',
    client: {
        id: MOCK_CLIENT_HEALTH.id,
        companyName: MOCK_CLIENT_HEALTH.companyName,
        contact: MOCK_CLIENT_HEALTH.contact,
        segment: MOCK_CLIENT_HEALTH.segment,
    },
    status: 'Nova',
    channel: 'WhatsApp',
    assignedAgent: null,
    messages: [
        { id: 'm1', sender: 'client', type: 'text', content: 'Preciso de um sistema para agendamento inteligente na clínica.', timestamp: new Date(new Date().getTime() - 3600000), read: false },
    ],
    unreadCount: 1,
    priority: 'Medium',
    startDate: new Date(new Date().getTime() - 3600000),
    lastUpdate: new Date(new Date().getTime() - 3600000),
    summary: 'Cliente solicitando informações sobre sistema de agendamento.',
    tags: ['Saúde', 'AI Native'],
  },
  {
    id: 'conv3',
    client: {
        id: MOCK_CLIENTS_DATA[2].id,
        companyName: MOCK_CLIENTS_DATA[2].companyName,
        contact: MOCK_CLIENTS_DATA[2].contact,
        segment: MOCK_CLIENTS_DATA[2].segment,
    },
    status: 'Resolvida',
    channel: 'Email',
    assignedAgent: MOCK_ADMIN,
    messages: [
        { id: 'm1', sender: 'client', type: 'text', content: 'O workflow de faturamento está funcionando perfeitamente. Obrigado!', timestamp: new Date(new Date().getTime() - 86400000), read: true },
        { id: 'm2', sender: 'system', type: 'text', content: 'Conversa marcada como Resolvida.', timestamp: new Date(new Date().getTime() - 86300000), read: true },
    ],
    unreadCount: 0,
    priority: 'Low',
    startDate: new Date(new Date().getTime() - 86400000 * 5),
    lastUpdate: new Date(new Date().getTime() - 86300000),
    summary: 'Feedback positivo sobre o workflow de faturamento.',
    tags: ['Workflow', 'Feedback'],
  },
];