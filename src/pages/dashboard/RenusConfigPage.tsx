import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Zap, Save, Settings, Wrench, BookOpen, Clock, RefreshCw, Shield, Users, Sliders } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { toast } from 'sonner';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import ConfigRenusPanel from '@/components/agents/config/ConfigRenusPanel'; // Using the new consolidated panel

const RenusConfigPage: React.FC = () => {
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

  return (
    <DashboardLayout>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold flex items-center">
          <Zap className="h-7 w-7 mr-3 text-[#FF6B35]" />
          Configuração Global do Renus
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
                    <div className="flex justify-between">
                        <span>Guardrails Ativos:</span>
                        <span className="font-semibold text-green-500">3/6</span>
                    </div>
                </CardContent>
            </Card>
        </div>

        {/* Main Configuration Tabs */}
        <div className="lg:col-span-9">
            <ConfigRenusPanel isGlobalConfig={true} />
        </div>
      </div>
    </DashboardLayout>
  );
};

export default RenusConfigPage;