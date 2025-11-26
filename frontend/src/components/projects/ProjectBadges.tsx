import React from 'react';
import { Badge } from '@/components/ui/badge';
import { ProjectStatus, ProjectType } from '@/types/project';
import { Zap, Workflow, MessageSquare, Clock, CheckCircle, Pause, AlertTriangle, RefreshCw } from 'lucide-react';
import { cn } from '@/lib/utils';

interface StatusBadgeProps {
  status: ProjectStatus;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  let icon: React.ReactNode;
  let colorClass: string;

  switch (status) {
    case 'Em Andamento':
      icon = <Clock className="h-3 w-3 mr-1" />;
      colorClass = 'bg-[#4e4ea8] hover:bg-[#4e4ea8]/80 text-white';
      break;
    case 'Concluído':
      icon = <CheckCircle className="h-3 w-3 mr-1" />;
      colorClass = 'bg-green-600 hover:bg-green-600/80 text-white';
      break;
    case 'Pausado':
      icon = <Pause className="h-3 w-3 mr-1" />;
      colorClass = 'bg-yellow-600 hover:bg-yellow-600/80 text-white';
      break;
    case 'Atrasado':
      icon = <AlertTriangle className="h-3 w-3 mr-1" />;
      colorClass = 'bg-red-600 hover:bg-red-600/80 text-white animate-pulse';
      break;
    case 'Em Revisão':
      icon = <RefreshCw className="h-3 w-3 mr-1" />;
      colorClass = 'bg-[#0ca7d2] hover:bg-[#0ca7d2]/80 text-white';
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

interface TypeBadgeProps {
  type: ProjectType;
}

export const TypeBadge: React.FC<TypeBadgeProps> = ({ type }) => {
  let icon: React.ReactNode;
  let colorClass: string;

  switch (type) {
    case 'AI Native':
      icon = <Zap className="h-3 w-3 mr-1" />;
      colorClass = 'bg-[#FF6B35] hover:bg-[#FF6B35]/80 text-white';
      break;
    case 'Workflow':
      icon = <Workflow className="h-3 w-3 mr-1" />;
      colorClass = 'bg-purple-600 hover:bg-purple-600/80 text-white';
      break;
    case 'Agente Solo':
      icon = <MessageSquare className="h-3 w-3 mr-1" />;
      colorClass = 'bg-indigo-600 hover:bg-indigo-600/80 text-white';
      break;
    default:
      icon = null;
      colorClass = 'bg-gray-500 text-white';
  }

  return (
    <Badge className={cn("capitalize", colorClass)}>
      {icon}
      {type}
    </Badge>
  );
};