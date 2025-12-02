import React from 'react';
import { AdvancedTab } from '@/components/renus-config/AdvancedTab';
import { Agent } from '@/types/agent';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Sliders } from 'lucide-react';

interface AgentAdvancedTabProps {
  agent: Agent;
}

const AgentAdvancedTab: React.FC<AgentAdvancedTabProps> = ({ agent }) => {
  return (
    <div className="space-y-4">
        <Card className="border-l-4 border-[#0ca7d2]">
            <CardHeader>
                <CardTitle className="text-lg flex items-center text-[#0ca7d2]">
                    <Sliders className="h-5 w-5 mr-2" /> Configurações Avançadas (LLM)
                </CardTitle>
            </CardHeader>
            <CardContent>
                <p className="text-sm text-muted-foreground">
                    Ajuste o modelo de linguagem, temperatura e tokens para o agente: <strong>{agent.name}</strong>.
                </p>
            </CardContent>
        </Card>
        <AdvancedTab />
    </div>
  );
};

export default AgentAdvancedTab;