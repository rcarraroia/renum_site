import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Sparkles, X, Send, Maximize2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { cn } from '@/lib/utils';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export const AssistenteIsaWidget = () => {
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Olá! Sou a Isa, sua assistente IA. Posso ajudar com comandos como: iniciar pesquisas, gerar relatórios, gerenciar agentes. Como posso ajudar?',
      timestamp: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;

    const newMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, newMessage]);
    setInput('');

    // Mock response
    setTimeout(() => {
      const response: Message = {
        role: 'assistant',
        content: 'Entendido! Processando seu comando...',
        timestamp: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, response]);
    }, 500);
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 z-50 flex items-center gap-2 px-4 py-3 bg-[#4e4ea8] hover:bg-[#3a3a80] text-white rounded-full shadow-lg transition-all"
      >
        <Sparkles className="h-5 w-5" />
        <span className="font-medium">Isa</span>
        <Badge className="bg-green-500 h-2 w-2 p-0 rounded-full" />
      </button>
    );
  }

  return (
    <Card className="fixed bottom-6 right-6 z-50 w-96 shadow-2xl border-2 border-[#4e4ea8] dark:border-[#0ca7d2]">
      <CardHeader className="bg-gradient-to-r from-[#4e4ea8] to-[#0ca7d2] text-white pb-3 pt-3">
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2 text-lg">
            <Sparkles className="h-5 w-5" />
            Assistente Isa
            <Badge className="bg-green-500 text-white text-xs">Online</Badge>
          </CardTitle>
          <div className="flex gap-1">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate('/dashboard/admin/assistente-isa')}
              className="text-white hover:bg-white/20"
            >
              <Maximize2 className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsOpen(false)}
              className="text-white hover:bg-white/20"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-4 space-y-4">
        {/* Messages */}
        <div className="h-64 overflow-y-auto space-y-3">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={cn(
                  "max-w-[80%] rounded-lg p-3",
                  msg.role === 'user'
                    ? 'bg-[#0ca7d2] text-white'
                    : 'bg-gray-100 dark:bg-gray-800 border'
                )}
              >
                <div className="text-sm">{msg.content}</div>
                <div
                  className={cn(
                    "text-xs mt-1",
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
            placeholder="Digite um comando..."
            rows={2}
            className="resize-none"
          />
          <Button
            onClick={handleSend}
            className="bg-[#0ca7d2] hover:bg-[#0987a8]"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};