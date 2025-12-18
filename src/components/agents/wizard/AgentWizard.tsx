import React, { useState, useMemo, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowLeft, ArrowRight, Zap, Save, CheckCircle } from 'lucide-react';
import Stepper from './Stepper';
import Step1Context from './Step1Context';
import Step2Identity from './Step2Identity';
import Step3Technical from './Step3Technical';
import Step4Behavior from './Step4Behavior';
import Step5Tools from './Step5Tools';
import Step5TestPublish from './Step5TestPublish';
import { toast } from 'sonner';
import { useNavigate, useParams } from 'react-router-dom';
import { wizardService } from '@/services/wizardService';

const steps = [
  'Contexto',
  'Identidade',
  'Config. Técnica',
  'Comportamento',
  'Ferramentas',
  'Publicação',
];

const initialFormData = {
  // Step 1: Contexto
  project_id: '',
  client_id: '',
  contract_type: 'b2b_empresa',

  // Step 2: Identidade
  name: '',
  description: '',
  niche: 'generico',
  template_type: 'custom',

  // Step 3: Técnica
  channels: ['web'],
  model: 'gpt-4o-mini',

  // Step 4: Comportamento
  personality: 'professional',
  tone_formal: 50,
  tone_direct: 50,
  system_prompt: '',
  custom_instructions: '',

  // Step 5: Ferramentas & Integrações
  standard_fields: {},
  custom_fields: [],
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

      setFormData({
        project_id: wizard.step_1_data?.project_id || '',
        client_id: wizard.step_1_data?.client_id || '',
        contract_type: wizard.step_1_data?.contract_type || 'b2b_empresa',
        name: wizard.step_2_data?.name || '',
        description: wizard.step_2_data?.description || '',
        niche: wizard.step_2_data?.niche || 'generico',
        template_type: wizard.step_2_data?.template_type || 'custom',
        channels: wizard.step_3_data?.channels || ['web'],
        model: wizard.step_3_data?.model || 'gpt-4o-mini',
        personality: wizard.step_4_data?.personality || 'professional',
        tone_formal: wizard.step_4_data?.tone_formal || 50,
        tone_direct: wizard.step_4_data?.tone_direct || 50,
        system_prompt: wizard.step_4_data?.system_prompt || '',
        custom_instructions: wizard.step_4_data?.custom_instructions || '',
        standard_fields: wizard.step_5_data?.standard_fields || {},
        custom_fields: wizard.step_5_data?.custom_fields || [],
        integrations: wizard.step_5_data?.integrations || {},
      });

      setCurrentStep(wizard.current_step || 1);
      setCurrentWizardId(id);
      toast.success('Wizard carregado com sucesso');
    } catch (error) {
      console.error('Error loading wizard:', error);
      toast.error('Erro ao carregar wizard');
    }
  };

  const createWizard = async () => {
    try {
      // We need a client_id to start. For now, let's use a default or ask? 
      // Actually, startWizard on backend expects a UUID. 
      // Mocking a default client ID for internal use if not selected yet
      const defaultClientId = "00000000-0000-0000-0000-000000000000";
      const wizard = await wizardService.startWizard(defaultClientId);
      setCurrentWizardId(wizard.id);
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
            project_id: formData.project_id,
            client_id: formData.client_id,
            contract_type: formData.contract_type,
          };
          break;
        case 2:
          stepData = {
            name: formData.name,
            description: formData.description,
            niche: formData.niche,
            template_type: formData.template_type,
          };
          break;
        case 3:
          stepData = {
            channels: formData.channels,
            model: formData.model,
          };
          break;
        case 4:
          stepData = {
            personality: formData.personality,
            tone_formal: formData.tone_formal,
            tone_direct: formData.tone_direct,
            system_prompt: formData.system_prompt,
            custom_instructions: formData.custom_instructions,
          };
          break;
        case 5:
          stepData = {
            standard_fields: formData.standard_fields,
            custom_fields: formData.custom_fields,
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
        return <Step1Context formData={formData} setFormData={setFormData} onValidate={() => true} />;
      case 2:
        return <Step2Identity formData={formData} setFormData={setFormData} />;
      case 3:
        return <Step3Technical formData={formData} setFormData={setFormData} />;
      case 4:
        return <Step4Behavior formData={formData} setFormData={setFormData} />;
      case 5:
        return <Step5Tools formData={formData} setFormData={setFormData} />;
      case 6:
        return <Step5TestPublish formData={formData} onPublish={handleDeploy} />;
      default:
        return null;
    }
  }, [currentStep, formData]);

  const validateStep = () => {
    switch (currentStep) {
      case 1:
        if (!formData.client_id || !formData.project_id) {
          toast.error("Selecione um Cliente e um Projeto.");
          return false;
        }
        return true;
      case 2:
        if (!formData.name || formData.name.length < 3) {
          toast.error("Nome do agente deve ter no mínimo 3 caracteres.");
          return false;
        }
        return true;
      case 3:
        if (!formData.channels || formData.channels.length === 0) {
          toast.error("Selecione pelo menos um canal.");
          return false;
        }
        return true;
      case 4:
        if (!formData.system_prompt) {
          toast.error("Defina o System Prompt do agente.");
          return false;
        }
        return true;
      case 5:
        // Tools/Integrations are optional but usually recommended
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


  const handleDeploy = async () => {
    if (!currentWizardId) return;

    setIsDeploying(true);
    toast.info("Publicando e implantando agente...");

    try {
      const result = await wizardService.publishAgent(currentWizardId);
      toast.success(`Agente '${formData.name}' implantado com sucesso!`);
      // Redirect to details page
      navigate(`/dashboard/admin/agents/${result.slug}`);
    } catch (error) {
      console.error('Error publishing agent:', error);
      toast.error('Erro ao implantar agente. Verifique os logs.');
    } finally {
      setIsDeploying(false);
    }
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