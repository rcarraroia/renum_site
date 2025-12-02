import React, { useState, useMemo } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Zap, CheckCircle, Briefcase, User, MessageSquare, Globe, Settings, Tag, DollarSign, Edit, Copy, Clock, FileText, Users, Play, Save, ArrowLeft, ArrowRight } from 'lucide-react';
import { mockProjects, mockClients, mockModels, mockCategories } from '@/mocks/agents.mock';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { cn } from '@/lib/utils';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { toast } from 'sonner';
import PreviewChat from '../PreviewChat';

interface Step5ReviewProps {
  formData: any;
  onDeploy: () => void;
  onBack: () => void;
}

const Step5Review: React.FC<Step5ReviewProps> = ({ formData, onDeploy, onBack }) => {
  const [initialStatus, setInitialStatus] = useState<'ativo' | 'rascunho'>('ativo');
  
  // Mock data retrieval based on formData
  const project = mockProjects.find(p => p.id === formData.project_id);
  const client = mockClients.find(c => c.id === formData.client_id);
  const model = mockModels.find(m => m.id === formData.model);
  const category = mockCategories.find(c => c.id === formData.category);

  const isB2B = formData.contract_type === 'b2b_empresa';
  const fullDomain = `${formData.slug || 'novo-agente'}.renum.com.br`;
  const mockLink = `https://${fullDomain}/cadastro?token=abc123xyz`;

  const handleCopy = () => {
    navigator.clipboard.writeText(mockLink);
    toast.info("Link de cadastro copiado!");
  };

  const handleSaveDraft = () => {
    toast.info("Configuração salva como rascunho.");
  };

  const SummaryCard: React.FC<{ title: string, icon: React.ElementType, children: React.ReactNode, onEdit?: () => void }> = ({ title, icon: Icon, children, onEdit }) => (
    <Card className="p-4">
        <CardHeader className="p-0 mb-3 flex flex-row items-center justify-between">
            <CardTitle className="text-lg flex items-center text-[#4e4ea8]">
                <Icon className="h-5 w-5 mr-2" /> {title}
            </CardTitle>
            {onEdit && (
                <Button variant="ghost" size="icon" className="h-6 w-6 text-muted-foreground" onClick={onEdit}>
                    <Edit className="h-4 w-4" />
                </Button>
            )}
        </CardHeader>
        <CardContent className="p-0 text-sm space-y-1">
            {children}
        </CardContent>
    </Card>
  );

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
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            
            {/* COLUNA ESQUERDA: RESUMO */}
            <div className="space-y-6">
              
              {/* Projeto & Cliente */}
              <SummaryCard title="Projeto & Cliente" icon={Briefcase}>
                <p><span className="font-semibold">Projeto:</span> {project?.name}</p>
                <p><span className="font-semibold">Cliente:</span> {client?.name}</p>
                <p><span className="font-semibold">Tipo:</span> <Badge variant="secondary">{isB2B ? 'B2B Corporativo' : 'B2C Individual'}</Badge></p>
              </SummaryCard>

              {/* Identidade */}
              <SummaryCard title="Identidade" icon={User}>
                <p><span className="font-semibold">Nome:</span> {formData.name}</p>
                <p><span className="font-semibold">Categoria:</span> <Badge className="bg-[#FF6B35] text-white">{category?.name}</Badge></p>
                <p className="text-xs font-mono break-all"><span className="font-semibold">Domínio:</span> {fullDomain}</p>
              </SummaryCard>

              {/* Configuração */}
              <SummaryCard title="Configuração" icon={Settings}>
                <p className="flex items-center"><span className="font-semibold mr-2">Canais:</span> 
                    {formData.channel.map((c: string) => <Badge key={c} variant="outline" className="text-xs capitalize mr-1">{c}</Badge>)}
                </p>
                <p><span className="font-semibold">Modelo:</span> {model?.name}</p>
                <p className="flex items-center"><span className="font-semibold mr-2">Custo Est.:</span> <Badge className="bg-green-500 text-white">{model?.cost}</Badge></p>
              </SummaryCard>

              {/* Comportamento */}
              <SummaryCard title="Comportamento" icon={FileText}>
                <p className="flex items-center"><span className="font-semibold mr-2">System Prompt:</span> <CheckCircle className="h-4 w-4 text-green-500" /></p>
                <p><span className="font-semibold">Ferramentas:</span> 2 ativas (Mock)</p>
                <p><span className="font-semibold">Knowledge Base:</span> 3 itens (Mock)</p>
              </SummaryCard>

              <Separator />

              {/* Limite de Instâncias */}
              <div className="space-y-2">
                <Label className="font-semibold flex items-center text-[#0ca7d2]"><Users className="h-4 w-4 mr-2" /> Limite de Instâncias:</Label>
                {isB2B ? (
                    <Input readOnly defaultValue="500" className="font-mono bg-gray-100 dark:bg-gray-800" />
                ) : (
                    <p className="text-sm font-medium text-muted-foreground">Ilimitado (Conforme plano B2C)</p>
                )}
              </div>

              {/* Link de Cadastro */}
              <div className="space-y-2">
                <Label className="font-semibold flex items-center text-[#FF6B35]"><Copy className="h-4 w-4 mr-2" /> Link de Cadastro:</Label>
                <div className="flex space-x-2">
                    <Input readOnly value={mockLink} className="font-mono text-xs flex-grow" />
                    <Button variant="outline" size="icon" onClick={handleCopy}>
                        <Copy className="h-4 w-4" />
                    </Button>
                </div>
                <p className="text-xs text-muted-foreground">Compartilhe este link com os usuários que vão usar o agente.</p>
              </div>

              {/* Status Inicial */}
              <div className="space-y-2">
                <Label className="font-semibold flex items-center text-[#4e4ea8]"><Clock className="h-4 w-4 mr-2" /> Status Inicial:</Label>
                <RadioGroup 
                    value={initialStatus} 
                    onValueChange={(v) => setInitialStatus(v as 'ativo' | 'rascunho')}
                    className="flex space-x-4"
                >
                    <div className="flex items-center space-x-2">
                        <RadioGroupItem value="ativo" id="ativo" />
                        <Label htmlFor="ativo">Ativo (Implantar imediatamente)</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                        <RadioGroupItem value="rascunho" id="rascunho" />
                        <Label htmlFor="rascunho">Rascunho (Testar antes de ativar)</Label>
                    </div>
                </RadioGroup>
              </div>

            </div>

            {/* COLUNA DIREITA: TESTE FINAL */}
            <div className="space-y-6">
                <Card className="h-full border-2 border-[#FF6B35]">
                    <CardHeader className="p-4 border-b">
                        <CardTitle className="text-xl flex items-center text-[#FF6B35]">
                            <Play className="h-6 w-6 mr-2" /> Teste Final
                        </CardTitle>
                        <CardDescription>
                            Simule uma conversa para validar as instruções e o comportamento do agente.
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="h-[600px] p-0">
                        <PreviewChat />
                    </CardContent>
                </Card>
            </div>
          </div>
        </CardContent>
      </Card>
      
      {/* FOOTER */}
      <div className="flex justify-between pt-4 border-t">
        <Button
          variant="outline"
          onClick={onBack}
        >
          <ArrowLeft className="h-4 w-4 mr-2" /> Voltar
        </Button>
        
        <div className="flex space-x-2">
            <Button
                onClick={handleSaveDraft}
                variant="secondary"
            >
                <Save className="h-4 w-4 mr-2" /> Salvar Rascunho
            </Button>
            <Button 
                onClick={onDeploy} 
                size="lg" 
                className="bg-green-600 hover:bg-green-700 text-white"
            >
                <CheckCircle className="h-4 w-4 mr-2" /> {initialStatus === 'ativo' ? 'Criar e Ativar' : 'Criar Rascunho'}
            </Button>
        </div>
      </div>
    </div>
  );
};

export default Step5Review;