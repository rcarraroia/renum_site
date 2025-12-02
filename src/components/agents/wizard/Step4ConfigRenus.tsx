import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Settings } from 'lucide-react';
import ConfigRenusPanel from '../config/ConfigRenusPanel';

interface Step4ConfigRenusProps {
  formData: any;
  setFormData: (data: any) => void;
  onValidate: () => boolean;
}

const Step4ConfigRenus: React.FC<Step4ConfigRenusProps> = ({ formData, setFormData, onValidate }) => {
  // Note: In a real scenario, this step would manage the complex state of all nested config tabs.
  // For this mock, we simply display the configuration panel.

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-[#4e4ea8]">
            <Settings className="h-5 w-5 mr-2" /> 4. Configuração do Agente (Renus)
          </CardTitle>
          <CardDescription>
            Defina as instruções, ferramentas, conhecimento e políticas de segurança específicas para este agente.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {/* The ConfigRenusPanel handles all nested tabs */}
          <ConfigRenusPanel isGlobalConfig={false} />
        </CardContent>
      </Card>
    </div>
  );
};

export default Step4ConfigRenus;