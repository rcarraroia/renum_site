
import React, { useState, useMemo } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Zap, Settings, Wrench, BookOpen, Clock, RefreshCw, Shield, Users, Sliders, FileText, Brain, Lock } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';

// Import Tab Components
import InstructionsTab from './InstructionsTab';
import SiccTab from './SiccTab';
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
    clientMode?: boolean; // New prop for client dashboard
    allowedTabs?: string[]; // Optional: explicitly allowed tabs
    hasAddons?: string[]; // Optional: list of active addons (e.g., ['subagents'])
}

const ConfigRenusPanel: React.FC<ConfigRenusPanelProps> = ({
    isGlobalConfig = false,
    initialTab = 'instructions',
    clientMode = false,
    allowedTabs,
    hasAddons = []
}) => {
    const activeTabState = useState(initialTab);
    const [activeTab, setActiveTab] = activeTabState;

    const tabs = useMemo(() => {
        // Define all available tabs
        const allTabs = [
            { value: 'instructions', label: 'Instruções', icon: Settings, component: InstructionsTab, restricted: false },
            { value: 'sicc', label: 'Inteligência', icon: Brain, component: SiccTab, restricted: false },
            { value: 'tools', label: 'Ferramentas', icon: Wrench, component: ToolsTab, restricted: false },
            { value: 'integrations', label: 'Integrações', icon: RefreshCw, component: IntegrationsTab, restricted: false },
            { value: 'knowledge', label: 'Conhecimento', icon: BookOpen, component: KnowledgeTab, restricted: false },
            { value: 'triggers', label: 'Gatilhos', icon: Clock, component: TriggersTab, restricted: false },
            { value: 'guardrails', label: 'Guardrails', icon: Shield, component: GuardrailsTab, restricted: false },
            { value: 'subagents', label: 'Sub-Agentes', icon: Users, component: SubAgentsTab, addonRequired: 'subagents' },
            { value: 'advanced', label: 'Avançado', icon: Sliders, component: AdvancedTab, restricted: true }, // Partially restricted
            { value: 'api-webhooks', label: 'API & Webhooks', icon: FileText, component: ApiWebhooksTab, restricted: false }
        ];

        let filteredTabs = allTabs;

        if (isGlobalConfig) {
            // Global config logic (existing)
            filteredTabs = allTabs.filter(t => t.value !== 'api-webhooks');
        } else if (clientMode) {
            // Client Mode Logic
            if (allowedTabs) {
                // If specific tabs provided, use them
                filteredTabs = allTabs.filter(t => allowedTabs.includes(t.value));
            } else {
                // Default client tabs logic
                // Remove tabs that are completely forbidden for clients if any (currently mostly open/restricted mode)
                // Filter out subagents if not in addon? 
                // Strategy: Show Subagents but locked if no addon? Or hide? 
                // Decision: Show all configured in "ANALISE_CONFIG_RENUS.md", logic handling inside components or here.
                // For now, let's keep all valid client tabs. 
                // Advanced is partial, so we keep it.
                filteredTabs = allTabs;
            }
        } else {
            // Admin Mode (exclude API/Webhooks if specific logic needed, otherwise show all)
            filteredTabs = allTabs;
        }

        return filteredTabs;
    }, [isGlobalConfig, clientMode, allowedTabs]);

    return (
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-3 md:grid-cols-5 lg:grid-cols-10 h-auto p-1 bg-gray-100 dark:bg-gray-800">
                {tabs.map(tab => {
                    const isLocked = tab.addonRequired && !hasAddons.includes(tab.addonRequired);

                    return (
                        <TabsTrigger
                            key={tab.value}
                            value={tab.value}
                            className={cn(
                                "flex items-center space-x-1 text-xs md:text-sm data-[state=active]:bg-[#0ca7d2] data-[state=active]:text-white transition-all",
                                isLocked && "opacity-70"
                            )}
                        >
                            <tab.icon className="h-4 w-4" />
                            <span className="hidden lg:inline">{tab.label}</span>
                            {isLocked && <Lock className="h-3 w-3 ml-1 text-muted-foreground" />}
                        </TabsTrigger>
                    );
                })}
            </TabsList>

            {tabs.map(tab => {
                const isLocked = tab.addonRequired && !hasAddons.includes(tab.addonRequired);

                return (
                    <TabsContent key={tab.value} value={tab.value} className="mt-6">
                        {isLocked ? (
                            <div className="flex flex-col items-center justify-center p-12 border-2 border-dashed rounded-lg bg-gray-50 dark:bg-gray-800/50">
                                <tab.icon className="h-12 w-12 text-muted-foreground mb-4" />
                                <h3 className="text-xl font-bold mb-2">Funcionalidade Adicional</h3>
                                <p className="text-muted-foreground text-center max-w-md mb-6">
                                    O gerenciamento de {tab.label} está disponível como um add-on do seu plano.
                                    Faça um upgrade para desbloquear este recurso.
                                </p>
                                <Button className="bg-[#FF6B35] hover:bg-[#e55f30]">
                                    Desbloquear {tab.label}
                                </Button>
                            </div>
                        ) : (
                            // Pass clientMode prop to children if they accept it
                            // We use TypeScript type casting to avoid strict check errors on dynamic components
                            <tab.component
                                clientMode={clientMode}
                                readOnly={clientMode && tab.restricted} // Example logic
                                {...(tab.value === 'advanced' && clientMode ? { restrictedMode: true } : {})}
                            />
                        )}
                    </TabsContent>
                );
            })}
        </Tabs>
    );
};

export default ConfigRenusPanel;