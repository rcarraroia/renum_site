import React, { useEffect, useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Zap, Users, Briefcase, MessageSquare } from 'lucide-react';
import { dashboardService, DashboardStats } from '@/services/dashboardService';
import { Loader2 } from 'lucide-react';
import ReportChart from '@/components/reports/ReportChart';

const AdminOverview: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        const data = await dashboardService.getStats();
        setStats(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching dashboard stats:', err);
        setError('Erro ao carregar estatísticas');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      </DashboardLayout>
    );
  }

  if (error || !stats) {
    return (
      <DashboardLayout>
        <div className="text-center text-red-500 p-4">
          {error || 'Erro ao carregar dados'}
        </div>
      </DashboardLayout>
    );
  }

  const metrics = [
    { title: 'Total de Clientes', value: stats.total_clients.toString(), icon: Users, color: 'text-[#4e4ea8]' },
    { title: 'Projetos Iniciais', value: stats.active_interviews.toString(), icon: Briefcase, color: 'text-[#FF6B35]' },
    { title: 'Conversas Ativas', value: stats.total_conversations.toString(), icon: MessageSquare, color: 'text-[#0ca7d2]' },
    { title: 'Taxa de Sucesso', value: `${stats.completion_rate.toFixed(0)}%`, icon: Zap, color: 'text-green-500' },
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
        <div className="lg:col-span-2">
          <ReportChart
            title="Status dos Projetos"
            description="Distribuição atual de todos os fluxos de prospecção"
            data={stats.project_status_distribution}
            type="donut"
            dataKeys={[]}
          />
        </div>
        <Card>
          <CardHeader>
            <CardTitle>Atividades Recentes</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3 text-sm">
              {stats.recent_activities.length > 0 ? (
                stats.recent_activities.slice(0, 5).map((activity, index) => (
                  <li key={index}>
                    [{new Date(activity.timestamp).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}] {activity.details}
                  </li>
                ))
              ) : (
                <li className="text-muted-foreground">Nenhuma atividade recente</li>
              )}
            </ul>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default AdminOverview;