import React, { useState, useMemo } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Zap, Settings, MessageSquare, LayoutDashboard, Terminal, Save, ArrowLeft, Server, BarChart, RefreshCw, Edit, Pause, Play, Download, MoreVertical, Trash2, Users } from 'lucide-react';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Link, useParams } from 'react-router-dom';
import { mockAgents } from '@/mocks/agents.mock';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';

// Configuration Panel
import ConfigRenusPanel from '@/components/agents/config/ConfigRenusPanel';

// Agent Specific Tabs
import AgentOverviewTab from '@/components/agents/AgentOverviewTab';
import AgentUsersTab from '@/components/agents/AgentUsersTab'; // Novo componente
import AgentMetricsTab from '@/components/agents/AgentMetricsTab';
import AgentLogsTab from '@/components/agents/AgentLogsTab';
import ApiWebhooksTab from '@/components/agents/ApiWebhooksTab';

const AgentDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [activeMainTab, setActiveMainTab] = useState('overview');
  const [isSaving, setIsSaving] = useState(false);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(true); // Mock state

  const agent = mockAgents.find(a => a.id === id) || {
    id: 'mock-100',
    name: 'Novo Agente (Mock)',
    description: 'Agente de fallback para testes.', // Adicionado para satisfazer a interface Agent
    status: 'inativo',
    version: 'V1.0',
    type: 'b2c_individual', // Default mock type
    created_at: 'N/A',
    client_id: '1',
    project_id: '1',
    category: 'custom',
    slug: 'mock-agent',
    domain: 'mock-agent.renum.com.br',
    channel: ['web'],
    model: 'gpt-4o-mini',
    instances_count: 0,
    conversations_today: 0,
  };

  const mainTabs = [
    { value: 'overview', label: 'Visão Geral', icon: LayoutDashboard, component: AgentOverviewTab },
    { value: 'config', label: 'Configuração', icon: Settings, component: ConfigRenusPanel },
    { value: 'instances', label: 'Instâncias/Usuários', icon: Users, component: AgentUsersTab },
    { value: 'metrics', label: 'Métricas', icon: BarChart, component: AgentMetricsTab },
    { value: 'logs', label: 'Logs', icon: Terminal, component: AgentLogsTab },
  ];

  const handleSaveAndPublish = () => {
    setIsSaving(true);
    setTimeout(() => {
      setIsSaving(false);
      setHasUnsavedChanges(false);
      toast.success(`Configuração do agente ${agent.name} publicada com sucesso!`);
    }, 1500);
  };
  
  const handleToggleStatus = () => {
    const newStatus = agent.status === 'ativo' ? 'pausado' : 'ativo';
    toast.info(`Agente ${agent.name} ${newStatus === 'ativo' ? 'ativado' : 'pausado'}. (Mock)`);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
        case 'ativo': return 'bg-green-500';
        case 'pausado': return 'bg-yellow-500';
        case 'inativo': return 'bg-gray-500';
        case 'erro': return 'bg-red-500';
        default: return 'bg-gray-500';
    }
  };

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
                {agent.status.toUpperCase()} | {agent.version}
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
        <TabsList className="grid w-full grid-cols-5 h-auto p-1 bg-gray-100 dark:bg-gray-800">
          {mainTabs.map(tab => (
            <TabsTrigger 
              key={tab.value} 
              value={tab.value} 
              className={cn(
                "flex items-center space-x-2 data-[state=active]:bg-[#FF6B35] data-[state=active]:text-white data-[state=active]:shadow-md transition-all",
                activeMainTab === tab.value && 'bg-[#FF6B35] text-white'
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
                    <ConfigRenusPanel isGlobalConfig={false} />
                </CardContent>
            </Card>
        </TabsContent>

        {/* Tab Content: Instances/Users */}
        <TabsContent value="instances" className="mt-6">
            <AgentUsersTab agentType={agent.type} />
        </TabsContent>

        {/* Tab Content: Metrics */}
        <TabsContent value="metrics" className="mt-6">
            <AgentMetricsTab />
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