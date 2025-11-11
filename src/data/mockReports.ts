import { ProjectStatus, ProjectType } from "@/types/project";
import { ConversationChannel } from "@/types/conversation";

// --- Overview Metrics Mock Data ---
export const MOCK_KPI_DATA = {
    totalProjects: { value: 15, change: 12, period: 'Last 30 days' },
    activeClients: { value: 8, change: 5, period: 'Last 30 days' },
    newLeads: { value: 25, change: -8, period: 'Last 30 days' },
    conversationVolume: { value: 150, change: 20, period: 'Last 30 days' },
    avgResponseTime: { value: '2.1 min', change: -15, period: 'Last 30 days' },
    completionRate: { value: '85%', change: 3, period: 'Last 30 days' },
};

// --- Chart Data Mocks ---

// Projects by Status (Donut Chart)
export const MOCK_PROJECT_STATUS_DATA: { name: ProjectStatus; value: number; fill: string }[] = [
    { name: 'Em Andamento', value: 7, fill: '#4e4ea8' },
    { name: 'Concluído', value: 5, fill: '#10b981' }, // Green
    { name: 'Em Revisão', value: 2, fill: '#0ca7d2' },
    { name: 'Pausado', value: 1, fill: '#f59e0b' }, // Yellow
];

// Projects by Type (Bar Chart)
export const MOCK_PROJECT_TYPE_DATA: { name: ProjectType; count: number; fill: string }[] = [
    { name: 'AI Native', count: 6, fill: '#FF6B35' },
    { name: 'Workflow', count: 5, fill: '#8b5cf6' }, // Purple
    { name: 'Agente Solo', count: 4, fill: '#4e4ea8' },
];

// Conversations by Channel (Pie Chart)
export const MOCK_CONVERSATION_CHANNEL_DATA: { name: ConversationChannel; value: number; fill: string }[] = [
    { name: 'Web', value: 80, fill: '#4e4ea8' },
    { name: 'WhatsApp', value: 50, fill: '#10b981' },
    { name: 'Email', value: 20, fill: '#FF6B35' },
];

// Timeline of Activities (Line Chart - last 7 days)
export const MOCK_ACTIVITY_TIMELINE = [
    { date: 'Seg', projects: 1, conversations: 15 },
    { date: 'Ter', projects: 0, conversations: 22 },
    { date: 'Qua', projects: 2, conversations: 18 },
    { date: 'Qui', projects: 1, conversations: 30 },
    { date: 'Sex', projects: 0, conversations: 25 },
    { date: 'Sáb', projects: 0, conversations: 10 },
    { date: 'Dom', projects: 0, conversations: 5 },
];

// --- Renus Performance Mocks ---
export const MOCK_RENUS_METRICS = {
    totalConversations: 150,
    resolutionRate: '75%',
    avgLength: '8.5 turns',
    avgResponseTime: '1.2 sec',
    userSatisfaction: '4.2/5',
};

export const MOCK_INTENT_BREAKDOWN = [
    { name: 'Discovery', value: 40, fill: '#4e4ea8' },
    { name: 'Suporte Técnico', value: 30, fill: '#0ca7d2' },
    { name: 'Vendas', value: 20, fill: '#FF6B35' },
    { name: 'Geral', value: 10, fill: '#9ca3af' },
];

export const MOCK_GUARDRAILS_STATS = [
    { reason: 'Conteúdo Sensível', count: 5 },
    { reason: 'Tentativa de Jailbreak', count: 2 },
    { reason: 'Informação Confidencial', count: 1 },
];

// --- Client & Project Mocks ---
export const MOCK_CLIENT_ACQUISITION = [
    { month: 'Jul', newClients: 2, projectsStarted: 3 },
    { month: 'Ago', newClients: 1, projectsStarted: 2 },
    { month: 'Set', newClients: 3, projectsStarted: 4 },
    { month: 'Out', newClients: 2, projectsStarted: 3 },
];

export const MOCK_BUDGET_COMPARISON = [
    { project: 'P1', budget: 15000, actual: 14500 },
    { project: 'P2', budget: 45000, actual: 48000 },
    { project: 'P3', budget: 8000, actual: 7500 },
];