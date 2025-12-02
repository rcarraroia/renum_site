import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Zap, User, Globe, MessageSquare } from 'lucide-react';
import { cn } from '@/lib/utils';

interface Step2IdentityProps {
  formData: any;
  setFormData: (data: any) => void;
  onValidate: () => boolean;
}

const Step2Identity: React.FC<Step2IdentityProps> = ({ formData, setFormData, onValidate }) => {
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { id, value } = e.target;
    setFormData({ ...formData, [id]: value });
  };

  const handleSlugChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const rawSlug = e.target.value;
    const slug = rawSlug.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
    setFormData({ ...formData, slug: slug });
  };

  const domainPrefix = formData.slug || 'novo-agente';
  const fullDomain = `${domainPrefix}.renum.com.br`;

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-[#4e4ea8]">
            <User className="h-5 w-5 mr-2" /> 2. Identidade do Agente
          </CardTitle>
          <CardDescription>
            Defina o nome, descrição e o identificador único do agente.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Name */}
          <div className="space-y-2">
            <Label htmlFor="name">Nome do Agente *</Label>
            <Input
              id="name"
              placeholder="Ex: Agente de Vendas Slim"
              value={formData.name || ''}
              onChange={handleInputChange}
            />
          </div>

          {/* Description */}
          <div className="space-y-2">
            <Label htmlFor="description">Descrição</Label>
            <Textarea
              id="description"
              placeholder="Breve resumo das capacidades e objetivo principal do agente."
              rows={3}
              value={formData.description || ''}
              onChange={handleInputChange}
            />
          </div>

          {/* Slug */}
          <div className="space-y-2">
            <Label htmlFor="slug">Identificador Único (Slug) *</Label>
            <Input
              id="slug"
              placeholder="ex: slim-vendas"
              value={formData.slug || ''}
              onChange={handleSlugChange}
            />
            <p className="text-xs text-muted-foreground">
              Usado para URLs e APIs. Deve ser único e em minúsculas.
            </p>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-[#FF6B35]">
            <Globe className="h-5 w-5 mr-2" /> Domínio e Endpoint
          </CardTitle>
          <CardDescription>
            Onde o agente será acessível (URL de teste e API).
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="domain">Domínio de Teste</Label>
            <Input
              id="domain"
              readOnly
              value={fullDomain}
              className="font-mono bg-gray-100 dark:bg-gray-700"
            />
            <p className="text-xs text-muted-foreground">
              Este é o link para o ambiente de teste do seu agente.
            </p>
          </div>
          <div className="space-y-2">
            <Label htmlFor="api_endpoint">Endpoint da API (Mock)</Label>
            <Input
              id="api_endpoint"
              readOnly
              value={`/api/v1/agents/${domainPrefix}`}
              className="font-mono bg-gray-100 dark:bg-gray-700"
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Step2Identity;