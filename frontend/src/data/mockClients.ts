import { Client, ClientStatus, ClientSegment, Contact, Address } from "@/types/client";

const MOCK_CONTACTS: Contact[] = [
    { name: 'João Silva', position: 'CEO', email: 'joao.silva@alpha.com', phone: '(11) 98765-4321' },
    { name: 'Maria Souza', position: 'Gerente de TI', email: 'maria.souza@health.com', phone: '(21) 99876-5432' },
    { name: 'Pedro Santos', position: 'Diretor de Vendas', email: 'pedro.santos@mmn.com', phone: '(31) 97654-3210' },
];

const MOCK_ADDRESSES: Address[] = [
    { zipCode: '01001-000', street: 'Rua Principal', number: '100', city: 'São Paulo', state: 'SP' },
    { zipCode: '20040-000', street: 'Av. Central', number: '50', city: 'Rio de Janeiro', state: 'RJ' },
    { zipCode: '30130-000', street: 'Rua da Paz', number: '200', city: 'Belo Horizonte', state: 'MG' },
];

export const MOCK_CLIENTS_DATA: Client[] = [
  {
    id: 'c1',
    companyName: 'Alpha Solutions',
    document: '12.345.678/0001-90',
    website: 'https://alphasolutions.com',
    segment: 'Tecnologia',
    status: 'Ativo',
    contact: MOCK_CONTACTS[0],
    address: MOCK_ADDRESSES[0],
    projectsCount: 2,
    lastInteraction: new Date(new Date().setDate(new Date().getDate() - 5)),
    tags: ['SaaS', 'Grande Porte'],
  },
  {
    id: 'c2',
    companyName: 'Health Clinic Pro',
    document: '98.765.432/0001-11',
    website: 'https://healthclinicpro.com',
    segment: 'Saúde',
    status: 'Prospecto',
    contact: MOCK_CONTACTS[1],
    address: MOCK_ADDRESSES[1],
    projectsCount: 1,
    lastInteraction: new Date(new Date().setDate(new Date().getDate() - 30)),
    tags: ['Clínica', 'B2B'],
  },
  {
    id: 'c3',
    companyName: 'MMN Global',
    document: '11.222.333/0001-44',
    website: 'https://mmnglobal.com',
    segment: 'MMN',
    status: 'Inativo',
    contact: MOCK_CONTACTS[2],
    address: MOCK_ADDRESSES[2],
    projectsCount: 1,
    lastInteraction: new Date(new Date().setDate(new Date().getDate() - 90)),
    tags: ['Vendas', 'Distribuição'],
  },
];

export const getMockClientsData = () => MOCK_CLIENTS_DATA;