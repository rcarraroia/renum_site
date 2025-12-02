import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Zap, Send, User, MessageSquare } from 'lucide-react';
import { cn } from '@/lib/utils';
import TypingIndicator from '../TypingIndicator';

interface Message {
  id: number;
  sender: 'user' | 'agent';
  text: string;
}

const initialMessages: Message[] = [
  { id: 1, sender: 'agent', text: 'Olá! Sou o Agente Slim. Como posso ajudar com suas vendas hoje?' },
];

const PreviewChat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [input, setInput] = useState('');
  const [isAgentTyping, setIsAgentTyping] = useState(false);
  const chatContentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chatContentRef.current) {
      chatContentRef.current.scrollTop = chatContentRef.current.scrollHeight;
    }
  }, [messages, isAgentTyping]);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() === '' || isAgentTyping) return;

    const userMessageText = input.trim();
    const newUserMessage: Message = {
      id: Date.now(),
      sender: 'user',
      text: userMessageText,
    };

    setMessages(prev => [...prev, newUserMessage]);
    setInput('');
    setIsAgentTyping(true);

    // Mock Agent response
    setTimeout(() => {
      const responseText = userMessageText.toLowerCase().includes('vendas') 
        ? 'Entendido. Para otimizar suas vendas, o Agente Slim pode qualificar leads automaticamente. Qual é o seu principal gargalo?'
        : 'Processando sua solicitação... O Agente Slim está focado em otimizar processos de vendas.';
      
      const agentResponse: Message = {
        id: Date.now() + 1,
        sender: 'agent',
        text: responseText,
      };
      setMessages(prev => [...prev, agentResponse]);
      setIsAgentTyping(false);
    }, 1500);
  };

  const MessageBubble: React.FC<{ message: Message }> = ({ message }) => (
    <div
      className={cn(
        "flex w-full mb-3",
        message.sender === 'user' ? 'justify-end' : 'justify-start'
      )}
    >
      <div
        className={cn(
          "max-w-[85%] p-3 rounded-xl shadow-md text-sm",
          message.sender === 'user'
            ? 'bg-[#4e4ea8] text-white rounded-br-none'
            : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white rounded-tl-none'
        )}
      >
        {message.sender === 'agent' && (
          <div className="flex items-center mb-1">
            <Zap className="h-4 w-4 mr-1 text-[#0ca7d2]" />
            <span className="font-semibold text-xs">Agente Slim</span>
          </div>
        )}
        <p className="whitespace-pre-wrap">{message.text}</p>
      </div>
    </div>
  );

  return (
    <Card className="flex flex-col h-full border-2 border-[#FF6B35] dark:border-[#0ca7d2]">
      <CardHeader className="p-4 border-b bg-gray-50 dark:bg-gray-800">
        <CardTitle className="text-lg flex items-center">
          <MessageSquare className="h-5 w-5 mr-2 text-[#FF6B35]" />
          Preview Chat (Simulação)
        </CardTitle>
      </CardHeader>
      
      <CardContent ref={chatContentRef} className="flex-grow overflow-y-auto p-4 space-y-3 bg-background">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        {isAgentTyping && (
            <div className="flex justify-start">
                <div className="max-w-[80%] p-3 rounded-xl bg-gray-100 dark:bg-gray-700 rounded-tl-none">
                    <TypingIndicator className="text-gray-500 dark:text-gray-300" />
                </div>
            </div>
        )}
      </CardContent>

      <div className="p-3 border-t bg-background">
        <form onSubmit={handleSend} className="flex w-full space-x-2">
          <Input
            placeholder="Digite sua mensagem..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-grow"
            disabled={isAgentTyping}
          />
          <Button type="submit" size="icon" className="bg-[#FF6B35] hover:bg-[#e55f30]" disabled={isAgentTyping}>
            <Send className="h-5 w-5" />
          </Button>
        </form>
      </div>
    </Card>
  );
};

export default PreviewChat;