import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, Briefcase, DollarSign, Clock, TrendingUp, Target, ArrowRight } from 'lucide-react';
// Mock data (local fallback)
const MOCK_CLIENT_ACQUISITION = [
  { month: 'Jan', clients: 12, revenue: 45000 },
  { month: 'Fev', clients: 15, revenue: 52000 },
  { month: 'Mar', clients: 18, revenue: 61000 },
  { month: 'Abr', clients: 22, revenue: 78000 },
  { month: 'Mai', clients: 25, revenue: 89000 },
  { month: 'Jun', clients: 28, revenue: 95000 }
];

const MOCK_BUDGET_COMPARISON = [
  { project: 'Agente MMN', planned: 50000, actual: 48000 },
  { project: 'Bot Clínica', planned: 35000, actual: 38000 },
  { project: 'Sistema Vereador', planned: 60000, actual: 55000 }
];

const MOCK_PROJECT_TYPE_DATA = [
  { name: 'AI Native', value: 45, color: '#4e4ea8' },
  { name: 'Workflow', value: 30, color: '#FF6B35' },
  { name: 'Agente Solo', value: 25, color: '#00D4AA' }
];
import ReportChart from './ReportChart';
import { cn } from '@/lib/utils';
import { Separator } from '@/components/ui/separator';
import { Progress } from '@/components/ui/progress';

const ClientProjectReportsTab: React.FC = () => {
    const clientIndustryDistribution = [
        { name: 'Tecnologia', value: 4, fill: '#4e4ea8' },
        { name: 'Saúde', value: 2, fill: '#FF6B35' },
        { name: 'MMN', value: 1, fill: '#0ca7d2' },
        { name: 'Serviços', value: 3, fill: '#10b981' },
    ];

    return (
        <div className="space-y-8">
            <div className="grid gap-8 lg:grid-cols-2">
                <ReportChart
                    title="Aquisição de Clientes e Projetos"
                    description="Novos clientes e projetos iniciados por mês."
                    data={MOCK_CLIENT_ACQUISITION}
                    type="bar"
                    dataKeys={[
                        { key: 'newClients', color: '#4e4ea8', name: 'Novos Clientes' },
                        { key: 'projectsStarted', color: '#FF6B35', name: 'Projetos Iniciados' },
                    ]}
                />
                <ReportChart
                    title="Distribuição de Clientes por Indústria"
                    description="Segmentos de mercado atendidos."
                    data={clientIndustryDistribution}
                    type="pie"
                    dataKeys={[]}
                />
            </div>

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center text-[#4e4ea8]">
                        <DollarSign className="h-5 w-5 mr-2" /> Comparação Orçamento vs. Real
                    </CardTitle>
                    <p className="text-sm text-muted-foreground">Análise de desvio orçamentário dos projetos.</p>
                </CardHeader>
                <CardContent className="space-y-4">
                    {MOCK_BUDGET_COMPARISON.map((comp, index) => {
                        const variance = comp.actual - comp.budget;
                        const variancePercent = (variance / comp.budget) * 100;
                        const isOverBudget = variance > 0;

                        return (
                            <div key={index} className="space-y-1 p-2 border rounded-md dark:border-gray-700">
                                <div className="flex justify-between text-sm font-medium">
                                    <span>Projeto: {comp.project}</span>
                                    <span className={cn(isOverBudget ? 'text-red-500' : 'text-green-500')}>
                                        {variancePercent.toFixed(1)}% ({variance > 0 ? '+' : ''}{variance.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })})
                                    </span>
                                </div>
                                <div className="flex justify-between text-xs text-muted-foreground">
                                    <span>Orçamento: {comp.budget.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</span>
                                    <span>Real: {comp.actual.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</span>
                                </div>
                            </div>
                        );
                    })}
                </CardContent>
            </Card>

            <div className="grid gap-8 lg:grid-cols-2">
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center text-[#FF6B35]">
                            <Target className="h-5 w-5 mr-2" /> Funil de Conversão (Mock)
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="text-center">
                            <p className="text-2xl font-bold text-[#4e4ea8]">100 Leads</p>
                            <ArrowRight className="h-6 w-6 mx-auto my-2 text-muted-foreground" />
                            <p className="text-xl font-semibold text-[#0ca7d2]">25 Prospectos (25%)</p>
                            <ArrowRight className="h-6 w-6 mx-auto my-2 text-muted-foreground" />
                            <p className="text-lg font-medium text-green-500">8 Clientes Ativos (32%)</p>
                        </div>
                    </CardContent>
                </Card>
                <ReportChart
                    title="Projetos por Tipo (Total)"
                    description="Distribuição total de projetos por categoria."
                    data={MOCK_PROJECT_TYPE_DATA}
                    type="bar"
                    dataKeys={[{ key: 'count', color: '#FF6B35', name: 'Contagem' }]}
                />
            </div>
        </div>
    );
};

export default ClientProjectReportsTab;