import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { siccService } from '@/services/siccService';
import { agentService } from '@/services/agentService';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Brain, Search, Plus, Filter, FileText, Lightbulb, BookOpen } from 'lucide-react';

export default function MemoryManagerPage() {
  const [memories, setMemories] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [agentId, setAgentId] = useState<string | null>(null);

  useEffect(() => {
    const init = async () => {
      try {
        const agent = await agentService.getSystemAgent('system_orchestrator');
        if (agent) {
          setAgentId(agent.id);
          loadMemories(agent.id);
        } else {
          setLoading(false);
        }
      } catch (error) {
        console.error('Error fetching system agent:', error);
        setLoading(false);
      }
    };
    init();
  }, []);

  const loadMemories = async (id: string) => {
    try {
      setLoading(true);
      const data = await siccService.listMemories(id);
      // Backend returns { items: [], total: 0 } or just []? 
      // Based on usual patterns, let's assume array or check structure.
      // SICC service usually returns 'data' from axios, which might be the array itself or paginated.
      // Assuming array for now based on service refactor.
      setMemories(Array.isArray(data) ? data : (data.items || []));
    } catch (error) {
      console.error('Erro ao carregar memórias:', error);
      setMemories([]);
    } finally {
      setLoading(false);
    }
  };

  const getMemoryIcon = (type: string) => {
    switch (type?.toLowerCase()) {
      case 'faq': return <FileText className="h-4 w-4" />;
      case 'strategy': return <Lightbulb className="h-4 w-4" />;
      case 'business_term': return <BookOpen className="h-4 w-4" />;
      default: return <Brain className="h-4 w-4" />;
    }
  };

  const getTypeLabel = (type: string) => {
    switch (type?.toLowerCase()) {
      case 'faq': return 'FAQ';
      case 'strategy': return 'Estratégia';
      case 'business_term': return 'Termo Negócio';
      default: return 'Geral';
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

  return (
    <DashboardLayout>
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold">🧠 Gerenciador de Memórias</h1>
          <Button className="bg-purple-600 hover:bg-purple-700">
            <Plus className="h-4 w-4 mr-2" />
            Nova Memória
          </Button>
        </div>

        <div className="grid gap-6 md:grid-cols-4 mb-6">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Total Memórias</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{memories.length}</div>
              <Badge variant="secondary" className="mt-1">Ativas</Badge>
            </CardContent>
          </Card>
          {/* Placeholder stats - In a real app we'd compute these or get from stats API */}
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Tipos</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-sm text-muted-foreground">
                Estatísticas detalhadas por tipo serão carregadas aqui.
              </div>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>📋 Lista de Memórias</CardTitle>
              <div className="flex space-x-2">
                <Button variant="outline" size="sm">
                  <Search className="h-4 w-4 mr-2" />
                  Buscar
                </Button>
                <Button variant="outline" size="sm">
                  <Filter className="h-4 w-4 mr-2" />
                  Filtrar
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {memories.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground border border-dashed rounded-lg">
                  <Brain className="h-12 w-12 mx-auto mb-3 opacity-20" />
                  <p>Nenhuma memória encontrada no banco de dados.</p>
                  <p className="text-xs">O agente ainda não aprendeu nada ou o banco foi resetado.</p>
                </div>
              ) : (
                memories.map((memory: any) => (
                  <div key={memory.id} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <Badge variant="secondary" className="flex items-center gap-1">
                            {getMemoryIcon(memory.type)}
                            {getTypeLabel(memory.type)}
                          </Badge>
                          <Badge variant="outline">Confiança: {(memory.confidence * 100).toFixed(0)}%</Badge>
                        </div>
                        <p className="text-sm font-medium mb-1">
                          {memory.content}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          Usado {memory.usage_count || 0} vezes • Criado em {new Date(memory.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      <Button variant="ghost" size="sm">
                        Editar
                      </Button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}