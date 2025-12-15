import React, { useState, useMemo, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Zap, Plus, Users, MessageSquare, Server, ArrowLeft, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';
import { Agent, AgentStatus } from '@/types/agent';
import agentService from '@/services/agentService';
import AgentCard from '@/components/agents/AgentCard';
import AgentFilters from '@/components/agents/AgentFilters';
import { toast } from 'sonner';

const AgentsListPage: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    search: '',
    status: 'all',
    template_type: 'all',
    client: 'all',
    category: 'all'
  });
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 6;

  // Carregar agentes reais da API
  useEffect(() => {
    const fetchAgents = async () => {
      try {
        setLoading(true);
        const apiParams: any = {};

        if (filters.status !== 'all') {
          // Mapeamento simples, assumindo valores compatíveis
          apiParams.status = filters.status;
        }

        const data = await agentService.listAgents(apiParams);

        // Cast AgentListItem to Agent
        setAgents(data as unknown as Agent[]);
      } catch (error) {
        toast.error('Erro ao carregar agentes.');
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchAgents();
  }, [filters.status]);

  const filteredAgents = useMemo(() => {
    return agents.filter(agent => {
      const matchesSearch = filters.search.toLowerCase() === '' ||
        agent.name.toLowerCase().includes(filters.search.toLowerCase()) ||
        (agent.slug ? agent.slug.toLowerCase().includes(filters.search.toLowerCase()) : false);

      const matchesStatus = filters.status === 'all' || agent.status === filters.status;
      const matchesTemplateType = filters.template_type === 'all' || agent.template_type === filters.template_type;

      return matchesSearch && matchesStatus && matchesTemplateType;
    });
  }, [agents, filters]);

  const paginatedAgents = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    return filteredAgents.slice(startIndex, startIndex + itemsPerPage);
  }, [filteredAgents, currentPage]);

  const totalPages = Math.ceil(filteredAgents.length / itemsPerPage);

  const metrics = useMemo(() => ({
    total: agents.length,
    active: agents.filter(a => a.status === 'active').length,
    conversations: 0, // Placeholder
    leadsQualified: 0, // Placeholder
    conversionRate: 0, // Placeholder
  }), [agents]);

  const handleEdit = (agent: Agent) => {
    // Navigation handled by Link in Card usually, but keeping handler for compatibility
    console.log('Edit agent', agent.id);
  };

  const handleClone = (agent: Agent) => {
    toast.info("Funcionalidade de clonar em breve.");
  };

  const handlePauseResume = async (agent: Agent) => {
    const newStatus: AgentStatus = agent.status === 'active' ? 'paused' : 'active';
    try {
      await agentService.changeAgentStatus(agent.id, newStatus);
      setAgents(prev => prev.map(a =>
        a.id === agent.id ? { ...a, status: newStatus } : a
      ));
      toast.success(`Agente "${agent.name}" status alterado para ${newStatus}`);
    } catch (e) {
      toast.error("Erro ao alterar status");
      console.error(e);
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm(`Tem certeza que deseja excluir este agente?`)) {
      try {
        await agentService.deleteAgent(id);
        setAgents(prev => prev.filter(a => a.id !== id));
        toast.warning(`Agente excluído.`);
      } catch (e) {
        toast.error("Erro ao excluir agente");
      }
    }
  };

  return (
    <DashboardLayout>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold flex items-center">
          <Zap className="h-7 w-7 mr-3 text-[#4e4ea8]" />
          Gerenciamento de Agentes
        </h2>
        <Link to="/dashboard/admin/agents/create">
          <Button className="bg-[#FF6B35] hover:bg-[#e55f30]">
            <Plus className="h-4 w-4 mr-2" /> Novo Agente
          </Button>
        </Link>
      </div>

      {/* Metrics Cards */}
      <div className="grid gap-4 md:grid-cols-4 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Agentes</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.total}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Agentes Ativos</CardTitle>
            <Server className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-500">{metrics.active}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversas (Hoje)</CardTitle>
            <MessageSquare className="h-4 w-4 text-[#0ca7d2]" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-[#0ca7d2]">{metrics.conversations}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Leads Qualificados</CardTitle>
            <Users className="h-4 w-4 text-[#FF6B35]" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-[#FF6B35]">{metrics.leadsQualified}</div>
            <p className="text-xs text-muted-foreground mt-1">
              Taxa de conversão: {metrics.conversionRate}%
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <div className="mb-6">
        <AgentFilters onFilterChange={setFilters as any} />
      </div>

      {/* Agent List */}
      <h3 className="text-xl font-semibold mb-4 flex items-center">
        <Users className="h-5 w-5 mr-2 text-muted-foreground" />
        Lista de Agentes ({loading ? '...' : filteredAgents.length})
      </h3>

      {loading ? (
        <div className="text-center py-10">Carregando agentes...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {paginatedAgents.map(agent => (
            <AgentCard
              key={agent.id}
              agent={agent}
              onEdit={handleEdit}
              onClone={handleClone}
              onPauseResume={handlePauseResume}
              onDelete={handleDelete}
            />
          ))}
          {filteredAgents.length === 0 && (
            <div className="col-span-full text-center py-12 border-2 border-dashed rounded-lg">
              <Zap className="h-10 w-10 mx-auto text-muted-foreground mb-3" />
              <p className="text-lg text-muted-foreground">Nenhum agente encontrado.</p>
            </div>
          )}
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-end items-center space-x-4 mt-6">
          <span className="text-sm text-muted-foreground">
            Página {currentPage} de {totalPages}
          </span>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
          >
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
            disabled={currentPage === totalPages}
          >
            <ArrowRight className="h-4 w-4" />
          </Button>
        </div>
      )}
    </DashboardLayout>
  );
};

export default AgentsListPage;