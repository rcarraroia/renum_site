import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { Zap, Send, MessageSquare, Brain, FileText } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useRenusChat } from '@/context/RenusChatContext';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import TypingIndicator from '@/components/TypingIndicator';
import { Link } from 'react-router-dom';
import { useInView } from 'react-intersection-observer';

import { ChatMessage } from '@/services/publicChatService';



const RenusShowcaseSection: React.FC = () => {
  const { messages, sendMessage, isTyping } = useRenusChat();
  const [input, setInput] = useState('');
  const chatContentRef = useRef<HTMLDivElement>(null);

  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  useEffect(() => {
    if (chatContentRef.current) {
      chatContentRef.current.scrollTop = chatContentRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() === '' || isTyping) return;
    sendMessage(input.trim());
    setInput('');
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
          "max-w-[85%] p-3 rounded-xl shadow-md",
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
    <section id="renus-showcase" className="py-20 md:py-32 bg-white dark:bg-gray-900 overflow-hidden">
      <div className="container mx-auto px-4">
        <motion.h2
          ref={ref}
          initial={{ opacity: 0, y: 50 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
          className="text-4xl md:text-5xl font-bold text-center mb-16 text-primary dark:text-white"
          style={{ fontFamily: 'Montserrat, sans-serif' }}
        >
          Conheça Renus: Seu Agente de Descoberta
        </motion.h2>

        <div className="grid md:grid-cols-2 gap-12 items-center">

          {/* Left Side: Visual Representation */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={inView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative flex flex-col items-center justify-center p-8 rounded-xl bg-gray-50 dark:bg-gray-800 h-full min-h-[400px]"
          >
            <Zap className="h-24 w-24 text-[#4e4ea8] dark:text-[#0ca7d2] mb-4" />
            <h3 className="text-2xl font-semibold mb-2">Inteligência e Propósito</h3>
            <p className="text-center text-muted-foreground">
              Renus combina algoritmos avançados com a sensibilidade humana para mapear soluções ideais.
            </p>

            {/* Live Demo Indicator */}
            <div className="absolute top-4 left-4 flex items-center space-x-2 text-sm font-medium text-green-500">
              <span className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
              </span>
              <span>Live Demo</span>
            </div>
          </motion.div>

          {/* Right Side: Interactive Chat Demo */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={inView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="h-full"
          >
            <Card className="flex flex-col h-[500px] border-2 border-[#0ca7d2] dark:border-[#4e4ea8]">
              <CardHeader className="p-4 border-b bg-gray-50 dark:bg-gray-800">
                <CardTitle className="text-lg flex items-center">
                  <MessageSquare className="h-5 w-5 mr-2 text-[#FF6B35]" />
                  Chat Demo
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

              <CardFooter className="p-3 border-t bg-background">
                <form onSubmit={handleSend} className="flex w-full space-x-2">
                  <Input
                    placeholder="Tente: 'Quero aumentar minha produtividade'"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    className="flex-grow"
                    disabled={isTyping}
                  />
                  <Button type="submit" size="icon" className="bg-[#FF6B35] hover:bg-[#e55f30]" disabled={isTyping}>
                    <Send className="h-5 w-5" />
                  </Button>
                </form>
              </CardFooter>
            </Card>
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="text-center mt-12"
        >
          <Link to="/renus">
            <Button size="lg" className="text-lg px-8 py-6 bg-[#4e4ea8] hover:bg-[#3a3a80] text-white shadow-lg">
              Experimente o Renus Completo
            </Button>
          </Link>
        </motion.div>
      </div>
    </section>
  );
};

export default RenusShowcaseSection;