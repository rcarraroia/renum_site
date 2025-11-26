import React, { useState, useMemo } from 'react';
import { Conversation, ConversationStatus, ConversationChannel } from '@/types/conversation';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Search, Filter, Clock, MessageSquare, Zap, List, LayoutGrid } from 'lucide-react';
import ConversationListItem from './ConversationListItem';
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { cn } from '@/lib/utils';

interface ConversationListPanelProps {
  conversations: Conversation[];
  selectedConversationId: string | null;
  onSelectConversation: (id: string) => void;
}

const ConversationListPanel: React.FC<ConversationListPanelProps> = ({ conversations, selectedConversationId, onSelectConversation }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState<ConversationStatus | 'all'>('all');
  const [filterChannel, setFilterChannel] = useState<ConversationChannel | 'all'>('all');

  const filteredConversations = useMemo(() => {
    return conversations
      .filter(conv => {
        const matchesSearch = searchTerm.toLowerCase() === '' || 
                              conv.client.companyName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                              conv.messages.some(msg => msg.content.toLowerCase().includes(searchTerm.toLowerCase()));
        
        const matchesStatus = filterStatus === 'all' || conv.status === filterStatus;
        const matchesChannel = filterChannel === 'all' || conv.channel === filterChannel;

        return matchesSearch && matchesStatus && matchesChannel;
      })
      .sort((a, b) => b.lastUpdate.getTime() - a.lastUpdate.getTime()); // Sort by newest first
  }, [conversations, searchTerm, filterStatus, filterChannel]);

  return (
    <div className="flex flex-col h-full border-r bg-background dark:bg-gray-950">
      <div className="p-4 border-b">
        <div className="relative mb-3">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input 
            placeholder="Buscar conversas..." 
            className="pl-10" 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        
        <div className="flex space-x-2">
            <Select value={filterStatus} onValueChange={(v) => setFilterStatus(v as ConversationStatus | 'all')}>
                <SelectTrigger className="w-1/2">
                    <Filter className="h-4 w-4 mr-2 text-[#4e4ea8]" />
                    <SelectValue placeholder="Status" />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="all">Todos os Status</SelectItem>
                    {['Nova', 'Em Andamento', 'Resolvida', 'Fechada', 'Pendente'].map(s => (
                        <SelectItem key={s} value={s}>{s}</SelectItem>
                    ))}
                </SelectContent>
            </Select>
            <Select value={filterChannel} onValueChange={(v) => setFilterChannel(v as ConversationChannel | 'all')}>
                <SelectTrigger className="w-1/2">
                    <MessageSquare className="h-4 w-4 mr-2 text-[#FF6B35]" />
                    <SelectValue placeholder="Canal" />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="all">Todos os Canais</SelectItem>
                    {['WhatsApp', 'Web', 'Email', 'API'].map(c => (
                        <SelectItem key={c} value={c}>{c}</SelectItem>
                    ))}
                </SelectContent>
            </Select>
        </div>
      </div>

      <div className="flex-grow overflow-y-auto">
        {filteredConversations.length === 0 ? (
          <div className="text-center p-8 text-muted-foreground">
            <List className="h-8 w-8 mx-auto mb-2" />
            <p>Nenhuma conversa encontrada.</p>
          </div>
        ) : (
          filteredConversations.map(conv => (
            <ConversationListItem
              key={conv.id}
              conversation={conv}
              isSelected={conv.id === selectedConversationId}
              onClick={onSelectConversation}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default ConversationListPanel;