import React, { useState, useMemo } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Zap, Settings, Wrench, BookOpen, Clock, RefreshCw, Shield, Users, Sliders, FileText } from 'lucide-react';
import { cn } from '@/lib/utils';

// Import Tab Components
import InstructionsTab from './InstructionsTab';
import ToolsTab from './ToolsTab';
import IntegrationsTab from './IntegrationsTab';
import KnowledgeTab from './KnowledgeTab';
import TriggersTab from './TriggersTab';
import GuardrailsTab from './GuardrailsTab';
import { SubAgentsTab } from './SubAgentsTab';
import { AdvancedTab } from './AdvancedTab';
import ApiWebhooksTab from '../ApiWebhooksTab';

interface ConfigRenusPanelProps {
    isGlobalConfig?: boolean;
    initialTab?: string;
}

const ConfigRenusPanel: React.FC<ConfigRenusPanelProps> = ({ isGlobalConfig = false, initialTab = 'instructions' }) => {
    const [activeTab, setActiveTab] = useState(initialTab);

    const tabs = useMemo(() => {
        const baseTabs = [
            { value: 'instructions', label: 'Instruções', icon: Settings, component: InstructionsTab },
            { value: 'tools', label: 'Ferramentas', icon: Wrench, component: ToolsTab },
            { value: 'integrations', label: 'Integrações', icon: RefreshCw, component: IntegrationsTab },
            { value: 'knowledge', label: 'Conhecimento', icon: BookOpen, component: KnowledgeTab },
            { value: 'triggers', label: 'Gatilhos', icon: Clock, component: TriggersTab },
            { value: 'guardrails', label: 'Guardrails', icon: Shield, component: GuardrailsTab },
            { value: 'subagents', label: 'Sub-Agentes', icon: Users, component: SubAgentsTab },
            { value: 'advanced', label: 'Avançado', icon: Sliders, component: AdvancedTab },
        ];

        if (!isGlobalConfig) {
            // Add API & Webhooks tab only for specific agent configuration
            baseTabs.push({ value: 'api-webhooks', label: 'API & Webhooks', icon: FileText, component: ApiWebhooksTab });
        }

        return baseTabs;
    }, [isGlobalConfig]);

    return (
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-3 md:grid-cols-9 h-auto p-1 bg-gray-100 dark:bg-gray-800">
                {tabs.map(tab => (
                    <TabsTrigger 
                        key={tab.value} 
                        value={tab.value} 
                        className={cn(
                            "flex items-center space-x-1 text-xs md:text-sm data-[state=active]:bg-[#0ca7d2] data-[state=active]:text-white transition-all"
                        )}
                    >
                        <tab.icon className="h-4 w-4" />
                        <span className="hidden lg:inline">{tab.label}</span>
                    </TabsTrigger>
                ))}
            </TabsList>

            {tabs.map(tab => (
                <TabsContent key={tab.value} value={tab.value} className="mt-6">
                    <tab.component />
                </TabsContent>
            ))}
        </Tabs>
    );
};

export default ConfigRenusPanel;