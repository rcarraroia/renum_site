import React from 'react';
import KnowledgeTab from '@/components/renus-config/KnowledgeTab';
import { Agent } from '@/types/agent';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BookOpen } from 'lucide-react';

interface AgentKnowledgeTabProps {
  agent: Agent;
}

const AgentKnowledgeTab: React.FC<AgentKnowledgeTabProps> = ({ agent }) => {
  return (
    <div className="space-y-4">
        <Card className="border-l-4 border-[#FF6B35]">
            <CardHeader>
                <CardTitle className="text-lg flex items-center text-[#FF6B35]">
                    <BookOpen className="h-5 w-5 mr-2" /> Base de Conhecimento
                </CardTitle>
            </CardHeader>
            <CardContent>
                <p className="text-sm text-muted-foreground">
                    Gerencie os documentos e textos que o agente <strong>{agent.name}</strong> usa para responder.
                </p>
            </CardContent>
        </Card>
        <KnowledgeTab />
    </div>
  );
};

export default AgentKnowledgeTab;