import React, { useState, useEffect, useMemo, useCallback } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, TrendingDown, Brain, Zap, Activity, Clock, Users, RefreshCw, Loader2, XCircle, CheckCircle } from 'lucide-react';
import { siccService } from '@/services/siccService';
import { EvolutionStats, RecentActivity } from '@/types/sicc';
import { cn } from '@/lib/utils';
import LineChart from '@/components/charts/LineChart';
import AreaChart from '@/components/charts/AreaChart';
import { formatDistanceToNow } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from 'sonner';

interface AgentOption {
    id: string;
    name: string;
    client_id: string;
}

const PERIOD_OPTIONS = [
    { value: '7', label: 'Últimos 7 dias' },
    { value: '30', label: 'Últimos 30 dias' },
    { value: '90', label: 'Últimos 90 dias' },
    { value: '365', label: 'Último Ano' },
];

const EvolutionPage: React.FC = () => {
    const [agents, setAgents] = useState<AgentOption[]>([]);
    const [selectedAgentId, setSelectedAgentId] = useState<string | undefined>(undefined);
    const [selectedPeriod, setSelectedPeriod] = useState('30');
    const [stats, setStats] = useState<EvolutionStats | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // 1. Fetch Agents on Mount
    useEffect(() => {
        siccService.getAgents().then(data => {
            setAgents(data);
            if (data.length > 0) {
                setSelectedAgentId(data[0].id);
            } else {
                setIsLoading(false);
            }
        }).catch(err => {
            setError("Falha ao carregar lista de agentes.");
            setIsLoading(false);
        });
    }, []);

    // 2. Fetch Stats when Agent or Period changes
    const fetchStats = useCallback(async (agentId: string, period: string) => {
        setIsLoading(true);
        setError(null);
        setStats(null);
        try {
            const data = await siccService.getEvolutionStats(agentId, parseInt(period));
            setStats(data);
        } catch (err) {
            setError((err as Error).message || "Erro ao carregar dados de evolução.");
            toast.error("Erro ao carregar dados de evolução.");
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        if (selectedAgentId) {
            fetchStats(selectedAgentId, selectedPeriod);
        }
    }, [selectedAgentId, selectedPeriod, fetchStats]);

    const selectedAgent = useMemo(() => agents.find(a => a.id === selectedAgentId), [agents, selectedAgentId]);

    // --- Components ---

    const MetricCard: React.FC<{ title: string, value: string | number, change: number, icon: React.ElementType, unit?: string }> = ({ title, value, change, icon: Icon, unit = '' }) => {
        const isPositive = change >= 0;
        const ChangeIcon = isPositive ? TrendingUp : TrendingDown;
        
        return (
            <Card className="border-l-4 border-indigo-600 dark:border-purple-600">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium text-muted-foreground flex items-center">
                        <Icon className="h-4 w-4 mr-2 text-purple-600 dark:text-indigo-400" />
                        {title}
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="text-3xl font-bold text-purple-600 dark:text-white">{value}{unit}</div>
                    <p className={cn("text-xs mt-1 flex items-center", isPositive ? 'text-cyan-500' : 'text-red-500')}>
                        <ChangeIcon className="h-3 w-3 mr-1" />
                        {Math.abs(change)}% vs. {selectedPeriod} dias anteriores
                    </p>
                </CardContent>
            </Card>
        );
    };

    const ActivityItem: React.FC<{ activity: RecentActivity }> = ({ activity }) => {
        const timeAgo = formatDistanceToNow(new Date(activity.timestamp), { addSuffix: true, locale: ptBR });
        
        let icon: React.ReactNode;
        let colorClass: string;
        let badgeText: string;

        switch (activity.type) {
            case 'memory':
                icon = <Brain className="h-4 w-4 text-purple-600" />;
                colorClass = 'border-purple-600';
                badgeText = activity.metadata.layer || 'Memória';
                break;
            case 'pattern':
                icon = <Zap className="h-4 w-4 text-cyan-500" />;
                colorClass = 'border-cyan-500';
                badgeText = `Conf: ${(activity.metadata.confidence! * 100).toFixed(0)}%`;
                break;
            case 'consolidation':
                icon = <Activity className="h-4 w-4 text-indigo-600" />;
                colorClass = 'border-indigo-600';
                badgeText = 'Consolidação';
                break;
        }

        return (
            <div className="flex items-start space-x-3 p-3 border-b dark:border-gray-800 last:border-b-0">
                <div className={cn("p-2 rounded-full border-2 flex-shrink-0", colorClass)}>
                    {icon}
                </div>
                <div className="flex-grow">
                    <p className="text-sm font-medium">{activity.description}</p>
                    <div className="flex items-center space-x-2 text-xs text-muted-foreground mt-1">
                        <Clock className="h-3 w-3" />
                        <span>{timeAgo}</span>
                        <Badge variant="secondary" className="bg-gray-200 dark:bg-gray-700 text-xs">{badgeText}</Badge>
                    </div>
                </div>
            </div>
        );
    };

    // --- Render Logic ---

    if (error) {
        return (
            <DashboardLayout>
                <div className="text-center p-12 bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 rounded-lg">
                    <XCircle className="h-10 w-10 mx-auto text-red-600 mb-4" />
                    <h3 className="text-xl font-bold text-red-600">Erro de Carregamento</h3>
                    <p className="text-red-500 mt-2">{error}</p>
                </div>
            </DashboardLayout>
        );
    }
    
    const renderContent = () => {
        if (isLoading) {
            return (
                <div className="space-y-6">
                    <div className="grid gap-4 md:grid-cols-4">
                        {[1, 2, 3, 4].map(i => <Skeleton key={i} className="h-32 w-full" />)}
                    </div>
                    <div className="grid gap-6 lg:grid-cols-2">
                        <Skeleton className="h-[350px] w-full" />
                        <Skeleton className="h-[350px] w-full" />
                    </div>
                    <Skeleton className="h-[300px] w-full" />
                </div>
            );
        }

        if (!stats) {
            return (
                <div className="text-center p-12 border-2 border-dashed rounded-lg">
                    <Brain className="h-10 w-10 mx-auto text-muted-foreground mb-4" />
                    <p className="text-lg text-muted-foreground">Nenhum dado de evolução encontrado para o agente selecionado.</p>
                </div>
            );
        }

        return (
            <div className="space-y-8">
                {/* Métricas Principais */}
                <div className="grid gap-4 md:grid-cols-4">
                    <MetricCard 
                        title="Total de Memórias" 
                        value={stats.total_memories.toLocaleString()} 
                        change={stats.total_memories_change} 
                        icon={Brain} 
                    />
                    <MetricCard 
                        title="Aprovados Auto" 
                        value={stats.auto_approved_rate.toFixed(1)} 
                        change={stats.auto_approved_rate_change} 
                        icon={CheckCircle} 
                        unit="%"
                    />
                    <MetricCard 
                        title="Taxa de Sucesso" 
                        value={stats.success_rate.toFixed(1)} 
                        change={stats.success_rate_change} 
                        icon={TrendingUp} 
                        unit="%"
                    />
                    <MetricCard 
                        title="Velocidade Aprendizado" 
                        value={stats.learning_velocity.toFixed(1)} 
                        change={stats.learning_velocity_change} 
                        icon={Zap} 
                        unit="/dia"
                    />
                </div>

                {/* Gráficos */}
                <div className="grid gap-6 lg:grid-cols-2">
                    <Card>
                        <CardHeader><CardTitle className="text-xl flex items-center text-purple-600"><Brain className="h-5 w-5 mr-2" /> Crescimento de Memórias</CardTitle></CardHeader>
                        <CardContent>
                            <LineChart 
                                data={stats.memory_growth.map(d => ({...d, date: d.date.substring(5)}))}
                                dataKey="count"
                                lineColor="#4e4ea8"
                                title="Memórias"
                            />
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader><CardTitle className="text-xl flex items-center text-indigo-600"><TrendingUp className="h-5 w-5 mr-2" /> Taxa de Sucesso</CardTitle></CardHeader>
                        <CardContent>
                            <AreaChart 
                                data={stats.success_trend.map(d => ({...d, date: d.date.substring(5)}))}
                                dataKey="rate"
                                areaColor="#0ca7d2"
                                title="Taxa de Sucesso"
                                unit="%"
                            />
                        </CardContent>
                    </Card>
                </div>

                {/* Atividade Recente */}
                <Card>
                    <CardHeader><CardTitle className="text-xl flex items-center text-cyan-500"><Activity className="h-5 w-5 mr-2" /> Atividade Recente</CardTitle></CardHeader>
                    <CardContent className="p-0">
                        {stats.recent_activity.slice(0, 10).map((activity, index) => (
                            <ActivityItem key={index} activity={activity} />
                        ))}
                    </CardContent>
                </Card>
            </div>
        );
    };

    return (
        <DashboardLayout>
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold flex items-center text-purple-600 dark:text-white">
                    <TrendingUp className="h-7 w-7 mr-3" />
                    Evolução do Agente
                </h2>
                <div className="flex space-x-4">
                    {/* Select Agente */}
                    <Select value={selectedAgentId} onValueChange={setSelectedAgentId} disabled={isLoading || agents.length === 0}>
                        <SelectTrigger className="w-[200px] bg-white dark:bg-gray-800 border-indigo-600 dark:border-purple-600">
                            <Users className="h-4 w-4 mr-2 text-indigo-600" />
                            <SelectValue placeholder="Selecione o Agente" />
                        </SelectTrigger>
                        <SelectContent>
                            {agents.map(agent => (
                                <SelectItem key={agent.id} value={agent.id}>{agent.name}</SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                    
                    {/* Select Período */}
                    <Select value={selectedPeriod} onValueChange={setSelectedPeriod} disabled={isLoading}>
                        <SelectTrigger className="w-[150px]">
                            <Clock className="h-4 w-4 mr-2" />
                            <SelectValue placeholder="Período" />
                        </SelectTrigger>
                        <SelectContent>
                            {PERIOD_OPTIONS.map(option => (
                                <SelectItem key={option.value} value={option.value}>{option.label}</SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                </div>
            </div>
            
            <p className="text-muted-foreground mb-8">
                Acompanhe o aprendizado e performance do agente {selectedAgent?.name || 'selecionado'} ao longo do tempo.
            </p>

            {renderContent()}
        </DashboardLayout>
    );
};

export default EvolutionPage;