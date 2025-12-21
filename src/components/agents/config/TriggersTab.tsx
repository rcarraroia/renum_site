import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Zap, Plus, Trash2, Save, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';
import { Badge } from '@/components/ui/badge';
import agentService from '@/services/agentService';

interface TriggerCondition {
  field: string;
  operator: 'equals' | 'contains' | 'not_contains';
  value: string;
}

interface TriggerAction {
  type: 'send_message' | 'add_tag';
  params: {
    message?: string;
    tag?: string;
  };
}

interface TriggerRule {
  id: string;
  name: string;
  event: 'on_message_received' | 'on_idle';
  conditions: TriggerCondition[];
  actions: TriggerAction[];
  enabled: boolean;
}

interface TriggersTabProps {
  agentId?: string;
  clientMode?: boolean;
}

const TriggersTab: React.FC<TriggersTabProps> = ({ agentId: propAgentId }) => {
  const [agent, setAgent] = useState<any>(null);
  const [triggers, setTriggers] = useState<TriggerRule[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // New Rule State
  const [isCreating, setIsCreating] = useState(false);
  const [newRule, setNewRule] = useState<TriggerRule>({
    id: '',
    name: 'Nova Regra',
    event: 'on_message_received',
    conditions: [{ field: 'message', operator: 'contains', value: '' }],
    actions: [{ type: 'send_message', params: { message: '' } }],
    enabled: true
  });

  useEffect(() => {
    loadAgent();
  }, []);

  const loadAgent = async () => {
    try {
      setIsLoading(true);
      let foundAgent;
      if (propAgentId) {
        foundAgent = await agentService.getAgent(propAgentId);
      } else {
        const agents = await agentService.listAgents();
        foundAgent = agents.find((a: any) => a.slug === 'renus' || a.role === 'system_orchestrator');
      }

      if (foundAgent) {
        setAgent(foundAgent);
        // Load triggers from config or init empty
        const existingTriggers = foundAgent.config?.triggers || [];
        setTriggers(existingTriggers);
      }
    } catch (error) {
      toast.error("Erro ao carregar configurações de gatilhos.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveTriggers = async (updatedTriggers: TriggerRule[]) => {
    if (!agent) return;
    try {
      const updatedConfig = {
        ...agent.config,
        triggers: updatedTriggers
      };

      await agentService.updateAgent(agent.id, { config: updatedConfig });

      setTriggers(updatedTriggers);
      setAgent({ ...agent, config: updatedConfig });
      toast.success("Regras de automação salvas com sucesso!");
    } catch (error) {
      toast.error("Erro ao salvar regras.");
    }
  };

  const handleAddRule = () => {
    const ruleToAdd = { ...newRule, id: Date.now().toString() };
    if (!ruleToAdd.name) {
      toast.error("Dê um nome para a regra.");
      return;
    }
    const updated = [...triggers, ruleToAdd];
    handleSaveTriggers(updated);
    setIsCreating(false);
    // Reset new rule
    setNewRule({
      id: '',
      name: 'Nova Regra',
      event: 'on_message_received',
      conditions: [{ field: 'message', operator: 'contains', value: '' }],
      actions: [{ type: 'send_message', params: { message: '' } }],
      enabled: true
    });
  };

  const handleDeleteRule = (id: string) => {
    const updated = triggers.filter(t => t.id !== id);
    handleSaveTriggers(updated);
  };

  const handleToggleRule = (id: string) => {
    const updated = triggers.map(t => t.id === id ? { ...t, enabled: !t.enabled } : t);
    handleSaveTriggers(updated);
  };

  if (isLoading) return <div>Carregando...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-medium text-primary">Automação e Gatilhos</h3>
          <p className="text-sm text-muted-foreground">Configure o agente para reagir automaticamente a eventos.</p>
        </div>
        <Button onClick={() => setIsCreating(!isCreating)} className="gap-2">
          <Plus className="h-4 w-4" /> Nova Regra
        </Button>
      </div>

      {/* Configurar Nova Regra */}
      {isCreating && (
        <Card className="border-primary/50 bg-accent/5">
          <CardHeader>
            <CardTitle className="text-base">Criar Nova Automação</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <label className="text-sm font-medium">Nome da Regra</label>
              <Input
                value={newRule.name}
                onChange={e => setNewRule({ ...newRule, name: e.target.value })}
                placeholder="Ex: Responder se mencionar preço"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Quando (Evento)</label>
                <Select
                  value={newRule.event}
                  onValueChange={(val: any) => setNewRule({ ...newRule, event: val })}
                >
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="on_message_received">Ao receber mensagem</SelectItem>
                    <SelectItem value="on_idle">Se ficar inativo (Beta)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Condição (Se...)</label>
                <div className="flex gap-2">
                  <Select
                    value={newRule.conditions[0].operator}
                    onValueChange={(val: any) => {
                      const conds = [...newRule.conditions];
                      conds[0].operator = val;
                      setNewRule({ ...newRule, conditions: conds });
                    }}
                  >
                    <SelectTrigger className="w-[140px]"><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="contains">Mensagem contém</SelectItem>
                      <SelectItem value="equals">Mensagem igual a</SelectItem>
                      <SelectItem value="not_contains">Não contém</SelectItem>
                    </SelectContent>
                  </Select>
                  <Input
                    value={newRule.conditions[0].value}
                    onChange={e => {
                      const conds = [...newRule.conditions];
                      conds[0].value = e.target.value;
                      setNewRule({ ...newRule, conditions: conds });
                    }}
                    placeholder="Valor..."
                  />
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Ação (Então...)</label>
              <div className="flex gap-2">
                <Select
                  value={newRule.actions[0].type}
                  onValueChange={(val: any) => {
                    const acts = [...newRule.actions];
                    acts[0].type = val;
                    setNewRule({ ...newRule, actions: acts });
                  }}
                >
                  <SelectTrigger className="w-[180px]"><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="send_message">Enviar Mensagem</SelectItem>
                    <SelectItem value="add_tag">Adicionar Tag (CRM)</SelectItem>
                  </SelectContent>
                </Select>
                {newRule.actions[0].type === 'send_message' ? (
                  <Input
                    value={newRule.actions[0].params.message}
                    onChange={e => {
                      const acts = [...newRule.actions];
                      acts[0].params.message = e.target.value;
                      setNewRule({ ...newRule, actions: acts });
                    }}
                    placeholder="Digitar mensagem de resposta..."
                  />
                ) : (
                  <Input
                    value={newRule.actions[0].params.tag}
                    onChange={e => {
                      const acts = [...newRule.actions];
                      acts[0].params.tag = e.target.value;
                      setNewRule({ ...newRule, actions: acts });
                    }}
                    placeholder="Ex: interessado, vip"
                  />
                )}
              </div>
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <Button variant="ghost" onClick={() => setIsCreating(false)}>Cancelar</Button>
              <Button onClick={handleAddRule} className="gap-2"><Save className="h-4 w-4" /> Salvar Regra</Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Lista de Regras */}
      <div className="grid gap-4">
        {triggers.length === 0 ? (
          <div className="text-center py-10 border-2 border-dashed rounded-lg text-muted-foreground">
            <Zap className="h-10 w-10 mx-auto mb-2 opacity-20" />
            <p>Nenhuma regra de automação ativa.</p>
          </div>
        ) : (
          triggers.map(rule => (
            <Card key={rule.id} className={!rule.enabled ? "opacity-60 bg-muted/50" : ""}>
              <CardContent className="p-4 flex items-center justify-between">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <h4 className="font-semibold">{rule.name}</h4>
                    <Badge variant={rule.enabled ? "default" : "secondary"} className="text-[10px] h-5">
                      {rule.enabled ? "ATIVO" : "PAUSADO"}
                    </Badge>
                  </div>
                  <div className="text-sm text-muted-foreground flex items-center gap-2">
                    <span>QUANDO {rule.event === 'on_message_received' ? 'receber msg' : 'ficar inativo'}</span>
                    <span>→</span>
                    <span>SE {rule.conditions[0].operator} "{rule.conditions[0].value}"</span>
                    <span>→</span>
                    <span className="text-primary font-medium">
                      {rule.actions[0].type === 'send_message' ? `Enviar: "${rule.actions[0].params.message}"` : `Tag: ${rule.actions[0].params.tag}`}
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Button size="sm" variant="outline" onClick={() => handleToggleRule(rule.id)}>
                    {rule.enabled ? "Pausar" : "Ativar"}
                  </Button>
                  <Button size="icon" variant="ghost" className="text-destructive hover:bg-destructive/10" onClick={() => handleDeleteRule(rule.id)}>
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};

export default TriggersTab;