import React, { useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Zap, Send, Menu, Settings, History, Plus, Upload, Brain } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ThemeToggle } from '@/components/ThemeToggle';
import RenumLogo from '@/components/RenumLogo';
import { cn } from '@/lib/utils';
import TypingIndicator from '@/components/TypingIndicator';
import { Separator } from '@/components/ui/separator';
// import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { useRenusChat } from '@/context/RenusChatContext';
import { ChatMessage } from '@/services/publicChatService';

const RenusPage: React.FC = () => {
  // Use real context
  const { messages, sendMessage, isTyping } = useRenusChat();

  const [inputLocal, setInputLocal] = React.useState('');
  const chatContentRef = useRef<HTMLDivElement>(null);

  // Auto-scroll on new messages
  useEffect(() => {
    if (chatContentRef.current) {
      chatContentRef.current.scrollTop = chatContentRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputLocal.trim() || isTyping) return;

    const text = inputLocal.trim();
    setInputLocal(''); // Clear immediately

    await sendMessage(text);
  };

  const handleNewChat = () => {
    // TODO: Implement clear/reset in Context if needed
    window.location.reload(); // Temporary way to reset state/localStorage if logic allows
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

        {/* Support for isThinking/Keywords only if backend sends it in data structure (current simplified backend doesn't, but UI handles it if present) */}
        {message.isThinking && (
          <div className="mt-2 p-2 bg-white/10 rounded-lg flex flex-wrap gap-2">
            <Brain className="h-4 w-4 text-[#FF6B35]" />
            <span className="text-xs font-medium">Analisando...</span>
          </div>
        )}
      </div>
    </motion.div>
  );

  const Sidebar: React.FC = () => (
    <div className="w-full md:w-64 bg-sidebar dark:bg-gray-950 border-r border-sidebar-border dark:border-gray-800 p-4 flex flex-col h-full">
      <Button
        className="w-full bg-[#FF6B35] hover:bg-[#e55f30] text-white mb-4"
        onClick={handleNewChat}
      >
        <Plus className="h-4 w-4 mr-2" /> Nova Conversa
      </Button>

      <h4 className="text-sm font-semibold text-sidebar-foreground mb-2">Sessão Atual</h4>
      <Card className="p-3 mb-6 bg-sidebar-accent dark:bg-gray-800 border-sidebar-border dark:border-gray-700">
        <p className="text-xs text-sidebar-accent-foreground">Status: Conectado (Real)</p>
        <p className="text-xs text-sidebar-accent-foreground mt-1">Mensagens: {messages.length}</p>
      </Card>

      {/* Histórico removido/simplificado pois o contexto atual foca na sessão ativa pública */}
      <h4 className="text-sm font-semibold text-sidebar-foreground mb-2 opacity-50">Histórico</h4>
      <div className="space-y-2 flex-grow overflow-y-auto opacity-50">
        <div className="text-xs text-muted-foreground p-2">
          Histórico de sessões disponível apenas para usuários logados. (Em breve)
        </div>
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
              {isTyping && (
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
                  value={inputLocal}
                  onChange={(e) => setInputLocal(e.target.value)}
                  className="flex-grow"
                  disabled={isTyping}
                />
                <Button type="submit" size="icon" className="bg-[#4e4ea8] hover:bg-[#3a3a80]" disabled={isTyping}>
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