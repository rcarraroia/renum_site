import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { isaService, IsaMessage } from '@/services/isaService';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Sparkles, Send, Trash2, Download } from 'lucide-react';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';

const AssistenteIsaPage = () => {
  const [messages, setMessages] = useState<IsaMessage[]>([
    {
      role: 'assistant',
      content: 'Olá! Sou a Isa, sua assistente de IA. Posso executar comandos no sistema como:\n\n• Iniciar/pausar pesquisas\n• Gerar relatórios\n• Gerenciar agentes\n• Consultar dados\n• Enviar mensagens em lote\n\nComo posso ajudar?',
      timestamp: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [input, setInput] = useState('');

  const commandExamples = [
    'Inicie pesquisa MMN com 50 contatos da lista X',
    'Gere relatório das pesquisas de ontem',
    'Pause todas as entrevistas ativas',
    'Liste os 10 leads com maior score',
    'Exporte conversas da última semana'
  ];

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: IsaMessage = {
      role: 'user',
      content: input,
      timestamp: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
    };

    // Adiciona mensagem do usuário imediatamente
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    try {
      const response = await isaService.sendMessage(input);
      // Backend deve retornar estrutura { role, content, timestamp }
      setMessages(prev => [...prev, response]);
    } catch (error) {
      console.error(error);
      toast.error('Erro ao enviar mensagem para ISA');
      // Remover mensagem do usuário em caso de erro ou marcar como falha?
      // Por enquanto mantemos.
    }
  };

  const handleClearChat = () => {
    setMessages([{
      role: 'assistant',
      content: 'Conversa limpa. Como posso ajudar agora?',
      timestamp: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
    }]);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-[#4e4ea8] flex items-center gap-2">
              <Sparkles className="h-8 w-8" />
              Assistente Isa
            </h1>
            <p className="text-muted-foreground mt-1">
              Execute comandos e tarefas no sistema usando linguagem natural
            </p>
          </div>
          <Badge className="bg-green-500 text-white">Online</Badge>
        </div>

        <div className="grid gap-6 lg:grid-cols-4">
          {/* Chat Area */}
          <div className="lg:col-span-3 space-y-4">
            <Card className="border-2 border-[#0ca7d2] dark:border-[#4e4ea8]">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>Conversa com Isa</CardTitle>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" onClick={handleClearChat}>
                      <Trash2 className="h-4 w-4 mr-2" />
                      Limpar
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => toast.info("Exportando histórico...")}>
                      <Download className="h-4 w-4 mr-2" />
                      Exportar
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Messages */}
                <div className="h-[500px] overflow-y-auto space-y-3 p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
                  {messages.map((msg, i) => (
                    <div
                      key={i}
                      className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={cn(
                          "max-w-[80%] rounded-lg p-4",
                          msg.role === 'user'
                            ? 'bg-[#0ca7d2] text-white'
                            : msg.commandExecuted
                              ? 'bg-green-50 dark:bg-green-950 border-2 border-green-500'
                              : 'bg-white dark:bg-gray-800 border-2'
                        )}
                      >
                        <div className="text-sm whitespace-pre-wrap">{msg.content}</div>
                        <div
                          className={cn(
                            "text-xs mt-2",
                            msg.role === 'user' ? 'text-white/70' : 'text-muted-foreground'
                          )}
                        >
                          {msg.timestamp}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Input */}
                <div className="flex gap-2">
                  <Textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleSend();
                      }
                    }}
                    placeholder="Digite um comando ou pergunta..."
                    rows={3}
                    className="resize-none"
                  />
                  <Button
                    onClick={handleSend}
                    className="bg-[#0ca7d2] hover:bg-[#0987a8]"
                    size="lg"
                  >
                    <Send className="h-5 w-5" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar - Exemplos */}
          <div className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Exemplos de Comandos</CardTitle>
                <CardDescription className="text-xs">
                  Clique para usar
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {commandExamples.map((example, i) => (
                    <button
                      key={i}
                      onClick={() => setInput(example)}
                      className="w-full text-left p-3 rounded-lg border hover:border-[#0ca7d2] hover:bg-blue-50 dark:hover:bg-blue-950 transition-all text-sm"
                    >
                      {example}
                    </button>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base">Capacidades</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-start gap-2">
                    <Badge className="bg-blue-500 text-white mt-0.5">1</Badge>
                    <span>Gerenciar pesquisas e entrevistas</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <Badge className="bg-blue-500 text-white mt-0.5">2</Badge>
                    <span>Gerar relatórios e análises</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <Badge className="bg-blue-500 text-white mt-0.5">3</Badge>
                    <span>Consultar dados do sistema</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <Badge className="bg-blue-500 text-white mt-0.5">4</Badge>
                    <span>Controlar sub-agentes</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <Badge className="bg-blue-500 text-white mt-0.5">5</Badge>
                    <span>Executar ações em lote</span>
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default AssistenteIsaPage;