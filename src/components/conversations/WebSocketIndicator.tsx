/**
 * WebSocket Connection Indicator - Sprint 09
 * Shows WebSocket connection status
 */

import React from 'react';
import { Wifi, WifiOff, RefreshCw } from 'lucide-react';
import { ConnectionStatus } from '@/services/websocket/types';
import { cn } from '@/lib/utils';

interface WebSocketIndicatorProps {
  status: ConnectionStatus;
  className?: string;
}

export const WebSocketIndicator: React.FC<WebSocketIndicatorProps> = ({
  status,
  className,
}) => {
  const getStatusConfig = () => {
    switch (status) {
      case 'connected':
        return {
          icon: Wifi,
          text: 'Conectado',
          color: 'text-green-500',
          bgColor: 'bg-green-50',
        };
      case 'connecting':
        return {
          icon: RefreshCw,
          text: 'Conectando...',
          color: 'text-yellow-500',
          bgColor: 'bg-yellow-50',
          animate: true,
        };
      case 'reconnecting':
        return {
          icon: RefreshCw,
          text: 'Reconectando...',
          color: 'text-orange-500',
          bgColor: 'bg-orange-50',
          animate: true,
        };
      case 'disconnected':
        return {
          icon: WifiOff,
          text: 'Desconectado',
          color: 'text-gray-500',
          bgColor: 'bg-gray-50',
        };
      case 'error':
        return {
          icon: WifiOff,
          text: 'Erro de conexão',
          color: 'text-red-500',
          bgColor: 'bg-red-50',
        };
      default:
        return {
          icon: WifiOff,
          text: 'Desconhecido',
          color: 'text-gray-500',
          bgColor: 'bg-gray-50',
        };
    }
  };

  const config = getStatusConfig();
  const Icon = config.icon;

  return (
    <div
      className={cn(
        'flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium',
        config.bgColor,
        config.color,
        className
      )}
    >
      <Icon
        className={cn('h-4 w-4', config.animate && 'animate-spin')}
      />
      <span>{config.text}</span>
    </div>
  );
};
