import React from 'react';
import TriggersTab from '@/components/renus-config/TriggersTab';
import { Agent } from '@/types/agent';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Clock } from 'lucide-react';

interface AgentTriggersTabProps {
  agent: Agent;
}

const AgentTriggersTab: React.FC<AgentTriggersTabProps> = ({ agent }) => {
  return (
    <div className="space-y-4">
        <Card className="border-l-4 border-[#4e4ea8]">
            <CardHeader>
                <CardTitle className="text-lg flex items-center text-[#4e4ea8]">
                    <Clock className="h-5 w-5 mr-2" /> Gatilhos e Automações
                </CardTitle>
            </CardHeader>
            <CardContent>
                <p className="text-sm text-muted-foreground">
                    Configure automações específicas para o fluxo de trabalho do agente: <strong>{agent.name}</strong>.
                </p>
            </CardContent>
        </Card>
        <TriggersTab />
    </div>
  );
};

export default AgentTriggersTab;