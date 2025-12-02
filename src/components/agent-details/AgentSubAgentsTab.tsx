import React from 'react';
import { SubAgentsTab } from '@/components/renus-config/SubAgentsTab';
import { Agent } from '@/types/agent';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Users } from 'lucide-react';

interface AgentSubAgentsTabProps {
  agent: Agent;
}

const AgentSubAgentsTab: React.FC<AgentSubAgentsTabProps> = ({ agent }) => {
  return (
    <div className="space-y-4">
        <Card className="border-l-4 border-[#FF6B35]">
            <CardHeader>
                <CardTitle className="text-lg flex items-center text-[#FF6B35]">
                    <Users className="h-5 w-5 mr-2" /> Sub-Agentes
                </CardTitle>
            </CardHeader>
            <CardContent>
                <p className="text-sm text-muted-foreground">
                    Gerencie os sub-agentes especializados que este agente principal pode delegar tarefas.
                </p>
            </CardContent>
        </Card>
        <SubAgentsTab />
    </div>
  );
};

export default AgentSubAgentsTab;