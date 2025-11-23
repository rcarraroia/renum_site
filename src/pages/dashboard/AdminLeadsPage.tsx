import React, { useState } from 'react';
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
  Filter, 
  UserPlus,
  ArrowRight,
  Eye,
  Trash2,
  Star,
  MessageSquare,
  Globe,
  Target,
  Users
} from 'lucide-react';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';

interface Lead {
  id: string;
  name: string;
  phone: string;
  email?: string;
  source: 'pesquisa' | 'home' | 'campanha' | 'indicacao';
  status: 'novo' | 'qualificado' | 'em_negociacao' | 'perdido';
  subagentName?: string;
  interviewId?: string;
  firstContactAt: string;
  lastInteractionAt: string;
  notes?: string;
  score?: number;
}

const MOCK_LEADS: Lead[] = [
    {
      id: '1',
      name: 'João Silva',
      phone: '+55 11 99999-8888',
      email: 'joao@email.com',
      source: 'pesquisa',
      status: 'qualificado',
      subagentName: 'Pesquisa MMN',
      interviewId: 'int-1',
      firstContactAt: '2025-01-18T10:30:00',
      lastInteractionAt: '2025-01-18T10:45:00',
      score: 85,
      notes: 'Muito interessado em automação. Tem 200 distribuidores.'
    },
    {
      id: '2',
      name: 'Maria Santos',
      phone: '+55 11 98888-7777',
      source: 'home',
      status: 'novo',
      firstContactAt: '2025-01-19T14:20:00',
      lastInteractionAt: '2025-01-19T14:25:00',
      score: 45
    },
    {
      id: '3',
      name: 'Pedro Costa',
      phone: '+55 21 97777-6666',
      email: 'pedro@vereador.com',
      source: 'pesquisa',
      status: 'em_negociacao',
      subagentName: 'Pesquisa Vereadores',
      interviewId: 'int-2',
      firstContactAt: '2025-01-17T16:00:00',
      lastInteractionAt: '2025-01-20T09:30:00',
      score: 92,
      notes: 'Pediu orçamento. Aguardando aprovação do gabinete.'
    },
    {
      id: '4',
      name: 'Ana Oliveira',
      phone: '+55 11 96666-5555',
      source: 'campanha',
      status: 'perdido',
      firstContactAt: '2025-01-15T11:00:00',
      lastInteractionAt: '2025-01-16T15:20:00',
      score: 30,
      notes: 'Não respondeu após 3 tentativas de contato.'
    }
];

const AdminLeadsPage = () => {
  const [leads, setLeads] = useState<Lead[]>(MOCK_LEADS);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterSource, setFilterSource] = useState<string>('all');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const getSourceBadge = (source: Lead['source']) => {
    const variants = {
      pesquisa: { label: 'Pesquisa', icon: Target, class: 'bg-blue-500 hover:bg-blue-500/80' },
      home: { label: 'Home/Site', icon: Globe, class: 'bg-purple-500 hover:bg-purple-500/80' },
      campanha: { label: 'Campanha', icon: MessageSquare, class: 'bg-orange-500 hover:bg-orange-500/80' },
      indicacao: { label: 'Indicação', icon: Users, class: 'bg-green-500 hover:bg-green-500/80' }
    };
    const variant = variants[source];
    const Icon = variant.icon;
    return (
      <Badge className={cn("text-white", variant.class)}>
        <Icon className="h-3 w-3 mr-1" />
        {variant.label}
      </Badge>
    );
  };

  const getStatusBadge = (status: Lead['status']) => {
    const variants = {
      novo: { label: 'Novo', class: 'bg-yellow-500 hover:bg-yellow-500/80 text-gray-900' },
      qualificado: { label: 'Qualificado', class: 'bg-[#0ca7d2] hover:bg-[#0ca7d2]/80 text-white' },
      em_negociacao: { label: 'Em Negociação', class: 'bg-green-600 hover:bg-green-600/80 text-white' },
      perdido: { label: 'Perdido', class: 'bg-red-600 hover:bg-red-600/80 text-white' }
    };
    const variant = variants[status];
    return <Badge className={cn("capitalize", variant.class)}>{variant.label}</Badge>;
  };

  const handleConvertToClient = (lead: Lead) => {
    setLeads(prev => prev.filter(l => l.id !== lead.id));
    toast.success(`${lead.name} convertido! Movido para Clientes (Prospectos).`);
    // Em um app real, aqui você chamaria a API para criar um novo cliente/prospecto
  };

  const handleViewDetails = (lead: Lead) => {
    setSelectedLead(lead);
    setIsDialogOpen(true);
  };

  const filteredLeads = leads.filter(lead => {
    const matchSearch = lead.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                        lead.phone.includes(searchTerm);
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
  const totalConverted = MOCK_LEADS.length - totalLeads; // Mock conversion count

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

        {/* Stats Cards */}
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
              <CardTitle className="text-sm font-medium">Leads Convertidos (Mock)</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-[#FF6B35]">
                {totalConverted}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Tabs por Origem */}
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
                            <Star className={cn(`h-4 w-4`, lead.score! >= 70 ? 'text-yellow-500 fill-yellow-500' : 'text-gray-300')} />
                            <span className="font-medium">{lead.score}</span>
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
                            {new Date(lead.firstContactAt).toLocaleDateString('pt-BR')}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="text-sm">
                            {new Date(lead.lastInteractionAt).toLocaleDateString('pt-BR')}
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
                      <Star className={cn(`h-4 w-4`, selectedLead.score! >= 70 ? 'text-yellow-500 fill-yellow-500' : 'text-gray-300')} />
                      <span className="font-medium">{selectedLead.score}/100</span>
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

                {selectedLead.subagentName && (
                  <div className="p-3 bg-blue-50 dark:bg-blue-950 rounded-lg border border-blue-200 dark:border-blue-800">
                    <div className="text-sm font-medium text-blue-700 dark:text-blue-300">
                      Participou de: {selectedLead.subagentName}
                    </div>
                    {selectedLead.interviewId && (
                      <Button
                        variant="link"
                        size="sm"
                        className="p-0 h-auto text-xs text-blue-600"
                      >
                        Ver entrevista completa →
                      </Button>
                    )}
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