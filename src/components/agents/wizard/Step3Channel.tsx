import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Zap, MessageSquare, Globe, Settings, DollarSign } from 'lucide-react';
import { mockChannels, mockModels } from '@/mocks/agents.mock';
import { AgentChannel } from '@/types/agent';
import { Checkbox } from '@/components/ui/checkbox';
import { cn } from '@/lib/utils';
import { Badge } from '@/components/ui/badge';

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

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-[#4e4ea8]">
            <MessageSquare className="h-5 w-5 mr-2" /> 3. Canais de Comunicação
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
                "flex items-center space-x-3 p-4 border rounded-lg cursor-pointer transition-all",
                formData.channel?.includes(channel.id) ? "border-2 border-[#FF6B35] bg-yellow-50/50 dark:bg-gray-800" : "hover:bg-gray-50 dark:hover:bg-gray-800"
              )}
              onClick={() => handleChannelToggle(channel.id as AgentChannel, !formData.channel?.includes(channel.id))}
            >
              <Checkbox
                id={channel.id}
                checked={formData.channel?.includes(channel.id)}
                onCheckedChange={(checked) => handleChannelToggle(channel.id as AgentChannel, checked as boolean)}
                className="h-5 w-5"
              />
              <div className="flex items-center space-x-3">
                <span className="text-2xl">{channel.icon}</span>
                <div>
                  <Label htmlFor={channel.id} className="text-base font-medium cursor-pointer">{channel.name}</Label>
                  <p className="text-xs text-muted-foreground">
                    {channel.id === 'whatsapp' ? 'Requer integração com API Business.' : channel.id === 'web' ? 'Widget embedável no site.' : 'Em breve.'}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-[#FF6B35]">
            <Zap className="h-5 w-5 mr-2" /> Modelo de IA
          </CardTitle>
          <CardDescription>
            Escolha o modelo de linguagem que irá alimentar o agente.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="model">Modelo de IA</Label>
            <Select value={formData.model} onValueChange={(v) => setFormData({ ...formData, model: v })}>
              <SelectTrigger>
                <SelectValue placeholder="Selecione o Modelo" />
              </SelectTrigger>
              <SelectContent>
                {mockModels.map(m => (
                  <SelectItem key={m.id} value={m.id}>
                    <div className="flex items-center justify-between w-full">
                      <span>{m.name} ({m.provider})</span>
                      <div className="flex items-center space-x-2 ml-4">
                        <Badge variant="outline" className={cn(m.cost === '$$$' ? 'border-red-500 text-red-700' : m.cost === '$$' ? 'border-green-500 text-green-700' : 'border-gray-500 text-gray-700', 'text-xs')}>
                            {m.cost}
                        </Badge>
                        {m.id === 'gpt-4o-mini' && <Badge className="bg-[#0ca7d2] text-white text-xs">Recomendado</Badge>}
                      </div>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          {selectedModel && (
            <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg text-sm flex items-center space-x-2">
                <DollarSign className="h-4 w-4 text-muted-foreground" />
                <p className="text-muted-foreground">
                    Custo: <span className="font-semibold">{selectedModel.cost}</span> | Descrição: {selectedModel.description}
                </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Step3Channel;