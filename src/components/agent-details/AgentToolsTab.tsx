import React from 'react';
import ToolsTab from '@/components/renus-config/ToolsTab';
import { Agent } from '@/types/agent';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Wrench } from 'lucide-react';

interface AgentToolsTabProps {
  agent: Agent;
}

const AgentToolsTab: React.FC<AgentToolsTabProps> = ({ agent }) => {
  return (
    <div className="space-y-4">
        <Card className="border-l-4 border-[#4e4ea8]">
            <CardHeader>
                <CardTitle className="text-lg flex items-center text-[#4e4ea8]">
                    <Wrench className="h-5 w-5 mr-2" /> Ferramentas Disponíveis
                </CardTitle>
            </CardHeader>
            <CardContent>
                <p className="text-sm text-muted-foreground">
                    Gerencie as ferramentas (funções) que o agente <strong>{agent.name}</strong> pode chamar.
                </p>
            </CardContent>
        </Card>
        <ToolsTab />
    </div>
  );
};

export default AgentToolsTab;