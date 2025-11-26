export type ClientStatus = 'Ativo' | 'Inativo' | 'Prospecto';
export type ClientSegment = 'MMN' | 'Saúde' | 'Governo' | 'Serviços' | 'Tecnologia';

export interface Contact {
  name: string;
  position: string;
  email: string;
  phone: string;
}

export interface Address {
  zipCode: string;
  street: string;
  number: string;
  complement?: string;
  city: string;
  state: string;
}

export interface Client {
  id: string;
  companyName: string;
  document: string; // CNPJ/CPF
  website?: string;
  segment: ClientSegment;
  status: ClientStatus;
  contact: Contact;
  address: Address;
  projectsCount: number;
  lastInteraction: Date;
  tags: string[];
  notes?: string;
}