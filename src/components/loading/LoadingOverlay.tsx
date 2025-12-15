/**
 * Loading Overlay Component
 * Full-screen loading overlay
 */

import React from 'react';
import { LoadingSpinner } from './LoadingSpinner';
import { cn } from '@/lib/utils';

interface LoadingOverlayProps {
  isLoading: boolean;
  text?: string;
  className?: string;
}

export function LoadingOverlay({ isLoading, text = 'Carregando...', className }: LoadingOverlayProps) {
  if (!isLoading) return null;

  return (
    <div className={cn(
      'fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm',
      className
    )}>
      <div className="bg-white rounded-lg p-8 shadow-xl">
        <LoadingSpinner size="xl" text={text} />
      </div>
    </div>
  );
}
