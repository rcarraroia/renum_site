import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { interviewService, Interview, InterviewList } from '@/services/interviewService';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '@/components/ui/select';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Search,
  Filter,
  Eye,
  Download,
  MessageSquare,
  Clock,
  CheckCircle,
  XCircle,
  User,
  ClipboardList
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface Entrevista {
  id: string;
  contactName: string;
  contactPhone: string;
  subagentName: string;
  status: 'pending' | 'in_progress' | 'completed' | 'abandoned';
  startedAt: string;
  completedAt?: string;
  messagesCount: number;
  topicsCovered: string[];
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

const PesquisasEntrevistasPage = () => {
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadInterviews();
  }, []);

  const loadInterviews = async () => {
    try {
      setLoading(true);
      const data = await interviewService.getInterviews();
      setInterviews(data.items);
    } catch (err) {
      setError('Erro ao carregar entrevistas');
      console.error('Erro:', err);
    } finally {
      setLoading(false);
    }
  };
  const [selectedEntrevista, setSelectedEntrevista] = useState<Interview | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [filterSubagent, setFilterSubagent] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');

  const filteredEntrevistas = interviews.filter(e => {
    const matchStatus = filterStatus === 'all' || e.status === filterStatus;
    const contactName = (e as any).lead?.name || 'Cliente';
    const matchSearch = contactName.toLowerCase().includes(searchTerm.toLowerCase());
    return matchStatus && matchSearch;
  });

  const handleViewConversation = (entrevista: Interview) => {
    setSelectedEntrevista(entrevista);
    setIsDialogOpen(true);
  };

  const getStatusBadge = (status: Interview['status']) => {
    const variants = {
      pending: { label: 'Pendente', class: 'bg-yellow-500 hover:bg-yellow-500/80 text-white' },
      in_progress: { label: 'Em Andamento', class: 'bg-[#4e4ea8] hover:bg-[#4e4ea8]/80 text-white' },
      completed: { label: 'Concluída', class: 'bg-green-600 hover:bg-green-600/80 text-white' },
      cancelled: { label: 'Cancelada', class: 'bg-red-600 hover:bg-red-600/80 text-white' },
      abandoned: { label: 'Abandonada', class: 'bg-red-600 hover:bg-red-600/80 text-white' }
    };
    const variant = (variants as any)[status] || variants.pending;
    return <Badge className={cn("capitalize", variant.class)}>{variant.label}</Badge>;
  };

  const getStatusIcon = (status: Interview['status']) => {
    const icons = {
      pending: <Clock className="h-4 w-4 text-yellow-600" />,
      in_progress: <MessageSquare className="h-4 w-4 text-[#4e4ea8]" />,
      completed: <CheckCircle className="h-4 w-4 text-green-600" />,
      cancelled: <XCircle className="h-4 w-4 text-red-600" />,
      abandoned: <XCircle className="h-4 w-4 text-red-600" />
    };
    return (icons as any)[status] || <Clock className="h-4 w-4 text-yellow-600" />;
  };

  const stats = {
    total: interviews.length,
    completed: interviews.filter(e => e.status === 'completed').length,
    inProgress: interviews.filter(e => e.status === 'in_progress').length,
    abandoned: interviews.filter(e => e.status === 'cancelled' || e.status === 'abandoned' as any).length
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center">
          <ClipboardList className="h-7 w-7 mr-3 text-[#4e4ea8]" />
          <h1 className="text-3xl font-bold text-[#4e4ea8]">Entrevistas Ativas</h1>
        </div>
        <p className="text-muted-foreground mt-1">
          Acompanhe em tempo real todas as entrevistas realizadas pelos sub-agentes
        </p>

        {/* Stats Cards */}
        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Total</CardTitle>
              <MessageSquare className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.total}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Concluídas</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{stats.completed}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Em Andamento</CardTitle>
              <Clock className="h-4 w-4 text-[#4e4ea8]" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-[#4e4ea8]">{stats.inProgress}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Abandonadas</CardTitle>
              <XCircle className="h-4 w-4 text-red-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">{stats.abandoned}</div>
            </CardContent>
          </Card>
        </div>

        {/* Filters */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Filtros</CardTitle>
              <Button variant="outline" size="sm">
                <Download className="h-4 w-4 mr-2" />
                Exportar CSV
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-3">
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
                  <SelectItem value="pending">Pendente</SelectItem>
                  <SelectItem value="in_progress">Em Andamento</SelectItem>
                  <SelectItem value="completed">Concluída</SelectItem>
                  <SelectItem value="abandoned">Abandonada</SelectItem>
                </SelectContent>
              </Select>
              <Select value={filterSubagent} onValueChange={setFilterSubagent}>
                <SelectTrigger>
                  <SelectValue placeholder="Todos os sub-agentes" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todos os sub-agentes</SelectItem>
                  <SelectItem value="Pesquisa MMN">Pesquisa MMN</SelectItem>
                  <SelectItem value="Pesquisa Vereadores">Pesquisa Vereadores</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Table */}
        <Card>
          <CardHeader>
            <CardTitle>Lista de Entrevistas</CardTitle>
            <CardDescription>
              Mostrando {filteredEntrevistas.length} de {entrevistas.length} entrevistas
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Status</TableHead>
                  <TableHead>Contato</TableHead>
                  <TableHead>Sub-Agente</TableHead>
                  <TableHead>Início</TableHead>
                  <TableHead>Mensagens</TableHead>
                  <TableHead>Tópicos</TableHead>
                  <TableHead className="text-right">Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredEntrevistas.map((entrevista) => (
                  <TableRow key={entrevista.id}>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        {getStatusIcon(entrevista.status)}
                        {getStatusBadge(entrevista.status)}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div>
                        <div className="font-medium">{entrevista.contactName}</div>
                        <div className="text-sm text-muted-foreground">{entrevista.contactPhone}</div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">{entrevista.subagentName}</Badge>
                    </TableCell>
                    <TableCell>
                      <div className="text-sm">
                        {new Date(entrevista.startedAt).toLocaleString('pt-BR')}
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="secondary">{entrevista.messagesCount} msgs</Badge>
                    </TableCell>
                    <TableCell>
                      <div className="text-sm text-muted-foreground">
                        {entrevista.topicsCovered.length > 0
                          ? `${entrevista.topicsCovered.length} tópicos`
                          : 'Nenhum'
                        }
                      </div>
                    </TableCell>
                    <TableCell className="text-right">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleViewConversation(entrevista)}
                      >
                        <Eye className="h-4 w-4 mr-1" />
                        Ver
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        {/* Dialog - Ver Conversa */}
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogContent className="sm:max-w-[700px] max-h-[80vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle className="flex items-center gap-2">
                <User className="h-5 w-5 text-[#4e4ea8]" />
                Conversa com {selectedEntrevista?.contactName}
              </DialogTitle>
            </DialogHeader>

            {selectedEntrevista && (
              <div className="space-y-4">
                {/* Info Header */}
                <div className="grid grid-cols-2 gap-4 p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
                  <div>
                    <div className="text-sm text-muted-foreground">Sub-Agente</div>
                    <div className="font-medium">{selectedEntrevista.subagentName}</div>
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">Status</div>
                    <div>{getStatusBadge(selectedEntrevista.status)}</div>
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">Telefone</div>
                    <div className="font-medium">{selectedEntrevista.contactPhone}</div>
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">Duração</div>
                    <div className="font-medium">
                      {selectedEntrevista.completedAt
                        ? `${Math.floor((new Date(selectedEntrevista.completedAt).getTime() - new Date(selectedEntrevista.startedAt).getTime()) / 60000)} min`
                        : 'Em andamento'
                      }
                    </div>
                  </div>
                </div>

                {/* Tópicos Cobertos */}
                {selectedEntrevista.topicsCovered.length > 0 && (
                  <div>
                    <div className="text-sm font-medium mb-2">Tópicos Cobertos:</div>
                    <div className="flex flex-wrap gap-2">
                      {selectedEntrevista.topicsCovered.map((topic, i) => (
                        <Badge key={i} variant="secondary">{topic}</Badge>
                      ))}
                    </div>
                  </div>
                )}

                {/* Messages */}
                <div className="space-y-3 max-h-[400px] overflow-y-auto p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
                  {mockMessages.map((msg, i) => (
                    <div
                      key={i}
                      className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={cn(
                          "max-w-[80%] rounded-lg p-3",
                          msg.role === 'user'
                            ? 'bg-[#0ca7d2] text-white'
                            : 'bg-white dark:bg-gray-800 border'
                        )}
                      >
                        <div className="text-sm">{msg.content}</div>
                        <div
                          className={cn(
                            "text-xs mt-1",
                            msg.role === 'user' ? 'text-white/70' : 'text-muted-foreground'
                          )}
                        >
                          {msg.timestamp}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </DialogContent>
        </Dialog>
      </div>
    </DashboardLayout>
  );
};

export default PesquisasEntrevistasPage;