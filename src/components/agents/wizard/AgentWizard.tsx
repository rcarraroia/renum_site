import React, { useState, useMemo, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowLeft, ArrowRight, Zap, Save, CheckCircle } from 'lucide-react';
import Stepper from './Stepper';
import Step1Objective from './Step1Objective';
import Step2Personality from './Step2Personality';
import Step3Fields from './Step3Fields';
import Step4Integrations from './Step4Integrations';
import Step5TestPublish from './Step5TestPublish';
import { toast } from 'sonner';
import { useNavigate, useParams } from 'react-router-dom';
import { wizardService } from '@/services/wizardService';

const steps = [
  'Objetivo do Agente',
  'Personalidade e Tom',
  'Informações a Coletar',
  'Integrações',
  'Teste e Publicação',
];

const initialFormData = {
    // Step 1: Objetivo
    template_type: 'custom',
    name: '',
    description: '',
    niche: 'generico',
    
    // Step 2: Personalidade
    personality: 'professional',
    tone_formal: 50,
    tone_direct: 50,
    custom_instructions: '',
    
    // Step 3: Campos
    standard_fields: {},
    custom_fields: [],
    
    // Step 4: Integrações
    integrations: {},
};

const AgentWizard: React.FC = () => {
  const { wizardId } = useParams<{ wizardId?: string }>();
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState(initialFormData);
  const [isDeploying, setIsDeploying] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');
  const [currentWizardId, setCurrentWizardId] = useState<string | null>(wizardId || null);
  const navigate = useNavigate();

  // Load existing wizard on mount
  useEffect(() => {
    if (wizardId) {
      loadWizard(wizardId);
    } else {
      // Create new wizard session
      createWizard();
    }
  }, [wizardId]);

  const loadWizard = async (id: string) => {
    try {
      const wizard = await wizardService.getWizard(id);
      
      // Reconstruct form data from wizard config
      const config = wizard.config || {};
      setFormData({
        template_type: config.step_1_data?.template_type || 'custom',
        name: config.step_1_data?.name || '',
        description: config.step_1_data?.description || '',
        niche: config.step_1_data?.niche || 'generico',
        personality: config.step_2_data?.personality || 'professional',
        tone_formal: config.step_2_data?.tone_formal || 50,
        tone_direct: config.step_2_data?.tone_direct || 50,
        custom_instructions: config.step_2_data?.custom_instructions || '',
        standard_fields: config.step_3_data?.standard_fields || {},
        custom_fields: config.step_3_data?.custom_fields || [],
        integrations: config.step_4_data?.integrations || {},
      });
      
      setCurrentStep(config.current_step || 1);
      setCurrentWizardId(id);
      toast.success('Wizard carregado com sucesso');
    } catch (error) {
      console.error('Error loading wizard:', error);
      toast.error('Erro ao carregar wizard');
    }
  };

  const createWizard = async () => {
    try {
      const wizard = await wizardService.startWizard({
        template_type: 'custom',
        name: '',
      });
      setCurrentWizardId(wizard.id);
      // Update URL without reload
      window.history.replaceState(null, '', `/dashboard/admin/agents/wizard/${wizard.id}`);
    } catch (error) {
      console.error('Error creating wizard:', error);
      toast.error('Erro ao criar wizard');
    }
  };

  const autoSave = async (stepNumber: number) => {
    if (!currentWizardId) return;

    setIsSaving(true);
    setSaveStatus('saving');

    try {
      // Prepare step data based on current step
      let stepData: any = {};
      
      switch (stepNumber) {
        case 1:
          stepData = {
            template_type: formData.template_type,
            name: formData.name,
            description: formData.description,
            niche: formData.niche,
          };
          break;
        case 2:
          stepData = {
            personality: formData.personality,
            tone_formal: formData.tone_formal,
            tone_direct: formData.tone_direct,
            custom_instructions: formData.custom_instructions,
          };
          break;
        case 3:
          stepData = {
            standard_fields: formData.standard_fields,
            custom_fields: formData.custom_fields,
          };
          break;
        case 4:
          stepData = {
            integrations: formData.integrations,
          };
          break;
      }

      await wizardService.saveStep(currentWizardId, stepNumber, stepData);
      
      setSaveStatus('saved');
      setTimeout(() => setSaveStatus('idle'), 2000);
    } catch (error) {
      console.error('Error saving wizard:', error);
      setSaveStatus('error');
      toast.error('Erro ao salvar progresso');
    } finally {
      setIsSaving(false);
    }
  };

  const handleBack = () => {
    setCurrentStep(prev => Math.max(prev - 1, 1));
  };

  const CurrentStepComponent = useMemo(() => {
    switch (currentStep) {
      case 1:
        return <Step1Objective formData={formData} setFormData={setFormData} onValidate={() => true} />;
      case 2:
        return <Step2Personality formData={formData} setFormData={setFormData} onValidate={() => true} />;
      case 3:
        return <Step3Fields formData={formData} setFormData={setFormData} onValidate={() => true} />;
      case 4:
        return <Step4Integrations formData={formData} setFormData={setFormData} onValidate={() => true} />;
      case 5:
        return <Step5TestPublish formData={formData} onPublish={handleDeploy} />;
      default:
        return null;
    }
  }, [currentStep, formData]);

  const validateStep = () => {
    switch (currentStep) {
      case 1:
        if (!formData.template_type) {
          toast.error("Selecione um template.");
          return false;
        }
        if (!formData.name || formData.name.length < 3) {
          toast.error("Nome do agente deve ter no mínimo 3 caracteres.");
          return false;
        }
        if (!formData.niche) {
          toast.error("Selecione um nicho de negócio.");
          return false;
        }
        return true;
      case 2:
        if (!formData.personality) {
          toast.error("Selecione uma personalidade.");
          return false;
        }
        return true;
      case 3:
        const enabledStandard = Object.values(formData.standard_fields || {}).filter((f: any) => f.enabled).length;
        const customCount = (formData.custom_fields || []).length;
        if (enabledStandard === 0 && customCount === 0) {
          toast.error("Selecione pelo menos um campo para coletar.");
          return false;
        }
        return true;
      case 4:
        // Integrations are optional
        return true;
      case 5:
        // Final step, no validation needed
        return true;
      default:
        return true;
    }
  };

  const handleNext = async () => {
    if (validateStep()) {
      // Auto-save current step before moving to next
      await autoSave(currentStep);
      setCurrentStep(prev => Math.min(prev + 1, steps.length));
    }
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

        <div className="flex justify-between items-center pt-4 border-t">
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              onClick={handleBack}
              disabled={currentStep === 1 || isDeploying || isSaving}
            >
              <ArrowLeft className="h-4 w-4 mr-2" /> Anterior
            </Button>
            
            {/* Save status indicator */}
            {saveStatus !== 'idle' && (
              <div className="flex items-center text-sm">
                {saveStatus === 'saving' && (
                  <>
                    <Save className="h-4 w-4 mr-1 animate-pulse text-blue-500" />
                    <span className="text-muted-foreground">Salvando...</span>
                  </>
                )}
                {saveStatus === 'saved' && (
                  <>
                    <CheckCircle className="h-4 w-4 mr-1 text-green-500" />
                    <span className="text-green-600">Salvo</span>
                  </>
                )}
                {saveStatus === 'error' && (
                  <span className="text-red-600">Erro ao salvar</span>
                )}
              </div>
            )}
          </div>
          
          {currentStep < steps.length && (
            <Button
              onClick={handleNext}
              className="bg-[#FF6B35] hover:bg-[#e55f30]"
              disabled={isDeploying || isSaving}
            >
              {isSaving ? 'Salvando...' : 'Próximo'} <ArrowRight className="h-4 w-4 ml-2" />
            </Button>
          )}
          
          {currentStep === steps.length && (
            <Button
              onClick={handleDeploy}
              className="bg-green-600 hover:bg-green-700"
              disabled={isDeploying || isSaving}
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