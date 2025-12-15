import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { interviewService } from '@/services/interviewService';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from '@/components/ui/select';
import { 
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs';
import { Download, BarChart3, PieChart, TrendingUp, ClipboardList, MessageSquare } from 'lucide-react';
import { cn } from '@/lib/utils';

interface TopicResponse {
  topic: string;
  responses: { answer: string; count: number; percentage: number }[];
}

const PesquisasResultadosPage = () => {
  const [selectedSubagent, setSelectedSubagent] = useState('all');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadResults();
  }, [selectedSubagent]);

  const loadResults = async () => {
    try {
      setLoading(true);
      const data = await interviewService.getAll({ status: 'completed' });
      setResults(data.items);
    } catch (err) {
      setError('Erro ao carregar resultados');
      console.error('Erro:', err);
    } finally {
      setLoading(false);
    }
  };

  // Mock data
  const topicResponses: TopicResponse[] = [
    {
      topic: 'Prospecção',
      responses: [
        { answer: 'Falta de tempo para prospectar', count: 32, percentage: 64 },
        { answer: 'Dificuldade em encontrar leads qualificados', count: 12, percentage: 24 },
        { answer: 'Alto custo de aquisição', count: 6, percentage: 12 }
      ]
    },
    {
      topic: 'Atendimento',
      responses: [
        { answer: 'Responder mesmas perguntas repetidamente', count: 28, percentage: 56 },
        { answer: 'Atendimento fora do horário comercial', count: 15, percentage: 30 },
        { answer: 'Dificuldade em escalar atendimento', count: 7, percentage: 14 }
      ]
    },
    {
      topic: 'Automação',
      responses: [
        { answer: 'FAQ automático 24/7', count: 45, percentage: 90 },
        { answer: 'Qualificação de leads automatizada', count: 38, percentage: 76 },
        { answer: 'Follow-up automatizado', count: 25, percentage: 50 }
      ]
    }
  ];

  const stats = {
    totalRespostas: 150,
    mediaTempoResposta: '4min 30s',
    taxaConclusao: 85,
    topicosCompletos: 5
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <ClipboardList className="h-7 w-7 mr-3 text-[#4e4ea8]" />
            <div>
                <h1 className="text-3xl font-bold text-[#4e4ea8]">Resultados das Pesquisas</h1>
                <p className="text-muted-foreground mt-1">
                  Visualize e analise os dados coletados de forma estruturada
                </p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline">
              <Download className="h-4 w-4 mr-2" />
              Exportar CSV
            </Button>
            <Button variant="outline">
              <Download className="h-4 w-4 mr-2" />
              Exportar Excel
            </Button>
          </div>
        </div>

        {/* Filter */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="flex-1">
                <Select value={selectedSubagent} onValueChange={setSelectedSubagent}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecionar sub-agente" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Todos os sub-agentes</SelectItem>
                    <SelectItem value="mmn">Pesquisa MMN</SelectItem>
                    <SelectItem value="vereadores">Pesquisa Vereadores</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Stats */}
        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Total de Respostas</CardTitle>
              <BarChart3 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.totalRespostas}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Tempo Médio</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.mediaTempoResposta}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Taxa de Conclusão</CardTitle>
              <PieChart className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{stats.taxaConclusao}%</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Tópicos Completos</CardTitle>
              <BarChart3 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.topicosCompletos}/5</div>
            </CardContent>
          </Card>
        </div>

        {/* Respostas por Tópico */}
        <Card>
          <CardHeader>
            <CardTitle>Respostas por Tópico</CardTitle>
            <CardDescription>
              Análise detalhada das respostas organizadas por tópico
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue={topicResponses[0].topic} className="w-full">
              <TabsList className="grid w-full grid-cols-3">
                {topicResponses.map((topic) => (
                  <TabsTrigger key={topic.topic} value={topic.topic}>
                    {topic.topic}
                  </TabsTrigger>
                ))}
              </TabsList>
              {topicResponses.map((topic) => (
                <TabsContent key={topic.topic} value={topic.topic} className="space-y-4 mt-6">
                  {topic.responses.map((response, i) => (
                    <div key={i} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Badge variant="outline">{response.count} menções</Badge>
                          <span className="text-sm font-medium">{response.answer}</span>
                        </div>
                        <span className="text-sm text-muted-foreground">
                          {response.percentage}%
                        </span>
                      </div>
                      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-[#0ca7d2] transition-all"
                          style={{ width: `${response.percentage}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </TabsContent>
              ))}
            </Tabs>
          </CardContent>
        </Card>

        {/* Citações Relevantes */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
                <MessageSquare className="h-5 w-5 text-[#FF6B35]" />
                Citações Relevantes
            </CardTitle>
            <CardDescription>
              Respostas textuais mais impactantes dos entrevistados
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <blockquote className="border-l-4 border-[#0ca7d2] pl-4 italic">
              "Perco 3 horas por dia respondendo as mesmas perguntas no WhatsApp. 
              Se tivesse um bot pra FAQ, economizaria 80% do meu tempo."
              <footer className="text-sm text-muted-foreground mt-2">
                — João Silva, Distribuidor MMN há 5 anos
              </footer>
            </blockquote>
            <blockquote className="border-l-4 border-[#0ca7d2] pl-4 italic">
              "O maior gargalo é prospectar novos distribuidores fora do horário comercial. 
              Muita gente só tem tempo à noite."
              <footer className="text-sm text-muted-foreground mt-2">
                — Maria Santos, Coordenadora de Equipe
              </footer>
            </blockquote>
            <blockquote className="border-l-4 border-[#0ca7d2] pl-4 italic">
              "Pagaria facilmente R$200-300/mês por uma solução que automatizasse 
              qualificação de leads e follow-up."
              <footer className="text-sm text-muted-foreground mt-2">
                — Pedro Costa, Líder Diamond
              </footer>
            </blockquote>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default PesquisasResultadosPage;