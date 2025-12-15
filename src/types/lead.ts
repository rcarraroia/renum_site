export type LeadStatus = 'novo' | 'qualificado' | 'em_negociacao' | 'perdido';
export type LeadSource = 'pesquisa' | 'home' | 'campanha' | 'indicacao';

export interface Lead {
  id: string;
  name: string;
  phone: string;
  email?: string;
  source: LeadSource;
  status: LeadStatus;
  subagent_id?: string;
  notes?: string;
  score?: number;
  first_contact_at?: string;
  last_interaction_at?: string;
  created_at: string;
  updated_at?: string;
}

export interface LeadCreate {
  name: string;
  phone: string;
  email?: string;
  source: LeadSource;
  status?: LeadStatus;
  subagent_id?: string;
  notes?: string;
  score?: number;
}

export interface LeadUpdate {
  name?: string;
  phone?: string;
  email?: string;
  source?: LeadSource;
  status?: LeadStatus;
  subagent_id?: string;
  notes?: string;
  score?: number;
}

export interface LeadList {
  items: Lead[];
  total: number;
  page: number;
  limit: number;
  has_next: boolean;
}

export interface LeadConvertRequest {
  company_name: string;
  cnpj: string;
  segment: string;
  plan: 'basic' | 'pro' | 'enterprise';
}
