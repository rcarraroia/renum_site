/**
 * Sub-Agents Page - Sprint 09
 * Page for managing sub-agents of an agent
 */

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Plus, MoreVertical, Edit, Trash2, Power, PowerOff } from 'lucide-react';
import { getAgent, listSubAgents, deleteSubAgent, toggleSubAgentActive } from '@/services/agentService';
import type { Agent, SubAgent } from '@/types/agent';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';

export default function SubAgentsPage() {
  const { agentId } = useParams<{ agentId: string }>();
  const navigate = useNavigate();
  const [agent, setAgent] = useState<Agent | null>(null);
  const [subAgents, setSubAgents] = useState<SubAgent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (agentId) {
      loadData();
    }
  }, [agentId]);

  async function loadData() {
    if (!agentId) return;

    try {
      setLoading(true);
      const [agentData, subAgentsData] = await Promise.all([
        getAgent(agentId),
        listSubAgents(agentId),
      ]);
      setAgent(agentData);
      setSubAgents(subAgentsData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(subAgentId: string) {
    if (!agentId || !confirm('Tem certeza que deseja deletar este sub-agent?')) {
      return;
    }

    try {
      await deleteSubAgent(agentId, subAgentId);
      await loadData();
    } catch (error) {
      console.error('Error deleting sub-agent:', error);
      alert('Erro ao deletar sub-agent');
    }
  }

  async function handleToggleActive(subAgentId: string) {
    if (!agentId) return;

    try {
      await toggleSubAgentActive(agentId, subAgentId);
      await loadData();
    } catch (error) {
      console.error('Error toggling sub-agent:', error);
      alert('Erro ao alterar status');
    }
  }

  const getChannelIcon = (channel: string) => {
    const icons: Record<string, string> = {
      whatsapp: '💬',
      web: '🌐',
      sms: '📱',
      email: '📧',
    };
    return icons[channel] || '❓';
  };

  if (loading) {
    return (
      <div className="container mx-auto py-6">
        <p className="text-center text-muted-foreground">Carregando...</p>
      </div>
    );
  }

  if (!agent) {
    return (
      <div className="container mx-auto py-6">
        <p className="text-center text-muted-foreground">Agent não encontrado</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-6 space-y-6">
      {/* Header */}
      <div className="space-y-4">
        <Button
          variant="ghost"
          onClick={() => navigate('/agents')}
          className="mb-2"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Voltar para Agents
        </Button>

        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Sub-Agents</h1>
            <p className="text-muted-foreground">
              Agent: <span className="font-semibold">{agent.name}</span>
            </p>
          </div>
          <Button onClick={() => navigate(`/agents/${agentId}/sub-agents/new`)}>
            <Plus className="w-4 h-4 mr-2" />
            Novo Sub-Agent
          </Button>
        </div>
      </div>

      {/* Agent Info Card */}
      <Card className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <p className="text-sm text-muted-foreground">Status</p>
            <Badge>{agent.status}</Badge>
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Channel</p>
            <p className="font-semibold">
              {getChannelIcon(agent.channel)} {agent.channel}
            </p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Template</p>
            <p className="font-semibold">{agent.template_type}</p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Model</p>
            <p className="font-mono text-sm">{agent.model}</p>
          </div>
        </div>
      </Card>

      {/* Sub-Agents List */}
      {subAgents.length === 0 ? (
        <Card className="p-12 text-center">
          <p className="text-muted-foreground mb-4">
            Nenhum sub-agent criado ainda
          </p>
          <Button onClick={() => navigate(`/agents/${agentId}/sub-agents/new`)}>
            <Plus className="w-4 h-4 mr-2" />
            Criar Primeiro Sub-Agent
          </Button>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {subAgents.map((subAgent) => (
            <Card key={subAgent.id} className="p-6 hover:shadow-lg transition-shadow">
              <div className="space-y-4">
                {/* Header */}
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-2xl">{getChannelIcon(subAgent.channel)}</span>
                      <h3 className="font-semibold text-lg">{subAgent.name}</h3>
                    </div>
                    {subAgent.description && (
                      <p className="text-sm text-muted-foreground line-clamp-2">
                        {subAgent.description}
                      </p>
                    )}
                  </div>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="icon">
                        <MoreVertical className="w-4 h-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem
                        onClick={() => navigate(`/agents/${agentId}/sub-agents/${subAgent.id}/edit`)}
                      >
                        <Edit className="w-4 h-4 mr-2" />
                        Editar
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => handleToggleActive(subAgent.id)}>
                        {subAgent.is_active ? (
                          <>
                            <PowerOff className="w-4 h-4 mr-2" />
                            Desativar
                          </>
                        ) : (
                          <>
                            <Power className="w-4 h-4 mr-2" />
                            Ativar
                          </>
                        )}
                      </DropdownMenuItem>
                      <DropdownMenuItem
                        onClick={() => handleDelete(subAgent.id)}
                        className="text-destructive"
                      >
                        <Trash2 className="w-4 h-4 mr-2" />
                        Deletar
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>

                {/* Status Badge */}
                <div>
                  <Badge variant={subAgent.is_active ? 'default' : 'secondary'}>
                    {subAgent.is_active ? 'Ativo' : 'Inativo'}
                  </Badge>
                </div>

                {/* Topics */}
                {subAgent.topics && subAgent.topics.length > 0 && (
                  <div>
                    <p className="text-sm text-muted-foreground mb-2">Tópicos:</p>
                    <div className="flex flex-wrap gap-1">
                      {subAgent.topics.map((topic, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {topic}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                {/* Info */}
                <div className="space-y-1 text-sm">
                  <div className="flex items-center justify-between">
                    <span className="text-muted-foreground">Model:</span>
                    <span className="font-mono text-xs">{subAgent.model}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-muted-foreground">Channel:</span>
                    <span>{subAgent.channel}</span>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex gap-2 pt-2">
                  <Button
                    variant="outline"
                    size="sm"
                    className="flex-1"
                    onClick={() => navigate(`/agents/${agentId}/sub-agents/${subAgent.id}/edit`)}
                  >
                    Editar
                  </Button>
                  <Button
                    variant={subAgent.is_active ? 'outline' : 'default'}
                    size="sm"
                    onClick={() => handleToggleActive(subAgent.id)}
                  >
                    {subAgent.is_active ? <PowerOff className="w-4 h-4" /> : <Power className="w-4 h-4" />}
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
