import React from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import AgentWizard from '@/components/agents/wizard/AgentWizard';
import { Zap } from 'lucide-react';

const AgentCreatePage: React.FC = () => {
  return (
    <DashboardLayout>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold flex items-center">
          <Zap className="h-7 w-7 mr-3 text-[#FF6B35]" />
          Criação de Agente
        </h2>
      </div>
      <AgentWizard />
    </DashboardLayout>
  );
};

export default AgentCreatePage;