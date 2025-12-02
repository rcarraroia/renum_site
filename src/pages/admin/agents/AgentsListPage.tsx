import React, { useState, useMemo } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Zap, Plus, Users, Briefcase, MessageSquare, Server, TrendingUp, ArrowLeft, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';
import { mockAgents, mockProjects } from '@/mocks/agents.mock';
import { Agent } from '@/types/agent';
import AgentCard from '@/components/agents/AgentCard';
import AgentFilters from '@/components/agents/AgentFilters';
import PreviewChat from '@/components/agents/PreviewChat';
import { toast } from 'sonner';

const AgentsListPage: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>(mockAgents);
  const [filters, setFilters] = useState({ search: '', status: 'all', client: 'all', category: 'all' });
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 6;

  const filteredAgents = useMemo(() => {
    return agents.filter(agent => {
      const matchesSearch = filters.search.toLowerCase() === '' || 
                            agent.name.toLowerCase().includes(filters.search.toLowerCase()) ||
                            agent.slug.toLowerCase().includes(filters.search.toLowerCase());
      
      const matchesStatus = filters.status === 'all' || agent.status === filters.status;
      const matchesClient = filters.client === 'all' || agent.client_id === filters.client;
      const matchesCategory = filters.category === 'all' || agent.category === filters.category;

      return matchesSearch && matchesStatus && matchesClient && matchesCategory;
    });
  }, [agents, filters]);

  const paginatedAgents = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    return filteredAgents.slice(startIndex, startIndex + itemsPerPage);
  }, [filteredAgents, currentPage]);

  const totalPages = Math.ceil(filteredAgents.length / itemsPerPage);

  const metrics = useMemo(() => ({
    total: agents.length,
    active: agents.filter(a => a.status === 'ativo').length,
    conversations: agents.reduce((sum, a) => sum + a.conversations_today, 0),
  }), [agents]);

  const handleEdit = (agent: Agent) => {
    toast.info(`Abrindo edição para: ${agent.name}`);
    // In a real app, this would open a modal or redirect to a specific config tab
  };

  const handleDelete = (id: string) => {
    setAgents(prev => prev.filter(a => a.id !== id));
    toast.warning(`Agente (ID: ${id}) excluído.`);
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
            <CardTitle className="text-sm font-medium">Slots Disponíveis (Mock)</CardTitle>
            <Briefcase className="h-4 w-4 text-[#FF6B35]" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-[#FF6B35]">
                {mockProjects.reduce((sum, p) => sum + p.agents_limit, 0) - agents.length}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters and Preview */}
      <div className="grid lg:grid-cols-3 gap-6 mb-6">
        <div className="lg:col-span-2">
            <AgentFilters onFilterChange={setFilters} />
        </div>
        <div className="lg:col-span-1 h-full">
            <PreviewChat />
        </div>
      </div>

      {/* Agent List */}
      <h3 className="text-xl font-semibold mb-4 flex items-center">
        <Users className="h-5 w-5 mr-2 text-muted-foreground" />
        Lista de Agentes ({filteredAgents.length})
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {paginatedAgents.map(agent => (
          <AgentCard 
            key={agent.id} 
            agent={agent} 
            onEdit={handleEdit} 
            onDelete={handleDelete} 
          />
        ))}
        {filteredAgents.length === 0 && (
            <div className="col-span-full text-center py-12 border-2 border-dashed rounded-lg">
                <Zap className="h-10 w-10 mx-auto text-muted-foreground mb-3" />
                <p className="text-lg text-muted-foreground">Nenhum agente corresponde à sua busca.</p>
            </div>
        )}
      </div>

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