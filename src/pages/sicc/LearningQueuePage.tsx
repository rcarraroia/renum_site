import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { siccService } from '@/services/siccService';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Clock, CheckCircle, XCircle, AlertCircle } from 'lucide-react';

export default function LearningQueuePage() {
  const [activeTab, setActiveTab] = useState('pending');
  const [learnings, setLearnings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLearnings();
  }, [activeTab]);

  const loadLearnings = async () => {
    try {
      setLoading(true);
      const data = await siccService.getLearningQueue('37ae9902-24bf-42b1-9d01-88c201ee0a6c', activeTab);
      setLearnings(data.data || []);
    } catch (error) {
      console.error('Erro ao carregar learnings:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold">⏳ Fila de Aprendizados</h1>
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
              <div className="text-2xl font-bold text-orange-600">12</div>
              <Badge variant="secondary" className="mt-1">Aguardando</Badge>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Aprovados</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">89</div>
              <Badge variant="secondary" className="mt-1">Este mês</Badge>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Rejeitados</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">15</div>
              <Badge variant="secondary" className="mt-1">Este mês</Badge>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Taxa Aprovação</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">85.6%</div>
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
                  Pendentes (12)
                </TabsTrigger>
                <TabsTrigger value="approved">
                  <CheckCircle className="h-4 w-4 mr-2" />
                  Aprovados (89)
                </TabsTrigger>
                <TabsTrigger value="rejected">
                  <XCircle className="h-4 w-4 mr-2" />
                  Rejeitados (15)
                </TabsTrigger>
              </TabsList>

              <TabsContent value="pending" className="mt-6">
                <div className="space-y-4">
                  <div className="border rounded-lg p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <Badge variant="secondary">Memória Adicionada</Badge>
                          <Badge variant="outline" className="bg-orange-50 text-orange-700">
                            Confiança: 85%
                          </Badge>
                        </div>
                        <p className="text-sm font-medium mb-1">
                          Criar nova memória sobre política de preços
                        </p>
                        <p className="text-xs text-muted-foreground mb-2">
                          Baseado na conversa #conv_123 • 1 hora atrás
                        </p>
                        <p className="text-xs text-gray-600">
                          <strong>Análise ISA:</strong> Cliente perguntou sobre desconto para grandes volumes. 
                          Sugerindo criar memória com política oficial.
                        </p>
                      </div>
                      <div className="flex space-x-2">
                        <Button size="sm" className="bg-green-600 hover:bg-green-700">
                          Aprovar
                        </Button>
                        <Button size="sm" variant="outline">
                          Rejeitar
                        </Button>
                      </div>
                    </div>
                  </div>

                  <div className="border rounded-lg p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <Badge variant="secondary">Padrão Detectado</Badge>
                          <Badge variant="outline" className="bg-green-50 text-green-700">
                            Confiança: 92%
                          </Badge>
                        </div>
                        <p className="text-sm font-medium mb-1">
                          Aplicar saudação personalizada baseada no histórico
                        </p>
                        <p className="text-xs text-muted-foreground mb-2">
                          Padrão: greeting_personalization • 2 horas atrás
                        </p>
                        <p className="text-xs text-gray-600">
                          <strong>Análise ISA:</strong> Detectado que saudações personalizadas aumentam 
                          engajamento em 78%. Recomendo aplicar automaticamente.
                        </p>
                      </div>
                      <div className="flex space-x-2">
                        <Button size="sm" className="bg-green-600 hover:bg-green-700">
                          Aprovar
                        </Button>
                        <Button size="sm" variant="outline">
                          Rejeitar
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="approved" className="mt-6">
                <div className="text-center py-8 text-muted-foreground">
                  <CheckCircle className="h-12 w-12 mx-auto mb-4 text-green-500" />
                  <p>89 aprendizados aprovados este mês</p>
                  <p className="text-sm">Histórico detalhado será implementado em breve</p>
                </div>
              </TabsContent>

              <TabsContent value="rejected" className="mt-6">
                <div className="text-center py-8 text-muted-foreground">
                  <XCircle className="h-12 w-12 mx-auto mb-4 text-red-500" />
                  <p>15 aprendizados rejeitados este mês</p>
                  <p className="text-sm">Histórico detalhado será implementado em breve</p>
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}