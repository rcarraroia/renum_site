import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Briefcase, ShoppingCart, Headphones, Users, Sparkles } from 'lucide-react';
import { Checkbox } from '@/components/ui/checkbox';

interface Step1ObjectiveProps {
  formData: any;
  setFormData: (data: any) => void;
  onValidate: () => boolean;
}

const templates = [
  {
    type: 'customer_service',
    name: 'Atendimento',
    description: 'Agente amigável para suporte ao cliente',
    icon: Headphones,
    color: 'bg-blue-500',
  },
  {
    type: 'sales',
    name: 'Vendas',
    description: 'Agente persuasivo para qualificação de leads',
    icon: ShoppingCart,
    color: 'bg-green-500',
  },
  {
    type: 'support',
    name: 'Suporte Técnico',
    description: 'Agente técnico para resolução de problemas',
    icon: Briefcase,
    color: 'bg-purple-500',
  },
  {
    type: 'recruitment',
    name: 'Recrutamento',
    description: 'Agente profissional para triagem de candidatos',
    icon: Users,
    color: 'bg-orange-500',
  },
  {
    type: 'custom',
    name: 'Personalizado',
    description: 'Crie do zero com total customização',
    icon: Sparkles,
    color: 'bg-pink-500',
  },
];

const niches = [
  { value: 'mmn', label: 'Marketing Multinível (MMN)' },
  { value: 'clinicas', label: 'Clínicas e Saúde' },
  { value: 'vereadores', label: 'Político/Eleitoral' },
  { value: 'ecommerce', label: 'E-commerce' },
  { value: 'generico', label: 'Genérico' },
];

const Step1Objective: React.FC<Step1ObjectiveProps> = ({ formData, setFormData }) => {
  const [slug, setSlug] = useState('');

  const generateSlug = (name: string) => {
    const generated = name
      .toLowerCase()
      .trim()
      .replace(/[^\w\s-]/g, '')
      .replace(/[-\s]+/g, '-')
      .replace(/^-+|-+$/g, '');
    setSlug(generated || 'agent');
  };

  useEffect(() => {
    if (formData.name) {
      generateSlug(formData.name);
    }
  }, [formData.name]);

  const handleTemplateSelect = (templateType: string) => {
    setFormData({ ...formData, template_type: templateType });
  };

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Escolha um Template</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {templates.map((template) => {
            const Icon = template.icon;
            const isSelected = formData.template_type === template.type;

            return (
              <Card
                key={template.type}
                className={`cursor-pointer transition-all duration-200 hover:shadow-lg hover:scale-105 ${isSelected
                  ? 'ring-2 ring-[#FF6B35] shadow-lg bg-[#FF6B35]/5'
                  : 'hover:border-[#FF6B35]/50'
                  }`}
                onClick={() => handleTemplateSelect(template.type)}
              >
                <CardContent className="p-4">
                  <div className="flex items-start space-x-3">
                    <div className={`${template.color} p-3 rounded-lg shadow-md transition-transform ${isSelected ? 'scale-110' : ''
                      }`}>
                      <Icon className="h-6 w-6 text-white" />
                    </div>
                    <div className="flex-1">
                      <h4 className={`font-semibold text-sm ${isSelected ? 'text-[#FF6B35]' : ''
                        }`}>
                        {template.name}
                      </h4>
                      <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                        {template.description}
                      </p>
                      {isSelected && (
                        <div className="mt-2 flex items-center text-xs text-[#FF6B35] font-medium">
                          <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                          Selecionado
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>

      <div className="space-y-4">
        <div>
          <Label htmlFor="name">Nome do Agente *</Label>
          <Input
            id="name"
            placeholder="Ex: Assistente de Vendas"
            value={formData.name || ''}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            className="mt-1"
          />
          {slug && (
            <p className="text-xs text-muted-foreground mt-1">
              URL: renum.com.br/chat/<span className="font-mono font-semibold">{slug}</span>
            </p>
          )}
        </div>

        <div>
          <Label htmlFor="description">Descrição (opcional)</Label>
          <Textarea
            id="description"
            placeholder="Descreva o propósito deste agente..."
            value={formData.description || ''}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className="mt-1"
            rows={3}
          />
        </div>

        <div>
          <Label htmlFor="niche">Nicho de Negócio *</Label>
          <Select
            value={formData.niche || ''}
            onValueChange={(value) => setFormData({ ...formData, niche: value })}
          >
            <SelectTrigger className="mt-1">
              <SelectValue placeholder="Selecione o nicho" />
            </SelectTrigger>
            <SelectContent>
              {niches.map((niche) => (
                <SelectItem key={niche.value} value={niche.value}>
                  {niche.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div>
          <Label htmlFor="category">Categoria do Template *</Label>
          <Select
            value={formData.category || ''}
            onValueChange={(value) => setFormData({ ...formData, category: value })}
          >
            <SelectTrigger className="mt-1">
              <SelectValue placeholder="Selecione a categoria" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="b2c">B2C - Individual</SelectItem>
              <SelectItem value="b2b">B2B - Empresarial</SelectItem>
            </SelectContent>
          </Select>
          <p className="text-xs text-muted-foreground mt-1">
            B2C: Para clientes individuais (limite 1 agente) | B2B: Para empresas (ilimitado)
          </p>
        </div>

        <div className="flex items-start space-x-2">
          <Checkbox
            id="marketplace_visible"
            checked={formData.marketplace_visible || false}
            onCheckedChange={(checked) => setFormData({ ...formData, marketplace_visible: checked })}
            className="mt-1"
          />
          <div className="grid gap-1.5 leading-none">
            <Label
              htmlFor="marketplace_visible"
              className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
            >
              Publicar no Marketplace
            </Label>
            <p className="text-xs text-muted-foreground">
              Tornar este template disponível para clientes escolherem
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Step1Objective;
