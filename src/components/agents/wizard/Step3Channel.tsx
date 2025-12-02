import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Zap, MessageSquare, Globe, DollarSign } from 'lucide-react';
import { mockChannels, mockModels } from '@/mocks/agents.mock';
import { AgentChannel } from '@/types/agent';
import { Checkbox } from '@/components/ui/checkbox';
import { cn } from '@/lib/utils';
import { Badge } from '@/components/ui/badge';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Alert, AlertDescription } from '@/components/ui/alert';

interface Step3ChannelProps {
  formData: any;
  setFormData: (data: any) => void;
  onValidate: () => boolean;
}

const Step3Channel: React.FC<Step3ChannelProps> = ({ formData, setFormData, onValidate }) => {
  const selectedModel = mockModels.find(m => m.id === formData.model);

  const handleChannelToggle = (channelId: AgentChannel, checked: boolean) => {
    const currentChannels = formData.channel || [];
    let newChannels: AgentChannel[];

    if (checked) {
      newChannels = [...currentChannels, channelId];
    } else {
      newChannels = currentChannels.filter((c: AgentChannel) => c !== channelId);
    }
    setFormData({ ...formData, channel: newChannels });
  };
  
  const getChannelDescription = (id: AgentChannel) => {
      switch (id) {
          case 'whatsapp': return 'Atendimento via WhatsApp Business';
          case 'web': return 'Widget de chat no website';
          case 'telegram': return 'Bot no Telegram';
          case 'sms': return 'Mensagens de texto';
          default: return 'Canal de comunicação.';
      }
  };

  return (
    <div className="space-y-6">
      {/* SEÇÃO 1: CANAIS DE ATENDIMENTO */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-[#4e4ea8]">
            <MessageSquare className="h-5 w-5 mr-2" /> Canais de Atendimento: *
          </CardTitle>
          <CardDescription>
            Selecione onde o agente estará ativo e interagindo com os usuários.
          </CardDescription>
        </CardHeader>
        <CardContent className="grid md:grid-cols-2 gap-4">
          {mockChannels.map(channel => (
            <div
              key={channel.id}
              className={cn(
                "flex items-start space-x-3 p-4 border rounded-lg cursor-pointer transition-all",
                formData.channel?.includes(channel.id) ? "border-2 border-[#FF6B35] bg-yellow-50/50 dark:bg-gray-800" : "hover:bg-gray-50 dark:hover:bg-gray-800"
              )}
              onClick={() => handleChannelToggle(channel.id as AgentChannel, !formData.channel?.includes(channel.id))}
            >
              <Checkbox
                id={channel.id}
                checked={formData.channel?.includes(channel.id)}
                onCheckedChange={(checked) => handleChannelToggle(channel.id as AgentChannel, checked as boolean)}
                className="h-5 w-5 mt-0.5"
              />
              <div className="flex items-start space-x-3">
                <span className="text-2xl">{channel.icon}</span>
                <div>
                  <Label htmlFor={channel.id} className="text-base font-medium cursor-pointer">{channel.name}</Label>
                  <p className="text-xs text-muted-foreground">
                    {getChannelDescription(channel.id as AgentChannel)}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* SEÇÃO 2: MODELO DE IA */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-[#FF6B35]">
            <Zap className="h-5 w-5 mr-2" /> Modelo de IA: *
          </CardTitle>
          <CardDescription>
            Escolha o modelo de linguagem que irá alimentar o agente.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <RadioGroup 
            value={formData.model} 
            onValueChange={(v) => setFormData({ ...formData, model: v })}
            className="grid md:grid-cols-2 gap-4"
          >
            {mockModels.map(m => (
              <div key={m.id}>
                <RadioGroupItem value={m.id} id={m.id} className="sr-only" />
                <Label 
                  htmlFor={m.id} 
                  className={cn(
                    "flex flex-col items-start space-y-3 p-4 border rounded-lg cursor-pointer transition-all h-full",
                    formData.model === m.id ? "border-2 border-[#4e4ea8] bg-blue-50/50 dark:bg-gray-800" : "hover:bg-gray-50 dark:hover:bg-gray-800"
                  )}
                >
                  <div className="flex items-center justify-between w-full">
                    <div className="flex items-center space-x-3">
                        <div className={cn(
                            "h-4 w-4 rounded-full border-2 flex items-center justify-center",
                            formData.model === m.id ? "border-[#4e4ea8]" : "border-gray-400"
                        )}>
                            <div className={cn(
                                "h-2 w-2 rounded-full",
                                formData.model === m.id ? "bg-[#4e4ea8]" : "bg-transparent"
                            )} />
                        </div>
                        <span className="text-lg font-bold">{m.name}</span>
                    </div>
                    {m.id === 'gpt-4o-mini' && <Badge className="bg-[#0ca7d2] text-white text-xs">Recomendado</Badge>}
                  </div>
                  
                  <div className="space-y-1 text-sm">
                    <p className="font-medium text-muted-foreground">
                        {m.provider} • <span className={cn(m.cost === '$$$' ? 'text-red-500' : 'text-green-500')}>{m.cost}</span>
                    </p>
                    <p className="text-xs text-muted-foreground">{m.description}</p>
                  </div>
                </Label>
              </div>
            ))}
          </RadioGroup>
        </CardContent>
      </Card>
      
      {/* ALERTA */}
      {selectedModel && (
        <Alert className="border-[#0ca7d2] bg-blue-50 dark:bg-blue-950">
          <DollarSign className="h-4 w-4 text-[#0ca7d2]" />
          <AlertDescription className="text-sm">
            💡 Custo estimado: <span className="font-semibold">{selectedModel.cost}</span>. 
            Exemplo: $0.02 por conversa com GPT-4o-mini.
          </AlertDescription>
        </Alert>
      )}
    </div>
  );
};

export default Step3Channel;