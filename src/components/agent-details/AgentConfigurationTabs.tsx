import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Zap, Save, Settings, Wrench, BookOpen, Clock, RefreshCw, Shield, Users, Sliders, Code } from 'lucide-react';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { Agent } from '@/types/agent';

// Import Sub-Tab Components
import AgentInstructionsTab from '@/components/agent-details/AgentInstructionsTab';
import AgentToolsTab from '@/components/agent-details/AgentToolsTab';
import AgentIntegrationsTab from '@/components/agent-details/AgentIntegrationsTab';
import AgentKnowledgeTab from '@/components/agent-details/AgentKnowledgeTab';
import AgentTriggersTab from '@/components/agent-details/AgentTriggersTab';
import AgentGuardrailsTab from '@/components/agent-details/AgentGuardrailsTab';
import AgentSubAgentsTab from '@/components/agent-details/AgentSubAgentsTab';
import AgentAdvancedTab from '@/components/agent-details/AgentAdvancedTab';
import ApiWebhooksTab from '@/components/agent-details/ApiWebhooksTab';

interface AgentConfigurationTabsProps {
  agent: Agent;
}

const AgentConfigurationTabs: React.FC<AgentConfigurationTabsProps> = ({ agent }) => {
  const [activeTab, setActiveTab] = useState('instructions');
  const [isSaving, setIsSaving] = useState(false);
  const [isUnsaved, setIsUnsaved] = useState(true); // Mock state

  const handleSaveAll = () => {
    setIsSaving(true);
    setTimeout(() => {
      setIsSaving(false);
      setIsUnsaved(false);
      toast.success(`Configuração do agente ${agent.name} publicada com sucesso!`);
    }, 1500);
  };

  const tabs = [
    { value: 'instructions', label: 'Instruções', icon: Settings, component: AgentInstructionsTab },
    { value: 'tools', label: 'Ferramentas', icon: Wrench, component: AgentToolsTab },
    { value: 'integrations', label: 'Integrações', icon: RefreshCw, component: AgentIntegrationsTab },
    { value: 'knowledge', label: 'Conhecimento', icon: BookOpen, component: AgentKnowledgeTab },
    { value: 'triggers', label: 'Gatilhos', icon: Clock, component: AgentTriggersTab },
    { value: 'guardrails', label: 'Guardrails', icon: Shield, component: AgentGuardrailsTab },
    { value: 'subagents', label: 'Sub-Agentes', icon: Users, component: AgentSubAgentsTab },
    { value: 'advanced', label: 'Avançado', icon: Sliders, component: AgentAdvancedTab },
    { value: 'api-webhooks', label: 'API & Webhooks', icon: Code, component: ApiWebhooksTab },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-end">
        <Button 
            onClick={handleSaveAll} 
            disabled={isSaving || !isUnsaved} 
            className="bg-[#4e4ea8] hover:bg-[#3a3a80]"
        >
            <Save className="h-4 w-4 mr-2" /> {isSaving ? 'Publicando...' : 'Salvar e Publicar'}
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-9 h-auto p-1 bg-gray-100 dark:bg-gray-800 overflow-x-auto">
          {tabs.map(tab => (
            <TabsTrigger 
              key={tab.value} 
              value={tab.value} 
              className={cn(
                "flex items-center space-x-2 data-[state=active]:bg-[#FF6B35] data-[state=active]:text-white data-[state=active]:shadow-md transition-all text-xs sm:text-sm",
                activeTab === tab.value && 'bg-[#FF6B35] text-white'
              )}
            >
              <tab.icon className="h-4 w-4" />
              <span className="hidden sm:inline">{tab.label}</span>
            </TabsTrigger>
          ))}
        </TabsList>

        {tabs.map(tab => (
          <TabsContent key={tab.value} value={tab.value} className="mt-6">
            <tab.component agent={agent} />
          </TabsContent>
        ))}
      </Tabs>
    </div>
  );
};

export default AgentConfigurationTabs;