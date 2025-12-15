/**
 * Sub-Agent Form - Sprint 09 Task F.5
 * Form for creating/editing sub-agents
 */

import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { X, Plus } from 'lucide-react';
import type { SubAgent, SubAgentCreate, SubAgentUpdate, Channel, Model } from '@/types/agent';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';
import { Badge } from '@/components/ui/badge';

interface SubAgentFormProps {
  subAgent?: SubAgent;
  onSubmit: (data: SubAgentCreate | SubAgentUpdate) => Promise<void>;
  onCancel: () => void;
  loading?: boolean;
}

export default function SubAgentForm({
  subAgent,
  onSubmit,
  onCancel,
  loading = false,
}: SubAgentFormProps) {
  const isEdit = !!subAgent;

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<SubAgentCreate | SubAgentUpdate>({
    defaultValues: subAgent
      ? {
          name: subAgent.name,
          description: subAgent.description,
          channel: subAgent.channel,
          system_prompt: subAgent.system_prompt,
          topics: subAgent.topics,
          model: subAgent.model,
          is_active: subAgent.is_active,
        }
      : {
          name: '',
          description: '',
          channel: 'whatsapp',
          system_prompt: '',
          topics: [],
          model: 'gpt-4o-mini',
          is_active: true,
        },
  });

  const [topics, setTopics] = useState<string[]>(subAgent?.topics || []);
  const [newTopic, setNewTopic] = useState('');

  const channel = watch('channel');
  const model = watch('model');
  const isActive = watch('is_active');

  useEffect(() => {
    setValue('topics', topics);
  }, [topics, setValue]);

  function handleAddTopic() {
    if (!newTopic.trim()) return;
    if (topics.includes(newTopic.trim())) {
      alert('Tópico já adicionado');
      return;
    }
    setTopics([...topics, newTopic.trim()]);
    setNewTopic('');
  }

  function handleRemoveTopic(topic: string) {
    setTopics(topics.filter((t) => t !== topic));
  }

  async function handleFormSubmit(data: SubAgentCreate | SubAgentUpdate) {
    try {
      await onSubmit({
        ...data,
        topics: topics.length > 0 ? topics : null,
      });
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  }

  const channels: Channel[] = ['whatsapp', 'web', 'sms', 'email'];
  const models: Model[] = [
    'gpt-4o-mini',
    'gpt-4',
    'gpt-4-turbo-preview',
    'claude-3-5-sonnet-20241022',
    'claude-3-opus',
  ];

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
      {/* Name */}
      <div className="space-y-2">
        <Label htmlFor="name">
          Nome <span className="text-destructive">*</span>
        </Label>
        <Input
          id="name"
          {...register('name', { required: 'Nome é obrigatório' })}
          placeholder="Ex: Agente de Vendas"
        />
        {errors.name && (
          <p className="text-sm text-destructive">{errors.name.message}</p>
        )}
      </div>

      {/* Description */}
      <div className="space-y-2">
        <Label htmlFor="description">Descrição</Label>
        <Textarea
          id="description"
          {...register('description')}
          placeholder="Descreva o propósito deste sub-agent..."
          rows={3}
        />
      </div>

      {/* Channel */}
      <div className="space-y-2">
        <Label htmlFor="channel">
          Canal <span className="text-destructive">*</span>
        </Label>
        <Select
          value={channel}
          onValueChange={(value) => setValue('channel', value as Channel)}
        >
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {channels.map((ch) => (
              <SelectItem key={ch} value={ch}>
                {ch}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Model */}
      <div className="space-y-2">
        <Label htmlFor="model">Modelo LLM</Label>
        <Select
          value={model}
          onValueChange={(value) => setValue('model', value as Model)}
        >
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {models.map((m) => (
              <SelectItem key={m} value={m}>
                {m}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Topics */}
      <div className="space-y-2">
        <Label>Tópicos</Label>
        <p className="text-sm text-muted-foreground">
          Palavras-chave que ativam este sub-agent (ex: vendas, suporte, pesquisa)
        </p>
        <div className="flex gap-2">
          <Input
            value={newTopic}
            onChange={(e) => setNewTopic(e.target.value)}
            placeholder="Digite um tópico..."
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                handleAddTopic();
              }
            }}
          />
          <Button type="button" onClick={handleAddTopic} variant="outline">
            <Plus className="w-4 h-4" />
          </Button>
        </div>
        {topics.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-2">
            {topics.map((topic) => (
              <Badge key={topic} variant="secondary" className="gap-1">
                {topic}
                <button
                  type="button"
                  onClick={() => handleRemoveTopic(topic)}
                  className="ml-1 hover:text-destructive"
                >
                  <X className="w-3 h-3" />
                </button>
              </Badge>
            ))}
          </div>
        )}
      </div>

      {/* System Prompt */}
      <div className="space-y-2">
        <Label htmlFor="system_prompt">
          System Prompt <span className="text-destructive">*</span>
        </Label>
        <Textarea
          id="system_prompt"
          {...register('system_prompt', {
            required: 'System prompt é obrigatório',
          })}
          placeholder="Você é um assistente especializado em..."
          rows={8}
          className="font-mono text-sm"
        />
        {errors.system_prompt && (
          <p className="text-sm text-destructive">{errors.system_prompt.message}</p>
        )}
      </div>

      {/* Is Active */}
      <div className="flex items-center justify-between">
        <div className="space-y-0.5">
          <Label htmlFor="is_active">Ativo</Label>
          <p className="text-sm text-muted-foreground">
            Sub-agent ativo pode processar mensagens
          </p>
        </div>
        <Switch
          id="is_active"
          checked={isActive}
          onCheckedChange={(checked) => setValue('is_active', checked)}
        />
      </div>

      {/* Actions */}
      <div className="flex gap-2 justify-end pt-4 border-t">
        <Button type="button" variant="outline" onClick={onCancel} disabled={loading}>
          Cancelar
        </Button>
        <Button type="submit" disabled={loading}>
          {loading ? 'Salvando...' : isEdit ? 'Atualizar' : 'Criar'}
        </Button>
      </div>
    </form>
  );
}
