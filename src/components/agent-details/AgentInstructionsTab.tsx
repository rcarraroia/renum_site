import React from 'react';
import InstructionsTab from '@/components/renus-config/InstructionsTab';
import { Agent } from '@/types/agent';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Zap } from 'lucide-react';

interface AgentInstructionsTabProps {
  agent: Agent;
}

// NOTE: This component currently reuses the global InstructionsTab which uses internal mock data.
// In a real application, we would pass agent.instructions as props to a modified InstructionsTab.
const AgentInstructionsTab: React.FC<AgentInstructionsTabProps> = ({ agent }) => {
  return (
    <div className="space-y-4">
        <Card className="border-l-4 border-[#FF6B35]">
            <CardHeader>
                <CardTitle className="text-lg flex items-center text-[#FF6B35]">
                    <Zap className="h-5 w-5 mr-2" /> Instruções Específicas
                </CardTitle>
            </CardHeader>
            <CardContent>
                <p className="text-sm text-muted-foreground">
                    Ajuste o prompt de sistema e a persona para o agente: <strong>{agent.name}</strong>.
                </p>
            </CardContent>
        </Card>
        <InstructionsTab />
    </div>
  );
};

export default AgentInstructionsTab;