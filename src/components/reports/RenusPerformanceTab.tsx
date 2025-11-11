import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Zap, MessageSquare, Clock, CheckCircle, Smile, Brain, Shield, TrendingUp } from 'lucide-react';
import { MOCK_RENUS_METRICS, MOCK_INTENT_BREAKDOWN, MOCK_GUARDRAILS_STATS } from '@/data/mockReports';
import ReportChart from './ReportChart';
import { cn } from '@/lib/utils';
import { Separator } from '@/components/ui/separator';
import { Progress } from '@/components/ui/progress';

interface RenusKPIProps {
    title: string;
    value: string | number;
    icon: React.ElementType;
    color: string;
}

const RenusKPI: React.FC<RenusKPIProps> = ({ title, value, icon: Icon, color }) => (
    <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{title}</CardTitle>
            <Icon className={cn("h-4 w-4", color)} />
        </CardHeader>
        <CardContent>
            <div className="text-2xl font-bold">{value}</div>
        </CardContent>
    </Card>
);

const RenusPerformanceTab: React.FC = () => {
    const kpis = [
        { title: 'Total de Conversas', value: MOCK_RENUS_METRICS.totalConversations, icon: MessageSquare, color: 'text-[#4e4ea8]' },
        { title: 'Taxa de Resolução', value: MOCK_RENUS_METRICS.resolutionRate, icon: CheckCircle, color: 'text-green-500' },
        { title: 'Duração Média', value: MOCK_RENUS_METRICS.avgLength, icon: Clock, color: 'text-yellow-500' },
        { title: 'Satisfação do Usuário', value: MOCK_RENUS_METRICS.userSatisfaction, icon: Smile, color: 'text-[#FF6B35]' },
    ];

    const performanceOverTime = [
        { month: 'Jul', resolution: 60, satisfaction: 3.8 },
        { month: 'Ago', resolution: 70, satisfaction: 4.0 },
        { month: 'Set', resolution: 75, satisfaction: 4.2 },
        { month: 'Out', resolution: 80, satisfaction: 4.5 },
    ];

    return (
        <div className="space-y-8">
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                {kpis.map((kpi, index) => (
                    <RenusKPI key={index} {...kpi} />
                ))}
            </div>

            <div className="grid gap-8 lg:grid-cols-3">
                <div className="lg:col-span-2">
                    <ReportChart
                        title="Resolução e Satisfação ao Longo do Tempo"
                        description="Acompanhamento mensal da performance do Renus."
                        data={performanceOverTime}
                        type="line"
                        dataKeys={[
                            { key: 'resolution', color: '#4e4ea8', name: 'Resolução (%)' },
                            { key: 'satisfaction', color: '#FF6B35', name: 'Satisfação (Escala 5)' },
                        ]}
                    />
                </div>
                <ReportChart
                    title="Classificação de Intenções"
                    description="Distribuição dos tópicos mais abordados."
                    data={MOCK_INTENT_BREAKDOWN}
                    type="donut"
                    dataKeys={[]}
                />
            </div>

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center text-red-500">
                        <Shield className="h-5 w-5 mr-2" /> Estatísticas de Guardrails
                    </CardTitle>
                    <p className="text-sm text-muted-foreground">Monitoramento de tentativas de desvio e conteúdo bloqueado.</p>
                </CardHeader>
                <CardContent className="space-y-4">
                    {MOCK_GUARDRAILS_STATS.map((stat, index) => (
                        <div key={index} className="space-y-1">
                            <div className="flex justify-between text-sm font-medium">
                                <span>{stat.reason}</span>
                                <span>{stat.count} Bloqueios</span>
                            </div>
                            <Progress value={stat.count * 10} className="h-2 [&>div]:bg-red-500" />
                        </div>
                    ))}
                    <Separator />
                    <div className="flex justify-between text-sm text-muted-foreground">
                        <span>Taxa de Detecção:</span>
                        <span className="font-semibold text-green-500">98.5%</span>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};

export default RenusPerformanceTab;