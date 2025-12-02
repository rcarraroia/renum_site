import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Zap, Plus, Trash2, Clock, MessageSquare, Send, Bell, CheckCircle, Settings, Play } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { toast } from 'sonner';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { cn } from '@/lib/utils';

interface Trigger {
  id: number;
  name: string;
  status: 'active' | 'inactive';
  when: string;
  condition: string;
  action: string;
}

const MOCK_TRIGGERS: Trigger[] = [
  {
    id: 1,
    name: 'Follow-up de Inatividade',
    status: 'active',
    when: '3 dias após a última mensagem do Renus',
    condition: 'Status da conversa: Aberta',
    action: 'Enviar mensagem de follow-up (Template 1)',
  },
  {
    id: 2,
    name: 'Alerta de Intenção Crítica',
    status: 'active',
    when: 'Intenção detectada: "Cancelamento" ou "Reclamação"',
    condition: 'Role do usuário: Cliente',
    action: 'Notificar Equipe de Sucesso do Cliente',
  },
  {
    id: 3,
    name: 'Geração Automática de Relatório',
    status: 'inactive',
    when: 'Conversa atinge 10 turnos',
    condition: 'Tópico: Discovery',
    action: 'Chamar ferramenta: generate_viability_report',
  },
];

const TriggersTab: React.FC = () => {
  const [triggers, setTriggers] = useState(MOCK_TRIGGERS);
  const [isTesting, setIsTesting] = useState(false);

  const handleToggle = (id: number) => {
    setTriggers(triggers.map(t => (t.id === id ? { ...t, status: t.status === 'active' ? 'inactive' : 'active' } : t)));
    toast.info("Status do gatilho atualizado.");
  };

  const handleTestTrigger = (name: string) => {
    setIsTesting(true);
    toast.info(`Simulando gatilho: ${name}...`);
    setTimeout(() => {
      setIsTesting(false);
      toast.success(`Gatilho '${name}' disparado com sucesso. Ação simulada: Notificação enviada.`);
    }, 1500);
  };

  return (
    <div className="space-y-8">
      <Card>
        <CardHeader>
          <CardTitle className="text-[#4e4ea8]">Gatilhos Ativos ({triggers.filter(t => t.status === 'active').length})</CardTitle>
          <CardDescription>Automatize ações do Renus com base em eventos e condições específicas.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {triggers.map(trigger => (
            <div key={trigger.id} className="p-4 border rounded-lg dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
              <div className="flex justify-between items-start mb-2">
                <h4 className="font-bold text-lg flex items-center">
                    <CheckCircle className={cn("h-5 w-5 mr-2", trigger.status === 'active' ? 'text-green-500' : 'text-red-500')} />
                    {trigger.name}
                </h4>
                <div className="flex items-center space-x-3">
                    <Button variant="outline" size="sm" onClick={() => handleTestTrigger(trigger.name)} disabled={isTesting}>
                        <Play className="h-4 w-4" />
                    </Button>
                    <Switch
                        checked={trigger.status === 'active'}
                        onCheckedChange={() => handleToggle(trigger.id)}
                        className={cn(trigger.status === 'active' ? 'data-[state=checked]:bg-[#FF6B35]' : '')}
                    />
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm mt-2">
                <div>
                    <Label className="text-muted-foreground">QUANDO (Trigger)</Label>
                    <p className="font-medium text-[#0ca7d2]">{trigger.when}</p>
                </div>
                <div>
                    <Label className="text-muted-foreground">SE (Condition)</Label>
                    <p className="font-medium">{trigger.condition}</p>
                </div>
                <div>
                    <Label className="text-muted-foreground">ENTÃO (Action)</Label>
                    <p className="font-medium text-[#FF6B35]">{trigger.action}</p>
                </div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      <Card className="border-2 border-dashed border-[#4e4ea8] dark:border-[#0ca7d2]">
        <CardHeader>
          <CardTitle className="flex items-center text-[#FF6B35]">
            <Plus className="h-5 w-5 mr-2" /> Novo Gatilho de Automação
          </CardTitle>
          <CardDescription>Crie um novo fluxo de automação baseado em eventos.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
            <div className="space-y-2">
                <Label>Nome do Gatilho</Label>
                <Input placeholder="Ex: Alerta de Lead Quente" />
            </div>
            
            <Separator />

            <h5 className="font-semibold text-sm text-[#0ca7d2]">1. QUANDO (Trigger)</h5>
            <div className="grid md:grid-cols-2 gap-4">
                <Select>
                    <SelectTrigger><SelectValue placeholder="Selecione o Evento..." /></SelectTrigger>
                    <SelectContent>
                        <SelectItem value="new_conv">Nova Conversa Iniciada</SelectItem>
                        <SelectItem value="intent_detect">Intenção Específica Detectada</SelectItem>
                        <SelectItem value="keyword">Palavra-chave Mencionada</SelectItem>
                        <SelectItem value="time_delay">Atraso de Tempo (Ex: 24h)</SelectItem>
                    </SelectContent>
                </Select>
                <Input placeholder="Detalhe a condição (Ex: 'Intenção: Vendas')" />
            </div>

            <h5 className="font-semibold text-sm text-[#FF6B35]">2. ENTÃO (Action)</h5>
            <div className="grid md:grid-cols-2 gap-4">
                <Select>
                    <SelectTrigger><SelectValue placeholder="Selecione a Ação..." /></SelectTrigger>
                    <SelectContent>
                        <SelectItem value="send_msg">Enviar Mensagem Específica</SelectItem>
                        <SelectItem value="notify_team">Notificar Equipe</SelectItem>
                        <SelectItem value="call_tool">Chamar Ferramenta Externa</SelectItem>
                        <SelectItem value="change_status">Mudar Status da Conversa</SelectItem>
                    </SelectContent>
                </Select>
                <Input placeholder="Detalhe a ação (Ex: 'Enviar para Slack #vendas')" />
            </div>

            <Button className="w-full bg-[#4e4ea8] hover:bg-[#3a3a80]">
                <Settings className="h-4 w-4 mr-2" /> Salvar Novo Gatilho
            </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default TriggersTab;