import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Settings } from 'lucide-react';
import ConfigRenusPanel from '../config/ConfigRenusPanel';
import PreviewChat from '../PreviewChat'; // Importando o PreviewChat

interface Step4ConfigRenusProps {
  formData: any;
  setFormData: (data: any) => void;
  onValidate: () => boolean;
}

const Step4ConfigRenus: React.FC<Step4ConfigRenusProps> = ({ formData, setFormData, onValidate }) => {
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
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Coluna 1 & 2: Configuração (ocupa 2/3) */}
            <div className="lg:col-span-2">
                <ConfigRenusPanel isGlobalConfig={false} />
            </div>
            
            {/* Coluna 3: Preview Chat (ocupa 1/3) */}
            <div className="lg:col-span-1 h-[700px] sticky top-4">
                <PreviewChat />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Step4ConfigRenus;