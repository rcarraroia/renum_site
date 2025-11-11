import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Zap, Save, Settings, Wrench, BookOpen, Clock, RefreshCw } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { toast } from 'sonner';
import InstructionsTab from '@/components/renus-config/InstructionsTab';
import ToolsTab from '@/components/renus-config/ToolsTab';
import IntegrationsTab from '@/components/renus-config/IntegrationsTab';
import KnowledgeTab from '@/components/renus-config/KnowledgeTab';
import TriggersTab from '@/components/renus-config/TriggersTab';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

const RenusConfigPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState('instructions');
  const [isSaving, setIsSaving] = useState(false);
  const [isUnsaved, setIsUnsaved] = useState(false); // Mock state for unsaved changes

  const handleSaveAll = () => {
    setIsSaving(true);
    // In a real app, this would trigger save functions in all child components
    setTimeout(() => {
      setIsSaving(false);
      setIsUnsaved(false);
      toast.success("Todas as configurações do Renus foram salvas e publicadas!");
    }, 1500);
  };

  const tabs = [
    { value: 'instructions', label: 'Instruções', icon: Settings, component: InstructionsTab },
    { value: 'tools', label: 'Ferramentas', icon: Wrench, component: ToolsTab },
    { value: 'integrations', label: 'Integrações', icon: RefreshCw, component: IntegrationsTab },
    { value: 'knowledge', label: 'Conhecimento', icon: BookOpen, component: KnowledgeTab },
    { value: 'triggers', label: 'Gatilhos', icon: Clock, component: TriggersTab },
  ];

  return (
    <DashboardLayout>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold flex items-center">
          <Zap className="h-7 w-7 mr-3 text-[#FF6B35]" />
          Configuração do Renus
        </h2>
        <div className="flex items-center space-x-4">
            <Badge variant="secondary" className={cn(
                "transition-colors",
                isUnsaved ? "bg-yellow-500 text-white" : "bg-green-500 text-white"
            )}>
                {isUnsaved ? 'Alterações Não Salvas' : 'Configuração Publicada'}
            </Badge>
            <Button 
                onClick={handleSaveAll} 
                disabled={isSaving} 
                className="bg-[#4e4ea8] hover:bg-[#3a3a80]"
            >
                <Save className="h-4 w-4 mr-2" /> {isSaving ? 'Publicando...' : 'Salvar e Publicar'}
            </Button>
        </div>
      </div>

      <div className="grid lg:grid-cols-12 gap-8">
        {/* Sidebar/Status Panel */}
        <div className="lg:col-span-3">
            <Card className="sticky top-4">
                <CardHeader>
                    <CardTitle className="text-lg">Status da Configuração</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3 text-sm">
                    <div className="flex justify-between">
                        <span>Versão Atual:</span>
                        <Badge variant="secondary">V1.3</Badge>
                    </div>
                    <div className="flex justify-between">
                        <span>Última Publicação:</span>
                        <span className="text-muted-foreground">2 min atrás</span>
                    </div>
                    <Separator className="my-2" />
                    <div className="flex justify-between">
                        <span>Ferramentas Ativas:</span>
                        <span className="font-semibold text-green-500">2/3</span>
                    </div>
                    <div className="flex justify-between">
                        <span>Integrações:</span>
                        <span className="font-semibold text-yellow-500">3/4</span>
                    </div>
                    <div className="flex justify-between">
                        <span>Gatilhos Ativos:</span>
                        <span className="font-semibold text-green-500">2</span>
                    </div>
                </CardContent>
            </Card>
        </div>

        {/* Main Configuration Tabs */}
        <div className="lg:col-span-9">
            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                <TabsList className="grid w-full grid-cols-5 h-auto p-1 bg-gray-100 dark:bg-gray-800">
                    {tabs.map(tab => (
                        <TabsTrigger 
                            key={tab.value} 
                            value={tab.value} 
                            className={cn(
                                "flex items-center space-x-2 data-[state=active]:bg-[#0ca7d2] data-[state=active]:text-white data-[state=active]:shadow-md transition-all",
                                activeTab === tab.value && 'bg-[#0ca7d2] text-white'
                            )}
                        >
                            <tab.icon className="h-4 w-4" />
                            <span className="hidden sm:inline">{tab.label}</span>
                        </TabsTrigger>
                    ))}
                </TabsList>

                {tabs.map(tab => (
                    <TabsContent key={tab.value} value={tab.value} className="mt-6">
                        <tab.component key={tab.value} />
                    </TabsContent>
                ))}
            </Tabs>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default RenusConfigPage;