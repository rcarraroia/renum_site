/**
 * Triggers Tab - Sprint 07A
 * Component for managing automation triggers
 */

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Zap, Plus, Trash2, Play, CheckCircle, XCircle, RefreshCw } from 'lucide-react';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { triggerService, type Trigger } from '@/services/triggerService';

const TriggersTab: React.FC = () => {
  const [triggers, setTriggers] = useState<Trigger[]>([]);
  const [loading, setLoading] = useState(true);
  const [testing, setTesting] = useState<string | null>(null);
  const [toggling, setToggling] = useState<string | null>(null);

  useEffect(() => {
    loadTriggers();
  }, []);

  const loadTriggers = async () => {
    try {
      setLoading(true);
      const data = await triggerService.getTriggers();
      setTriggers(data);
    } catch (error) {
      console.error('Error loading triggers:', error);
      toast.error('Erro ao carregar gatilhos');
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (trigger: Trigger) => {
    try {
      setToggling(trigger.id);
      await triggerService.toggleTrigger(trigger.id, !trigger.active);
      toast.success(`Gatilho ${!trigger.active ? 'ativado' : 'desativado'} com sucesso`);
      await loadTriggers();
    } catch (error: any) {
      console.error('Error toggling trigger:', error);
      toast.error(error.message || 'Erro ao alterar status do gatilho');
    } finally {
      setToggling(null);
    }
  };

  const handleTest = async (trigger: Trigger) => {
    try {
      setTesting(trigger.id);
      toast.info(`Testando gatilho: ${trigger.name}...`);
      
      const result = await triggerService.testTrigger(trigger.id);
      
      if (result.success) {
        toast.success(`Gatilho testado com sucesso!`);
      } else {
        toast.error(`Falha no teste: ${result.message}`);
      }
    } catch (error: any) {
      console.error('Error testing trigger:', error);
      toast.error(error.message || 'Erro ao testar gatilho');
    } finally {
      setTesting(null);
    }
  };

  const handleDelete = async (trigger: Trigger) => {
    if (!confirm(`Tem certeza que deseja excluir o gatilho "${trigger.name}"?`)) {
      return;
    }

    try {
      await triggerService.deleteTrigger(trigger.id);
      toast.success('Gatilho excluído com sucesso');
      await loadTriggers();
    } catch (error: any) {
      console.error('Error deleting trigger:', error);
      toast.error(error.message || 'Erro ao excluir gatilho');
    }
  };

  const getTriggerTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      time_based: 'Baseado em Tempo',
      event_based: 'Baseado em Evento',
      condition_based: 'Baseado em Condição'
    };
    return labels[type] || type;
  };

  const getActionTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      send_message: 'Enviar Mensagem',
      send_email: 'Enviar Email',
      call_tool: 'Chamar Ferramenta',
      change_status: 'Mudar Status',
      notify_team: 'Notificar Equipe'
    };
    return labels[type] || type;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <RefreshCw className="h-6 w-6 animate-spin text-[#4e4ea8]" />
      </div>
    );
  }

  const activeTriggers = triggers.filter(t => t.active);

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-[#4e4ea8]">
                Gatilhos Ativos ({activeTriggers.length}/{triggers.length})
              </CardTitle>
              <CardDescription>
                Automatize ações com base em eventos e condições específicas
              </CardDescription>
            </div>
            <Button size="sm" onClick={() => toast.info('Funcionalidade de adicionar gatilho em desenvolvimento')}>
              <Plus className="h-4 w-4 mr-2" /> Novo Gatilho
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {triggers.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <Zap className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>Nenhum gatilho configurado</p>
              <p className="text-sm mt-2">Clique em "Novo Gatilho" para começar</p>
            </div>
          ) : (
            <div className="space-y-4">
              {triggers.map((trigger) => (
                <div
                  key={trigger.id}
                  className="p-4 border rounded-lg dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                >
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex items-start space-x-3">
                      {trigger.active ? (
                        <CheckCircle className="h-5 w-5 text-green-500 mt-0.5" />
                      ) : (
                        <XCircle className="h-5 w-5 text-gray-400 mt-0.5" />
                      )}
                      <div>
                        <h4 className="font-bold text-lg">{trigger.name}</h4>
                        {trigger.description && (
                          <p className="text-sm text-gray-500 mt-1">{trigger.description}</p>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleTest(trigger)}
                        disabled={testing === trigger.id}
                      >
                        <Play className={cn("h-4 w-4", testing === trigger.id && "animate-spin")} />
                      </Button>
                      <Switch
                        checked={trigger.active}
                        onCheckedChange={() => handleToggle(trigger)}
                        disabled={toggling === trigger.id}
                        className={cn(trigger.active && 'data-[state=checked]:bg-[#FF6B35]')}
                      />
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleDelete(trigger)}
                      >
                        <Trash2 className="h-4 w-4 text-red-500" />
                      </Button>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                    <div>
                      <Label className="text-muted-foreground">QUANDO (Trigger)</Label>
                      <p className="font-medium text-[#0ca7d2]">
                        {getTriggerTypeLabel(trigger.trigger_type)}
                      </p>
                    </div>
                    <div>
                      <Label className="text-muted-foreground">SE (Condition)</Label>
                      <p className="font-medium">
                        {trigger.condition_type || 'Sempre'}
                      </p>
                    </div>
                    <div>
                      <Label className="text-muted-foreground">ENTÃO (Action)</Label>
                      <p className="font-medium text-[#FF6B35]">
                        {getActionTypeLabel(trigger.action_type)}
                      </p>
                    </div>
                  </div>

                  {trigger.last_executed_at && (
                    <div className="mt-3 text-xs text-gray-500">
                      Última execução: {new Date(trigger.last_executed_at).toLocaleString('pt-BR')} 
                      {' '}({trigger.execution_count} execuções)
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default TriggersTab;
