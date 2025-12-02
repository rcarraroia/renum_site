import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Zap, CheckCircle, Briefcase, User, MessageSquare, Globe, Settings, Tag, DollarSign } from 'lucide-react';
import { mockProjects, mockClients, mockModels, mockCategories } from '@/mocks/agents.mock';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { cn } from '@/lib/utils';

interface Step5ReviewProps {
  formData: any;
  onDeploy: () => void;
}

const Step5Review: React.FC<Step5ReviewProps> = ({ formData, onDeploy }) => {
  const project = mockProjects.find(p => p.id === formData.project_id);
  const client = mockClients.find(c => c.id === formData.client_id);
  const model = mockModels.find(m => m.id === formData.model);
  const category = mockCategories.find(c => c.id === formData.category);

  const getAgentTypeLabel = (type: string) => {
    switch (type) {
        case 'b2b_empresa': return 'B2B (Empresa)';
        case 'b2c_marketplace': return 'B2C (Marketplace)';
        case 'b2c_individual': return 'B2C (Individual)';
        default: return 'N/A';
    }
  };

  return (
    <div className="space-y-6">
      <Card className="border-2 border-green-500">
        <CardHeader>
          <CardTitle className="flex items-center text-green-600">
            <CheckCircle className="h-5 w-5 mr-2" /> 5. Revisão Final
          </CardTitle>
          <CardDescription>
            Verifique todos os detalhes antes de implantar o agente em produção.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          {/* Identity & Project */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-2 p-4 border rounded-lg">
                <h4 className="font-semibold flex items-center text-[#4e4ea8]"><User className="h-4 w-4 mr-2" /> Identidade</h4>
                <p className="text-lg font-bold">{formData.name}</p>
                <p className="text-sm text-muted-foreground">{formData.description}</p>
                <p className="text-xs font-mono mt-2">Slug: {formData.slug}</p>
            </div>
            <div className="space-y-2 p-4 border rounded-lg">
                <h4 className="font-semibold flex items-center text-[#FF6B35]"><Briefcase className="h-4 w-4 mr-2" /> Projeto</h4>
                <p className="text-sm font-medium">Cliente: {client?.name}</p>
                <p className="text-sm font-medium">Projeto: {project?.name}</p>
                <p className="text-xs text-muted-foreground">Tipo: {getAgentTypeLabel(formData.type)}</p>
            </div>
          </div>

          <Separator />

          {/* Channels & Model */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-2">
                <h4 className="font-semibold flex items-center text-[#0ca7d2]"><MessageSquare className="h-4 w-4 mr-2" /> Canais Ativos</h4>
                <div className="flex flex-wrap gap-2">
                    {(formData.channel || []).map((c: string) => (
                        <Badge key={c} className="bg-[#0ca7d2] text-white capitalize">{c}</Badge>
                    ))}
                </div>
            </div>
            <div className="space-y-2">
                <h4 className="font-semibold flex items-center text-purple-500"><Zap className="h-4 w-4 mr-2" /> Modelo de IA</h4>
                <p className="font-medium">{model?.name} ({model?.provider})</p>
                <p className="text-xs text-muted-foreground">Custo Estimado: {model?.cost}</p>
            </div>
          </div>

          <Separator />

          {/* Configuration Summary (Mock) */}
          <div className="space-y-2">
            <h4 className="font-semibold flex items-center text-green-600"><Settings className="h-4 w-4 mr-2" /> Configurações Renus</h4>
            <ul className="text-sm text-muted-foreground list-disc pl-5">
                <li>Instruções de Sistema: <span className="font-medium text-primary dark:text-white">Definidas</span></li>
                <li>Ferramentas: <span className="font-medium text-primary dark:text-white">2 Ativas (Mock)</span></li>
                <li>Guardrails: <span className="font-medium text-primary dark:text-white">Ativos (PII, Secret)</span></li>
            </ul>
          </div>

        </CardContent>
      </Card>
      
      <div className="flex justify-end">
        <Button onClick={onDeploy} size="lg" className="bg-green-600 hover:bg-green-700 text-white text-lg px-8 py-6">
          <Zap className="h-5 w-5 mr-3" /> Implantar Agente
        </Button>
      </div>
    </div>
  );
};

export default Step5Review;