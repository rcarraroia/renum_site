import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Briefcase, Clock, CheckCircle, FileText, MessageSquare } from 'lucide-react';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { dashboardService, DashboardStats } from '@/services/dashboardService';
import { Loader2 } from 'lucide-react';
import { toast } from 'sonner';

const ClientOverview: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadClientMetrics = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await dashboardService.getClientMetrics();
      setStats(data);
    } catch (err) {
      setError('Erro ao carregar métricas. Tente novamente.');
      console.error('Erro ao carregar métricas:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadClientMetrics();
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex justify-center items-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-[#0ca7d2]" />
          <span className="ml-2 text-muted-foreground">Carregando métricas...</span>
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="text-center py-12">
          <p className="text-red-500 mb-4">{error}</p>
          <Button onClick={loadClientMetrics} variant="outline">
            Tentar Novamente
          </Button>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <h2 className="text-3xl font-bold mb-6">Bem-vindo(a) ao seu Portal</h2>
      
      <div className="grid gap-6 lg:grid-cols-3 mb-8">
        <Card className="lg:col-span-2 border-l-4 border-[#4e4ea8]">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Briefcase className="h-5 w-5 text-[#4e4ea8]" />
              <span>Status do Projeto Atual</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <h3 className="text-xl font-semibold mb-2">Projeto Ativo</h3>
            <p className="text-sm text-muted-foreground mb-4">Status: Em Desenvolvimento</p>
            
            <div className="space-y-2">
              <div className="flex justify-between text-sm font-medium">
                <span>Progresso Geral</span>
                <span>{stats?.completion_rate ? Math.round(stats.completion_rate * 100) : 0}%</span>
              </div>
              <Progress value={stats?.completion_rate ? stats.completion_rate * 100 : 0} className="h-3 bg-gray-200 dark:bg-gray-700 [&>div]:bg-[#FF6B35]" />
            </div>
            
            <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-muted-foreground">Total Leads:</span>
                <span className="ml-2 font-medium">{stats?.total_leads || 0}</span>
              </div>
              <div>
                <span className="text-muted-foreground">Conversas:</span>
                <span className="ml-2 font-medium">{stats?.total_conversations || 0}</span>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Ações Rápidas</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button className="w-full bg-[#FF6B35] hover:bg-[#e55f30]">
              <FileText className="h-4 w-4 mr-2" /> Ver Último Relatório
            </Button>
            <Button variant="outline" className="w-full">
              <MessageSquare className="h-4 w-4 mr-2" /> Contatar Equipe
            </Button>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Entregáveis Recentes</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-3 text-sm">
            <li className="flex items-center justify-between p-2 border rounded">
              <span><CheckCircle className="h-4 w-4 mr-2 inline text-green-500" /> Mockup Frontend V1.0</span>
              <span className="text-xs text-muted-foreground">2 dias atrás</span>
            </li>
            <li className="flex items-center justify-between p-2 border rounded">
              <span><FileText className="h-4 w-4 mr-2 inline text-[#0ca7d2]" /> Documento de Escopo Final</span>
              <span className="text-xs text-muted-foreground">1 semana atrás</span>
            </li>
          </ul>
        </CardContent>
      </Card>
    </DashboardLayout>
  );
};

export default ClientOverview;