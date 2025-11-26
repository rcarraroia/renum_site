import React from 'react';
import { Badge } from '@/components/ui/badge';
import { ClientStatus, ClientSegment } from '@/types/client';
import { CheckCircle, XCircle, Clock, Tag, Briefcase, HeartPulse, Landmark, Network, Wrench } from 'lucide-react';
import { cn } from '@/lib/utils';

interface StatusBadgeProps {
  status: ClientStatus;
}

export const ClientStatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  let icon: React.ReactNode;
  let colorClass: string;

  switch (status) {
    case 'Ativo':
      icon = <CheckCircle className="h-3 w-3 mr-1" />;
      colorClass = 'bg-green-600 hover:bg-green-600/80 text-white';
      break;
    case 'Inativo':
      icon = <XCircle className="h-3 w-3 mr-1" />;
      colorClass = 'bg-red-600 hover:bg-red-600/80 text-white';
      break;
    case 'Prospecto':
      icon = <Clock className="h-3 w-3 mr-1" />;
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

interface SegmentBadgeProps {
  segment: ClientSegment;
}

export const ClientSegmentBadge: React.FC<SegmentBadgeProps> = ({ segment }) => {
  let icon: React.ReactNode;
  let colorClass: string;

  switch (segment) {
    case 'MMN':
      icon = <Network className="h-3 w-3 mr-1" />;
      colorClass = 'bg-indigo-600 hover:bg-indigo-600/80 text-white';
      break;
    case 'Saúde':
      icon = <HeartPulse className="h-3 w-3 mr-1" />;
      colorClass = 'bg-pink-600 hover:bg-pink-600/80 text-white';
      break;
    case 'Governo':
      icon = <Landmark className="h-3 w-3 mr-1" />;
      colorClass = 'bg-blue-600 hover:bg-blue-600/80 text-white';
      break;
    case 'Serviços':
      icon = <Wrench className="h-3 w-3 mr-1" />;
      colorClass = 'bg-orange-600 hover:bg-orange-600/80 text-white';
      break;
    case 'Tecnologia':
      icon = <Briefcase className="h-3 w-3 mr-1" />;
      colorClass = 'bg-purple-600 hover:bg-purple-600/80 text-white';
      break;
    default:
      icon = <Tag className="h-3 w-3 mr-1" />;
      colorClass = 'bg-gray-500 text-white';
  }

  return (
    <Badge className={cn("capitalize", colorClass)}>
      {icon}
      {segment}
    </Badge>
  );
};