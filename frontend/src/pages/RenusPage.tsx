import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Zap, Send, Menu, Settings, History, Plus, Upload, FileText, X, Brain } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ThemeToggle } from '@/components/ThemeToggle';
import RenumLogo from '@/components/RenumLogo';
import { cn } from '@/lib/utils';
import TypingIndicator from '@/components/TypingIndicator';
import { Separator } from '@/components/ui/separator';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';

interface ChatMessage {
  id: number;
  sender: 'user' | 'renus';
  text: string;
  isThinking?: boolean;
  keywords?: string[];
  actions?: { label: string; payload: string }[];
}

const initialMessages: ChatMessage[] = [
  { id: 1, sender: 'renus', text: 'Bem-vindo à experiência completa do Renus! Eu sou seu assistente de Discovery, pronto para mapear as soluções de IA ideais para o seu negócio.' },
  { id: 2, sender: 'renus', text: 'Para começarmos, qual é o nome da sua empresa ou projeto e qual setor ela atua?' },
];

const RenusPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [input, setInput] = useState('');
  const [isRenusTyping, setIsRenusTyping] = useState(false);
  const [isRenusThinking, setIsRenusThinking] = useState(false);
  const chatContentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chatContentRef.current) {
      chatContentRef.current.scrollTop = chatContentRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = (e: React.FormEvent | string) => {
    let userMessageText: string;
    if (typeof e === 'string') {
        userMessageText = e;
    } else {
        e.preventDefault();
        userMessageText = input.trim();
    }
    
    if (userMessageText === '' || isRenusTyping || isRenusThinking) return;

    const newUserMessage: ChatMessage = {
      id: Date.now(),
      sender: 'user',
      text: userMessageText,
    };

    setMessages(prev => [...prev, newUserMessage]);
    setInput('');
    
    setTimeout(() => {
      processRenusResponse(userMessageText);
    }, 500);
  };

  const processRenusResponse = (userInput: string) => {
    setIsRenusThinking(true);
    
    const keywords = ['Setor', 'Desafio', 'Objetivos', 'ROI', 'Automação'];
    
    const thinkingMessage: ChatMessage = {
        id: Date.now() + 1,
        sender: 'renus',
        text: 'Processando informações...',
        isThinking: true,
        keywords: keywords.slice(0, 3),
    };
    setMessages(prev => [...prev, thinkingMessage]);

    setTimeout(() => {
      setIsRenusThinking(false);
      setMessages(prev => prev.filter(msg => !msg.isThinking)); 

      setIsRenusTyping(true);
      
      setTimeout(() => {
        let responseText = '';
        let actions = undefined;

        if (messages.length === 2) {
            responseText = `Ótimo! Entendi que você atua no setor de ${userInput}. Agora, me diga: qual é o principal problema ou gargalo que você gostaria de resolver com a ajuda da IA?`;
        } else if (messages.length === 4) {
            responseText = `Excelente foco no gargalo. Para eu entender melhor o escopo, você tem alguma expectativa de prazo ou orçamento para essa solução?`;
        } else if (messages.length === 6) {
            responseText = `Perfeito. Com base nas suas respostas, Renus já tem dados suficientes para gerar um relatório preliminar de viabilidade.`;
            actions = [{ label: 'Gerar Relatório Preliminar', payload: 'GERAR_RELATORIO' }];
        } else {
            responseText = 'Agradeço a informação! Renus continua aprendendo. O que mais você gostaria de me contar sobre seus objetivos?';
        }

        const renusResponse: ChatMessage = {
          id: Date.now() + 2,
          sender: 'renus',
          text: responseText,
          actions: actions,
        };
        setMessages(prev => [...prev, renusResponse]);
        setIsRenusTyping(false);
      }, 2000);
    }, 3000); 
  };

  const handleAction = (payload: string) => {
    if (payload === 'GERAR_RELATORIO') {
        handleSend('GERAR RELATÓRIO');
        // Simulate report generation
        setTimeout(() => {
            setMessages(prev => [...prev, {
                id: Date.now() + 3,
                sender: 'renus',
                text: 'Relatório de Viabilidade Preliminar concluído! Clique abaixo para visualizar e baixar.',
                actions: [{ label: 'Visualizar Relatório (Mock)', payload: 'VIEW_REPORT' }]
            }]);
        }, 4000);
    }
    // Add more actions here if needed
  };

  const MessageBubble: React.FC<{ message: ChatMessage }> = ({ message }) => (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={cn(
        "flex w-full mb-3",
        message.sender === 'user' ? 'justify-end' : 'justify-start'
      )}
    >
      <div
        className={cn(
          "max-w-[80%] p-3 rounded-xl shadow-md",
          message.sender === 'user'
            ? 'bg-[#4e4ea8] text-white rounded-br-none'
            : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white rounded-tl-none'
        )}
      >
        {message.sender === 'renus' && (
          <div className="flex items-center mb-1">
            <Zap className="h-4 w-4 mr-1 text-[#0ca7d2]" />
            <span className="font-semibold text-sm">Renus</span>
          </div>
        )}
        <p className="text-sm whitespace-pre-wrap">{message.text}</p>
        
        {message.isThinking && message.keywords && (
            <div className="mt-2 p-2 bg-white/10 rounded-lg flex flex-wrap gap-2">
                <Brain className="h-4 w-4 text-[#FF6B35]" />
                <span className="text-xs font-medium">Analisando:</span>
                {message.keywords.map((k, i) => (
                    <motion.span 
                        key={i} 
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: i * 0.2 }}
                        className="text-xs font-mono bg-[#0ca7d2] text-white px-2 py-0.5 rounded-full"
                    >
                        {k}
                    </motion.span>
                ))}
            </div>
        )}

        {message.actions && (
            <div className="mt-3 space-y-2">
                {message.actions.map((action, i) => (
                    <Button 
                        key={i} 
                        size="sm" 
                        className="w-full bg-[#FF6B35] hover:bg-[#e55f30] text-white"
                        onClick={() => handleAction(action.payload)}
                    >
                        {action.label}
                    </Button>
                ))}
            </div>
        )}
      </div>
    </motion.div>
  );

  const Sidebar: React.FC = () => (
    <div className="w-full md:w-64 bg-sidebar dark:bg-gray-950 border-r border-sidebar-border dark:border-gray-800 p-4 flex flex-col h-full">
        <Button 
            className="w-full bg-[#FF6B35] hover:bg-[#e55f30] text-white mb-4"
            onClick={() => setMessages(initialMessages)}
        >
            <Plus className="h-4 w-4 mr-2" /> Nova Conversa
        </Button>
        
        <h4 className="text-sm font-semibold text-sidebar-foreground mb-2">Sessão Atual</h4>
        <Card className="p-3 mb-6 bg-sidebar-accent dark:bg-gray-800 border-sidebar-border dark:border-gray-700">
            <p className="text-xs text-sidebar-accent-foreground">Status: Discovery em Andamento</p>
            <p className="text-xs text-sidebar-accent-foreground mt-1">Duração: 15 min</p>
        </Card>

        <h4 className="text-sm font-semibold text-sidebar-foreground mb-2">Histórico (Mock)</h4>
        <div className="space-y-2 flex-grow overflow-y-auto">
            {['Sessão 1: Vendas MMN', 'Sessão 2: Saúde Clínica', 'Sessão 3: Automação'].map((session, index) => (
                <div key={index} className="flex items-center text-sm text-sidebar-accent-foreground hover:bg-sidebar-accent dark:hover:bg-gray-800 p-2 rounded cursor-pointer transition-colors">
                    <History className="h-4 w-4 mr-2 opacity-70" />
                    {session}
                </div>
            ))}
        </div>

        <Separator className="my-4 bg-sidebar-border dark:bg-gray-700" />
        
        <div className="flex items-center text-sm text-sidebar-accent-foreground hover:bg-sidebar-accent dark:hover:bg-gray-800 p-2 rounded cursor-pointer transition-colors">
            <Settings className="h-4 w-4 mr-2 opacity-70" />
            Configurações
        </div>
    </div>
  );

  return (
    <div className="min-h-screen flex flex-col bg-background">
      {/* Header */}
      <header className="flex items-center justify-between p-4 border-b bg-card dark:bg-gray-900">
        <div className="flex items-center space-x-4">
          <RenumLogo />
          <span className="text-sm text-muted-foreground hidden sm:inline">Powered by Renum Tech Agency</span>
        </div>
        <div className="flex items-center space-x-4">
          <ThemeToggle />
          <Button variant="ghost" size="icon" className="md:hidden">
            <Menu className="h-5 w-5" />
          </Button>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="flex flex-grow overflow-hidden">
        {/* Sidebar (Desktop) */}
        <div className="hidden md:block flex-shrink-0 w-64">
            <Sidebar />
        </div>

        {/* Chat Area */}
        <main className="flex-grow flex flex-col p-4 md:p-8 overflow-hidden">
          <Card className="flex flex-col flex-grow border-2 border-[#0ca7d2] dark:border-[#4e4ea8] shadow-xl">
            <CardHeader className="p-4 border-b bg-gray-50 dark:bg-gray-800">
              <CardTitle className="text-xl flex items-center">
                <Zap className="h-6 w-6 mr-2 text-[#FF6B35]" />
                Renus - Discovery Agent
              </CardTitle>
            </CardHeader>
            
            <CardContent ref={chatContentRef} className="flex-grow overflow-y-auto p-4 space-y-3 bg-background">
              {messages.map((msg) => (
                <MessageBubble key={msg.id} message={msg} />
              ))}
              {(isRenusTyping || isRenusThinking) && (
                  <div className="flex justify-start">
                      <div className="max-w-[80%] p-3 rounded-xl bg-gray-100 dark:bg-gray-700 rounded-tl-none">
                          <TypingIndicator className="text-gray-500 dark:text-gray-300" />
                      </div>
                  </div>
              )}
            </CardContent>

            <div className="p-4 border-t bg-background">
              <form onSubmit={handleSend} className="flex w-full space-x-2">
                <Button type="button" size="icon" variant="outline" className="flex-shrink-0">
                    <Upload className="h-5 w-5" />
                </Button>
                <Input
                  placeholder="Digite sua resposta ou solicitação..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  className="flex-grow"
                  disabled={isRenusTyping || isRenusThinking}
                />
                <Button type="submit" size="icon" className="bg-[#4e4ea8] hover:bg-[#3a3a80]" disabled={isRenusTyping || isRenusThinking}>
                  <Send className="h-5 w-5" />
                </Button>
              </form>
            </div>
          </Card>
        </main>
      </div>

      {/* Footer */}
      <footer className="p-3 border-t bg-card dark:bg-gray-900 text-center text-xs text-muted-foreground">
        <p>&copy; {new Date().getFullYear()} Renum Tech Agency. <Link to="/" className="hover:underline text-[#FF6B35]">Voltar ao Site Principal</Link> | Política de Privacidade</p>
      </footer>
    </div>
  );
};

export default RenusPage;