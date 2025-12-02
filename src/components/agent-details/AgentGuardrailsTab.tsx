import React from 'react';
import GuardrailsTab from '@/components/renus-config/GuardrailsTab';
import { Agent } from '@/types/agent';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Shield } from 'lucide-react';

interface AgentGuardrailsTabProps {
  agent: Agent;
}

const AgentGuardrailsTab: React.FC<AgentGuardrailsTabProps> = ({ agent }) => {
  return (
    <div className="space-y-4">
        <Card className="border-l-4 border-[#0ca7d2]">
            <CardHeader>
                <CardTitle className="text-lg flex items-center text-[#0ca7d2]">
                    <Shield className="h-5 w-5 mr-2" /> Guardrails de Segurança
                </CardTitle>
            </CardHeader>
            <CardContent>
                <p className="text-sm text-muted-foreground">
                    Defina políticas de segurança e filtragem de conteúdo para o agente: <strong>{agent.name}</strong>.
                </p>
            </CardContent>
        </Card>
        <GuardrailsTab />
    </div>
  );
};

export default AgentGuardrailsTab;