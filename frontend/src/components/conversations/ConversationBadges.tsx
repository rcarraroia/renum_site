import React from 'react';
import { Badge } from '@/components/ui/badge';
import { ConversationStatus, ConversationChannel } from '@/types/conversation';
import { CheckCircle, Clock, MessageSquare, Zap, Mail, Globe, AlertTriangle, RefreshCw, Hash } from 'lucide-react';
import { cn } from '@/lib/utils';

interface StatusBadgeProps {
  status: ConversationStatus;
}

export const ConversationStatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  let icon: React.ReactNode;
  let colorClass: string;

  switch (status) {
    case 'Nova':
      icon = <Zap className="h-3 w-3 mr-1" />;
      colorClass = 'bg-[#FF6B35] hover:bg-[#FF6B35]/80 text-white';
      break;
    case 'Em Andamento':
      icon = <Clock className="h-3 w-3 mr-1" />;
      colorClass = 'bg-[#4e4ea8] hover:bg-[#4e4ea8]/80 text-white';
      break;
    case 'Resolvida':
      icon = <CheckCircle className="h-3 w-3 mr-1" />;
      colorClass = 'bg-green-600 hover:bg-green-600/80 text-white';
      break;
    case 'Fechada':
      icon = <Hash className="h-3 w-3 mr-1" />;
      colorClass = 'bg-gray-500 hover:bg-gray-500/80 text-white';
      break;
    case 'Pendente':
      icon = <RefreshCw className="h-3 w-3 mr-1" />;
      colorClass = 'bg-yellow-600 hover:bg-yellow-600/80 text-white';
      break;
    default:
      icon = null;
      colorClass = 'bg-gray-500 text-white';
  }

  return (
    <Badge className={cn("capitalize", colorClass)}>
      {icon}
      {status}
    </Badge>
  );
};

interface ChannelIconProps {
  channel: ConversationChannel;
}

export const ChannelIcon: React.FC<ChannelIconProps> = ({ channel }) => {
  switch (channel) {
    case 'WhatsApp':
      return <MessageSquare className="h-4 w-4 text-green-500" />;
    case 'Web':
      return <Globe className="h-4 w-4 text-[#4e4ea8]" />;
    case 'Email':
      return <Mail className="h-4 w-4 text-[#FF6B35]" />;
    case 'API':
      return <Zap className="h-4 w-4 text-[#0ca7d2]" />;
    default:
      return <MessageSquare className="h-4 w-4 text-muted-foreground" />;
  }
};

interface PriorityBadgeProps {
    priority: 'Low' | 'Medium' | 'High';
}

export const PriorityBadge: React.FC<PriorityBadgeProps> = ({ priority }) => {
    let colorClass: string;
    switch (priority) {
        case 'High':
            colorClass = 'bg-red-500 text-white';
            break;
        case 'Medium':
            colorClass = 'bg-yellow-500 text-gray-900';
            break;
        case 'Low':
            colorClass = 'bg-green-500 text-white';
            break;
    }
    return (
        <Badge className={cn("capitalize", colorClass)}>
            <AlertTriangle className="h-3 w-3 mr-1" />
            {priority}
        </Badge>
    );
};