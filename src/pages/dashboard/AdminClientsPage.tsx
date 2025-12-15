import React, { useState, useMemo, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Building, Users, CheckCircle, Plus, Filter, Download, List, LayoutGrid, Search, Mail, Phone, Briefcase, Clock, Edit, Archive, MoreHorizontal, User, Info, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Client, ClientList } from '@/types/client';
import { clientService } from '@/services/clientService';
import ClientCreationModal from '@/components/clients/ClientCreationModal';
import { toast } from 'sonner';
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { format, formatDistanceToNow } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Alert, AlertDescription } from '@/components/ui/alert';

const AdminClientsPage: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [clients, setClients] = useState<Client[]>([]);
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingClient, setEditingClient] = useState<Client | undefined>(undefined);
  const [viewMode, setViewMode] = useState<'table' | 'grid'>('table');
  const [searchTerm, setSearchTerm] = useState('');
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 10,
    total: 0,
    hasNext: false
  });

  // Carregar cliente específico por ID
  const loadClientById = async (clientId: string) => {
    try {
      setLoading(true);
      setError(null);
      const client = await clientService.getById(clientId);
      setSelectedClient(client);
    } catch (err) {
      setError('Erro ao carregar cliente');
      console.error('Erro ao carregar cliente:', err);
    } finally {
      setLoading(false);
    }
  };

  // Carregar cliente por ID se presente na URL
  useEffect(() => {
    if (id) {
      loadClientById(id);
    }
  }, [id]);

  // Carregar clientes do backend
  const loadClients = async (page = 1, search = '') => {
    try {
      setLoading(true);
      setError(null);
      const params = {
        page,
        limit: pagination.limit,
        ...(search && { search }),
        status: 'active' // Filtrar apenas clientes ativos (não prospectos)
      };
      
      const response: ClientList = await clientService.getAll(params);
      setClients(response.items);
      setPagination({
        page: response.page,
        limit: response.limit,
        total: response.total,
        hasNext: response.has_next
      });
    } catch (err) {
      setError('Erro ao carregar clientes. Tente novamente.');
      console.error('Erro ao carregar clientes:', err);
    } finally {
      setLoading(false);
    }
  };

  // Carregar dados na inicialização
  useEffect(() => {
    loadClients();
  }, []);

  // Recarregar quando busca mudar
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      loadClients(1, searchTerm);
    }, 300);
    
    return () => clearTimeout(timeoutId);
  }, [searchTerm]);

  const metrics = useMemo(() => ({
    total: pagination.total,
    active: clients.filter(c => c.status === 'active').length,
    inactive: clients.filter(c => c.status === 'inactive').length,
    suspended: clients.filter(c => c.status === 'suspended').length,
  }), [clients, pagination.total]);

  const handleCreateClient = async (newClientData: any) => {
    try {
      setLoading(true);
      await clientService.create(newClientData);
      toast.success('Cliente criado com sucesso!');
      loadClients(); // Recarregar lista
      setIsModalOpen(false);
    } catch (err) {
      toast.error('Erro ao criar cliente. Tente novamente.');
      console.error('Erro ao criar cliente:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleViewClient = (client: Client) => {
    navigate(`/dashboard/admin/clients/${client.id}`);
  };

  const handleEditClient = (client: Client) => {
    setEditingClient(client);
    setIsModalOpen(true);
  };

  const handleArchiveClient = async (clientId: string) => {
    try {
      await clientService.delete(clientId);
      toast.success('Cliente arquivado com sucesso!');
      loadClients(); // Recarregar lista
    } catch (err) {
      toast.error('Erro ao arquivar cliente. Tente novamente.');
      console.error('Erro ao arquivar cliente:', err);
    }
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
                  <button 
                    onClick={() => handleViewClient(client)}
                    className="text-[#4e4ea8] dark:text-[#0ca7d2] hover:underline text-left"
                  >
                    {client.company_name}
                  </button>
                  <p className="text-xs text-muted-foreground mt-1">{client.document}</p>
                </TableCell>
                <TableCell>
                  <div className="text-sm font-medium">{client.contact?.email || 'N/A'}</div>
                  <p className="text-xs text-muted-foreground">Contato Principal</p>
                  <div className="flex items-center space-x-1 mt-1">
                    {client.contact?.email && (
                      <Button variant="ghost" size="icon" className="h-6 w-6 p-0" onClick={() => handleCopy(client.contact.email!, 'Email')}>
                          <Mail className="h-3 w-3 text-[#FF6B35]" />
                      </Button>
                    )}
                    {client.contact?.phone && (
                      <Button variant="ghost" size="icon" className="h-6 w-6 p-0" onClick={() => handleCopy(client.contact.phone!, 'Telefone')}>
                          <Phone className="h-3 w-3 text-[#0ca7d2]" />
                      </Button>
                    )}
                  </div>
                </TableCell>
                <TableCell>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    client.status === 'active' ? 'bg-green-100 text-green-800' :
                    client.status === 'inactive' ? 'bg-gray-100 text-gray-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {client.status === 'active' ? 'Ativo' : 
                     client.status === 'inactive' ? 'Inativo' : 'Suspenso'}
                  </span>
                </TableCell>
                <TableCell>{client.segment || 'N/A'}</TableCell>
                <TableCell>
                    <Link to={`/dashboard/admin/projects?client=${client.id}`} className="text-sm font-medium text-[#4e4ea8] dark:text-[#0ca7d2] hover:underline">
                        0
                    </Link>
                </TableCell>
                <TableCell className="text-sm text-muted-foreground">
                    {client.last_interaction ? (
                      <span title={format(new Date(client.last_interaction), 'dd/MM/yyyy HH:mm', { locale: ptBR })}>
                          {formatDistanceToNow(new Date(client.last_interaction), { addSuffix: true, locale: ptBR })}
                      </span>
                    ) : 'N/A'}
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
                      <DropdownMenuItem onClick={() => handleViewClient(client)}>
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
                        <button 
                          onClick={() => handleViewClient(client)}
                          className="hover:underline text-left"
                        >
                          {client.company_name}
                        </button>
                    </CardTitle>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      client.status === 'active' ? 'bg-green-100 text-green-800' :
                      client.status === 'inactive' ? 'bg-gray-100 text-gray-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {client.status === 'active' ? 'Ativo' : 
                       client.status === 'inactive' ? 'Inativo' : 'Suspenso'}
                    </span>
                </CardHeader>
                <CardContent className="space-y-3">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {client.segment || 'N/A'}
                    </span>
                    <div className="text-sm text-muted-foreground">
                        <p className="flex items-center"><User className="h-4 w-4 mr-2" /> {client.contact?.email || 'N/A'}</p>
                        <p className="flex items-center"><Briefcase className="h-4 w-4 mr-2" /> 0 Projetos</p>
                        <p className="flex items-center"><Clock className="h-4 w-4 mr-2" /> 
                          Última Interação: {client.last_interaction ? 
                            formatDistanceToNow(new Date(client.last_interaction), { addSuffix: true, locale: ptBR }) : 
                            'N/A'}
                        </p>
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

  // Se há um ID na URL, mostrar detalhes do cliente
  if (id && selectedClient) {
    return (
      <DashboardLayout>
        <div className="flex items-center mb-6">
          <Button variant="ghost" onClick={() => navigate('/dashboard/admin/clients')} className="mr-4">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Voltar
          </Button>
          <h2 className="text-3xl font-bold flex items-center">
            <Building className="h-7 w-7 mr-3 text-[#0ca7d2]" />
            {selectedClient.company_name}
          </h2>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Informações Gerais</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium text-muted-foreground">Empresa</label>
                <p className="text-lg font-semibold">{selectedClient.company_name}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Documento</label>
                <p>{selectedClient.document || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Segmento</label>
                <p>{selectedClient.segment}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Status</label>
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  selectedClient.status === 'active' ? 'bg-green-100 text-green-800' :
                  selectedClient.status === 'inactive' ? 'bg-gray-100 text-gray-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {selectedClient.status === 'active' ? 'Ativo' : 
                   selectedClient.status === 'inactive' ? 'Inativo' : 'Suspenso'}
                </span>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Website</label>
                <p>{selectedClient.website || 'N/A'}</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Contato</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium text-muted-foreground">Email</label>
                <p>{selectedClient.contact?.email || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Telefone</label>
                <p>{selectedClient.contact?.phone || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">WhatsApp</label>
                <p>{selectedClient.contact?.whatsapp || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Criado em</label>
                <p>{selectedClient.created_at ? format(new Date(selectedClient.created_at), 'dd/MM/yyyy HH:mm', { locale: ptBR }) : 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Última Interação</label>
                <p>{selectedClient.last_interaction ? formatDistanceToNow(new Date(selectedClient.last_interaction), { addSuffix: true, locale: ptBR }) : 'N/A'}</p>
              </div>
            </CardContent>
          </Card>

          {selectedClient.address && (
            <Card className="md:col-span-2">
              <CardHeader>
                <CardTitle>Endereço</CardTitle>
              </CardHeader>
              <CardContent className="grid gap-4 md:grid-cols-3">
                <div>
                  <label className="text-sm font-medium text-muted-foreground">Rua</label>
                  <p>{selectedClient.address.street || 'N/A'}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">Número</label>
                  <p>{selectedClient.address.number || 'N/A'}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">Bairro</label>
                  <p>{selectedClient.address.neighborhood || 'N/A'}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">Cidade</label>
                  <p>{selectedClient.address.city || 'N/A'}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">Estado</label>
                  <p>{selectedClient.address.state || 'N/A'}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">CEP</label>
                  <p>{selectedClient.address.zipcode || 'N/A'}</p>
                </div>
              </CardContent>
            </Card>
          )}

          {selectedClient.notes && (
            <Card className="md:col-span-2">
              <CardHeader>
                <CardTitle>Observações</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="whitespace-pre-wrap">{selectedClient.notes}</p>
              </CardContent>
            </Card>
          )}
        </div>

        <div className="mt-6 flex space-x-2">
          <Button onClick={() => handleEditClient(selectedClient)}>
            <Edit className="h-4 w-4 mr-2" />
            Editar Cliente
          </Button>
          <Button variant="outline" onClick={() => handleArchiveClient(selectedClient.id)} className="text-red-500">
            <Archive className="h-4 w-4 mr-2" />
            Arquivar Cliente
          </Button>
        </div>
      </DashboardLayout>
    );
  }

  // Se há um ID mas está carregando
  if (id && loading) {
    return (
      <DashboardLayout>
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#0ca7d2]"></div>
          <span className="ml-2 text-muted-foreground">Carregando cliente...</span>
        </div>
      </DashboardLayout>
    );
  }

  // Se há um ID mas deu erro
  if (id && error) {
    return (
      <DashboardLayout>
        <Alert className="mb-4">
          <Info className="h-4 w-4" />
          <AlertDescription>
            {error}
            <Button variant="link" onClick={() => loadClientById(id)} className="ml-2 p-0 h-auto">
              Tentar novamente
            </Button>
          </AlertDescription>
        </Alert>
        <Button variant="ghost" onClick={() => navigate('/dashboard/admin/clients')}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          Voltar para lista
        </Button>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <Alert className="mb-4">
        <Info className="h-4 w-4" />
        <AlertDescription>
          Esta página exibe apenas <strong>Clientes</strong> (quem contratou ou está em negociação). 
          Contatos que ainda não contrataram estão em <Link to="/dashboard/admin/leads" className="text-[#0ca7d2] hover:underline">Leads</Link>.
        </AlertDescription>
      </Alert>
      
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
            <CardTitle className="text-sm font-medium">Clientes Inativos</CardTitle>
            <Clock className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-500">{metrics.inactive}</div>
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

      {/* Loading State */}
      {loading && (
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#0ca7d2]"></div>
          <span className="ml-2 text-muted-foreground">Carregando clientes...</span>
        </div>
      )}

      {/* Error State */}
      {error && (
        <Alert className="mb-4">
          <Info className="h-4 w-4" />
          <AlertDescription>
            {error}
            <Button variant="link" onClick={() => loadClients()} className="ml-2 p-0 h-auto">
              Tentar novamente
            </Button>
          </AlertDescription>
        </Alert>
      )}

      {/* Main Content Area */}
      {!loading && !error && (
        viewMode === 'table' ? (
          <ClientTable clients={clients} />
        ) : (
          <ClientGrid clients={clients} />
        )
      )}

      {/* Pagination */}
      {!loading && !error && (
        <div className="mt-6 flex justify-between items-center text-sm text-muted-foreground">
          <span>
            Mostrando {clients.length > 0 ? ((pagination.page - 1) * pagination.limit + 1) : 0} a {Math.min(pagination.page * pagination.limit, pagination.total)} de {pagination.total} clientes.
          </span>
          <div className="flex space-x-2">
            <Button 
              variant="outline" 
              size="sm" 
              disabled={pagination.page === 1}
              onClick={() => loadClients(pagination.page - 1, searchTerm)}
            >
              Anterior
            </Button>
            <Button 
              variant="outline" 
              size="sm" 
              disabled={!pagination.hasNext}
              onClick={() => loadClients(pagination.page + 1, searchTerm)}
            >
              Próximo
            </Button>
          </div>
        </div>
      )}

      <ClientCreationModal 
        isOpen={isModalOpen} 
        onClose={handleModalClose} 
        onCreate={async (clientData) => {
            if (editingClient) {
                // Handle update logic
                try {
                  await clientService.update(editingClient.id, clientData);
                  toast.success('Cliente atualizado com sucesso!');
                  loadClients();
                  setIsModalOpen(false);
                } catch (err) {
                  toast.error('Erro ao atualizar cliente. Tente novamente.');
                  console.error('Erro ao atualizar cliente:', err);
                }
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