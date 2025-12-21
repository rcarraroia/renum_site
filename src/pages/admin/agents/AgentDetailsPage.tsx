import React, { useState, useMemo, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Zap, Settings, MessageSquare, LayoutDashboard, Terminal, Save, ArrowLeft, Server, BarChart, RefreshCw, Edit, Pause, Play, Download, MoreVertical, Trash2, Users, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import PreviewChat from '@/components/agents/PreviewChat';
import { cn } from '@/lib/utils';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Link, useParams } from 'react-router-dom';
import { agentService } from '@/services/agentService';
import { Agent } from '@/types/agent';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';

// Configuration Panel
import ConfigRenusPanel from '@/components/agents/config/ConfigRenusPanel';

// Agent Specific Tabs
import AgentOverviewTab from '@/components/agents/AgentOverviewTab';
import AgentUsersTab from '@/components/agents/AgentUsersTab';
import AgentMetricsTab from '@/components/agents/AgentMetricsTab';
import AgentLogsTab from '@/components/agents/AgentLogsTab';

const AgentDetailsPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const [activeMainTab, setActiveMainTab] = useState('overview');
  const [agent, setAgent] = useState<Agent | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);

  useEffect(() => {
    const fetchAgent = async () => {
      if (!slug) return;
      try {
        setIsLoading(true);
        const data = await agentService.getAgentBySlug(slug);
        setAgent(data);
      } catch (error) {
        toast.error('Erro ao carregar detalhes do agente.');
        console.error(error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchAgent();
  }, [slug]);

  const mainTabs = [
    { value: 'overview', label: 'Visão Geral', icon: LayoutDashboard, component: AgentOverviewTab },
    { value: 'config', label: 'Configuração', icon: Settings, component: ConfigRenusPanel },
    { value: 'chat', label: 'Chat de Teste', icon: MessageSquare, component: PreviewChat },
    { value: 'users', label: 'Usuários/Instâncias', icon: Users, component: AgentUsersTab },
    { value: 'metrics', label: 'Métricas', icon: BarChart, component: AgentMetricsTab },
    { value: 'logs', label: 'Logs', icon: Terminal, component: AgentLogsTab },
  ];

  const handleSaveAndPublish = async () => {
    if (!agent) return;
    setIsSaving(true);
    try {
      // Aqui integraria com save agent se necessário, mas o painel de config já faz isso internamente
      // Simulação de publicação final se houver algo global
      toast.success(`Configuração do agente ${agent.name} publicada com sucesso!`);
      setHasUnsavedChanges(false);
    } catch (error) {
      toast.error('Erro ao publicar alterações.');
    } finally {
      setIsSaving(false);
    }
  };

  const handleToggleStatus = async () => {
    if (!agent) return;
    const newStatus = agent.status === 'active' ? 'paused' : 'active';
    try {
      const updated = await agentService.changeAgentStatus(agent.id, newStatus);
      setAgent(updated);
      toast.success(`Agente ${agent.name} ${newStatus === 'active' ? 'ativado' : 'pausado'}.`);
    } catch (error) {
      toast.error('Erro ao alterar status do agente.');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-600';
      case 'paused': return 'bg-yellow-600';
      case 'inactive': return 'bg-gray-500';
      case 'archived': return 'bg-red-600';
      default: return 'bg-gray-500';
    }
  };

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex flex-col items-center justify-center h-[60vh]">
          <Loader2 className="h-12 w-12 animate-spin text-[#FF6B35] mb-4" />
          <p className="text-muted-foreground animate-pulse text-lg">Carregando inteligência do agente...</p>
        </div>
      </DashboardLayout>
    );
  }

  if (!agent) {
    return (
      <DashboardLayout>
        <div className="text-center py-20">
          <Zap className="h-16 w-16 mx-auto text-muted-foreground mb-4 opacity-20" />
          <h2 className="text-2xl font-bold mb-2">Agente não encontrado</h2>
          <p className="text-muted-foreground mb-6">O agente solicitado não existe ou você não tem permissão para acessá-lo.</p>
          <Link to="/dashboard/admin/agents">
            <Button className="bg-[#4e4ea8]">Voltar para Lista</Button>
          </Link>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="flex items-center mb-4">
        <Link to="/dashboard/admin/agents" className="text-muted-foreground hover:text-primary flex items-center text-sm">
          <ArrowLeft className="h-4 w-4 mr-2" /> Voltar à Lista de Agentes
        </Link>
      </div>

      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold flex items-center">
          <Zap className="h-7 w-7 mr-3 text-[#FF6B35]" />
          {agent.name}
        </h2>
        <div className="flex items-center space-x-4">
          <Badge className={cn(
            "transition-colors text-white",
            getStatusColor(agent.status)
          )}>
            {(agent.status || 'unknown').toUpperCase()}
          </Badge>

          {/* Ações Rápidas */}
          <Button
            variant="outline"
            size="sm"
            onClick={handleToggleStatus}
            className={cn(agent.status === 'ativo' ? 'text-red-500 border-red-500 hover:bg-red-50' : 'text-green-500 border-green-500 hover:bg-green-50')}
          >
            {agent.status === 'ativo' ? <Pause className="h-4 w-4 mr-2" /> : <Play className="h-4 w-4 mr-2" />}
            {agent.status === 'ativo' ? 'Pausar' : 'Ativar'}
          </Button>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="icon">
                <MoreVertical className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Ações do Agente</DropdownMenuLabel>
              <DropdownMenuItem onClick={() => toast.info("Abrindo modal de edição...")}>
                <Edit className="h-4 w-4 mr-2" /> Editar Detalhes
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => toast.info("Exportando dados...")}>
                <Download className="h-4 w-4 mr-2" /> Exportar Dados
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => toast.warning("Excluindo agente...")} className="text-red-500">
                <Trash2 className="h-4 w-4 mr-2" /> Excluir Agente
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          {activeMainTab === 'config' && (
            <Button
              onClick={handleSaveAndPublish}
              disabled={isSaving || !hasUnsavedChanges}
              className="bg-[#4e4ea8] hover:bg-[#3a3a80]"
            >
              <Save className="h-4 w-4 mr-2" /> {isSaving ? 'Publicando...' : 'Salvar e Publicar'}
            </Button>
          )}
        </div>
      </div>

      {/* Main Tabs */}
      <Tabs value={activeMainTab} onValueChange={setActiveMainTab} className="w-full">
        <TabsList className="grid w-full grid-cols-6 h-auto p-1 bg-gray-100 dark:bg-gray-800">
          {mainTabs.map(tab => (
            <TabsTrigger
              key={tab.value}
              value={tab.value}
              className={cn(
                "flex items-center space-x-2 data-[state=active]:bg-[#FF6B35] data-[state=active]:text-white data-[state=active]:shadow-md transition-all"
              )}
            >
              <tab.icon className="h-4 w-4" />
              <span className="hidden sm:inline">{tab.label}</span>
            </TabsTrigger>
          ))}
        </TabsList>

        {/* Tab Content: Overview */}
        <TabsContent value="overview" className="mt-6">
          <AgentOverviewTab agent={agent} />
        </TabsContent>

        {/* Tab Content: Configuration (Nested Tabs) */}
        <TabsContent value="config" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">Configuração Detalhada do Agente</CardTitle>
              <p className="text-sm text-muted-foreground">Ajuste as instruções, ferramentas e políticas de segurança específicas para este agente.</p>
            </CardHeader>
            <CardContent>
              <ConfigRenusPanel agentId={agent.id} isGlobalConfig={false} />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Tab Content: Users/Instances */}
        <TabsContent value="users" className="mt-6">
          <AgentUsersTab agentType={agent.type} />
        </TabsContent>

        {/* Tab Content: Metrics */}
        <TabsContent value="metrics" className="mt-6">
          <AgentMetricsTab />
        </TabsContent>

        {/* Tab Content: Chat de Teste */}
        <TabsContent value="chat" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">Chat de Teste - {agent.name}</CardTitle>
              <p className="text-sm text-muted-foreground">Teste o agente em tempo real para validar comportamento e respostas.</p>
            </CardHeader>
            <CardContent className="p-0">
              <div className="h-[600px]">
                <PreviewChat
                  agentName={agent.name}
                  agentSlug={agent.slug}
                  systemPrompt="Você é um agente de teste. Responda de forma profissional e útil."
                  useRealAgent={true}
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Tab Content: Logs */}
        <TabsContent value="logs" className="mt-6">
          <AgentLogsTab />
        </TabsContent>
      </Tabs>
    </DashboardLayout>
  );
};

export default AgentDetailsPage;