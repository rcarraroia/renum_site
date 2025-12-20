
import React, { useEffect, useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Button } from '@/components/ui/button';
import { Plus, Search, Filter } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Agent } from '@/types/agent';
import AgentCard from '@/components/agents/AgentCard';
import { clientDashboardService } from '@/services/clientDashboardService';
import { Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const ClientAgentsPage: React.FC = () => {
    const navigate = useNavigate();
    const [agents, setAgents] = useState<Agent[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        const fetchAgents = async () => {
            try {
                setLoading(true);
                const data = await clientDashboardService.getAgents();
                setAgents(data);
            } catch (error) {
                console.error('Error fetching agents:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchAgents();
    }, []);

    const filteredAgents = agents.filter(agent =>
        agent.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (agent.slug && agent.slug.toLowerCase().includes(searchTerm.toLowerCase()))
    );

    return (
        <DashboardLayout>
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Meus Agentes</h1>
                    <p className="text-muted-foreground mt-1">Gerencie seus assistentes virtuais ativos.</p>
                </div>
                <Button
                    onClick={() => navigate('/marketplace')}
                    className="bg-[#FF6B35] hover:bg-[#e55f30] text-white"
                >
                    <Plus className="w-4 h-4 mr-2" />
                    Novo Agente (Marketplace)
                </Button>
            </div>

            <div className="flex items-center space-x-2 mb-6 bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
                <div className="relative flex-1">
                    <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                    <Input
                        placeholder="Buscar por nome..."
                        className="pl-9"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <Button variant="outline">
                    <Filter className="w-4 h-4 mr-2" />
                    Filtros
                </Button>
            </div>

            {loading ? (
                <div className="flex justify-center items-center h-64">
                    <Loader2 className="w-8 h-8 animate-spin text-primary" />
                </div>
            ) : filteredAgents.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredAgents.map((agent) => (
                        <div key={agent.id} className="cursor-pointer">
                            <AgentCard
                                agent={agent}
                                basePath="/dashboard/client/agents"
                                onClick={() => navigate(`/dashboard/client/agents/${agent.slug}`)}
                                onEdit={() => { }}
                                onDelete={() => { }}
                            />
                        </div>
                    ))}
                </div>
            ) : (
                <div className="text-center py-12 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-dashed">
                    <h3 className="text-lg font-semibold mb-2">Você ainda não tem agentes</h3>
                    <p className="text-muted-foreground mb-4">Explore o Marketplace para começar com seu primeiro agente IA.</p>
                    <Button onClick={() => navigate('/marketplace')} variant="outline">
                        Ir para Marketplace
                    </Button>
                </div>
            )}
        </DashboardLayout>
    );
};

export default ClientAgentsPage;
