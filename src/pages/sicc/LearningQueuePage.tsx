import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { siccService } from '@/services/siccService';
import { agentService } from '@/services/agentService';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Clock, CheckCircle, XCircle, AlertCircle, ArrowLeft } from 'lucide-react';

export default function LearningQueuePage() {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('pending');
  const [learnings, setLearnings] = useState<any[]>([]);
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

  useEffect(() => {
    if (agent?.id) {
      loadLearnings(agent.id);
    }
  }, [agent?.id, activeTab]);

  const loadLearnings = async (id: string) => {
    try {
      setLoading(true);
      const data: any = await siccService.getLearningQueue(id, activeTab);
      setLearnings(Array.isArray(data) ? data : (data?.items || []));
    } catch (error) {
      console.error('Erro ao carregar learnings:', error);
      setLearnings([]);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (learningId: string) => {
    if (!agent?.id) return;
    try {
      await siccService.approveLearning(learningId);
      loadLearnings(agent.id);
    } catch (error) {
      console.error('Erro ao aprovar:', error);
    }
  };

  const handleReject = async (learningId: string) => {
    if (!agent?.id) return;
    try {
      await siccService.rejectLearning(learningId, 'Rejeitado manualmente pelo administrador');
      loadLearnings(agent.id);
    } catch (error) {
      console.error('Erro ao rejeitar:', error);
    }
  };

  if (loading && !agent) {
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
              <h1 className="text-3xl font-bold">⏳ Fila de Aprendizados</h1>
              <p className="text-muted-foreground">{agent?.name || slug}</p>
            </div>
          </div>
          <div className="flex space-x-2">
            <Button variant="outline" size="sm">
              Aprovar Selecionados
            </Button>
            <Button variant="outline" size="sm">
              Rejeitar Selecionados
            </Button>
          </div>
        </div>

        <div className="grid gap-6 md:grid-cols-4 mb-6">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Pendentes</CardTitle>
            </CardHeader>
            <CardContent>
              {/* These counts should be real stats, but for now using list length if tab is pending */}
              <div className="text-2xl font-bold text-orange-600">
                {activeTab === 'pending' ? learnings.length : '-'}
              </div>
              <Badge variant="secondary" className="mt-1">Aguardando</Badge>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Aprovados</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">
                {activeTab === 'approved' ? learnings.length : '-'}
              </div>
              <Badge variant="secondary" className="mt-1">Este mês</Badge>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Rejeitados</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">
                {activeTab === 'rejected' ? learnings.length : '-'}
              </div>
              <Badge variant="secondary" className="mt-1">Este mês</Badge>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Taxa Aprovação</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">-</div>
              <Badge variant="secondary" className="mt-1">Média</Badge>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>📋 Aprendizados por Status</CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="pending">
                  <Clock className="h-4 w-4 mr-2" />
                  Pendentes
                </TabsTrigger>
                <TabsTrigger value="approved">
                  <CheckCircle className="h-4 w-4 mr-2" />
                  Aprovados
                </TabsTrigger>
                <TabsTrigger value="rejected">
                  <XCircle className="h-4 w-4 mr-2" />
                  Rejeitados
                </TabsTrigger>
              </TabsList>

              <div className="mt-6">
                {loading ? (
                  <div className="p-4 flex justify-center">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-purple-600"></div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {learnings.length === 0 ? (
                      <div className="text-center py-8 text-muted-foreground border border-dashed rounded-lg">
                        <AlertCircle className="h-12 w-12 mx-auto mb-3 opacity-20" />
                        <p>Nenhum aprendizado encontrado nesta categoria.</p>
                      </div>
                    ) : (
                      learnings.map((learning: any) => (
                        <div key={learning.id} className="border rounded-lg p-4">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <div className="flex items-center space-x-2 mb-2">
                                <Badge variant="secondary">{learning.source_type || 'Desconhecido'}</Badge>
                                <Badge variant="outline" className="bg-orange-50 text-orange-700">
                                  Confiança: {(learning.confidence * 100).toFixed(0)}%
                                </Badge>
                              </div>
                              <p className="text-sm font-medium mb-1">
                                {learning.description || learning.content}
                              </p>
                              <p className="text-xs text-muted-foreground mb-2">
                                {learning.source_id ? `Origem: ${learning.source_id}` : ''} • {new Date(learning.created_at).toLocaleString()}
                              </p>
                              {learning.analysis && (
                                <p className="text-xs text-gray-600">
                                  <strong>Análise ISA:</strong> {
                                    typeof learning.analysis === 'string' 
                                      ? learning.analysis 
                                      : learning.analysis.suggestion || JSON.stringify(learning.analysis)
                                  }
                                </p>
                              )}
                            </div>
                            {activeTab === 'pending' && (
                              <div className="flex space-x-2">
                                <Button size="sm" className="bg-green-600 hover:bg-green-700" onClick={() => handleApprove(learning.id)}>
                                  Aprovar
                                </Button>
                                <Button size="sm" variant="outline" onClick={() => handleReject(learning.id)}>
                                  Rejeitar
                                </Button>
                              </div>
                            )}
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                )}
              </div>
            </Tabs>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}