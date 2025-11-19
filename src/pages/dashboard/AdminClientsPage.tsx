import React, { useState, useMemo } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Building, Users, CheckCircle, Plus, Filter, Download, List, LayoutGrid, Search, Mail, Phone, Briefcase, Clock, Edit, Archive, MoreHorizontal, Copy, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { MOCK_CLIENTS_DATA } from '@/data/mockClients';
import { Client } from '@/types/client';
import ClientCreationModal from '@/components/clients/ClientCreationModal';
import { toast } from 'sonner';
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group';
import { ClientStatusBadge, ClientSegmentBadge } from '@/components/clients/ClientBadges';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { cn } from '@/lib/utils';
import { format, formatDistanceToNow } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Link } from 'react-router-dom';

const AdminClientsPage: React.FC = () => {
  const [clients, setClients] = useState<Client[]>(MOCK_CLIENTS_DATA);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingClient, setEditingClient] = useState<Client | undefined>(undefined);
  const [viewMode, setViewMode] = useState<'table' | 'grid'>('table');
  const [searchTerm, setSearchTerm] = useState('');

  const filteredClients = useMemo(() => {
    if (!searchTerm) return clients;
    const lowerCaseSearch = searchTerm.toLowerCase();
    return clients.filter(client => 
        client.companyName.toLowerCase().includes(lowerCaseSearch) ||
        client.contact.name.toLowerCase().includes(lowerCaseSearch) ||
        client.segment.toLowerCase().includes(lowerCaseSearch)
    );
  }, [clients, searchTerm]);

  const metrics = useMemo(() => ({
    total: clients.length,
    active: clients.filter(c => c.status === 'Ativo').length,
    prospects: clients.filter(c => c.status === 'Prospecto').length,
  }), [clients]);

  const handleCreateClient = (newClientData: Omit<Client, 'id' | 'projectsCount' | 'lastInteraction'>) => {
    const newClient: Client = {
      ...newClientData,
      id: `c${Date.now()}`,
      projectsCount: 0,
      lastInteraction: new Date(),
    };
    setClients(prev => [newClient, ...prev]);
  };

  const handleEditClient = (client: Client) => {
    setEditingClient(client);
    setIsModalOpen(true);
  };

  const handleArchiveClient = (clientId: string) => {
    setClients(prev => prev.filter(c => c.id !== clientId));
    toast.warning(`Cliente arquivado (ID: ${clientId})`);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setEditingClient(undefined);
  };

  const handleCopy = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    toast.info(`${label} copiado!`);
  };

  const ClientTable: React.FC<{ clients: Client[] }> = ({ clients }) => (
    <div className="rounded-md border overflow-x-auto">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Empresa</TableHead>
            <TableHead>Contato Principal</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Segmento</TableHead>
            <TableHead>Projetos</TableHead>
            <TableHead>Última Interação</TableHead>
            <TableHead className="text-right">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {clients.length > 0 ? (
            clients.map((client) => (
              <TableRow key={client.id} className="hover:bg-accent/50 transition-colors">
                <TableCell className="font-medium">
                  <Link to={`/dashboard/admin/clients/${client.id}`} className="text-[#4e4ea8] dark:text-[#0ca7d2] hover:underline">
                    {client.companyName}
                  </Link>
                  <p className="text-xs text-muted-foreground mt-1">{client.document}</p>
                </TableCell>
                <TableCell>
                  <div className="text-sm font-medium">{client.contact.name}</div>
                  <p className="text-xs text-muted-foreground">{client.contact.position}</p>
                  <div className="flex items-center space-x-1 mt-1">
                    <Button variant="ghost" size="icon" className="h-6 w-6 p-0" onClick={() => handleCopy(client.contact.email, 'Email')}>
                        <Mail className="h-3 w-3 text-[#FF6B35]" />
                    </Button>
                    <Button variant="ghost" size="icon" className="h-6 w-6 p-0" onClick={() => handleCopy(client.contact.phone, 'Telefone')}>
                        <Phone className="h-3 w-3 text-[#0ca7d2]" />
                    </Button>
                  </div>
                </TableCell>
                <TableCell><ClientStatusBadge status={client.status} /></TableCell>
                <TableCell><ClientSegmentBadge segment={client.segment} /></TableCell>
                <TableCell>
                    <Link to={`/dashboard/admin/projects?client=${client.id}`} className="text-sm font-medium text-[#4e4ea8] dark:text-[#0ca7d2] hover:underline">
                        {client.projectsCount}
                    </Link>
                </TableCell>
                <TableCell className="text-sm text-muted-foreground">
                    <span title={format(client.lastInteraction, 'dd/MM/yyyy HH:mm', { locale: ptBR })}>
                        {formatDistanceToNow(client.lastInteraction, { addSuffix: true, locale: ptBR })}
                    </span>
                </TableCell>
                <TableCell className="text-right">
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" className="h-8 w-8 p-0">
                        <span className="sr-only">Abrir menu</span>
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuLabel>Ações</DropdownMenuLabel>
                      <DropdownMenuItem onClick={() => console.log('Ver detalhes', client.id)}>
                        <Building className="mr-2 h-4 w-4" /> Ver Detalhes
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => handleEditClient(client)}>
                        <Edit className="mr-2 h-4 w-4" /> Editar
                      </DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem onClick={() => handleArchiveClient(client.id)} className="text-red-500">
                        <Archive className="mr-2 h-4 w-4" /> Arquivar
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={7} className="h-24 text-center text-muted-foreground">
                Nenhum cliente encontrado.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );

  const ClientGrid: React.FC<{ clients: Client[] }> = ({ clients }) => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {clients.map(client => (
            <Card key={client.id} className="hover:shadow-lg transition-shadow">
                <CardHeader className="flex flex-row items-center justify-between">
                    <CardTitle className="text-lg flex items-center space-x-2">
                        <Building className="h-5 w-5 text-[#4e4ea8]" />
                        <Link to={`/dashboard/admin/clients/${client.id}`} className="hover:underline">{client.companyName}</Link>
                    </CardTitle>
                    <ClientStatusBadge status={client.status} />
                </CardHeader>
                <CardContent className="space-y-3">
                    <ClientSegmentBadge segment={client.segment} />
                    <div className="text-sm text-muted-foreground">
                        <p className="flex items-center"><User className="h-4 w-4 mr-2" /> {client.contact.name} ({client.contact.position})</p>
                        <p className="flex items-center"><Briefcase className="h-4 w-4 mr-2" /> {client.projectsCount} Projetos</p>
                        <p className="flex items-center"><Clock className="h-4 w-4 mr-2" /> Última Interação: {formatDistanceToNow(client.lastInteraction, { addSuffix: true, locale: ptBR })}</p>
                    </div>
                    <div className="flex justify-end space-x-2 pt-2 border-t">
                        <Button variant="outline" size="sm"><Mail className="h-4 w-4" /></Button>
                        <Button variant="outline" size="sm"><Phone className="h-4 w-4" /></Button>
                        <Button size="sm" onClick={() => handleEditClient(client)}>Editar</Button>
                    </div>
                </CardContent>
            </Card>
        ))}
        {clients.length === 0 && (
            <div className="col-span-full text-center py-12 border-2 border-dashed rounded-lg">
                <Users className="h-10 w-10 mx-auto text-muted-foreground mb-3" />
                <p className="text-lg text-muted-foreground">Nenhum cliente corresponde à sua busca.</p>
            </div>
        )}
    </div>
  );

  return (
    <DashboardLayout>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold flex items-center">
          <Users className="h-7 w-7 mr-3 text-[#0ca7d2]" />
          Clientes
        </h2>
        <div className="flex space-x-2">
          <Button onClick={() => handleEditClient(undefined)} className="bg-[#FF6B35] hover:bg-[#e55f30]">
            <Plus className="h-4 w-4 mr-2" /> Novo Cliente
          </Button>
        </div>
      </div>
      
      {/* Metrics Cards */}
      <div className="grid gap-4 md:grid-cols-3 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Clientes</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.total}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Clientes Ativos</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-500">{metrics.active}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Prospectos</CardTitle>
            <Clock className="h-4 w-4 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-500">{metrics.prospects}</div>
          </CardContent>
        </Card>
      </div>

      {/* Toolbar and View Toggle */}
      <div className="flex flex-col md:flex-row justify-between items-center mb-6 space-y-4 md:space-y-0">
        <div className="flex w-full md:w-auto space-x-2">
            <div className="relative w-full md:w-64">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input 
                    placeholder="Buscar cliente, email ou segmento..." 
                    className="pl-10" 
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>
            <Button variant="outline"><Filter className="h-4 w-4 mr-2" /> Filtros</Button>
            <Button variant="outline"><Download className="h-4 w-4 mr-2" /> Exportar</Button>
        </div>
        
        <ToggleGroup type="single" value={viewMode} onValueChange={(value: 'table' | 'grid') => value && setViewMode(value)} className="flex-shrink-0">
            <ToggleGroupItem value="table" aria-label="Visualização em Tabela">
                <List className="h-4 w-4" />
            </ToggleGroupItem>
            <ToggleGroupItem value="grid" aria-label="Visualização em Grid">
                <LayoutGrid className="h-4 w-4" />
            </ToggleGroupItem>
        </ToggleGroup>
      </div>

      {/* Main Content Area */}
      {viewMode === 'table' ? (
        <ClientTable clients={filteredClients} />
      ) : (
        <ClientGrid clients={filteredClients} />
      )}

      {/* Pagination (Mock) */}
      <div className="mt-6 flex justify-end text-sm text-muted-foreground">
        Mostrando 1 a {filteredClients.length} de {clients.length} clientes.
      </div>

      <ClientCreationModal 
        isOpen={isModalOpen} 
        onClose={handleModalClose} 
        onCreate={(clientData) => {
            if (editingClient) {
                // Handle update logic
                setClients(clients.map(c => c.id === editingClient.id ? { ...c, ...clientData } as Client : c));
            } else {
                handleCreateClient(clientData);
            }
        }}
        initialData={editingClient}
      />
    </DashboardLayout>
  );
};

export default AdminClientsPage;