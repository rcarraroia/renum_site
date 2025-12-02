import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Edit, Trash2, MessageSquare, Globe, ChevronDown, ChevronUp, Users, Zap, Server, TrendingUp, Clock, ArrowRight, Settings, MoreVertical, Copy, Pause, Play } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Agent, AgentStatus, AgentCategory, AgentChannel, CategoryMock } from '@/types/agent';
import { mockCategories, mockClients, mockProjects } from '@/mocks/agents.mock';
import { Link } from 'react-router-dom';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { toast } from 'sonner';

interface AgentCardProps {
  agent: Agent;
  onEdit: (agent: Agent) => void;
  onDelete: (id: string) => void;
}

const getStatusBadge = (status: AgentStatus) => {
    switch (status) {
        case 'ativo': return <Badge className="bg-green-600 text-white">Ativo</Badge>;
        case 'inativo': return <Badge variant="secondary">Inativo</Badge>;
        case 'pausado': return <Badge className="bg-yellow-500 text-gray-900">Pausado</Badge>;
        case 'erro': return <Badge className="bg-red-500 text-white">Erro</Badge>;
    }
};

const getCategoryInfo = (category: AgentCategory): CategoryMock | undefined => {
    return mockCategories.find(c => c.id === category);
};

const getAgentTypeLabel = (type: string) => {
    switch (type) {
        case 'b2b_empresa': return 'B2B';
        case 'b2c_marketplace': return 'B2C';
        case 'b2c_individual': return 'B2C';
        default: return 'Custom';
    }
};

const AgentCard: React.FC<AgentCardProps> = ({ agent, onEdit, onDelete }) => {
  const categoryInfo = getCategoryInfo(agent.category);
  const client = mockClients.find(c => c.id === agent.client_id);
  const project = mockProjects.find(p => p.id === agent.project_id);

  const handleToggleStatus = () => {
    // Mock action
    const newStatus = agent.status === 'ativo' ? 'pausado' : 'ativo';
    toast.info(`Agente ${agent.name} ${newStatus === 'ativo' ? 'ativado' : 'pausado'}.`);
  };

  return (
    <Card 
      className={cn(
        "transition-all hover:shadow-xl hover:scale-[1.01] h-full flex flex-col",
        agent.status === 'ativo' 
          ? "border-2 border-[#0ca7d2]" 
          : "border-dashed opacity-80"
      )}
    >
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="space-y-1 flex-1">
            <CardTitle className="flex items-center gap-2 text-lg">
              {agent.name}
            </CardTitle>
            <CardDescription className="text-sm line-clamp-2">
              {client?.name} / {project?.name}
            </CardDescription>
          </div>
          <div className="flex flex-col items-end space-y-1">
            {getStatusBadge(agent.status)}
            <Badge variant="outline" className="text-xs bg-gray-100 dark:bg-gray-700">
                {getAgentTypeLabel(agent.type)}
            </Badge>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-3 flex-grow">
        {/* Category and Domain */}
        <div className="flex items-center gap-2 text-sm">
          <Zap className="h-4 w-4 text-[#FF6B35]" />
          <span className="font-medium">{categoryInfo?.name || 'Custom'}</span>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Globe className="h-4 w-4" />
            <span className="font-mono text-xs truncate">{agent.domain}</span>
        </div>

        {/* Channels */}
        <div className="flex items-center gap-2 text-sm pt-2 border-t dark:border-gray-800">
          <MessageSquare className="h-4 w-4 text-[#4e4ea8]" />
          <span className="text-muted-foreground">Canais:</span>
          {agent.channel.map(c => (
            <Badge key={c} variant="secondary" className="text-xs capitalize">{c}</Badge>
          ))}
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-2 gap-2 text-sm pt-2">
            <div className="flex items-center gap-1">
                <Server className="h-4 w-4 text-green-500" />
                <span className="text-muted-foreground">Instâncias:</span>
                <span className="font-semibold">{agent.instances_count}</span>
            </div>
            <div className="flex items-center gap-1">
                <TrendingUp className="h-4 w-4 text-yellow-500" />
                <span className="text-muted-foreground">Conversas (Hoje):</span>
                <span className="font-semibold">{agent.conversations_today}</span>
            </div>
        </div>
      </CardContent>

      <CardFooter className="flex gap-2 pt-3 border-t">
        <Link to={`/dashboard/admin/agents/${agent.id}`} className="flex-1">
            <Button
                size="sm"
                className="w-full bg-[#4e4ea8] hover:bg-[#3a3a80]"
            >
                <Settings className="h-3 w-3 mr-1" />
                Configurar
            </Button>
        </Link>
        
        <Button
          variant="outline"
          size="sm"
          onClick={handleToggleStatus}
        >
          {agent.status === 'ativo' ? <Pause className="h-3 w-3" /> : <Play className="h-3 w-3" />}
        </Button>

        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="outline" size="sm">
                    <MoreVertical className="h-3 w-3" />
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
                <DropdownMenuLabel>Ações Rápidas</DropdownMenuLabel>
                <DropdownMenuItem onClick={() => onEdit(agent)}>
                    <Edit className="h-4 w-4 mr-2" /> Editar Detalhes
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => toast.info(`Clonando agente ${agent.name}...`)}>
                    <Copy className="h-4 w-4 mr-2" /> Clonar
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => onDelete(agent.id)} className="text-red-500">
                    <Trash2 className="h-4 w-4 mr-2" /> Excluir
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
      </CardFooter>
    </Card>
  );
};

export default AgentCard;