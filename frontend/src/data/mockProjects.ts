import { Project, ProjectStatus, ProjectType, TeamMember } from "@/types/project";

const MOCK_TEAM: TeamMember[] = [
  { id: 't1', name: 'Renato Carraro', avatarUrl: 'https://i.pravatar.cc/150?img=1' },
  { id: 't2', name: 'Ana Silva', avatarUrl: 'https://i.pravatar.cc/150?img=2' },
  { id: 't3', name: 'Bruno Costa', avatarUrl: 'https://i.pravatar.cc/150?img=3' },
];

const MOCK_CLIENTS = [
    { id: 'c1', name: 'Alpha Solutions' },
    { id: 'c2', name: 'Health Clinic Pro' },
    { id: 'c3', name: 'MMN Global' },
];

const today = new Date();
const nextMonth = new Date();
nextMonth.setMonth(today.getMonth() + 1);
const lastMonth = new Date();
lastMonth.setMonth(today.getMonth() - 1);

export const MOCK_PROJECTS: Project[] = [
  {
    id: 'p1',
    name: 'Sistema de Qualificação de Leads',
    clientName: MOCK_CLIENTS[0].name,
    clientId: MOCK_CLIENTS[0].id,
    status: 'Em Andamento',
    type: 'Agente Solo',
    startDate: lastMonth,
    dueDate: nextMonth,
    progress: 65,
    responsible: MOCK_TEAM[1],
    budget: 15000,
    description: 'Implementação de um agente de IA para qualificar leads via WhatsApp.',
    scope: 'Integração com CRM, treinamento do modelo de linguagem.',
  },
  {
    id: 'p2',
    name: 'Plataforma de Análise de KPIs',
    clientName: MOCK_CLIENTS[1].name,
    clientId: MOCK_CLIENTS[1].id,
    status: 'Em Revisão',
    type: 'AI Native',
    startDate: new Date('2024-07-01'),
    dueDate: new Date('2024-11-30'),
    progress: 90,
    responsible: MOCK_TEAM[0],
    budget: 45000,
    description: 'Desenvolvimento de um SaaS para monitoramento de indicadores de saúde.',
    scope: 'Dashboard, API de dados, módulo de relatórios.',
  },
  {
    id: 'p3',
    name: 'Automação de Faturamento Mensal',
    clientName: MOCK_CLIENTS[2].name,
    clientId: MOCK_CLIENTS[2].id,
    status: 'Concluído',
    type: 'Workflow',
    startDate: new Date('2024-05-15'),
    dueDate: new Date('2024-09-01'),
    progress: 100,
    responsible: MOCK_TEAM[2],
    budget: 8000,
    description: 'Criação de um workflow para gerar e enviar faturas automaticamente.',
    scope: 'Integração com sistema financeiro e email.',
  },
  {
    id: 'p4',
    name: 'Sistema de Gestão Parlamentar',
    clientName: MOCK_CLIENTS[0].name,
    clientId: MOCK_CLIENTS[0].id,
    status: 'Pausado',
    type: 'AI Native',
    startDate: new Date('2024-10-01'),
    dueDate: new Date('2025-03-01'),
    progress: 10,
    responsible: MOCK_TEAM[0],
    budget: 60000,
    description: 'Sistema para gerenciar demandas de assessoria parlamentar.',
    scope: 'Módulo de documentos e comunicação interna.',
  },
];

export const getMockTeam = () => MOCK_TEAM;
export const getMockClients = () => MOCK_CLIENTS;