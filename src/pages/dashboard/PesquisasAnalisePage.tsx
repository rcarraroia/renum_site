import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Textarea } from '@/components/ui/textarea';
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from '@/components/ui/select';
import { Sparkles, Download, Copy, RefreshCw, Loader2, AlertCircle, TrendingUp, Target, Lightbulb, ClipboardList } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { interviewService } from '@/services/interviewService';

const PesquisasAnalisePage = () => {
  const { toast } = useToast();
  const [selectedSubagent, setSelectedSubagent] = useState('mmn');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [analysis, setAnalysis] = useState<string | null>(null);
  const [analytics, setAnalytics] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  // Carregar analytics na inicialização
  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await interviewService.getAnalytics();
      setAnalytics(data);
    } catch (err) {
      setError('Erro ao carregar analytics. Usando dados de exemplo.');
      console.error('Erro ao carregar analytics:', err);
      // Usar dados mock em caso de erro
      setAnalytics({
        total_interviews: 50,
        completed_interviews: 42,
        completion_rate: 84,
        avg_duration: 8.5
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Mock analysis
  const mockAnalysis = `# 📊 Análise Completa - Pesquisa MMN (50 entrevistas)

## 🎯 PRINCIPAIS DORES IDENTIFICADAS

### 1. Gestão de Tempo (78% dos entrevistados)
**Problema crítico:** Distribuidores gastam em média 3-4 horas/dia respondendo perguntas repetitivas.

**Citações relevantes:**
- "Passo o dia inteiro no WhatsApp respondendo as mesmas coisas"
- "Não sobra tempo para prospectar porque estou sempre apagando incêndio"

**Impacto:** Alta frustração, baixa produtividade, perda de oportunidades.

### 2. Dificuldade de Prospecção (65%)
**Problema:** Falta de ferramentas para qualificar leads automaticamente.

**Citações:**
- "Não sei quem realmente tem perfil para o negócio até perder tempo conversando"
- "Muitos leads frios que nunca convertem"

**Impacto:** Alto CAC (custo de aquisição de cliente), baixa taxa de conversão.

### 3. Treinamento de Equipe (54%)
**Problema:** Dificuldade em escalar conhecimento para novos distribuidores.

---

## 💡 FUNCIONALIDADES MAIS DESEJADAS

### 1. FAQ Automático 24/7 (90% mencionaram)
**Descrição:** Bot que responde dúvidas comuns automaticamente.

**Valor percebido:** "Economizaria 80% do meu tempo"

**Disposição a pagar:** R$150-300/mês

### 2. Qualificação Automática de Leads (76%)
**Descrição:** Sistema que filtra leads qualificados vs. não-qualificados.

**Valor percebido:** "Focaria apenas em quem realmente tem potencial"

**Disposição a pagar:** R$200-400/mês

### 3. Onboarding Automatizado (68%)
**Descrição:** Sequência de mensagens que ensina novos distribuidores.

---

## 🚨 INSIGHTS CRÍTICOS

### Timing é Tudo
67% dos entrevistados mencionaram que leads respondem fora do horário comercial (18h-22h).

**Recomendação:** Atendimento 24/7 não é "nice to have", é **essencial**.

### Simplicidade > Funcionalidades
45% disseram que já tentaram outras ferramentas mas eram "muito complicadas".

**Recomendação:** UX ultra-simples, onboarding de 15 minutos máximo.

### Integração com Instagram
38% querem integração com Instagram além de WhatsApp.

**Recomendação:** Feature roadmap prioritária.

---

## 💰 ANÁLISE DE PRECIFICAÇÃO

### Faixa Declarada
- **Mínimo aceitável:** R$97/mês
- **Ideal (maioria):** R$150-250/mês
- **Enterprise (grandes redes):** R$500-1000/mês

### Ancoragem de Valor
Distribuidores calculam ROI baseado em "horas economizadas":
- 3h/dia x R$50/hora = R$150/dia economizado
- R$150 x 20 dias úteis = **R$3.000/mês de valor gerado**

**Conclusão:** Preço de R$200-300/mês é facilmente justificável.

---

## 🎯 RECOMENDAÇÕES ESTRATÉGICAS

### 1. MVP Deve Incluir
- ✅ FAQ automático
- ✅ Atendimento 24/7
- ✅ Qualificação básica de leads

### 2. Roadmap Próximos 6 Meses
- Onboarding automatizado
- Relatórios de performance
- Integração Instagram

### 3. Posicionamento de Marketing
Focar em **ROI tangível**: "Economize 3 horas/dia e aumente suas vendas em 40%"

### 4. Canais de Aquisição
- Grupos de WhatsApp/Telegram de MMN
- Parcerias com grandes redes (Herbalife, Hinode, etc)
- Eventos de MMN

---

## 📈 PRÓXIMOS PASSOS

1. Validar precificação com testes A/B
2. Desenvolver protótipo do FAQ automático
3. Captar 10 clientes beta (R$97/mês)
4. Coletar feedback intensivo
5. Iterar e escalar`;

  const handleGenerate = () => {
    setIsGenerating(true);
    // Simular chamada de API
    setTimeout(() => {
      setAnalysis(mockAnalysis);
      setIsGenerating(false);
      toast({
        title: "Análise gerada com sucesso!",
        description: "Os insights foram processados pela IA."
      });
    }, 3000);
  };

  const handleCopy = () => {
    if (analysis) {
      navigator.clipboard.writeText(analysis);
      toast({
        title: "Copiado!",
        description: "Análise copiada para a área de transferência."
      });
    }
  };

  const handleDownload = () => {
    if (analysis) {
      const blob = new Blob([analysis], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `analise-${selectedSubagent}-${Date.now()}.md`;
      a.click();
      toast({
        title: "Download iniciado!",
        description: "Arquivo Markdown sendo baixado."
      });
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center">
            <ClipboardList className="h-7 w-7 mr-3 text-[#4e4ea8]" />
            <h1 className="text-3xl font-bold text-[#4e4ea8]">Análise com IA</h1>
        </div>
        <p className="text-muted-foreground mt-1">
          Gere insights automáticos usando inteligência artificial
        </p>

        {/* Config Card */}
        <Card className="border-2 border-[#0ca7d2]">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-[#0ca7d2]" />
              <CardTitle>Configuração da Análise</CardTitle>
            </div>
            <CardDescription>
              Selecione o sub-agente e gere insights automaticamente
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <label className="text-sm font-medium">Sub-Agente</label>
                <Select value={selectedSubagent} onValueChange={setSelectedSubagent}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="mmn">Pesquisa MMN (50 respostas)</SelectItem>
                    <SelectItem value="vereadores">Pesquisa Vereadores (12 respostas)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Modelo de IA</label>
                <Select defaultValue="claude">
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="claude">Claude Sonnet 4</SelectItem>
                    <SelectItem value="gpt4">GPT-4 Turbo</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="flex gap-2">
              <Button 
                onClick={handleGenerate}
                disabled={isGenerating}
                className="bg-[#0ca7d2] hover:bg-[#0987a8]"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Gerando insights...
                  </>
                ) : (
                  <>
                    <Sparkles className="h-4 w-4 mr-2" />
                    Gerar Análise Completa
                  </>
                )}
              </Button>
              {analysis && (
                <>
                  <Button variant="outline" onClick={handleCopy}>
                    <Copy className="h-4 w-4 mr-2" />
                    Copiar
                  </Button>
                  <Button variant="outline" onClick={handleDownload}>
                    <Download className="h-4 w-4 mr-2" />
                    Download MD
                  </Button>
                  <Button 
                    variant="outline" 
                    onClick={() => setAnalysis(null)}
                  >
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Nova Análise
                  </Button>
                </>
              )}
            </div>

            {!analysis && !isGenerating && (
              <div className="flex items-start gap-2 p-4 rounded-lg bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800">
                <AlertCircle className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
                <div className="text-sm text-blue-700 dark:text-blue-300">
                  <strong>Como funciona:</strong> A IA analisa todas as respostas coletadas, 
                  identifica padrões, dores principais, funcionalidades mais desejadas e gera 
                  recomendações estratégicas automaticamente. Leva ~30 segundos.
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Loading State */}
        {isGenerating && (
          <Card>
            <CardContent className="py-12">
              <div className="flex flex-col items-center justify-center space-y-4">
                <Loader2 className="h-12 w-12 animate-spin text-[#0ca7d2]" />
                <div className="text-center">
                  <h3 className="font-semibold text-lg">Processando dados...</h3>
                  <p className="text-sm text-muted-foreground mt-1">
                    A IA está analisando {selectedSubagent === 'mmn' ? '50' : '12'} respostas
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Analysis Result */}
        {analysis && !isGenerating && (
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-[#0ca7d2]" />
                  Resultado da Análise
                </CardTitle>
                <Badge className="bg-green-500">Concluído</Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="prose prose-sm max-w-none dark:prose-invert">
                <Textarea
                  value={analysis}
                  readOnly
                  className="min-h-[600px] font-mono text-sm"
                />
              </div>
            </CardContent>
          </Card>
        )}

        {/* Quick Insights (sempre visível) */}
        {!isGenerating && (
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader className="pb-3">
                <div className="flex items-center gap-2">
                  <Target className="h-4 w-4 text-red-600" />
                  <CardTitle className="text-sm">Top 3 Dores</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-start gap-2">
                    <span className="text-red-600">1.</span>
                    <span>Gestão de tempo (78%)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-600">2.</span>
                    <span>Prospecção difícil (65%)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-600">3.</span>
                    <span>Treinamento equipe (54%)</span>
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <div className="flex items-center gap-2">
                  <Lightbulb className="h-4 w-4 text-yellow-600" />
                  <CardTitle className="text-sm">Features Desejadas</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-start gap-2">
                    <span className="text-yellow-600">1.</span>
                    <span>FAQ automático (90%)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-yellow-600">2.</span>
                    <span>Qualificação leads (76%)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-yellow-600">3.</span>
                    <span>Onboarding auto (68%)</span>
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <div className="flex items-center gap-2">
                  <TrendingUp className="h-4 w-4 text-green-600" />
                  <CardTitle className="text-sm">Precificação</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm">
                  <li className="flex justify-between">
                    <span className="text-muted-foreground">Mínimo:</span>
                    <span className="font-medium">R$97/mês</span>
                  </li>
                  <li className="flex justify-between">
                    <span className="text-muted-foreground">Ideal:</span>
                    <span className="font-medium text-green-600">R$150-250</span>
                  </li>
                  <li className="flex justify-between">
                    <span className="text-muted-foreground">Enterprise:</span>
                    <span className="font-medium">R$500-1000</span>
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default PesquisasAnalisePage;