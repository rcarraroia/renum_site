import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { siccService } from '@/services/siccService';
import { agentService } from '@/services/agentService';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { Slider } from '@/components/ui/slider';
import { Settings, Save, RotateCcw, AlertTriangle } from 'lucide-react';
import { useToast } from "@/components/ui/use-toast";

export default function SettingsPage() {
  const [learningEnabled, setLearningEnabled] = useState(true);
  const [autoApprovalThreshold, setAutoApprovalThreshold] = useState([80]);
  const [memoryLimit, setMemoryLimit] = useState([10000]);
  const [loading, setLoading] = useState(true);
  const [activeSnapshots, setActiveSnapshots] = useState<any[]>([]);
  const [agentId, setAgentId] = useState<string | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    const init = async () => {
      try {
        const agent = await agentService.getSystemAgent('system_orchestrator');
        if (agent) {
          setAgentId(agent.id);
          loadSettings(agent.id);
          loadSnapshots(agent.id);
        } else {
          setLoading(false);
        }
      } catch (error) {
        console.error('Error fetching system agent:', error);
        setLoading(false);
      }
    };
    init();
  }, []);

  const loadSettings = async (id: string) => {
    try {
      const data = await siccService.getSettings(id);
      if (data) {
        setLearningEnabled(data.learning_enabled ?? true);
        setAutoApprovalThreshold([data.auto_approval_threshold ? data.auto_approval_threshold * 100 : 80]);
        setMemoryLimit([data.max_memory_items || 10000]);
      }
    } catch (error) {
      console.error('Erro ao carregar settings:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadSnapshots = async (id: string) => {
    try {
      const data = await siccService.listSnapshots(id);
      setActiveSnapshots(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Erro ao carregar snapshots', error);
    }
  };

  const handleSave = async () => {
    if (!agentId) return;
    try {
      await siccService.updateSettings(agentId, {
        learning_enabled: learningEnabled,
        auto_approval_threshold: autoApprovalThreshold[0] / 100,
        max_memory_items: memoryLimit[0]
      });
      toast({
        title: "Sucesso",
        description: "Configurações salvas com sucesso.",
        variant: "default"
      });
    } catch (error) {
      toast({
        title: "Erro",
        description: "Falha ao salvar configurações.",
        variant: "destructive"
      });
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="p-6 flex justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold">⚙️ Configurações IA</h1>
          <div className="flex space-x-2">
            <Button variant="outline">
              <RotateCcw className="h-4 w-4 mr-2" />
              Restaurar Padrões
            </Button>
            <Button className="bg-purple-600 hover:bg-purple-700" onClick={handleSave}>
              <Save className="h-4 w-4 mr-2" />
              Salvar Alterações
            </Button>
          </div>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>🎛️ Configurações de Aprendizado</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">Aprendizado Automático</p>
                  <p className="text-sm text-muted-foreground">
                    Permite que o agente aprenda automaticamente com conversas
                  </p>
                </div>
                <Switch
                  checked={learningEnabled}
                  onCheckedChange={setLearningEnabled}
                />
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <p className="font-medium">Limite de Auto-Aprovação</p>
                  <Badge variant="outline">{autoApprovalThreshold[0]}%</Badge>
                </div>
                <Slider
                  value={autoApprovalThreshold}
                  onValueChange={setAutoApprovalThreshold}
                  max={100}
                  min={50}
                  step={5}
                  className="w-full"
                />
                <p className="text-xs text-muted-foreground">
                  Aprendizados com confiança acima deste valor são aprovados automaticamente
                </p>
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <p className="font-medium">Limite de Memórias</p>
                  <Badge variant="outline">{memoryLimit[0].toLocaleString()}</Badge>
                </div>
                <Slider
                  value={memoryLimit}
                  onValueChange={setMemoryLimit}
                  max={50000}
                  min={1000}
                  step={1000}
                  className="w-full"
                />
                <p className="text-xs text-muted-foreground">
                  Número máximo de memórias que o agente pode armazenar
                </p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>📊 Status do Sistema</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <div>
                  <p className="font-medium text-green-800">Sistema SICC</p>
                  <p className="text-sm text-green-600">Funcionando normalmente</p>
                </div>
                <Badge className="bg-green-600">Ativo</Badge>
              </div>

              <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                <div>
                  <p className="font-medium text-blue-800">Análise de Conversas</p>
                  <p className="text-sm text-blue-600">Última análise: 5 min atrás</p>
                </div>
                <Badge className="bg-blue-600">Ativo</Badge>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>📸 Snapshots do Conhecimento</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {activeSnapshots.length === 0 ? (
                <p className="text-sm text-muted-foreground">Nenhum snapshot encontrado.</p>
              ) : (
                activeSnapshots.map((snap) => (
                  <div key={snap.id} className="border rounded-lg p-3">
                    <div className="flex items-center justify-between mb-2">
                      <p className="font-medium">Snapshot - {new Date(snap.created_at).toLocaleDateString()}</p>
                      <Button variant="ghost" size="sm">Restaurar</Button>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      {snap.memory_count} memórias • {new Date(snap.created_at).toLocaleString()}
                    </p>
                  </div>
                ))
              )}

              <Button variant="outline" className="w-full">
                Criar Snapshot Manual
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-red-600">⚠️ Ações Perigosas</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="p-3 bg-red-50 rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <AlertTriangle className="h-4 w-4 text-red-600" />
                  <p className="font-medium text-red-800">Limpar Todas as Memórias</p>
                </div>
                <p className="text-sm text-red-600 mb-3">
                  Remove permanentemente todas as memórias do agente. Esta ação não pode ser desfeita.
                </p>
                <Button variant="destructive" size="sm">
                  Limpar Memórias
                </Button>
              </div>

              <div className="p-3 bg-red-50 rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <AlertTriangle className="h-4 w-4 text-red-600" />
                  <p className="font-medium text-red-800">Resetar Configurações</p>
                </div>
                <p className="text-sm text-red-600 mb-3">
                  Restaura todas as configurações para os valores padrão de fábrica.
                </p>
                <Button variant="destructive" size="sm">
                  Resetar Sistema
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}