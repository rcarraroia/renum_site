/**
 * Agent Detail Page - Sprint 09 Task F.4
 * Detailed view of a single agent with sub-agents management
 */

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  Edit,
  Trash2,
  Power,
  Plus,
  MoreVertical,
  Eye,
  EyeOff,
  Activity,
  MessageSquare,
  Users,
  TrendingUp,
} from 'lucide-react';
import {
  getAgent,
  getAgentStats,
  deleteAgent,
  changeAgentStatus,
  listSubAgents,
  deleteSubAgent,
  toggleSubAgentActive,
} from '@/services/agentService';
import type { Agent, AgentStats, SubAgent, AgentStatus } from '@/types/agent';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs';

export default function AgentDetailPage() {
  const { agentId } = useParams<{ agentId: string }>();
  const navigate = useNavigate();

  const [agent, setAgent] = useState<Agent | null>(null);
  const [stats, setStats] = useState<AgentStats | null>(null);
  const [subAgents, setSubAgents] = useState<SubAgent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (agentId) {
      loadData();
    }
  }, [agentId]);

  async function loadData() {
    if (!agentId) return;

    try {
      setLoading(true);
      const [agentData, statsData, subAgentsData] = await Promise.all([
        getAgent(agentId),
        getAgentStats(agentId),
        listSubAgents(agentId),
      ]);

      setAgent(agentData);
      setStats(statsData);
      setSubAgents(subAgentsData);
    } catch (error) {
      console.error('Error loading agent data:', error);
      alert('Erro ao carregar dados do agent');
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete() {
    if (!agentId || !agent) return;

    if (
      !confirm(
        `Tem certeza que deseja deletar o agent "${agent.name}"? Todos os sub-agents serão deletados também.`
      )
    ) {
      return;
    }

    try {
      await deleteAgent(agentId);
      navigate('/agents');
    } catch (error) {
      console.error('Error deleting agent:', error);
      alert('Erro ao deletar agent');
    }
  }

  async function handleStatusChange(newStatus: AgentStatus) {
    if (!agentId) return;

    try {
      await changeAgentStatus(agentId, newStatus);
      await loadData();
    } catch (error) {
      console.error('Error changing status:', error);
      alert('Erro ao alterar status');
    }
  }

  async function handleDeleteSubAgent(subAgentId: string) {
    if (!agentId) return;

    if (!confirm('Tem certeza que deseja deletar este sub-agent?')) {
      return;
    }

    try {
      await deleteSubAgent(agentId, subAgentId);
      await loadData();
    } catch (error) {
      console.error('Error deleting sub-agent:', error);
      alert('Erro ao deletar sub-agent');
    }
  }

  async function handleToggleSubAgentActive(subAgentId: string) {
    if (!agentId) return;

    try {
      await toggleSubAgentActive(agentId, subAgentId);
      await loadData();
    } catch (error) {
      console.error('Error toggling sub-agent:', error);
      alert('Erro ao alterar status do sub-agent');
    }
  }

  if (loading) {
    return (
      <div className="container mx-auto py-6">
        <p className="text-center text-muted-foreground">Carregando...</p>
      </div>
    );
  }

  if (!agent) {
    return (
      <div className="container mx-auto py-6">
        <p className="text-center text-muted-foreground">Agent não encontrado</p>
      </div>
    );
  }

  const getStatusBadge = (status: AgentStatus) => {
    const variants: Record<AgentStatus, 'default' | 'secondary' | 'destructive' | 'outline'> = {
      draft: 'secondary',
      active: 'default',
      paused: 'outline',
      archived: 'destructive',
    };

    return <Badge variant={variants[status]}>{status}</Badge>;
  };

  return (
    <div className="container mx-auto py-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => navigate('/agents')}>
            <ArrowLeft className="w-4 h-4" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold">{agent.name}</h1>
            {agent.description && (
              <p className="text-muted-foreground">{agent.description}</p>
            )}
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => navigate(`/agents/${agentId}/edit`)}>
            <Edit className="w-4 h-4 mr-2" />
            Editar
          </Button>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="icon">
                <MoreVertical className="w-4 h-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => handleStatusChange('active')}>
                <Power className="w-4 h-4 mr-2" />
                Ativar
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleStatusChange('paused')}>
                <Power className="w-4 h-4 mr-2" />
                Pausar
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleStatusChange('archived')}>
                <Power className="w-4 h-4 mr-2" />
                Arquivar
              </DropdownMenuItem>
              <DropdownMenuItem onClick={handleDelete} className="text-destructive">
                <Trash2 className="w-4 h-4 mr-2" />
                Deletar
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid gap-4 md:grid-cols-4">
          <Card className="p-4">
            <div className="flex items-center gap-2 mb-2">
              <Users className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm text-muted-foreground">Sub-Agents</span>
            </div>
            <p className="text-2xl font-bold">{stats.sub_agents_count}</p>
          </Card>
          <Card className="p-4">
            <div className="flex items-center gap-2 mb-2">
              <MessageSquare className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm text-muted-foreground">Conversas</span>
            </div>
            <p className="text-2xl font-bold">{stats.total_conversations}</p>
            <p className="text-xs text-muted-foreground">
              {stats.active_conversations} ativas
            </p>
          </Card>
          <Card className="p-4">
            <div className="flex items-center gap-2 mb-2">
              <Activity className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm text-muted-foreground">Mensagens</span>
            </div>
            <p className="text-2xl font-bold">{stats.total_messages}</p>
          </Card>
          <Card className="p-4">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm text-muted-foreground">Acessos</span>
            </div>
            <p className="text-2xl font-bold">{stats.access_count}</p>
          </Card>
        </div>
      )}

      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Visão Geral</TabsTrigger>
          <TabsTrigger value="sub-agents">Sub-Agents ({subAgents.length})</TabsTrigger>
          <TabsTrigger value="config">Configuração</TabsTrigger>
          <TabsTrigger value="evolution">Evolução SICC</TabsTrigger>
          <TabsTrigger value="memory">Memória</TabsTrigger>
          <TabsTrigger value="learning">Aprendizados</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-4">
          <Card className="p-6">
            <h3 className="font-semibold mb-4">Informações</h3>
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <p className="text-sm text-muted-foreground">Status</p>
                <div className="mt-1">{getStatusBadge(agent.status)}</div>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Canal</p>
                <p className="mt-1">{agent.channel}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Template</p>
                <p className="mt-1">{agent.template_type}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Modelo</p>
                <p className="mt-1 font-mono text-sm">{agent.model}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Público</p>
                <p className="mt-1">{agent.is_public ? 'Sim' : 'Não'}</p>
              </div>
              {agent.slug && (
                <div>
                  <p className="text-sm text-muted-foreground">Slug</p>
                  <p className="mt-1 font-mono text-sm">{agent.slug}</p>
                </div>
              )}
            </div>
          </Card>

          <Card className="p-6">
            <h3 className="font-semibold mb-4">System Prompt</h3>
            <pre className="text-sm bg-muted p-4 rounded-lg overflow-x-auto whitespace-pre-wrap">
              {agent.system_prompt}
            </pre>
          </Card>
        </TabsContent>

        {/* Sub-Agents Tab */}
        <TabsContent value="sub-agents" className="space-y-4">
          <div className="flex justify-between items-center">
            <p className="text-sm text-muted-foreground">
              {subAgents.length} sub-agent(s) configurado(s)
            </p>
            <Button onClick={() => navigate(`/agents/${agentId}/sub-agents/new`)}>
              <Plus className="w-4 h-4 mr-2" />
              Novo Sub-Agent
            </Button>
          </div>

          {subAgents.length === 0 ? (
            <Card className="p-12 text-center">
              <p className="text-muted-foreground mb-4">
                Nenhum sub-agent configurado ainda
              </p>
              <Button onClick={() => navigate(`/agents/${agentId}/sub-agents/new`)}>
                <Plus className="w-4 h-4 mr-2" />
                Criar Primeiro Sub-Agent
              </Button>
            </Card>
          ) : (
            <div className="grid gap-4">
              {subAgents.map((subAgent) => (
                <Card key={subAgent.id} className="p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <h4 className="font-semibold">{subAgent.name}</h4>
                        {subAgent.is_active ? (
                          <Badge variant="default">
                            <Eye className="w-3 h-3 mr-1" />
                            Ativo
                          </Badge>
                        ) : (
                          <Badge variant="secondary">
                            <EyeOff className="w-3 h-3 mr-1" />
                            Inativo
                          </Badge>
                        )}
                      </div>
                      {subAgent.description && (
                        <p className="text-sm text-muted-foreground mb-2">
                          {subAgent.description}
                        </p>
                      )}
                      <div className="flex gap-4 text-sm">
                        <span className="text-muted-foreground">
                          Canal: <span className="text-foreground">{subAgent.channel}</span>
                        </span>
                        <span className="text-muted-foreground">
                          Modelo:{' '}
                          <span className="text-foreground font-mono text-xs">
                            {subAgent.model}
                          </span>
                        </span>
                      </div>
                      {subAgent.topics && subAgent.topics.length > 0 && (
                        <div className="flex gap-2 mt-2">
                          {subAgent.topics.map((topic) => (
                            <Badge key={topic} variant="outline">
                              {topic}
                            </Badge>
                          ))}
                        </div>
                      )}
                    </div>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon">
                          <MoreVertical className="w-4 h-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem
                          onClick={() =>
                            navigate(`/agents/${agentId}/sub-agents/${subAgent.id}/edit`)
                          }
                        >
                          <Edit className="w-4 h-4 mr-2" />
                          Editar
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          onClick={() => handleToggleSubAgentActive(subAgent.id)}
                        >
                          {subAgent.is_active ? (
                            <>
                              <EyeOff className="w-4 h-4 mr-2" />
                              Desativar
                            </>
                          ) : (
                            <>
                              <Eye className="w-4 h-4 mr-2" />
                              Ativar
                            </>
                          )}
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          onClick={() => handleDeleteSubAgent(subAgent.id)}
                          className="text-destructive"
                        >
                          <Trash2 className="w-4 h-4 mr-2" />
                          Deletar
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>

        {/* Config Tab */}
        <TabsContent value="config" className="space-y-4">
          <Card className="p-6">
            <h3 className="font-semibold mb-4">Configuração JSON</h3>
            <pre className="text-sm bg-muted p-4 rounded-lg overflow-x-auto">
              {JSON.stringify(agent.config, null, 2)}
            </pre>
          </Card>
        </TabsContent>

        {/* Evolution SICC Tab */}
        <TabsContent value="evolution" className="space-y-4">
          <Card className="p-6">
            <h3 className="font-semibold mb-4">Evolução do Agente - SICC</h3>
            <p className="text-sm text-muted-foreground">
              Esta aba exibirá gráficos e métricas de evolução deste agente ao longo do tempo.
            </p>
            <div className="mt-4 p-4 bg-muted rounded-lg">
              <p className="text-sm">
                📊 <strong>Funcionalidades em desenvolvimento:</strong>
              </p>
              <ul className="mt-2 text-sm space-y-1 list-disc list-inside">
                <li>Crescimento de memórias ao longo do tempo</li>
                <li>Taxa de sucesso de aprendizados</li>
                <li>Velocidade de aprendizado</li>
                <li>Histórico de atividades recentes</li>
              </ul>
            </div>
          </Card>
        </TabsContent>

        {/* Memory Tab */}
        <TabsContent value="memory" className="space-y-4">
          <Card className="p-6">
            <h3 className="font-semibold mb-4">Gerenciamento de Memória</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Gerenciar chunks de memória adaptativa deste agente.
            </p>
            <div className="space-y-2">
              <div className="flex items-center justify-between p-3 border rounded">
                <div>
                  <p className="font-medium">Memórias Totais</p>
                  <p className="text-sm text-muted-foreground">
                    Aguardando implementação da busca de memórias para este agente
                  </p>
                </div>
                <Badge>Em breve</Badge>
              </div>
              <div className="mt-4 p-4 bg-muted rounded-lg">
                <p className="text-sm">
                  🧠 <strong>Funcionalidades planejadas:</strong>
                </p>
                <ul className="mt-2 text-sm space-y-1 list-disc list-inside">
                  <li>Visualização de chunks de memória</li>
                  <li>Busca semântica por similaridade</li>
                  <li>Edição/Exclusão de memórias</li>
                  <li>Filtro por tipo (FAQ, Pattern, Insight, etc.)</li>
                </ul>
              </div>
            </div>
          </Card>
        </TabsContent>

        {/* Learning Queue Tab */}
        <TabsContent value="learning" className="space-y-4">
          <Card className="p-6">
            <h3 className="font-semibold mb-4">Fila de Aprendizados</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Aprovar ou rejeitar aprendizados pendentes deste agente.
            </p>
            <div className="space-y-2">
              <div className="flex items-center justify-between p-3 border rounded">
                <div>
                  <p className="font-medium">Aprendizados Pendentes</p>
                  <p className="text-sm text-muted-foreground">
                    Aguardando implementação da busca de aprendizados
                  </p>
                </div>
                <Badge variant="secondary">0</Badge>
              </div>
              <div className="mt-4 p-4 bg-muted rounded-lg">
                <p className="text-sm">
                  🎓 <strong>Funcionalidades planejadas:</strong>
                </p>
                <ul className="mt-2 text-sm space-y-1 list-disc list-inside">
                  <li>Visualização de aprendizados pendentes</li>
                  <li>Aprovação em lote</li>
                  <li>Análise de confiança e qualidade</li>
                  <li>Histórico de aprendizados aprovados/rejeitados</li>
                </ul>
              </div>
            </div>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
