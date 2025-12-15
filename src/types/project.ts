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
  type: ProjectType;
  description?: string;
  scope?: string;
  status: ProjectStatus;
  start_date?: string;
  due_date?: string;
  progress: number; // 0 to 100
  client_id?: string;
  responsible_id?: string;
  budget?: number;
  created_at: string;
  updated_at?: string;
}

export interface ProjectCreate {
  name: string;
  type: ProjectType;
  description?: string;
  scope?: string;
  status?: ProjectStatus;
  start_date?: string;
  due_date?: string;
  progress?: number;
  client_id?: string;
  responsible_id?: string;
  budget?: number;
}

export interface ProjectUpdate {
  name?: string;
  type?: ProjectType;
  description?: string;
  scope?: string;
  status?: ProjectStatus;
  start_date?: string;
  due_date?: string;
  progress?: number;
  client_id?: string;
  responsible_id?: string;
  budget?: number;
}

export interface ProjectList {
  items: Project[];
  total: number;
  page: number;
  limit: number;
  has_next: boolean;
}