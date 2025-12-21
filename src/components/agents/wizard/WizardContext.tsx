import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import { wizardService } from '@/services/wizardService';
import { toast } from 'sonner';

export interface WizardData {
    agent_type: 'template' | 'client' | 'system';
    category?: 'b2b' | 'b2c';
    client_id?: string;
    project_id?: string;
    name: string;
    description: string;
    niche: string;
    personality: string;
    tone_formal: number;
    tone_direct: number;
    collect_data: boolean;
    data_fields: any[];
    integrations: string[];
    is_template: boolean;
    model: string;
}

const initialData: WizardData = {
    agent_type: 'template',
    category: 'b2c',
    name: '',
    description: '',
    niche: 'generico',
    personality: 'professional',
    tone_formal: 50,
    tone_direct: 50,
    collect_data: false,
    data_fields: [],
    integrations: ['web'],
    is_template: false,
    model: 'gpt-4o-mini'
};

interface WizardContextType {
    data: WizardData;
    setData: (data: Partial<WizardData>) => void;
    currentStep: number;
    setCurrentStep: (step: number) => void;
    wizardId: string | null;
    isSaving: boolean;
    saveStep: (step: number) => Promise<void>;
    resetWizard: () => void;
}

const WizardContext = createContext<WizardContextType | undefined>(undefined);

export const WizardProvider: React.FC<{ children: React.ReactNode; initialWizardId?: string }> = ({
    children,
    initialWizardId
}) => {
    const [data, setWizardData] = useState<WizardData>(initialData);
    const [currentStep, setCurrentStep] = useState(1);
    const [wizardId, setWizardId] = useState<string | null>(initialWizardId || null);
    const [isSaving, setIsSaving] = useState(false);

    const setData = useCallback((newData: Partial<WizardData>) => {
        setWizardData(prev => ({ ...prev, ...newData }));
    }, []);

    const saveStep = async (step: number) => {
        if (!wizardId) {
            try {
                // Pass client_id AND category (if available) to start
                const session = await wizardService.startWizard(data.client_id, data.category);
                setWizardId(session.id);
            } catch (error) {
                console.error('Error starting wizard:', error);
                throw error;
            }
        }

        setIsSaving(true);
        try {
            await wizardService.saveStep(wizardId!, step, data);
        } catch (error) {
            console.error('Error saving step:', error);
            toast.error('Erro ao salvar progresso');
        } finally {
            setIsSaving(false);
        }
    };

    const resetWizard = () => {
        setWizardData(initialData);
        setCurrentStep(1);
        setWizardId(null);
    };

    return (
        <WizardContext.Provider value={{
            data,
            setData,
            currentStep,
            setCurrentStep,
            wizardId,
            isSaving,
            saveStep,
            resetWizard
        }}>
            {children}
        </WizardContext.Provider>
    );
};

export const useWizard = () => {
    const context = useContext(WizardContext);
    if (!context) {
        throw new Error('useWizard must be used within a WizardProvider');
    }
    return context;
};
