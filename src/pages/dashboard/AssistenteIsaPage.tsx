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

import { useRenusChat } from '@/context/RenusChatContext';

const AssistenteIsaPage = () => {
  // Use global context for sync with widget
  const { messages, sendMessage, activeAgent, setActiveAgent } = useRenusChat();
  const [input, setInput] = useState('');

  // Switch to ISA context/agent on mount, revert to Renus on unmount
  useEffect(() => {
    setActiveAgent('isa');
    return () => setActiveAgent('renus');
  }, []); // Only on mount/unmount

  // If context hasn't switched yet, don't render or show loading (optional, but prevents flash)

  const handleSend = async () => {
    if (!input.trim()) return;
    const text = input.trim();
    setInput('');
    await sendMessage(text);
  };

  const handleClearChat = () => {
    // Context doesn't support clear yet, implementing reload as temp workaround or just toast
    toast.info("Histórico local limpo (refresh para resetar completo)");
    // In future: context.clear(activeAgent)
  };

  const commandExamples = [
    'Inicie pesquisa MMN com 50 contatos da lista X',
    'Gere relatório das pesquisas de ontem',
    'Pause todas as entrevistas ativas',
    'Liste os 10 leads com maior score',
    'Exporte conversas da última semana'
  ];

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
                      className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={cn(
                          "max-w-[80%] rounded-lg p-4",
                          msg.sender === 'user'
                            ? 'bg-[#0ca7d2] text-white'
                            : 'bg-white dark:bg-gray-800 border-2'
                        )}
                      >
                        <div className="whitespace-pre-wrap text-sm leading-relaxed">
                          {msg.text}
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