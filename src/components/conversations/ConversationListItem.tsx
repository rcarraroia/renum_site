import React from 'react';
import { Conversation } from '@/types/conversation';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';
import { formatDistanceToNow } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { ConversationStatusBadge, ChannelIcon } from './ConversationBadges';
import { Zap, User, AlertTriangle } from 'lucide-react';

interface ConversationListItemProps {
  conversation: Conversation;
  isSelected: boolean;
  onClick: (id: string) => void;
}

const ConversationListItem: React.FC<ConversationListItemProps> = ({ conversation, isSelected, onClick }) => {
  const messages = conversation.messages || [];
  const lastMessage = messages[messages.length - 1];
  const lastMessageContent = lastMessage?.content || 'Nenhuma mensagem.';
  const isUnread = conversation.unreadCount > 0;

  const getInitials = (name: string) => {
    return name.split(' ').map(n => n[0]).join('').toUpperCase();
  };

  return (
    <div
      className={cn(
        "flex items-start space-x-3 p-3 border-b cursor-pointer transition-colors",
        isSelected ? "bg-accent dark:bg-gray-800 border-l-4 border-[#FF6B35]" : "hover:bg-gray-50 dark:hover:bg-gray-800/50",
        isUnread && !isSelected && "bg-gray-100 dark:bg-gray-900 font-semibold"
      )}
      onClick={() => onClick(conversation.id)}
    >
      <div className="relative flex-shrink-0">
        <Avatar className="h-10 w-10 bg-[#4e4ea8] text-white dark:bg-[#0ca7d2]">
          <AvatarFallback className="text-sm">
            {getInitials(conversation.client.contact.name)}
          </AvatarFallback>
        </Avatar>
        <div className="absolute bottom-0 right-0 p-1 bg-background rounded-full border">
          <ChannelIcon channel={conversation.channel} />
        </div>
      </div>

      <div className="flex-grow overflow-hidden">
        <div className="flex justify-between items-center">
          <h4 className={cn("text-sm font-bold truncate", isUnread && "text-primary dark:text-white")}>
            {conversation.client.companyName}
          </h4>
          <span className="text-xs text-muted-foreground flex-shrink-0">
            {formatDistanceToNow(conversation.lastUpdate, { addSuffix: true, locale: ptBR })}
          </span>
        </div>

        <p className={cn("text-sm truncate mt-1", isUnread ? "text-primary dark:text-white" : "text-muted-foreground")}>
          {lastMessageContent}
        </p>

        <div className="flex items-center justify-between mt-1">
          <ConversationStatusBadge status={conversation.status} />
          {conversation.priority === 'High' && <AlertTriangle className="h-4 w-4 text-red-500" />}
        </div>
      </div>

      {isUnread && (
        <div className="flex-shrink-0 ml-2">
          <span className="inline-flex items-center justify-center h-5 w-5 rounded-full bg-[#FF6B35] text-xs text-white">
            {conversation.unreadCount}
          </span>
        </div>
      )}
    </div>
  );
};

export default ConversationListItem;