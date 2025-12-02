import React from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Zap, Users, Briefcase, MessageSquare } from 'lucide-react';

const AdminOverview: React.FC = () => {
  const metrics = [
    { title: 'Projetos Ativos', value: '12', icon: Briefcase, color: 'text-[#4e4ea8]' },
    { title: 'Novos Leads', value: '4', icon: Users, color: 'text-[#FF6B35]' },
    { title: 'Conversas Ativas', value: '35', icon: MessageSquare, color: 'text-[#0ca7d2]' },
    { title: 'ROI Médio', value: '+30%', icon: Zap, color: 'text-green-500' },
  ];

  return (
    <DashboardLayout>
      <h2 className="text-3xl font-bold mb-6">Visão Geral do Administrador</h2>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-8">
        {metrics.map((metric, index) => (
          <Card key={index}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{metric.title}</CardTitle>
              <metric.icon className={`h-4 w-4 ${metric.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{metric.value}</div>
              <p className="text-xs text-muted-foreground mt-1">Últimos 30 dias</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Status dos Projetos (Mock Chart)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64 flex items-center justify-center text-muted-foreground">
              Gráfico de Status de Projetos
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Atividades Recentes</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3 text-sm">
              <li>[10:30] Novo cliente 'Alpha' adicionado.</li>
              <li>[09:45] Projeto 'MMN Flow' atualizado para 'Design'.</li>
              <li>[Ontem] Renus Config: Nova ferramenta 'CRM Sync' criada.</li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default AdminOverview;