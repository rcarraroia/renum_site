export type ProjectStatus = 'Em Andamento' | 'Concluído' | 'Pausado' | 'Atrasado' | 'Em Revisão';
export type ProjectType = 'AI Native' | 'Workflow' | 'Agente Solo';

export interface TeamMember {
  id: string;
  name: string;
  avatarUrl?: string;
}

export interface Project {
  id: string;
  name: string;
  clientName: string;
  clientId: string;
  status: ProjectStatus;
  type: ProjectType;
  startDate: Date;
  dueDate: Date;
  progress: number; // 0 to 100
  responsible: TeamMember;
  budget: number;
  description: string;
  scope: string;
}