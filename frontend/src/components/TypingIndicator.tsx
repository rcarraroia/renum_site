import React from 'react';
import { cn } from '@/lib/utils';

const TypingIndicator: React.FC<{ className?: string }> = ({ className }) => {
  return (
    <div className={cn("flex space-x-1 items-center", className)}>
      <div className="h-2 w-2 bg-gray-500 dark:bg-gray-300 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
      <div className="h-2 w-2 bg-gray-500 dark:bg-gray-300 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
      <div className="h-2 w-2 bg-gray-500 dark:bg-gray-300 rounded-full animate-bounce"></div>
    </div>
  );
};

export default TypingIndicator;