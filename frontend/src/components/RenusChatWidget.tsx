import React from 'react';
import { MessageSquare, X, Send, Zap } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useRenusChat } from '@/context/RenusChatContext';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { motion, AnimatePresence } from 'framer-motion';

// Placeholder for chat messages
interface ChatMessage {
  id: number;
  sender: 'user' | 'renus';
  text: string;
}

const mockMessages: ChatMessage[] = [
  { id: 1, sender: 'renus', text: 'Olá! Eu sou Renus, seu assistente de descoberta. Como posso ajudar a transformar seu negócio hoje?' },
  { id: 2, sender: 'user', text: 'Quero automatizar meu processo de vendas.' },
];

const RenusChatWidget: React.FC = () => {
  const { isChatOpen, toggleChat, closeChat } = useRenusChat();
  const [messages, setMessages] = React.useState<ChatMessage[]>(mockMessages);
  const [input, setInput] = React.useState('');
  const chatContentRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    if (chatContentRef.current) {
      chatContentRef.current.scrollTop = chatContentRef.current.scrollHeight;
    }
  }, [messages, isChatOpen]);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() === '') return;

    const newUserMessage: ChatMessage = {
      id: Date.now(),
      sender: 'user',
      text: input.trim(),
    };

    setMessages(prev => [...prev, newUserMessage]);
    setInput('');

    // Mock Renus response after a delay
    setTimeout(() => {
      const renusResponse: ChatMessage = {
        id: Date.now() + 1,
        sender: 'renus',
        text: 'Entendido! Para otimizar seu processo de vendas, precisamos analisar seus funis atuais. Você pode me dar mais detalhes sobre seus desafios?',
      };
      setMessages(prev => [...prev, renusResponse]);
    }, 1500);
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
        <p className="text-sm">{message.text}</p>
      </div>
    </motion.div>
  );

  return (
    <div className="fixed bottom-4 right-4 z-[100]">
      <AnimatePresence>
        {isChatOpen ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.8, y: 50 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 50 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="w-80 md:w-96 h-[70vh] max-h-[600px] shadow-2xl rounded-lg overflow-hidden"
          >
            <Card className="flex flex-col h-full border-2 border-[#4e4ea8] dark:border-[#0ca7d2]">
              <CardHeader className="flex flex-row items-center justify-between p-4 bg-[#4e4ea8] dark:bg-gray-800 text-white">
                <CardTitle className="text-lg font-bold flex items-center">
                  <Zap className="h-5 w-5 mr-2 text-[#0ca7d2]" />
                  Renus - Assistente Discovery
                </CardTitle>
                <Button variant="ghost" size="icon" onClick={closeChat} className="text-white hover:bg-white/20">
                  <X className="h-5 w-5" />
                </Button>
              </CardHeader>
              
              <CardContent ref={chatContentRef} className="flex-grow overflow-y-auto p-4 space-y-3 bg-background">
                {messages.map((msg) => (
                  <MessageBubble key={msg.id} message={msg} />
                ))}
              </CardContent>

              <CardFooter className="p-3 border-t bg-background">
                <form onSubmit={handleSend} className="flex w-full space-x-2">
                  <Input
                    placeholder="Digite sua mensagem..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    className="flex-grow"
                  />
                  <Button type="submit" size="icon" className="bg-[#FF6B35] hover:bg-[#e55f30]">
                    <Send className="h-5 w-5" />
                  </Button>
                </form>
              </CardFooter>
            </Card>
          </motion.div>
        ) : (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 500, damping: 30 }}
          >
            <Button
              size="icon"
              className="h-14 w-14 rounded-full bg-[#4e4ea8] hover:bg-[#3a3a80] shadow-xl relative"
              onClick={toggleChat}
            >
              <Zap className="h-7 w-7 text-[#0ca7d2]" />
              {/* Subtle pulse animation */}
              <span className="absolute inset-0 inline-flex h-full w-full rounded-full bg-[#4e4ea8] opacity-75 animate-ping"></span>
            </Button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default RenusChatWidget;