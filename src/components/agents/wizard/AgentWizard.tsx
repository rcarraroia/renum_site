import React, { useState, useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowLeft, ArrowRight, Zap } from 'lucide-react';
import Stepper from './Stepper';
import Step1Project from './Step1Project';
import Step2Identity from './Step2Identity';
import Step3Channel from './Step3Channel';
import Step4ConfigRenus from './Step4ConfigRenus';
import Step5Review from './Step5Review';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';
import { mockProjects, mockClients } from '@/mocks/agents.mock';

const steps = [
  'Projeto & Cliente',
  'Identidade',
  'Canal & Modelo',
  'Configuração RENUS',
  'Revisão & Teste',
];

const initialFormData = {
    project_id: mockProjects[0].id,
    client_id: mockProjects[0].client_id,
    type: mockClients.find(c => c.id === mockProjects[0].client_id)?.type || 'b2b_empresa',
    category: 'discovery',
    name: '',
    description: '',
    slug: '',
    channel: ['whatsapp'],
    model: 'gpt-4o-mini',
    // Mock for Renus Config state (complex object in real app)
    renus_config: {}, 
};

const AgentWizard: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState(initialFormData);
  const [isDeploying, setIsDeploying] = useState(false);
  const navigate = useNavigate();

  const CurrentStepComponent = useMemo(() => {
    switch (currentStep) {
      case 1:
        return <Step1Project formData={formData} setFormData={setFormData} onValidate={() => true} />;
      case 2:
        return <Step2Identity formData={formData} setFormData={setFormData} onValidate={() => true} />;
      case 3:
        return <Step3Channel formData={formData} setFormData={setFormData} onValidate={() => true} />;
      case 4:
        return <Step4ConfigRenus formData={formData} setFormData={setFormData} onValidate={() => true} />;
      case 5:
        return <Step5Review formData={formData} onDeploy={handleDeploy} />;
      default:
        return null;
    }
  }, [currentStep, formData]);

  const validateStep = () => {
    switch (currentStep) {
      case 1:
        if (!formData.project_id || !formData.client_id || !formData.category) {
          toast.error("Selecione o projeto, cliente e categoria.");
          return false;
        }
        return true;
      case 2:
        if (!formData.name || !formData.slug) {
          toast.error("Nome e Slug do agente são obrigatórios.");
          return false;
        }
        return true;
      case 3:
        if (formData.channel.length === 0 || !formData.model) {
          toast.error("Selecione pelo menos um canal e um modelo de IA.");
          return false;
        }
        return true;
      case 4:
        // Assume Renus config is valid for mock purposes
        return true;
      default:
        return true;
    }
  };

  const handleNext = () => {
    if (validateStep()) {
      setCurrentStep(prev => Math.min(prev + 1, steps.length));
    }
  };

  const handleBack = () => {
    setCurrentStep(prev => Math.max(prev - 1, 1));
  };

  const handleDeploy = () => {
    setIsDeploying(true);
    toast.info("Iniciando implantação do agente...");
    
    // Mock deployment process
    setTimeout(() => {
        setIsDeploying(false);
        toast.success(`Agente '${formData.name}' implantado com sucesso!`);
        // Redirect to the new agent's detail page (mock ID 100)
        navigate('/dashboard/admin/agents/100');
    }, 2500);
  };

  return (
    <Card className="max-w-4xl mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl flex items-center text-[#4e4ea8]">
          <Zap className="h-6 w-6 mr-2" /> Criar Novo Agente de IA
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Stepper steps={steps} currentStep={currentStep} />

        <div className="min-h-[400px] py-4">
          {CurrentStepComponent}
        </div>

        <div className="flex justify-between pt-4 border-t">
          <Button
            variant="outline"
            onClick={handleBack}
            disabled={currentStep === 1 || isDeploying}
          >
            <ArrowLeft className="h-4 w-4 mr-2" /> Anterior
          </Button>
          
          {currentStep < steps.length && (
            <Button
              onClick={handleNext}
              className="bg-[#FF6B35] hover:bg-[#e55f30]"
              disabled={isDeploying}
            >
              Próximo <ArrowRight className="h-4 w-4 ml-2" />
            </Button>
          )}
          
          {currentStep === steps.length && (
            <Button
              onClick={handleDeploy}
              className="bg-green-600 hover:bg-green-700"
              disabled={isDeploying}
            >
              {isDeploying ? 'Implantando...' : 'Implantar Agente'}
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default AgentWizard;