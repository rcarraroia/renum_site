import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Zap, Send, User, MessageSquare } from 'lucide-react';
import { cn } from '@/lib/utils';
import TypingIndicator from '../TypingIndicator';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Textarea } from '@/components/ui/textarea';

interface Message {
  id: number;
  sender: 'user' | 'agent';
  text: string;
}

interface PreviewChatProps {
  agentName?: string;
  systemPrompt?: string;
  onTest?: (message: string) => void;
}

const PreviewChat: React.FC<PreviewChatProps> = ({ agentName = 'Agente Renum', systemPrompt, onTest }) => {
  const initialMessages: Message[] = [
    { id: 1, sender: 'agent', text: `Olá! Sou o ${agentName}. Como posso ajudar você hoje?` },
  ];
  
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [input, setInput] = useState('');
  const [isAgentTyping, setIsAgentTyping] = useState(false);
  const chatContentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chatContentRef.current) {
      chatContentRef.current.scrollTop = chatContentRef.current.scrollHeight;
    }
  }, [messages, isAgentTyping]);

  const handleSend = (e?: React.FormEvent) => {
    if (e) {
        e.preventDefault();
    }
    
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

    // Mock Agent response based on input/system prompt
    setTimeout(() => {
      let responseText = '';
      if (userMessageText.toLowerCase().includes('ajuda')) {
        responseText = `Compreendo. Para mapear a solução ideal, preciso entender seu desafio. Qual é o seu principal gargalo hoje?`;
      } else if (systemPrompt) {
        responseText = `Processando sua solicitação com base nas instruções de sistema (${systemPrompt.substring(0, 30)}...).`;
      } else {
        responseText = `O ${agentName} está processando a informação. Qual é o seu principal objetivo?`;
      }
      
      const agentResponse: Message = {
        id: Date.now() + 1,
        sender: 'agent',
        text: responseText,
      };
      setMessages(prev => [...prev, agentResponse]);
      setIsAgentTyping(false);
      
      if (onTest) {
          onTest(userMessageText); // Notify parent component if needed
      }
    }, 1500);
  };

  const MessageBubble: React.FC<{ message: Message }> = ({ message }) => (
    <div
      className={cn(
        "flex w-full mb-3",
        message.sender === 'user' ? 'justify-end' : 'justify-start'
      )}
    >
      <div className={cn("flex items-end", message.sender === 'user' ? 'flex-row-reverse' : 'flex-row')}>
        <Avatar className={cn("h-8 w-8 flex-shrink-0", message.sender === 'user' ? 'ml-2 bg-[#FF6B35]' : 'mr-2 bg-[#0ca7d2]')}>
            <AvatarFallback className="text-xs text-white">
                {message.sender === 'user' ? <User className="h-4 w-4" /> : <Zap className="h-4 w-4" />}
            </AvatarFallback>
        </Avatar>
        <div
          className={cn(
            "max-w-[85%] p-3 rounded-xl shadow-md text-sm",
            message.sender === 'user'
              ? 'bg-[#4e4ea8] text-white rounded-br-none'
              : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white rounded-tl-none'
          )}
        >
          <p className="whitespace-pre-wrap">{message.text}</p>
          <div className={cn("text-right text-xs mt-1 opacity-70", message.sender === 'user' ? 'text-white/80' : 'text-muted-foreground')}>
            {new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <Card className="flex flex-col h-full border-2 border-[#FF6B35] dark:border-[#0ca7d2]">
      <CardHeader className="p-4 border-b bg-gray-50 dark:bg-gray-800 flex-shrink-0">
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
                <div className="flex items-end">
                    <Avatar className="h-8 w-8 mr-2 bg-[#0ca7d2] flex-shrink-0">
                        <AvatarFallback className="text-xs text-white"><Zap className="h-4 w-4" /></AvatarFallback>
                    </Avatar>
                    <div className="max-w-[80%] p-3 rounded-xl bg-gray-100 dark:bg-gray-700 rounded-tl-none">
                        <TypingIndicator className="text-gray-500 dark:text-gray-300" />
                    </div>
                </div>
            </div>
        )}
      </CardContent>

      <div className="p-3 border-t bg-background flex-shrink-0">
        <form onSubmit={handleSend} className="flex w-full space-x-2">
          <Textarea
            placeholder="Digite sua mensagem..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            rows={1}
            className="flex-grow resize-none min-h-[40px]"
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