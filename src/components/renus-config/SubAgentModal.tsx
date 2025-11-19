import React from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Plus, Zap, MessageSquare, Globe, FileText, Upload, Info, Tag, Trash2 } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { SubAgent } from './types'; // Importando o tipo SubAgent

interface SubAgentModalProps {
  isOpen: boolean;
  onClose: () => void;
  formData: Partial<SubAgent>;
  setFormData: React.Dispatch<React.SetStateAction<Partial<SubAgent>>>;
  onSave: () => void;
  editingAgent: SubAgent | null;
  addTopic: () => void;
  removeTopic: (index: number) => void;
}

export const SubAgentModal: React.FC<SubAgentModalProps> = ({
  isOpen,
  onClose,
  formData,
  setFormData,
  onSave,
  editingAgent,
  addTopic,
  removeTopic,
}) => {
  const isEdit = !!editingAgent;

  const handleBasicChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: value }));
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[700px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-[#4e4ea8]">
            {isEdit ? 'Editar Sub-Agente' : 'Novo Sub-Agente'}
          </DialogTitle>
          <DialogDescription>
            Configure um agente especializado para um nicho e tipo específico
          </DialogDescription>
        </DialogHeader>

        <div className="grid gap-4 py-4">
          {/* Nome */}
          <div className="space-y-2">
            <Label htmlFor="name">Nome do Sub-Agente *</Label>
            <Input
              id="name"
              placeholder="Ex: Pesquisa MMN, Atendimento Clínicas, Vendas E-commerce"
              value={formData.name || ''}
              onChange={handleBasicChange}
            />
            <p className="text-xs text-muted-foreground">
              Escolha um nome descritivo que identifique o nicho e tipo
            </p>
          </div>

          {/* Descrição */}
          <div className="space-y-2">
            <Label htmlFor="description">Descrição</Label>
            <Textarea
              id="description"
              placeholder="Breve descrição do objetivo e público-alvo deste sub-agente..."
              rows={3}
              value={formData.description || ''}
              onChange={handleBasicChange}
            />
          </div>

          {/* Canal */}
          <div className="space-y-2">
            <Label>Canal de Atendimento *</Label>
            <RadioGroup
              value={formData.channel}
              onValueChange={(value) => setFormData(prev => ({...prev, channel: value as 'site' | 'whatsapp'}))}
            >
              <div className="flex items-center space-x-2 p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-900 cursor-pointer">
                <RadioGroupItem value="whatsapp" id="whatsapp" />
                <Label htmlFor="whatsapp" className="flex items-center gap-2 cursor-pointer flex-1">
                  <MessageSquare className="h-4 w-4 text-green-600" />
                  <div>
                    <div className="font-medium">WhatsApp</div>
                    <div className="text-xs text-muted-foreground">Atendimento via WhatsApp Business</div>
                  </div>
                </Label>
              </div>
              <div className="flex items-center space-x-2 p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-900 cursor-pointer">
                <RadioGroupItem value="site" id="site" />
                <Label htmlFor="site" className="flex items-center gap-2 cursor-pointer flex-1">
                  <Globe className="h-4 w-4 text-blue-600" />
                  <div>
                    <div className="font-medium">Site</div>
                    <div className="text-xs text-muted-foreground">Widget de chat no website</div>
                  </div>
                </Label>
              </div>
            </RadioGroup>
          </div>

          {/* System Prompt */}
          <div className="space-y-2">
            <Label htmlFor="systemPrompt">Prompt Base (System Prompt) *</Label>
            <Textarea
              id="systemPrompt"
              placeholder="Você é um assistente especializado em... Seu objetivo é... Mantenha um tom..."
              rows={8}
              className="font-mono text-sm"
              value={formData.systemPrompt || ''}
              onChange={handleBasicChange}
            />
            <p className="text-xs text-muted-foreground">
              💡 Defina claramente: função, comportamento, tom e objetivo do agente
            </p>
          </div>

          {/* Tópicos Obrigatórios */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <div>
                <Label>Tópicos/Contextos Principais</Label>
                <p className="text-xs text-muted-foreground">
                  Principais assuntos que o agente deve dominar
                </p>
              </div>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={addTopic}
              >
                <Plus className="h-3 w-3 mr-1" />
                Adicionar
              </Button>
            </div>
            <div className="flex flex-wrap gap-2 min-h-[40px] p-3 border rounded-lg">
              {(formData.topics || []).length === 0 ? (
                <span className="text-sm text-muted-foreground">
                  Nenhum tópico adicionado
                </span>
              ) : (
                (formData.topics || []).map((topic, index) => (
                  <Badge
                    key={index}
                    variant="secondary"
                    className="flex items-center gap-1"
                  >
                    {topic}
                    <button
                      type="button"
                      onClick={() => removeTopic(index)}
                      className="hover:text-destructive ml-1"
                    >
                      ×
                    </button>
                  </Badge>
                ))
              )}
            </div>
          </div>
          
          {/* Seção Fine-tuning */}
          <div className="space-y-4 p-4 border-2 border-dashed border-blue-300 dark:border-blue-700 rounded-lg bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950 dark:to-indigo-950">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <Zap className="h-5 w-5 text-blue-600" />
                  <Label className="text-lg font-semibold text-blue-900 dark:text-blue-100">
                    ⚡ Fine-tuning (Otimização Avançada)
                  </Label>
                  <Badge variant="secondary" className="text-xs">
                    Em Breve
                  </Badge>
                </div>
                <p className="text-sm text-muted-foreground mt-1 ml-7">
                  Economize até 90% em tokens e melhore a qualidade das respostas
                </p>
              </div>
              <Switch
                checked={formData.useFineTuning || false}
                onCheckedChange={(checked) => setFormData(prev => ({...prev, useFineTuning: checked}))}
                disabled={true}
                className="opacity-50"
              />
            </div>

            {/* Área expansível (sempre visível para preview) */}
            <div className="space-y-3 pt-3 border-t border-blue-200 dark:border-blue-800 opacity-60">
              {/* Info cards */}
              <div className="grid grid-cols-3 gap-2">
                <div className="p-2 rounded bg-white dark:bg-gray-900 border border-blue-200 dark:border-blue-800">
                  <div className="text-xs text-muted-foreground">Economia</div>
                  <div className="text-lg font-bold text-blue-600">~90%</div>
                </div>
                <div className="p-2 rounded bg-white dark:bg-gray-900 border border-blue-200 dark:border-blue-800">
                  <div className="text-xs text-muted-foreground">Tokens/msg</div>
                  <div className="text-lg font-bold text-green-600">50</div>
                  <div className="text-xs line-through text-gray-400">800</div>
                </div>
                <div className="p-2 rounded bg-white dark:bg-gray-900 border border-blue-200 dark:border-blue-800">
                  <div className="text-xs text-muted-foreground">Exemplos</div>
                  <div className="text-lg font-bold text-purple-600">50+</div>
                </div>
              </div>

              {/* Upload placeholder */}
              <div className="space-y-2">
                <Label className="text-sm flex items-center gap-2 opacity-50">
                  <FileText className="h-4 w-4" />
                  Dataset de Treinamento (JSONL)
                </Label>
                <div className="border-2 border-dashed rounded-lg p-4 text-center bg-white dark:bg-gray-900 opacity-50">
                  <Upload className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
                  <p className="text-sm text-muted-foreground">
                    Arraste o arquivo .jsonl aqui ou clique para selecionar
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    Mínimo 50 exemplos de conversas
                  </p>
                </div>
              </div>

              {/* Status placeholder */}
              <div className="p-3 rounded-lg bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 opacity-50">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-gray-400"></div>
                  <span className="text-sm text-muted-foreground">
                    Aguardando ativação do fine-tuning...
                  </span>
                </div>
              </div>

              {/* Info footer */}
              <div className="flex items-start gap-2 p-2 rounded bg-blue-100 dark:bg-blue-900">
                <Info className="h-4 w-4 text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0" />
                <p className="text-xs text-blue-700 dark:text-blue-300">
                  <strong>Como funciona:</strong> Você treina o modelo uma vez com exemplos reais de conversas. 
                  Depois, ele já sabe como responder naturalmente, sem precisar de prompts gigantes toda vez.
                  Isso reduz drasticamente o consumo de tokens e melhora a qualidade das respostas.
                </p>
              </div>
            </div>
          </div>

          {/* Status */}
          <div className="flex items-center justify-between p-4 border rounded-lg bg-gray-50 dark:bg-gray-900">
            <div>
              <Label>Status Inicial</Label>
              <p className="text-sm text-muted-foreground">
                Ativar sub-agente imediatamente após criação
              </p>
            </div>
            <Switch
              checked={formData.isActive}
              onCheckedChange={(checked) => setFormData(prev => ({...prev, isActive: checked}))}
            />
          </div>
        </div>

        <DialogFooter>
          <Button
            variant="outline"
            onClick={onClose}
          >
            Cancelar
          </Button>
          <Button
            onClick={onSave}
            className="bg-[#4e4ea8] hover:bg-[#3a3a80]"
          >
            {isEdit ? 'Salvar Alterações' : 'Criar Sub-Agente'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};