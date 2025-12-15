/**
 * Skeleton Card Component
 * Skeleton loading state for cards
 */

import React from 'react';
import { cn } from '@/lib/utils';

interface SkeletonCardProps {
  className?: string;
  lines?: number;
}

export function SkeletonCard({ className, lines = 3 }: SkeletonCardProps) {
  return (
    <div className={cn('bg-white rounded-lg border p-6 animate-pulse', className)}>
      <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className={cn(
            'h-3 bg-gray-200 rounded mb-2',
            i === lines - 1 ? 'w-1/2' : 'w-full'
          )}
        ></div>
      ))}
    </div>
  );
}
