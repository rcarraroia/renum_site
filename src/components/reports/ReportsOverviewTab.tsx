import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Zap, Briefcase, Users, MessageSquare, Clock, CheckCircle, TrendingUp, TrendingDown, Shield, AlertTriangle } from 'lucide-react';
// Mock data (local fallback)
const MOCK_KPI_DATA = {
  totalProjects: 24,
  activeClients: 18,
  totalConversations: 1542,
  avgResponseTime: 1.8
};

const MOCK_PROJECT_STATUS_DATA = [
  { name: 'Ativo', value: 45, color: '#00D4AA' },
  { name: 'Em Desenvolvimento', value: 30, color: '#FF6B35' },
  { name: 'Pausado', value: 15, color: '#FFA500' },
  { name: 'Concluído', value: 10, color: '#4e4ea8' }
];

const MOCK_PROJECT_TYPE_DATA = [
  { name: 'AI Native', value: 45, color: '#4e4ea8' },
  { name: 'Workflow', value: 30, color: '#FF6B35' },
  { name: 'Agente Solo', value: 25, color: '#00D4AA' }
];

const MOCK_CONVERSATION_CHANNEL_DATA = [
  { name: 'WhatsApp', value: 60, color: '#25D366' },
  { name: 'SMS', value: 25, color: '#FF6B35' },
  { name: 'Email', value: 15, color: '#4e4ea8' }
];

const MOCK_ACTIVITY_TIMELINE = [
  { time: '00:00', messages: 45 },
  { time: '04:00', messages: 12 },
  { time: '08:00', messages: 89 },
  { time: '12:00', messages: 156 },
  { time: '16:00', messages: 134 },
  { time: '20:00', messages: 98 }
];

const MOCK_GUARDRAILS_METRICS = {
  totalChecks: 8420,
  blocked: 156,
  warnings: 89,
  passed: 8175
};
import ReportChart from './ReportChart';
import { cn } from '@/lib/utils';
import { Separator } from '@/components/ui/separator';

interface KPIProps {
    title: string;
    value: string | number;
    change: number;
    icon: React.ElementType;
    color: string;
}

const KPI: React.FC<KPIProps> = ({ title, value, change, icon: Icon, color }) => {
    const isPositive = change >= 0;
    const ChangeIcon = isPositive ? TrendingUp : TrendingDown;

    return (
        <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{title}</CardTitle>
                <Icon className={cn("h-4 w-4", color)} />
            </CardHeader>
            <CardContent>
                <div className="text-2xl font-bold">{value}</div>
                <p className={cn("text-xs mt-1 flex items-center", isPositive ? 'text-green-500' : 'text-red-500')}>
                    <ChangeIcon className="h-3 w-3 mr-1" />
                    {Math.abs(change)}% vs. período anterior
                </p>
            </CardContent>
        </Card>
    );
};

const ReportsOverviewTab: React.FC = () => {
    const kpis = [
        { title: 'Total de Projetos', value: MOCK_KPI_DATA.totalProjects.value, change: MOCK_KPI_DATA.totalProjects.change, icon: Briefcase, color: 'text-[#4e4ea8]' },
        { title: 'Clientes Ativos', value: MOCK_KPI_DATA.activeClients.value, change: MOCK_KPI_DATA.activeClients.change, icon: Users, color: 'text-[#0ca7d2]' },
        { title: 'Novos Leads', value: MOCK_KPI_DATA.newLeads.value, change: MOCK_KPI_DATA.newLeads.change, icon: Zap, color: 'text-[#FF6B35]' },
        { title: 'Vol. Conversas', value: MOCK_KPI_DATA.conversationVolume.value, change: MOCK_KPI_DATA.conversationVolume.change, icon: MessageSquare, color: 'text-purple-500' },
        { title: 'Taxa Intervenção GR', value: MOCK_GUARDRAILS_METRICS.interventionRate.value, change: MOCK_GUARDRAILS_METRICS.interventionRate.change, icon: Shield, color: 'text-red-500' },
        { title: 'Taxa de Conclusão', value: MOCK_KPI_DATA.completionRate.value, change: MOCK_KPI_DATA.completionRate.change, icon: CheckCircle, color: 'text-green-500' },
    ];

    const recentActivity = [
        { time: '10 min atrás', description: 'Novo lead "Health Clinic Pro" iniciado conversa via WhatsApp.' },
        { time: '1h atrás', description: 'Projeto "Qualificação de Leads" atingiu 75% de progresso.' },
        { time: 'Ontem', description: 'Relatório de Viabilidade gerado para Alpha Solutions.' },
    ];

    return (
        <div className="space-y-8">
            {/* KPIs */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
                {kpis.map((kpi, index) => (
                    <KPI key={index} {...kpi} value={String(kpi.value)} />
                ))}
            </div>

            {/* Charts */}
            <div className="grid gap-8 lg:grid-cols-3">
                <div className="lg:col-span-2">
                    <ReportChart
                        title="Atividade Semanal (Projetos vs. Conversas)"
                        description="Tendência de volume de trabalho nos últimos 7 dias."
                        data={MOCK_ACTIVITY_TIMELINE}
                        type="line"
                        dataKeys={[
                            { key: 'projects', color: '#4e4ea8', name: 'Projetos Iniciados' },
                            { key: 'conversations', color: '#FF6B35', name: 'Conversas' },
                        ]}
                    />
                </div>
                <ReportChart
                    title="Conversas por Canal"
                    description="Distribuição das interações do Renus."
                    data={MOCK_CONVERSATION_CHANNEL_DATA}
                    type="pie"
                    dataKeys={[]} // Pie chart uses data.fill
                />
            </div>

            <div className="grid gap-8 lg:grid-cols-3">
                <ReportChart
                    title="Projetos por Status"
                    description="Visão geral do pipeline de desenvolvimento."
                    data={MOCK_PROJECT_STATUS_DATA}
                    type="donut"
                    dataKeys={[]}
                />
                <ReportChart
                    title="Projetos por Tipo"
                    description="Distribuição das soluções entregues."
                    data={MOCK_PROJECT_TYPE_DATA}
                    type="bar"
                    dataKeys={[{ key: 'count', color: '#0ca7d2', name: 'Contagem' }]}
                />
                <Card>
                    <CardHeader>
                        <CardTitle>Feed de Atividades Recentes</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                        {recentActivity.map((activity, index) => (
                            <div key={index} className="flex items-start space-x-3">
                                <Clock className="h-4 w-4 flex-shrink-0 mt-1 text-muted-foreground" />
                                <div>
                                    <p className="text-sm">{activity.description}</p>
                                    <p className="text-xs text-muted-foreground">{activity.time}</p>
                                </div>
                            </div>
                        ))}
                        <Separator />
                        <p className="text-xs text-[#4e4ea8] cursor-pointer hover:underline">Ver todas as atividades</p>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

export default ReportsOverviewTab;