import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Zap, Shield, AlertTriangle, Lock, Clock, TrendingUp, TrendingDown, MessageSquare, Tag, Brain, CheckCircle } from 'lucide-react';
import { MOCK_GUARDRAILS_METRICS, MOCK_INTERVENTION_BREAKDOWN, MOCK_VALIDATOR_BREAKDOWN, MOCK_LATENCY_DATA, MOCK_TOP_BLOCKED_KEYWORDS } from '@/data/mockReports';
import ReportChart from './ReportChart';
import { cn } from '@/lib/utils';
import { Separator } from '@/components/ui/separator';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';

interface GuardrailKPIProps {
    title: string;
    value: string | number;
    change: number;
    icon: React.ElementType;
    color: string;
}

const GuardrailKPI: React.FC<GuardrailKPIProps> = ({ title, value, change, icon: Icon, color }) => {
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
                {typeof change === 'number' && (
                    <p className={cn("text-xs mt-1 flex items-center", isPositive ? 'text-green-500' : 'text-red-500')}>
                        <ChangeIcon className="h-3 w-3 mr-1" />
                        {Math.abs(change)}% vs. período anterior
                    </p>
                )}
            </CardContent>
        </Card>
    );
};

const GuardrailsReportsTab: React.FC = () => {
    const kpis = [
        { title: 'Total de Validações', value: MOCK_GUARDRAILS_METRICS.totalValidations.value, change: MOCK_GUARDRAILS_METRICS.totalValidations.change, icon: Shield, color: 'text-[#4e4ea8]' },
        { title: 'Taxa de Intervenção', value: MOCK_GUARDRAILS_METRICS.interventionRate.value, change: MOCK_GUARDRAILS_METRICS.interventionRate.change, icon: AlertTriangle, color: 'text-red-500' },
        { title: 'Principal Violação', value: MOCK_GUARDRAILS_METRICS.topViolation.value, change: MOCK_GUARDRAILS_METRICS.topViolation.change, icon: Lock, color: 'text-yellow-500' },
        { title: 'Latência Média', value: MOCK_GUARDRAILS_METRICS.avgLatency.value, change: MOCK_GUARDRAILS_METRICS.avgLatency.change, icon: Clock, color: 'text-green-500' },
    ];

    const totalInterventions = MOCK_INTERVENTION_BREAKDOWN.reduce((sum, item) => sum + item.value, 0);

    return (
        <div className="space-y-8">
            <h3 className="text-2xl font-bold flex items-center text-[#4e4ea8]">
                <Shield className="h-6 w-6 mr-2" /> Performance dos Guardrails
            </h3>
            <p className="text-muted-foreground">Monitoramento detalhado das políticas de segurança e filtragem do Renus.</p>

            {/* KPIs */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                {kpis.map((kpi, index) => (
                    <GuardrailKPI key={index} {...kpi} />
                ))}
            </div>

            {/* Charts: Breakdown & Latency */}
            <div className="grid gap-8 lg:grid-cols-3">
                <ReportChart
                    title="Intervenções por Tipo de Ação"
                    description="Bloqueio, Sanitização e Alerta."
                    data={MOCK_INTERVENTION_BREAKDOWN}
                    type="donut"
                    dataKeys={[]}
                    className="lg:col-span-1"
                />
                <ReportChart
                    title="Latência de Validação (Média vs. P95)"
                    description="Tempo de processamento dos validadores por hora."
                    data={MOCK_LATENCY_DATA}
                    type="line"
                    dataKeys={[
                        { key: 'avg', color: '#4e4ea8', name: 'Média (ms)' },
                        { key: 'p95', color: '#FF6B35', name: 'P95 (ms)' },
                    ]}
                    className="lg:col-span-2"
                />
            </div>

            {/* Validator Breakdown & Insights */}
            <div className="grid gap-8 lg:grid-cols-3">
                <ReportChart
                    title="Violações por Validador"
                    description="Quais validadores estão sendo mais acionados."
                    data={MOCK_VALIDATOR_BREAKDOWN}
                    type="bar"
                    dataKeys={[{ key: 'count', color: '#0ca7d2', name: 'Contagem' }]}
                    className="lg:col-span-2"
                />
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center text-[#FF6B35]">
                            <Tag className="h-5 w-5 mr-2" /> Insights de Segurança
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <h4 className="font-semibold text-sm">Top Palavras Bloqueadas (Últimos 30 dias)</h4>
                            <ul className="space-y-1 text-sm">
                                {MOCK_TOP_BLOCKED_KEYWORDS.map((item, index) => (
                                    <li key={index} className="flex justify-between items-center p-2 bg-gray-50 dark:bg-gray-800 rounded">
                                        <Badge variant="secondary">{item.keyword}</Badge>
                                        <span className="font-mono text-muted-foreground">{item.count}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                        <Separator />
                        <div className="space-y-2">
                            <h4 className="font-semibold text-sm flex items-center"><Brain className="h-4 w-4 mr-2" /> Taxa de Continuação</h4>
                            <p className="text-xs text-muted-foreground">Conversas que continuaram após uma intervenção de Guardrail.</p>
                            <div className="flex justify-between text-lg font-bold text-green-500">
                                <span>78%</span>
                                <CheckCircle className="h-5 w-5" />
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

export default GuardrailsReportsTab;