export type ClientStatus = 'active' | 'inactive' | 'suspended';

export interface ContactInfo {
  phone?: string;
  email?: string;
  whatsapp?: string;
  telegram?: string;
}

export interface AddressInfo {
  street?: string;
  number?: string;
  complement?: string;
  neighborhood?: string;
  city?: string;
  state?: string;
  zipcode?: string;
  country?: string;
}

export interface Client {
  id: string;
  company_name: string;
  document?: string;
  website?: string;
  segment: string;  // Obrigatório no backend
  status: ClientStatus;
  contact?: ContactInfo;
  address?: AddressInfo;
  tags?: string[];
  notes?: string;
  last_interaction?: string;
  created_at: string;
  updated_at?: string;
}

export interface ClientCreate {
  company_name: string;
  document?: string;
  website?: string;
  segment?: string;
  status?: ClientStatus;
  contact?: ContactInfo;
  address?: AddressInfo;
  tags?: string[];
  notes?: string;
}

export interface ClientUpdate {
  company_name?: string;
  document?: string;
  website?: string;
  segment?: string;
  status?: ClientStatus;
  contact?: ContactInfo;
  address?: AddressInfo;
  tags?: string[];
  notes?: string;
}

export interface ClientList {
  items: Client[];
  total: number;
  page: number;
  limit: number;
  has_next: boolean;
}