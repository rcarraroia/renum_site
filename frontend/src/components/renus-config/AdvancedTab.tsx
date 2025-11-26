import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Zap, Info, DollarSign } from 'lucide-react';

export const AdvancedTab = () => {
  const [config, setConfig] = useState({
    provider: 'openrouter',
    model: 'anthropic/claude-sonnet-4',
    temperature: 0.7,
    maxTokens: 4000,
    apiKey: ''
  });

  const modelOptions = [
    { 
      value: 'anthropic/claude-sonnet-4', 
      label: 'Claude Sonnet 4',
      tier: 'premium',
      cost: '$15/1M tokens'
    },
    { 
      value: 'openai/gpt-4o', 
      label: 'GPT-4 Turbo',
      tier: 'premium',
      cost: '$10/1M tokens'
    },
    { 
      value: 'openai/gpt-4o-mini', 
      label: 'GPT-4o Mini',
      tier: 'standard',
      cost: '$0.15/1M tokens'
    },
    { 
      value: 'google/gemini-pro-1.5', 
      label: 'Gemini Pro 1.5',
      tier: 'standard',
      cost: '$7/1M tokens'
    },
    { 
      value: 'meta-llama/llama-3.1-8b-instruct:free', 
      label: 'Llama 3.1 8B',
      tier: 'free',
      cost: 'FREE'
    },
    { 
      value: 'meta-llama/llama-3.1-70b-instruct', 
      label: 'Llama 3.1 70B',
      tier: 'standard',
      cost: '$0.80/1M tokens'
    }
  ];

  const selectedModelInfo = modelOptions.find(m => m.value === config.model);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-[#4e4ea8] flex items-center gap-2">
          <Zap className="h-6 w-6" />
          Configurações Avançadas
        </h2>
        <p className="text-muted-foreground mt-1">
          Configure o modelo de IA, parâmetros e integrações avançadas
        </p>
      </div>

      {/* Provider Section */}
      <Card>
        <CardHeader>
          <CardTitle>Provider de IA</CardTitle>
          <CardDescription>
            OpenRouter oferece acesso unificado a múltiplos modelos de IA
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>Provider</Label>
            <Select value={config.provider} onValueChange={(value) => setConfig({...config, provider: value})}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="openrouter">
                  <div className="flex items-center gap-2">
                    <span>OpenRouter</span>
                    <Badge variant="secondary" className="text-xs">Recomendado</Badge>
                  </div>
                </SelectItem>
                <SelectItem value="openai">OpenAI Direto</SelectItem>
                <SelectItem value="anthropic">Anthropic Direto</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label>API Key do OpenRouter</Label>
            <Input
              type="password"
              placeholder="sk-or-v1-..."
              value={config.apiKey}
              onChange={(e) => setConfig({...config, apiKey: e.target.value})}
            />
            <p className="text-xs text-muted-foreground">
              Obtenha sua chave em: <a href="https://openrouter.ai/keys" target="_blank" className="text-[#0ca7d2] hover:underline">openrouter.ai/keys</a>
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Model Configuration */}
      <Card>
        <CardHeader>
          <CardTitle>Modelo Padrão (Agente Principal)</CardTitle>
          <CardDescription>
            Este modelo será usado pelo agente Renus principal. Sub-agentes podem ter modelos diferentes.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>Modelo de IA</Label>
            <Select value={config.model} onValueChange={(value) => setConfig({...config, model: value})}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {modelOptions.map((model) => (
                  <SelectItem key={model.value} value={model.value}>
                    <div className="flex items-center justify-between w-full">
                      <span>{model.label}</span>
                      <div className="flex items-center gap-2 ml-4">
                        <Badge 
                          variant="outline" 
                          className={
                            model.tier === 'premium' ? 'border-purple-500 text-purple-700' :
                            model.tier === 'free' ? 'border-green-500 text-green-700' :
                            'border-blue-500 text-blue-700'
                          }
                        >
                          {model.tier}
                        </Badge>
                        <span className="text-xs text-muted-foreground">{model.cost}</span>
                      </div>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {selectedModelInfo && (
            <Alert>
              <DollarSign className="h-4 w-4" />
              <AlertDescription>
                <strong>{selectedModelInfo.label}</strong> • {selectedModelInfo.cost}
              </AlertDescription>
            </Alert>
          )}

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label>Temperature</Label>
              <span className="text-sm text-muted-foreground">{config.temperature}</span>
            </div>
            <Slider
              value={[config.temperature]}
              onValueChange={(value) => setConfig({...config, temperature: value[0]})}
              min={0}
              max={2}
              step={0.1}
              className="w-full"
            />
            <p className="text-xs text-muted-foreground">
              Menor = mais preciso e consistente | Maior = mais criativo e variado
            </p>
          </div>

          <div className="space-y-2">
            <Label>Max Tokens</Label>
            <Input
              type="number"
              value={config.maxTokens}
              onChange={(e) => setConfig({...config, maxTokens: parseInt(e.target.value)})}
              min={100}
              max={8000}
            />
            <p className="text-xs text-muted-foreground">
              Limite de tokens por resposta (recomendado: 2000-4000)
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Info Box */}
      <Alert>
        <Info className="h-4 w-4" />
        <AlertDescription>
          <strong>Dica:</strong> Modelos diferentes têm custos e capacidades variadas. 
          Use modelos premium (Claude Sonnet 4, GPT-4) para tarefas críticas e modelos 
          mais baratos ou FREE para testes e tarefas simples.
        </AlertDescription>
      </Alert>
    </div>
  );
};