import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Zap, Clock, MessageSquare, TrendingUp } from 'lucide-react';

const AgentOverviewTab: React.FC = () => {
  const metrics = [
    { title: 'Status', value: 'Ativo', icon: Zap, color: 'text-green-500' },
    { title: 'Conversas (24h)', value: '45', icon: MessageSquare, color: 'text-[#0ca7d2]' },
    { title: 'Taxa de Resolução', value: '88%', icon: TrendingUp, color: 'text-[#FF6B35]' },
    { title: 'Latência Média', value: '1.5s', icon: Clock, color: 'text-[#4e4ea8]' },
  ];

  return (
    <div className="space-y-6">
      <h3 className="text-xl font-semibold">Visão Geral do Agente de Vendas Slim</h3>
      <div className="grid gap-4 md:grid-cols-4">
        {metrics.map((metric, index) => (
          <Card key={index}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{metric.title}</CardTitle>
              <metric.icon className={`h-4 w-4 ${metric.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{metric.value}</div>
            </CardContent>
          </Card>
        ))}
      </div>
      <Card>
        <CardHeader><CardTitle>Resumo da Performance</CardTitle></CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            O Agente de Vendas Slim está performando acima da média, com alta taxa de qualificação de leads.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default AgentOverviewTab;