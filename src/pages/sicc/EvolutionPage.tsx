import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { siccService } from '@/services/siccService';
import { agentService } from '@/services/agentService';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { TrendingUp, Brain, Activity, Zap, ArrowLeft } from 'lucide-react';

export default function EvolutionPage() {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [agent, setAgent] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const init = async () => {
      if (!slug) {
        setError('Slug do agente não fornecido');
        setLoading(false);
        return;
      }
      
      try {
        // Busca agente pelo slug da URL
        const agentData = await agentService.getAgentBySlug(slug);
        if (agentData) {
          setAgent(agentData);
          loadStats(agentData.id);
        } else {
          setError(`Agente "${slug}" não encontrado`);
          setLoading(false);
        }
      } catch (error) {
        console.error('Error fetching agent:', error);
        setError('Erro ao carregar agente');
        setLoading(false);
      }
    };
    init();
  }, [slug]);

  const loadStats = async (id: string) => {
    try {
      setLoading(true);
      const data = await siccService.getEvolutionStats(id);
      setStats(data);
    } catch (error) {
      console.error('Erro ao carregar stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="p-6 flex justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="p-6">
          <div className="text-center py-12">
            <p className="text-red-500 mb-4">{error}</p>
            <Button onClick={() => navigate('/dashboard/admin/agents')}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Voltar para Agentes
            </Button>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            {/* Bug #3 - Corrigido: Voltar para aba Inteligência */}
            <Button variant="ghost" size="sm" onClick={() => navigate(`/dashboard/admin/agents/${slug}?tab=intelligence`)}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Voltar
            </Button>
            <div>
              <h1 className="text-3xl font-bold">📈 Evolução do Agente</h1>
              <p className="text-muted-foreground">{agent?.name || slug}</p>
            </div>
          </div>
          <Badge variant="secondary" className="bg-purple-100 text-purple-800">
            SICC v1.0 {agent ? '(Conectado)' : '(Desconectado)'}
          </Badge>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Memórias</CardTitle>
              <Brain className="h-4 w-4 text-purple-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.total_memories || 0}</div>
              <p className="text-xs text-muted-foreground">
                <TrendingUp className="inline h-3 w-3 mr-1" />
                {stats?.total_memories_change > 0 ? '+' : ''}{stats?.total_memories_change || 0}% este mês
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Taxa Aprovação</CardTitle>
              <Activity className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.auto_approved_rate || 0}%</div>
              <p className="text-xs text-muted-foreground">
                <TrendingUp className="inline h-3 w-3 mr-1" />
                {stats?.auto_approved_rate_change > 0 ? '+' : ''}{stats?.auto_approved_rate_change || 0}% este mês
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Taxa Sucesso</CardTitle>
              <Zap className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.success_rate || 0}%</div>
              <p className="text-xs text-muted-foreground">
                <TrendingUp className="inline h-3 w-3 mr-1" />
                {stats?.success_rate_change > 0 ? '+' : ''}{stats?.success_rate_change || 0}% este mês
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Velocidade</CardTitle>
              <Activity className="h-4 w-4 text-orange-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.learning_velocity || 0}</div>
              <p className="text-xs text-muted-foreground">
                <TrendingUp className="inline h-3 w-3 mr-1" />
                {stats?.learning_velocity_change > 0 ? '+' : ''}{stats?.learning_velocity_change || 0} aprendizados/dia
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>📊 Crescimento de Memórias</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-[200px] flex items-center justify-center text-muted-foreground">
                {/* Placeholder para gráfico real - Dados viriam de stats.memory_growth */}
                {(!stats?.memory_growth || stats?.memory_growth.length === 0)
                  ? "Sem dados suficientes para gerar gráfico"
                  : "Gráfico carregado (Visualização pendente)"}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>🎯 Atividades Recentes</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {(!stats?.recent_activity || stats?.recent_activity.length === 0) ? (
                  <p className="text-sm text-muted-foreground">Nenhuma atividade recente registrada.</p>
                ) : (
                  stats.recent_activity.map((activity: any, index: number) => (
                    <div key={index} className="flex items-center space-x-3">
                      <div className={`w-2 h-2 rounded-full ${activity.type === 'memory' ? 'bg-green-500' :
                          activity.type === 'learning' ? 'bg-blue-500' : 'bg-gray-500'
                        }`}></div>
                      <div className="flex-1">
                        <p className="text-sm font-medium">{activity.description}</p>
                        <p className="text-xs text-muted-foreground">{new Date(activity.timestamp).toLocaleString()}</p>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}