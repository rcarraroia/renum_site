import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Edit, Trash2, MessageSquare, Globe, ChevronDown, ChevronUp, Users, Zap } from 'lucide-react';
import { cn } from '@/lib/utils';
import { SubAgent } from './types'; // Importando o tipo SubAgent

interface SubAgentCardProps {
  agent: SubAgent;
  onEdit: (agent: SubAgent) => void;
  onDelete: (id: string) => void;
  onToggleActive: (id: string) => void;
  isExpanded: boolean;
  onToggleExpand: (id: string) => void;
}

export const SubAgentCard: React.FC<SubAgentCardProps> = ({ agent, onEdit, onDelete, onToggleActive, isExpanded, onToggleExpand }) => {
  
  const getModelLabel = (model?: string) => {
    switch (model) {
      case 'default': return 'Modelo Padrão';
      case 'anthropic/claude-sonnet-4': return 'Claude Sonnet 4';
      case 'openai/gpt-4o-mini': return 'GPT-4o Mini';
      case 'meta-llama/llama-3.1-8b-instruct:free': return 'Llama 3.1 (FREE)';
      default: return 'Personalizado';
    }
  };

  return (
    <Card 
      className={cn(
        "transition-all hover:shadow-lg",
        agent.isActive 
          ? "border-[#0ca7d2]" 
          : "border-dashed opacity-60"
      )}
    >
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="space-y-1 flex-1">
            <CardTitle className="flex items-center gap-2 text-lg">
              {agent.name}
              {agent.isActive ? (
                <Badge className="bg-green-500 text-xs">Ativo</Badge>
              ) : (
                <Badge variant="secondary" className="text-xs">Inativo</Badge>
              )}
            </CardTitle>
            <CardDescription className="text-sm">
              {agent.description}
            </CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-3">
        {/* Canal */}
        <div className="flex items-center gap-2 text-sm">
          {agent.channel === 'whatsapp' ? (
            <>
              <MessageSquare className="h-4 w-4 text-green-600" />
              <span className="text-muted-foreground">WhatsApp</span>
            </>
          ) : (
            <>
              <Globe className="h-4 w-4 text-blue-600" />
              <span className="text-muted-foreground">Site</span>
            </>
          )}
        </div>

        {/* Modelo (NOVO) */}
        <div className="flex items-center gap-2 text-sm">
          <Zap className="h-4 w-4 text-purple-600" />
          <span className="text-muted-foreground">
            {getModelLabel(agent.model)}
          </span>
        </div>

        {/* Tópicos (expansível) */}
        <div>
          <Button
            variant="ghost"
            size="sm"
            className="w-full justify-between p-0 h-auto hover:bg-transparent"
            onClick={() => onToggleExpand(agent.id)}
          >
            <span className="text-sm text-muted-foreground">
              🔖 {agent.topics.length} tópicos configurados
            </span>
            {isExpanded ? (
              <ChevronUp className="h-4 w-4" />
            ) : (
              <ChevronDown className="h-4 w-4" />
            )}
          </Button>
          
          {isExpanded && (
            <div className="flex flex-wrap gap-1 mt-2">
              {agent.topics.map((topic, i) => (
                <Badge key={i} variant="outline" className="text-xs">
                  {topic}
                </Badge>
              ))}
            </div>
          )}
        </div>
      </CardContent>

      <CardFooter className="flex gap-2 pt-3 border-t">
        <Button
          variant="outline"
          size="sm"
          onClick={() => onEdit(agent)}
          className="flex-1"
        >
          <Edit className="h-3 w-3 mr-1" />
          Editar
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => onToggleActive(agent.id)}
          className="flex-1"
        >
          {agent.isActive ? 'Pausar' : 'Ativar'}
        </Button>
        <Button
          variant="destructive"
          size="sm"
          onClick={() => onDelete(agent.id)}
        >
          <Trash2 className="h-3 w-3" />
        </Button>
      </CardFooter>
    </Card>
  );
};