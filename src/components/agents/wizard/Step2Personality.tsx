import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Textarea } from '@/components/ui/textarea';
import { Briefcase, Smile, Cpu, Coffee } from 'lucide-react';

interface Step2PersonalityProps {
  formData: any;
  setFormData: (data: any) => void;
  onValidate: () => boolean;
}

const personalities = [
  {
    type: 'professional',
    name: 'Profissional',
    description: 'Formal, respeitoso e focado em resultados',
    icon: Briefcase,
    color: 'bg-blue-500',
  },
  {
    type: 'friendly',
    name: 'Amigável',
    description: 'Caloroso, empático e acolhedor',
    icon: Smile,
    color: 'bg-green-500',
  },
  {
    type: 'technical',
    name: 'Técnico',
    description: 'Preciso, detalhado e metódico',
    icon: Cpu,
    color: 'bg-purple-500',
  },
  {
    type: 'casual',
    name: 'Casual',
    description: 'Descontraído, natural e leve',
    icon: Coffee,
    color: 'bg-orange-500',
  },
];

const exampleConversations = {
  professional: {
    greeting: "Bom dia. Como posso auxiliá-lo hoje?",
    response: "Compreendo sua situação. Vou analisar as opções disponíveis e retornar com uma solução adequada.",
    closing: "Agradeço pelo contato. Estou à disposição para futuras necessidades."
  },
  friendly: {
    greeting: "Olá! Que bom ter você aqui! Como posso te ajudar hoje? 😊",
    response: "Entendo perfeitamente! Vamos resolver isso juntos. Tenho algumas ideias que podem te ajudar.",
    closing: "Foi um prazer conversar com você! Qualquer coisa, estou aqui, tá?"
  },
  technical: {
    greeting: "Olá. Identifique o problema para que eu possa diagnosticar a solução apropriada.",
    response: "Analisando os dados fornecidos, identifiquei três possíveis causas. Vamos proceder sistematicamente.",
    closing: "Processo concluído. Documentação enviada para referência futura."
  },
  casual: {
    greeting: "E aí! Tudo certo? No que posso dar uma força?",
    response: "Saquei! Olha, já passei por isso também. Deixa eu te mostrar um jeito fácil de resolver.",
    closing: "Valeu pela conversa! Qualquer coisa, só chamar!"
  },
};

const Step2Personality: React.FC<Step2PersonalityProps> = ({ formData, setFormData }) => {
  const selectedPersonality = formData.personality || 'professional';
  const toneFormal = formData.tone_formal ?? 50;
  const toneDirect = formData.tone_direct ?? 50;

  const handlePersonalitySelect = (personalityType: string) => {
    setFormData({ ...formData, personality: personalityType });
  };

  const examples = exampleConversations[selectedPersonality as keyof typeof exampleConversations] || exampleConversations.professional;

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Escolha a Personalidade</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {personalities.map((personality) => {
            const Icon = personality.icon;
            const isSelected = selectedPersonality === personality.type;
            
            return (
              <Card
                key={personality.type}
                className={`cursor-pointer transition-all hover:shadow-lg ${
                  isSelected ? 'ring-2 ring-[#FF6B35] shadow-lg' : ''
                }`}
                onClick={() => handlePersonalitySelect(personality.type)}
              >
                <CardContent className="p-4">
                  <div className="flex items-start space-x-3">
                    <div className={`${personality.color} p-2 rounded-lg`}>
                      <Icon className="h-5 w-5 text-white" />
                    </div>
                    <div className="flex-1">
                      <h4 className="font-semibold text-sm">{personality.name}</h4>
                      <p className="text-xs text-muted-foreground mt-1">
                        {personality.description}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>

      <div className="space-y-4">
        <div>
          <Label>Tom de Comunicação: Formal vs Informal</Label>
          <div className="flex items-center space-x-4 mt-2">
            <span className="text-xs text-muted-foreground w-16">Informal</span>
            <Slider
              value={[toneFormal]}
              onValueChange={(value) => setFormData({ ...formData, tone_formal: value[0] })}
              max={100}
              step={1}
              className="flex-1"
            />
            <span className="text-xs text-muted-foreground w-16 text-right">Formal</span>
          </div>
          <p className="text-xs text-muted-foreground mt-1 text-center">
            Nível: {toneFormal}%
          </p>
        </div>

        <div>
          <Label>Estilo de Resposta: Descritivo vs Direto</Label>
          <div className="flex items-center space-x-4 mt-2">
            <span className="text-xs text-muted-foreground w-20">Descritivo</span>
            <Slider
              value={[toneDirect]}
              onValueChange={(value) => setFormData({ ...formData, tone_direct: value[0] })}
              max={100}
              step={1}
              className="flex-1"
            />
            <span className="text-xs text-muted-foreground w-16 text-right">Direto</span>
          </div>
          <p className="text-xs text-muted-foreground mt-1 text-center">
            Nível: {toneDirect}%
          </p>
        </div>

        <div>
          <Label htmlFor="custom_instructions">Instruções Personalizadas (opcional)</Label>
          <Textarea
            id="custom_instructions"
            placeholder="Adicione instruções específicas para o comportamento do agente..."
            value={formData.custom_instructions || ''}
            onChange={(e) => setFormData({ ...formData, custom_instructions: e.target.value })}
            className="mt-1"
            rows={3}
          />
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-3">Preview de Conversação</h3>
        <Card>
          <CardContent className="p-4 space-y-3">
            <div className="bg-muted p-3 rounded-lg">
              <p className="text-sm font-medium mb-1">Saudação:</p>
              <p className="text-sm">{examples.greeting}</p>
            </div>
            <div className="bg-muted p-3 rounded-lg">
              <p className="text-sm font-medium mb-1">Resposta:</p>
              <p className="text-sm">{examples.response}</p>
            </div>
            <div className="bg-muted p-3 rounded-lg">
              <p className="text-sm font-medium mb-1">Encerramento:</p>
              <p className="text-sm">{examples.closing}</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Step2Personality;
