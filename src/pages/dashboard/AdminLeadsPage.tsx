import { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from '@/components/ui/select';
import { 
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import { 
  Search, 
  UserPlus,
  ArrowRight,
  Eye,
  Star,
  MessageSquare,
  Globe,
  Target,
  Users,
  Loader2
} from 'lucide-react';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { leadService } from '@/services/leadService';
import { Lead as LeadType } from '@/types/lead';

// Usando tipos do backend
type Lead = LeadType;

const AdminLeadsPage = () => {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterSource, setFilterSource] = useState<string>('all');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  // Carregar leads do backend
  const loadLeads = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await leadService.getAll({ limit: 100 });
      setLeads(response.items);
    } catch (err) {
      setError('Erro ao carregar leads. Tente novamente.');
      console.error('Erro ao carregar leads:', err);
    } finally {
      setLoading(false);
    }
  };

  // Carregar dados na inicialização
  useEffect(() => {
    loadLeads();
  }, []);

  const getSourceBadge = (source?: string) => {
    if (!source) return <Badge className="bg-gray-500">N/A</Badge>;
    
    const variants: Record<string, { label: string; icon: any; class: string }> = {
      pesquisa: { label: 'Pesquisa', icon: Target, class: 'bg-blue-500 hover:bg-blue-500/80' },
      home: { label: 'Home/Site', icon: Globe, class: 'bg-purple-500 hover:bg-purple-500/80' },
      campanha: { label: 'Campanha', icon: MessageSquare, class: 'bg-orange-500 hover:bg-orange-500/80' },
      indicacao: { label: 'Indicação', icon: Users, class: 'bg-green-500 hover:bg-green-500/80' }
    };
    
    const variant = variants[source] || { label: source, icon: Target, class: 'bg-gray-500' };
    const Icon = variant.icon;
    return (
      <Badge className={cn("text-white", variant.class)}>
        <Icon className="h-3 w-3 mr-1" />
        {variant.label}
      </Badge>
    );
  };

  const getStatusBadge = (status: string) => {
    const variants: Record<string, { label: string; class: string }> = {
      novo: { label: 'Novo', class: 'bg-yellow-500 hover:bg-yellow-500/80 text-gray-900' },
      qualificado: { label: 'Qualificado', class: 'bg-[#0ca7d2] hover:bg-[#0ca7d2]/80 text-white' },
      em_negociacao: { label: 'Em Negociação', class: 'bg-green-600 hover:bg-green-600/80 text-white' },
      perdido: { label: 'Perdido', class: 'bg-red-600 hover:bg-red-600/80 text-white' }
    };
    const variant = variants[status] || { label: status, class: 'bg-gray-500' };
    return <Badge className={cn("capitalize", variant.class)}>{variant.label}</Badge>;
  };

  const handleConvertToClient = async (lead: Lead) => {
    try {
      await leadService.convertToClient(lead.id, {
        company_name: lead.name,
        cnpj: '00.000.000/0001-00',
        segment: 'Geral',
        plan: 'basic' as const
      });
      
      toast.success(`${lead.name} convertido para cliente com sucesso!`);
      loadLeads();
    } catch (err) {
      toast.error('Erro ao converter lead. Tente novamente.');
      console.error('Erro ao converter lead:', err);
    }
  };

  const handleViewDetails = (lead: Lead) => {
    setSelectedLead(lead);
    setIsDialogOpen(true);
  };

  const filteredLeads = leads.filter(lead => {
    const matchSearch = lead.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                        lead.phone.includes(searchTerm) ||
                        (lead.email && lead.email.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchSource = filterSource === 'all' || lead.source === filterSource;
    const matchStatus = filterStatus === 'all' || lead.status === filterStatus;
    return matchSearch && matchSource && matchStatus;
  });

  const leadsBySource = {
    pesquisa: leads.filter(l => l.source === 'pesquisa').length,
    home: leads.filter(l => l.source === 'home').length,
    campanha: leads.filter(l => l.source === 'campanha').length,
    indicacao: leads.filter(l => l.source === 'indicacao').length
  };

  const leadsByStatus = {
    novo: leads.filter(l => l.status === 'novo').length,
    qualificado: leads.filter(l => l.status === 'qualificado').length,
    em_negociacao: leads.filter(l => l.status === 'em_negociacao').length,
    perdido: leads.filter(l => l.status === 'perdido').length
  };

  const totalLeads = leads.length;
  const totalConverted = 0;

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-[#4e4ea8] flex items-center gap-2">
              <UserPlus className="h-8 w-8" />
              Leads
            </h1>
            <p className="text-muted-foreground mt-1">
              Gerencie todos os contatos que interagiram mas ainda não contrataram
            </p>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center items-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-[#0ca7d2]" />
            <span className="ml-2 text-muted-foreground">Carregando leads...</span>
          </div>
        )}

        {/* Error State */}
        {error && (
          <Card className="p-6">
            <div className="text-center">
              <p className="text-red-500 mb-4">{error}</p>
              <Button onClick={loadLeads} variant="outline">
                Tentar Novamente
              </Button>
            </div>
          </Card>
        )}

        {/* Stats Cards */}
        {!loading && !error && (
          <div className="grid gap-4 md:grid-cols-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Total de Leads</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{totalLeads}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Qualificados</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-[#0ca7d2]">{leadsByStatus.qualificado}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Em Negociação</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-600">{leadsByStatus.em_negociacao}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Convertidos</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-[#FF6B35]">{totalConverted}</div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Tabs por Origem */}
        {!loading && !error && (
          <Tabs defaultValue="all" onValueChange={setFilterSource} className="w-full">
            <TabsList className="grid w-full grid-cols-5 h-auto p-1 bg-gray-100 dark:bg-gray-800">
              <TabsTrigger value="all" className="flex items-center">
                Todas ({totalLeads})
              </TabsTrigger>
              <TabsTrigger value="pesquisa" className="flex items-center">
                <Target className="h-4 w-4 mr-1" />
                Pesquisas ({leadsBySource.pesquisa})
              </TabsTrigger>
              <TabsTrigger value="home" className="flex items-center">
                <Globe className="h-4 w-4 mr-1" />
                Home/Site ({leadsBySource.home})
              </TabsTrigger>
              <TabsTrigger value="campanha" className="flex items-center">
                <MessageSquare className="h-4 w-4 mr-1" />
                Campanhas ({leadsBySource.campanha})
              </TabsTrigger>
              <TabsTrigger value="indicacao" className="flex items-center">
                <Users className="h-4 w-4 mr-1" />
                Indicações ({leadsBySource.indicacao})
              </TabsTrigger>
            </TabsList>

            <TabsContent value={filterSource} className="space-y-4 mt-6">
              {/* Filters */}
              <Card>
                <CardHeader>
                  <CardTitle>Filtros</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="relative">
                      <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                      <Input
                        placeholder="Buscar por nome ou telefone..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="pl-8"
                      />
                    </div>
                    <Select value={filterStatus} onValueChange={setFilterStatus}>
                      <SelectTrigger>
                        <SelectValue placeholder="Todos os status" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">Todos os status</SelectItem>
                        <SelectItem value="novo">Novo</SelectItem>
                        <SelectItem value="qualificado">Qualificado</SelectItem>
                        <SelectItem value="em_negociacao">Em Negociação</SelectItem>
                        <SelectItem value="perdido">Perdido</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </CardContent>
              </Card>

              {/* Table */}
              <Card>
                <CardHeader>
                  <CardTitle>Lista de Leads</CardTitle>
                  <CardDescription>
                    Mostrando {filteredLeads.length} de {totalLeads} leads
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Score</TableHead>
                        <TableHead>Nome</TableHead>
                        <TableHead>Origem</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Primeiro Contato</TableHead>
                        <TableHead>Última Interação</TableHead>
                        <TableHead className="text-right">Ações</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {filteredLeads.map((lead) => (
                        <TableRow key={lead.id}>
                          <TableCell>
                            <div className="flex items-center gap-1">
                              <Star className={cn(`h-4 w-4`, (lead.score || 0) >= 70 ? 'text-yellow-500 fill-yellow-500' : 'text-gray-300')} />
                              <span className="font-medium">{lead.score || 0}</span>
                            </div>
                          </TableCell>
                          <TableCell>
                            <div>
                              <div className="font-medium">{lead.name}</div>
                              <div className="text-sm text-muted-foreground">{lead.phone}</div>
                            </div>
                          </TableCell>
                          <TableCell>{getSourceBadge(lead.source)}</TableCell>
                          <TableCell>{getStatusBadge(lead.status)}</TableCell>
                          <TableCell>
                            <div className="text-sm">
                              {lead.created_at ? new Date(lead.created_at).toLocaleDateString('pt-BR') : 'N/A'}
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="text-sm">
                              {lead.updated_at ? new Date(lead.updated_at).toLocaleDateString('pt-BR') : 'N/A'}
                            </div>
                          </TableCell>
                          <TableCell className="text-right">
                            <div className="flex gap-1 justify-end">
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleViewDetails(lead)}
                              >
                                <Eye className="h-4 w-4" />
                              </Button>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleConvertToClient(lead)}
                                className="text-green-600 hover:text-green-700"
                              >
                                <ArrowRight className="h-4 w-4" />
                              </Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        )}

        {/* Dialog - Detalhes do Lead */}
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogContent className="sm:max-w-[600px]">
            <DialogHeader>
              <DialogTitle className="flex items-center gap-2">
                <UserPlus className="h-5 w-5 text-[#4e4ea8]" />
                Detalhes do Lead
              </DialogTitle>
            </DialogHeader>
            
            {selectedLead && (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="text-sm text-muted-foreground">Nome</div>
                    <div className="font-medium">{selectedLead.name}</div>
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">Telefone</div>
                    <div className="font-medium">{selectedLead.phone}</div>
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">E-mail</div>
                    <div className="font-medium">{selectedLead.email || 'Não informado'}</div>
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">Score</div>
                    <div className="flex items-center gap-1">
                      <Star className={cn(`h-4 w-4`, (selectedLead.score || 0) >= 70 ? 'text-yellow-500 fill-yellow-500' : 'text-gray-300')} />
                      <span className="font-medium">{selectedLead.score || 0}/100</span>
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">Origem</div>
                    <div>{getSourceBadge(selectedLead.source)}</div>
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">Status</div>
                    <div>{getStatusBadge(selectedLead.status)}</div>
                  </div>
                </div>

                {selectedLead.notes && (
                  <div>
                    <div className="text-sm text-muted-foreground mb-1">Observações</div>
                    <div className="p-3 bg-gray-50 dark:bg-gray-900 rounded-lg text-sm">
                      {selectedLead.notes}
                    </div>
                  </div>
                )}

                {selectedLead.subagent_id && (
                  <div className="p-3 bg-blue-50 dark:bg-blue-950 rounded-lg border border-blue-200 dark:border-blue-800">
                    <div className="text-sm font-medium text-blue-700 dark:text-blue-300">
                      Sub-agente ID: {selectedLead.subagent_id}
                    </div>
                  </div>
                )}
              </div>
            )}

            <DialogFooter>
              <Button variant="outline" onClick={() => setIsDialogOpen(false)}>
                Fechar
              </Button>
              <Button
                onClick={() => {
                  if (selectedLead) handleConvertToClient(selectedLead);
                  setIsDialogOpen(false);
                }}
                className="bg-[#4e4ea8] hover:bg-[#3a3a80]"
              >
                <ArrowRight className="h-4 w-4 mr-2" />
                Converter em Cliente
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </DashboardLayout>
  );
};

export default AdminLeadsPage;