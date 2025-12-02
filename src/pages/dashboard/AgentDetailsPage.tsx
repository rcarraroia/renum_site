import React, { useState, useMemo } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Zap, Settings, MessageSquare, BarChart, Clock, Wrench, LayoutDashboard, RefreshCw, Code, Users } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { useParams, Navigate } from 'react-router-dom';
import { getAgentById } from '@/data/mockAgents';
import AgentConfigurationTabs from '@/components/agent-details/AgentConfigurationTabs';
import { Separator } from '@/components/ui/separator';
import { Agent } from '@/types/agent';

const AgentDetailsPage: React.FC = () => {
  const { agentId } = useParams<{ agentId: string }>();
  const [activeTab, setActiveTab] = useState('overview');

  // Mock data retrieval
  const agent = useMemo(() => {
    // In a real app, we would fetch this data
    return getAgentById(agentId || 'a1');
  }, [agentId]);

  if (!agent) {
    return <Navigate to="/dashboard/admin" replace />;
  }

  const getStatusColor = (status: typeof agent.status) => {
    switch (status) {
        case 'Active': return 'bg-green-500';
        case 'Inactive': return 'bg-red-500';
        case 'Draft': return 'bg-yellow-500';
        case 'Training': return 'bg-blue-500';
    }
  };

  const mainTabs = [
    { value: 'overview', label: 'Visão Geral', icon: LayoutDashboard, component: () => <AgentOverview agent={agent} /> },
    { value: 'configuration', label: 'Configuração', icon: Settings, component: () => <AgentConfigurationTabs agent={agent} /> },
    { value: 'instances', label: 'Instâncias', icon: Users, component: () => <AgentInstances agent={agent} /> },
    { value: 'metrics', label: 'Métricas', icon: BarChart, component: () => <AgentMetrics agent={agent} /> },
    { value: 'logs', label: 'Logs', icon: Clock, component: () => <AgentLogs agent={agent} /> },
  ];

  return (
    <DashboardLayout>
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center space-x-3">
          <Zap className="h-8 w-8 text-[#FF6B35]" />
          <h2 className="text-3xl font-bold">{agent.name}</h2>
          <Badge className={cn("capitalize text-white", getStatusColor(agent.status))}>
            {agent.status}
          </Badge>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline">
            <RefreshCw className="h-4 w-4 mr-2" /> Reverter para V{agent.version}
          </Button>
          <Button className="bg-[#FF6B35] hover:bg-[#e55f30]">
            <Zap className="h-4 w-4 mr-2" /> Testar em Sandbox
          </Button>
        </div>
      </div>
      
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-5 h-auto p-1 bg-gray-100 dark:bg-gray-800">
          {mainTabs.map(tab => (
            <TabsTrigger 
              key={tab.value} 
              value={tab.value} 
              className={cn(
                "flex items-center space-x-2 data-[state=active]:bg-[#4e4ea8] data-[state=active]:text-white data-[state=active]:shadow-md transition-all",
                activeTab === tab.value && 'bg-[#4e4ea8] text-white'
              )}
            >
              <tab.icon className="h-4 w-4" />
              <span className="hidden sm:inline">{tab.label}</span>
            </TabsTrigger>
          ))}
        </TabsList>

        {mainTabs.map(tab => (
          <TabsContent key={tab.value} value={tab.value} className="mt-6">
            <tab.component />
          </TabsContent>
        ))}
      </Tabs>
    </DashboardLayout>
  );
};

// --- Placeholder Components for Main Tabs ---

const AgentOverview: React.FC<{ agent: Agent }> = ({ agent }) => (
    <div className="space-y-6">
        <Card>
            <CardHeader><CardTitle>Informações Básicas</CardTitle></CardHeader>
            <CardContent className="grid md:grid-cols-2 gap-4">
                <div><span className="font-semibold">Descrição:</span> {agent.description}</div>
                <div><span className="font-semibold">Canal Principal:</span> {agent.channel}</div>
                <div><span className="font-semibold">Versão Atual:</span> {agent.version}</div>
                <div><span className="font-semibold">Última Publicação:</span> {agent.lastPublished}</div>
            </CardContent>
        </Card>
        <Card>
            <CardHeader><CardTitle>Resumo de Performance (Mock)</CardTitle></CardHeader>
            <CardContent>
                <p className="text-muted-foreground">Nenhuma métrica disponível para esta visualização.</p>
            </CardContent>
        </Card>
    </div>
);

const AgentInstances: React.FC<{ agent: Agent }> = ({ agent }) => (
    <Card>
        <CardHeader><CardTitle>Instâncias Ativas</CardTitle></CardHeader>
        <CardContent><p className="text-muted-foreground">Gerenciamento de instâncias de execução (Mock).</p></CardContent>
    </Card>
);

const AgentMetrics: React.FC<{ agent: Agent }> = ({ agent }) => (
    <Card>
        <CardHeader><CardTitle>Métricas de Uso</CardTitle></CardHeader>
        <CardContent><p className="text-muted-foreground">Gráficos de performance e uso de tokens (Mock).</p></CardContent>
    </Card>
);

const AgentLogs: React.FC<{ agent: Agent }> = ({ agent }) => (
    <Card>
        <CardHeader><CardTitle>Logs de Execução</CardTitle></CardHeader>
        <CardContent><p className="text-muted-foreground">Logs detalhados de chamadas de ferramentas e respostas (Mock).</p></CardContent>
    </Card>
);

export default AgentDetailsPage;