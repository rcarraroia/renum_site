import React, { useState, useRef, useEffect } from 'react';
import { Conversation, ConversationMessage, MessageSender, ConversationStatus } from '@/types/conversation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Zap, User, Send, MessageSquare, Clock, FileText, Settings, MoreHorizontal, CheckCircle, XCircle, Tag, Briefcase, Mail, Phone, Clipboard, CornerDownLeft, Brain } from 'lucide-react';
import { cn } from '@/lib/utils';
import { format, formatDistanceToNow } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { ConversationStatusBadge, ChannelIcon } from './ConversationBadges';
import TypingIndicator from '@/components/TypingIndicator';
import { toast } from 'sonner';
import { Link } from 'react-router-dom';
import { ClientSegmentBadge } from '../clients/ClientBadges';

interface ConversationDetailPanelProps {
  conversation: Conversation;
  onUpdateStatus: (id: string, status: ConversationStatus) => void;
  onSendMessage: (id: string, content: string, isInternal: boolean) => void;
}

const MessageBubble: React.FC<{ message: ConversationMessage }> = ({ message }) => {
    const isClient = message.sender === 'client';
    const isRenus = message.sender === 'renus';
    const isAdmin = message.sender === 'admin';
    const isSystem = message.sender === 'system';

    if (isSystem) {
        return (
            <div className="text-center text-xs text-muted-foreground my-3">
                <span className="bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full">{message.content}</span>
            </div>
        );
    }
    
    if (message.metadata?.internal_note) {
        return (
            <div className="flex justify-center my-2">
                <div className="max-w-[80%] p-2 rounded-lg bg-yellow-100 dark:bg-yellow-900/50 text-yellow-800 dark:text-yellow-300 text-xs italic">
                    <Clipboard className="h-3 w-3 mr-1 inline" /> Nota Interna: {message.content}
                </div>
            </div>
        );
    }

    return (
        <div
            className={cn(
                "flex w-full mb-3",
                isClient ? 'justify-end' : 'justify-start'
            )}
        >
            <div
                className={cn(
                    "max-w-[75%] p-3 rounded-xl shadow-sm text-sm",
                    isClient
                        ? 'bg-[#4e4ea8] text-white rounded-br-none'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white rounded-tl-none'
                )}
            >
                {(isRenus || isAdmin) && (
                    <div className="flex items-center mb-1">
                        {isRenus && <Zap className="h-4 w-4 mr-1 text-[#0ca7d2]" />}
                        {isAdmin && <User className="h-4 w-4 mr-1 text-[#FF6B35]" />}
                        <span className="font-semibold text-xs">{isRenus ? 'Renus' : 'Admin'}</span>
                    </div>
                )}
                <p className="whitespace-pre-wrap">{message.content}</p>
                
                {message.metadata?.intent && (
                    <div className="mt-2 text-xs text-muted-foreground flex items-center">
                        <Brain className="h-3 w-3 mr-1" /> Intenção: {message.metadata.intent}
                    </div>
                )}

                <div className="text-right text-xs mt-1 opacity-70">
                    {format(message.timestamp, 'HH:mm')}
                </div>
            </div>
        </div>
    );
};

const ConversationDetailPanel: React.FC<ConversationDetailPanelProps> = ({ conversation, onUpdateStatus, onSendMessage }) => {
  const [messageInput, setMessageInput] = useState('');
  const [isInternalNote, setIsInternalNote] = useState(false);
  const [isRenusTyping, setIsRenusTyping] = useState(false);
  const chatContentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chatContentRef.current) {
      chatContentRef.current.scrollTop = chatContentRef.current.scrollHeight;
    }
  }, [conversation.messages, isRenusTyping]);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (messageInput.trim() === '') return;

    onSendMessage(conversation.id, messageInput.trim(), isInternalNote);
    setMessageInput('');
    setIsInternalNote(false);

    // Mock Renus response if admin sends a public message
    if (!isInternalNote) {
        setIsRenusTyping(true);
        setTimeout(() => {
            setIsRenusTyping(false);
            onSendMessage(conversation.id, "Obrigado pela sua mensagem. O agente Renus está processando a informação e retornará em breve.", false, 'renus');
        }, 2000);
    }
  };

  const handleCopy = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    toast.info(`${label} copiado!`);
  };

  return (
    <div className="flex flex-col h-full bg-background dark:bg-gray-900">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b bg-card dark:bg-gray-800 flex-shrink-0">
        <div className="flex items-center space-x-3">
          <ChannelIcon channel={conversation.channel} />
          <div>
            <h3 className="text-lg font-bold">{conversation.client.companyName}</h3>
            <p className="text-xs text-muted-foreground">Início: {format(conversation.startDate, 'dd/MM/yyyy HH:mm', { locale: ptBR })}</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-3">
            <Select 
                value={conversation.status} 
                onValueChange={(v) => onUpdateStatus(conversation.id, v as ConversationStatus)}
            >
                <SelectTrigger className="w-[150px]">
                    <SelectValue placeholder="Mudar Status" />
                </SelectTrigger>
                <SelectContent>
                    {['Nova', 'Em Andamento', 'Resolvida', 'Fechada', 'Pendente'].map(s => (
                        <SelectItem key={s} value={s}>{s}</SelectItem>
                    ))}
                </SelectContent>
            </Select>

            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <Button variant="outline" size="icon">
                        <MoreHorizontal className="h-4 w-4" />
                    </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                    <DropdownMenuLabel>Ações da Conversa</DropdownMenuLabel>
                    <DropdownMenuItem onClick={() => toast.info("Exportando conversa...")}>
                        <FileText className="mr-2 h-4 w-4" /> Exportar Chat
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => onUpdateStatus(conversation.id, 'Resolvida')}>
                        <CheckCircle className="mr-2 h-4 w-4" /> Marcar como Resolvida
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem className="text-red-500">
                        <XCircle className="mr-2 h-4 w-4" /> Deletar Conversa
                    </DropdownMenuItem>
                </DropdownMenuContent>
            </DropdownMenu>
        </div>
      </div>

      {/* Main Content: Messages and Context */}
      <div className="flex flex-grow overflow-hidden">
        
        {/* Message Timeline */}
        <div className="flex flex-col flex-grow overflow-y-auto p-4" ref={chatContentRef}>
          {conversation.messages.map(msg => (
            <MessageBubble key={msg.id} message={msg} />
          ))}
          {isRenusTyping && (
            <div className="flex justify-start">
                <div className="max-w-[75%] p-3 rounded-xl bg-gray-100 dark:bg-gray-700 rounded-tl-none">
                    <TypingIndicator className="text-gray-500 dark:text-gray-300" />
                </div>
            </div>
          )}
        </div>

        {/* Context Sidebar */}
        <Card className="w-72 flex-shrink-0 border-l dark:border-gray-700 rounded-none overflow-y-auto hidden lg:block">
            <CardHeader className="p-4 border-b">
                <CardTitle className="text-base flex items-center text-[#0ca7d2]">
                    <Settings className="h-4 w-4 mr-2" /> Contexto & Detalhes
                </CardTitle>
            </CardHeader>
            <CardContent className="p-4 space-y-4 text-sm">
                
                {/* Client Info */}
                <div className="space-y-2">
                    <h4 className="font-semibold flex items-center text-[#FF6B35]"><User className="h-4 w-4 mr-2" /> Cliente</h4>
                    <p className="text-xs text-muted-foreground">{conversation.client.contact.name} ({conversation.client.contact.position})</p>
                    <div className="flex items-center space-x-1">
                        <Mail className="h-3 w-3 text-muted-foreground" />
                        <span className="text-xs">{conversation.client.contact.email}</span>
                        <Button variant="ghost" size="icon" className="h-5 w-5 p-0" onClick={() => handleCopy(conversation.client.contact.email, 'Email')}><Copy className="h-3 w-3" /></Button>
                    </div>
                    <ClientSegmentBadge segment={conversation.client.segment} />
                    <Link to={`/dashboard/admin/clients/${conversation.client.id}`} className="text-xs text-[#4e4ea8] hover:underline block mt-1">Ver Perfil Completo</Link>
                </div>

                <div className="border-t pt-4 space-y-2">
                    <h4 className="font-semibold flex items-center text-[#4e4ea8]"><Briefcase className="h-4 w-4 mr-2" /> Projetos Relacionados</h4>
                    <p className="text-xs text-muted-foreground">Alpha Solutions tem 2 projetos ativos.</p>
                </div>

                <div className="border-t pt-4 space-y-2">
                    <h4 className="font-semibold flex items-center text-green-500"><Brain className="h-4 w-4 mr-2" /> Resumo (AI)</h4>
                    <p className="text-xs italic text-muted-foreground">{conversation.summary}</p>
                </div>

                <div className="border-t pt-4 space-y-2">
                    <h4 className="font-semibold flex items-center text-muted-foreground"><Tag className="h-4 w-4 mr-2" /> Tags</h4>
                    <div className="flex flex-wrap gap-1">
                        {conversation.tags.map(tag => (
                            <Badge key={tag} variant="secondary" className="text-xs">{tag}</Badge>
                        ))}
                    </div>
                </div>
            </CardContent>
        </Card>
      </div>

      {/* Input Area */}
      <div className="p-4 border-t bg-card dark:bg-gray-800 flex-shrink-0">
        <form onSubmit={handleSend} className="flex flex-col space-y-2">
            <Textarea
                placeholder={isInternalNote ? "Adicionar nota interna (invisível ao cliente)..." : "Responder ao cliente..."}
                value={messageInput}
                onChange={(e) => setMessageInput(e.target.value)}
                rows={2}
                className="resize-none"
            />
            <div className="flex justify-between items-center">
                <div className="flex items-center space-x-2">
                    <Button 
                        type="button" 
                        variant={isInternalNote ? "default" : "outline"} 
                        size="sm"
                        onClick={() => setIsInternalNote(prev => !prev)}
                        className={cn(isInternalNote ? "bg-yellow-500 hover:bg-yellow-600 text-gray-900" : "")}
                    >
                        <Clipboard className="h-4 w-4 mr-2" /> Nota Interna
                    </Button>
                    <Button type="button" variant="outline" size="sm">
                        <FileText className="h-4 w-4 mr-2" /> Anexar
                    </Button>
                </div>
                <Button type="submit" className={cn("bg-[#FF6B35] hover:bg-[#e55f30]", isInternalNote && "bg-[#4e4ea8] hover:bg-[#3a3a80]")}>
                    <Send className="h-4 w-4 mr-2" /> {isInternalNote ? 'Salvar Nota' : 'Enviar Resposta'}
                </Button>
            </div>
        </form>
      </div>
    </div>
  );
};

export default ConversationDetailPanel;