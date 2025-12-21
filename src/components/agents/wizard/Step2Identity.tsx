import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Zap, User, Globe, MessageSquare, Tag, CheckCircle, XCircle, Upload, FileJson } from 'lucide-react';
import { cn } from '@/lib/utils';
import { AgentCategory } from '@/types/agent';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { wizardService } from '@/services/wizardService';
import { agentService } from '@/services/agentService';

interface Step2IdentityProps {
  formData: any;
  setFormData: (data: any) => void;
}

const Step2Identity: React.FC<Step2IdentityProps> = ({ formData, setFormData }) => {
  const MAX_DESCRIPTION_LENGTH = 500;
  const [slugStatus, setSlugStatus] = useState<'checking' | 'available' | 'unavailable' | 'initial'>('initial');

  // Categorias Reais (Mapeadas do banco se tivéssemos serviço, mas por agora usaremos as globais)
  const categories = [
    { id: 'vendas', name: 'Vendas & Atendimento', icon: '💰' },
    { id: 'suporte', name: 'Suporte Técnico', icon: '🛠️' },
    { id: 'imobiliario', name: 'Imobiliário / Real Estate', icon: '🏠' },
    { id: 'educacao', name: 'Educação / Cursos', icon: '🎓' },
    { id: 'marketing', name: 'Marketing / Captação', icon: '📈' },
    { id: 'generico', name: 'Geral / Outros', icon: '🤖' }
  ];

  const checkSlugAvailability = async (slug: string) => {
    if (slug.length < 3) return 'initial';
    try {
      setSlugStatus('checking');
      const agent = await agentService.getAgentBySlug(slug);
      return agent ? 'unavailable' : 'available';
    } catch (error: any) {
      // Se der 404, significa que está disponível
      if (error.response?.status === 404) return 'available';
      return 'available'; // Default para disponível se houver erro ou não existir
    }
  };

  useEffect(() => {
    if (!formData.slug) return;
    const handler = setTimeout(async () => {
      const status = await checkSlugAvailability(formData.slug);
      setSlugStatus(status);
    }, 500);
    return () => clearTimeout(handler);
  }, [formData.slug]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { id, value } = e.target;
    setFormData({ ...formData, [id]: value });
  };

  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const name = e.target.value;
    const slug = name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
    setFormData({ ...formData, name: name, slug: slug });
  };

  const handleSlugChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const rawSlug = e.target.value;
    const slug = rawSlug.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
    setFormData({ ...formData, slug: slug });
  };

  const getSlugIcon = () => {
    switch (slugStatus) {
      case 'checking':
        return <div className="h-4 w-4 border-2 border-primary border-t-transparent animate-spin rounded-full" />;
      case 'available':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'unavailable':
        return <XCircle className="h-4 w-4 text-red-500" />;
      default:
        return null;
    }
  };

  const getSlugMessage = () => {
    if (!formData.slug || formData.slug.length < 3) return "Mínimo de 3 caracteres.";
    switch (slugStatus) {
      case 'checking':
        return "Verificando disponibilidade...";
      case 'available':
        return <span className="text-green-500 flex items-center"><CheckCircle className="h-4 w-4 mr-1" /> Disponível para uso</span>;
      case 'unavailable':
        return <span className="text-red-500 flex items-center"><XCircle className="h-4 w-4 mr-1" /> Este slug já está sendo usado</span>;
      default:
        return "Este será o endereço único do seu agente.";
    }
  };

  const handleN8nUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      const text = await file.text();
      const json = JSON.parse(text);

      toast.promise(wizardService.convertN8n(json), {
        loading: 'Analisando lógica do n8n...',
        success: (data) => {
          setFormData({
            ...formData,
            name: data.name,
            description: data.description,
            system_prompt: data.system_prompt_hint
          });
          return `Workflow convertido com sucesso!`;
        },
        error: 'Erro ao converter workflow n8n.'
      });
    } catch (err) {
      toast.error('Arquivo JSON inválido.');
    }
  };

  const fullDomain = `${formData.slug || 'novo-agente'}.renum.com.br`;

  return (
    <div className="space-y-6">
      <Card className="border-dashed border-2 bg-blue-50/30 dark:bg-blue-900/10 border-blue-200 dark:border-blue-800">
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-base flex items-center text-blue-600 dark:text-blue-400">
              <Zap className="h-5 w-5 mr-2" /> Possui um workflow n8n?
            </CardTitle>
            <FileJson className="h-5 w-5 text-blue-400 opacity-50" />
          </div>
          <CardDescription>
            Importe seu arquivo JSON para que nossa IA configure a base do seu novo agente.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center space-x-4">
            <Label
              htmlFor="n8n-upload"
              className="flex items-center justify-center px-4 py-2 border border-blue-300 dark:border-blue-700 rounded-md bg-white dark:bg-gray-800 text-blue-600 dark:text-blue-400 cursor-pointer hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
            >
              <Upload className="h-4 w-4 mr-2" /> Importar Workflow JSON
              <input
                id="n8n-upload"
                type="file"
                accept=".json"
                className="hidden"
                onChange={handleN8nUpload}
              />
            </Label>
            <p className="text-xs text-muted-foreground">
              Nome, descrição e o System Prompt inicial serão preenchidos automaticamente.
            </p>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-[#4e4ea8]">
            <User className="h-5 w-5 mr-2" /> 2. Identidade do Agente
          </CardTitle>
          <CardDescription>
            Defina como seu agente será identificado e onde ele atuará.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Name */}
          <div className="space-y-2">
            <Label htmlFor="name">Nome do Agente *</Label>
            <Input
              id="name"
              placeholder="Ex: Consultor Slim Quality"
              value={formData.name || ''}
              onChange={handleNameChange}
            />
          </div>

          {/* Description */}
          <div className="space-y-2">
            <Label htmlFor="description" className="flex justify-between">
              <span>Descrição Interna</span>
              <span className="text-xs text-muted-foreground">{formData.description?.length || 0}/{MAX_DESCRIPTION_LENGTH}</span>
            </Label>
            <Textarea
              id="description"
              placeholder="Breve resumo da finalidade deste agente..."
              rows={3}
              value={formData.description || ''}
              onChange={handleInputChange}
              maxLength={MAX_DESCRIPTION_LENGTH}
            />
          </div>

          {/* Category */}
          <div className="space-y-2">
            <Label htmlFor="category" className="flex items-center"><Tag className="h-4 w-4 mr-2" /> Categoria de Atuação *</Label>
            <Select value={formData.category} onValueChange={(v) => setFormData({ ...formData, category: v as AgentCategory })}>
              <SelectTrigger>
                <SelectValue placeholder="Selecione a categoria" />
              </SelectTrigger>
              <SelectContent>
                {categories.map(c => (
                  <SelectItem key={c.id} value={c.id}>
                    <div className="flex items-center">
                      <span className="mr-2">{c.icon}</span> {c.name}
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Slug */}
          <div className="space-y-2">
            <Label htmlFor="slug">Slug (subdomínio): *</Label>
            <div className="flex items-center space-x-2">
              <Input
                id="slug"
                placeholder="slim-vendas"
                value={formData.slug || ''}
                onChange={handleSlugChange}
                className="flex-grow"
              />
              <span className="text-sm text-muted-foreground flex-shrink-0">.renum.com.br</span>
            </div>
            <div className="flex items-center justify-between text-xs text-muted-foreground">
              <p>{getSlugMessage()}</p>
              {getSlugIcon()}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Preview Box */}
      <Card className="bg-gray-50 dark:bg-gray-800 border-l-4 border-[#FF6B35]">
        <CardHeader className="p-4 pb-2">
          <CardTitle className="text-base flex items-center text-[#FF6B35]">
            <Globe className="h-4 w-4 mr-2" /> Preview de Acesso
          </CardTitle>
        </CardHeader>
        <CardContent className="p-4 pt-0">
          <p className="text-sm text-muted-foreground">Seu agente será acessível em:</p>
          <p className="font-mono text-sm text-primary dark:text-white break-all mt-1">
            https://{fullDomain}
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default Step2Identity;