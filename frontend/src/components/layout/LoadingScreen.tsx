import React from 'react';
import { Zap } from 'lucide-react';

const LoadingScreen: React.FC = () => (
  <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 dark:bg-gray-950 text-primary dark:text-white">
    <Zap className="h-12 w-12 text-[#FF6B35] animate-pulse" />
    <p className="mt-4 text-lg font-medium">Carregando...</p>
  </div>
);

export default LoadingScreen;