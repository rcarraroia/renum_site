import React, { useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowLeft, ArrowRight, Zap, Save, CheckCircle, Loader2 } from 'lucide-react';
import Stepper from './Stepper';
import { WizardStep1TypeSelection } from './steps/WizardStep1TypeSelection';
import { WizardStep2BasicInfo } from './steps/WizardStep2BasicInfo';
import { WizardStep3Personality } from './steps/WizardStep3Personality';
import { WizardStep4DataCollection } from './steps/WizardStep4DataCollection';
import { WizardStep5Integrations } from './steps/WizardStep5Integrations';
import { WizardStep6TestPublish } from './steps/WizardStep6TestPublish';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';
import { wizardService } from '@/services/wizardService';
import { WizardProvider, useWizard } from './WizardContext';

const steps = [
  'Tipo',
  'Identidade',
  'Personalidade',
  'Coleta',
  'Canais',
  'Publicação',
];

const WizardContent: React.FC = () => {
  const {
    data,
    setData,
    currentStep,
    setCurrentStep,
    wizardId,
    isSaving,
    saveStep
  } = useWizard();
  const navigate = useNavigate();
  const [isPublishing, setIsPublishing] = React.useState(false);

  const handleNext = async () => {
    if (!validateStep()) return;

    try {
      await saveStep(currentStep);
      setCurrentStep(Math.min(currentStep + 1, steps.length));
    } catch (error) {
      toast.error('Erro ao salvar progresso.');
    }
  };

  const handleBack = () => {
    setCurrentStep(Math.max(currentStep - 1, 1));
  };

  const handlePublish = async () => {
    if (!wizardId) return;
    setIsPublishing(true);
    try {
      const result = await wizardService.publishAgent(wizardId);
      toast.success('Agente publicado com sucesso!');
      navigate(`/dashboard/admin/agents/${result.slug || result.agent_id}`);
    } catch (error) {
      toast.error('Erro ao publicar agente.');
    } finally {
      setIsPublishing(false);
    }
  };

  const validateStep = () => {
    if (currentStep === 1 && !data.agent_type) {
      toast.error('Selecione o tipo de agente.');
      return false;
    }
    if (currentStep === 2 && (!data.name || data.name.length < 3)) {
      toast.error('Nome do agente é obrigatório e deve ter 3+ caracteres.');
      return false;
    }
    // Outras validações conforme necessário
    return true;
  };

  const CurrentStepComponent = useMemo(() => {
    switch (currentStep) {
      case 1: return <WizardStep1TypeSelection data={data} onChange={setData} />;
      case 2: return <WizardStep2BasicInfo />;
      case 3: return <WizardStep3Personality />;
      case 4: return <WizardStep4DataCollection />;
      case 5: return <WizardStep5Integrations />;
      case 6: return <WizardStep6TestPublish onPublish={handlePublish} />;
      default: return null;
    }
  }, [currentStep, data, setData]);

  return (
    <Card className="max-w-4xl mx-auto border-[#4e4ea8]/20 shadow-xl overflow-hidden">
      <CardHeader className="bg-gradient-to-r from-[#4e4ea8]/10 to-transparent border-b">
        <CardTitle className="text-2xl flex items-center text-[#4e4ea8]">
          <Zap className="h-6 w-6 mr-2 fill-[#FF6B35] text-[#FF6B35]" />
          Criar Novo Agente de IA
        </CardTitle>
      </CardHeader>
      <CardContent className="pt-6">
        <Stepper steps={steps} currentStep={currentStep} />

        <div className="min-h-[450px] py-8">
          {CurrentStepComponent}
        </div>

        <div className="flex justify-between items-center pt-6 border-t mt-4">
          <div className="flex items-center space-x-4">
            <Button
              variant="outline"
              onClick={handleBack}
              disabled={currentStep === 1 || isPublishing || isSaving}
              className="bg-background hover:bg-muted"
            >
              <ArrowLeft className="h-4 w-4 mr-2" /> Anterior
            </Button>

            {isSaving && (
              <div className="flex items-center text-xs text-muted-foreground animate-pulse">
                <Loader2 className="h-3 w-3 mr-1 animate-spin" />
                Salvando...
              </div>
            )}
          </div>

          <div className="flex items-center space-x-2">
            {currentStep < steps.length ? (
              <Button
                onClick={handleNext}
                className="bg-[#FF6B35] hover:bg-[#e55f30] text-white transition-all shadow-md active:scale-95"
                disabled={isPublishing || isSaving}
              >
                {isSaving ? 'Processando...' : 'Próximo'}
                <ArrowRight className="h-4 w-4 ml-2" />
              </Button>
            ) : (
              <Button
                onClick={handlePublish}
                className="bg-[#4e4ea8] hover:bg-[#3d3d8a] text-white shadow-lg active:scale-95 transition-all"
                disabled={isPublishing || isSaving}
              >
                {isPublishing ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Publicando...
                  </>
                ) : (
                  <>
                    Lançar Agente <CheckCircle className="h-4 w-4 ml-2" />
                  </>
                )}
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export const AgentWizard: React.FC = () => {
  return (
    <WizardProvider>
      <WizardContent />
    </WizardProvider>
  );
};

export default AgentWizard;
