import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Zap, MessageSquare, Globe, Settings, DollarSign, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { mockChannels, mockModels } from '@/mocks/agents.mock';
import { AgentChannel } from '@/types/agent';
import { Checkbox } from '@/components/ui/checkbox';
import { cn } from '@/lib/utils';
import { Badge } from '@/components/ui/badge';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { toast } from 'sonner';

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
  
  const handleModelChange = (modelId: string) => {
    setFormData({ ...formData, model: modelId });
  };

  const getModelCostColor = (cost: string) => {
    if (cost === '$$$') return 'text-red-500';
    if (cost === '$$') return 'text-green-500';
    return 'text-gray-500';
  };

  const getModelCostBadge = (cost: string) => {
    if (cost === '$$$') return 'bg-red-500 text-white';
    if (cost === '$$') return 'bg-green-500 text-white';
    return 'bg-gray-500 text-white';
  };

  const getChannelIcon = (icon: string) => {
    switch (icon) {
        case '📱': return <MessageSquare className="h-5 w-5 text-green-600" />;
        case '🌐': return <Globe className="h-5 w-5 text-blue-600" />;
        case '✈️': return <Zap className="h-5 w-5 text-purple-600" />;
        case '💬': return <MessageSquare className="h-5 w-5 text-gray-600" />;
        default: return <Zap className="h-5 w-5 text-muted-foreground" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* SEÇÃO 1: CANAIS DE ATENDIMENTO */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-[#4e4ea8]">
            <MessageSquare className="h-5 w-5 mr-2" /> Canais de Comunicação *
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
                {getChannelIcon(channel.icon)}
                <div>
                  <Label htmlFor={channel.id} className="text-base font-medium cursor-pointer">{channel.name}</Label>
                  <p className="text-xs text-muted-foreground">
                    {channel.id === 'whatsapp' ? 'Requer integração com API Business.' : channel.id === 'web' ? 'Widget embedável no site.' : channel.description}
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
            <Zap className="h-5 w-5 mr-2" /> Modelo de IA *
          </CardTitle>
          <CardDescription>
            Escolha o modelo de linguagem que irá alimentar o agente.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <RadioGroup 
            value={formData.model} 
            onValueChange={handleModelChange}
            className="grid md:grid-cols-2 gap-4"
          >
            {mockModels.map(m => (
              <div 
                key={m.id}
                className={cn(
                  "p-4 border rounded-lg cursor-pointer transition-all",
                  formData.model === m.id ? "border-2 border-[#4e4ea8] bg-blue-50/50 dark:bg-gray-800" : "hover:bg-gray-50 dark:hover:bg-gray-800"
                )}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value={m.id} id={m.id} />
                    <Label htmlFor={m.id} className="text-lg font-bold cursor-pointer flex items-center">
                      {m.name}
                      {m.id === 'gpt-4o-mini' && <Badge className="bg-[#0ca7d2] text-white text-xs ml-2">Recomendado</Badge>}
                    </Label>
                  </div>
                  <Badge className={getModelCostBadge(m.cost)}>{m.cost}</Badge>
                </div>
                <div className="ml-6 mt-1 space-y-1">
                  <p className="text-sm text-muted-foreground">
                    {m.provider} • <span className={getModelCostColor(m.cost)}>{m.cost}</span>
                  </p>
                  <p className="text-xs text-muted-foreground">{m.description}</p>
                </div>
              </div>
            ))}
          </RadioGroup>
        </CardContent>
      </Card>

      {/* ALERTA */}
      {selectedModel && (
        <Alert className="border-l-4 border-[#0ca7d2] bg-blue-50 dark:bg-blue-950">
          <AlertCircle className="h-4 w-4 text-[#0ca7d2]" />
          <AlertDescription>
            <strong>Custo estimado:</strong> O modelo <span className="font-semibold">{selectedModel.name}</span> tem um custo de <span className="font-semibold">{selectedModel.cost}</span>. Para o Agente de Vendas Slim, estimamos um custo de ~$0.02 por conversa.
          </AlertDescription>
        </Alert>
      )}
    </div>
  );
};

export default Step3Channel;