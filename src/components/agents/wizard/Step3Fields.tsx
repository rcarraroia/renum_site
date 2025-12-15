import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Plus, Trash2, GripVertical } from 'lucide-react';

interface Step3FieldsProps {
  formData: any;
  setFormData: (data: any) => void;
  onValidate: () => boolean;
}

const standardFields = [
  { id: 'name', label: 'Nome' },
  { id: 'email', label: 'Email' },
  { id: 'phone', label: 'Telefone/WhatsApp' },
  { id: 'country', label: 'País' },
  { id: 'company', label: 'Empresa' },
];

const fieldTypes = [
  { value: 'text', label: 'Texto Curto' },
  { value: 'textarea', label: 'Texto Longo' },
  { value: 'number', label: 'Número' },
  { value: 'date', label: 'Data' },
  { value: 'time', label: 'Hora' },
  { value: 'radio', label: 'Múltipla Escolha (Radio)' },
  { value: 'checkbox', label: 'Caixa de Seleção' },
  { value: 'dropdown', label: 'Lista Suspensa' },
];

const Step3Fields: React.FC<Step3FieldsProps> = ({ formData, setFormData }) => {
  const [newFieldLabel, setNewFieldLabel] = useState('');
  const [newFieldType, setNewFieldType] = useState('text');

  const standardFieldsConfig = formData.standard_fields || {};
  const customFields = formData.custom_fields || [];

  const handleStandardFieldToggle = (fieldId: string, checked: boolean) => {
    const updated = {
      ...standardFieldsConfig,
      [fieldId]: {
        ...standardFieldsConfig[fieldId],
        enabled: checked,
        required: standardFieldsConfig[fieldId]?.required || false,
      },
    };
    setFormData({ ...formData, standard_fields: updated });
  };

  const handleStandardFieldRequired = (fieldId: string, required: boolean) => {
    const updated = {
      ...standardFieldsConfig,
      [fieldId]: {
        ...standardFieldsConfig[fieldId],
        required,
      },
    };
    setFormData({ ...formData, standard_fields: updated });
  };

  const handleAddCustomField = () => {
    if (!newFieldLabel.trim()) return;

    const newField = {
      id: `custom_${Date.now()}`,
      label: newFieldLabel,
      type: newFieldType,
      required: false,
      order: customFields.length,
    };

    setFormData({
      ...formData,
      custom_fields: [...customFields, newField],
    });

    setNewFieldLabel('');
    setNewFieldType('text');
  };

  const handleRemoveCustomField = (fieldId: string) => {
    setFormData({
      ...formData,
      custom_fields: customFields.filter((f: any) => f.id !== fieldId),
    });
  };

  const handleCustomFieldUpdate = (fieldId: string, updates: any) => {
    setFormData({
      ...formData,
      custom_fields: customFields.map((f: any) =>
        f.id === fieldId ? { ...f, ...updates } : f
      ),
    });
  };

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Campos Padrão</h3>
        <Card>
          <CardContent className="p-4 space-y-3">
            {standardFields.map((field) => {
              const config = standardFieldsConfig[field.id] || { enabled: false, required: false };
              
              return (
                <div key={field.id} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <Checkbox
                      checked={config.enabled}
                      onCheckedChange={(checked) =>
                        handleStandardFieldToggle(field.id, checked as boolean)
                      }
                    />
                    <Label className="cursor-pointer">{field.label}</Label>
                  </div>
                  {config.enabled && (
                    <div className="flex items-center space-x-2">
                      <Checkbox
                        checked={config.required}
                        onCheckedChange={(checked) =>
                          handleStandardFieldRequired(field.id, checked as boolean)
                        }
                      />
                      <span className="text-sm text-muted-foreground">Obrigatório</span>
                    </div>
                  )}
                </div>
              );
            })}
          </CardContent>
        </Card>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-4">Campos Personalizados</h3>
        
        <div className="space-y-3 mb-4">
          {customFields.map((field: any) => (
            <Card key={field.id}>
              <CardContent className="p-4">
                <div className="flex items-start space-x-3">
                  <GripVertical className="h-5 w-5 text-muted-foreground mt-1 cursor-move" />
                  <div className="flex-1 space-y-2">
                    <div className="flex items-center justify-between">
                      <Input
                        value={field.label}
                        onChange={(e) =>
                          handleCustomFieldUpdate(field.id, { label: e.target.value })
                        }
                        placeholder="Nome do campo"
                        className="max-w-xs"
                      />
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleRemoveCustomField(field.id)}
                      >
                        <Trash2 className="h-4 w-4 text-red-500" />
                      </Button>
                    </div>
                    <div className="flex items-center space-x-4">
                      <Select
                        value={field.type}
                        onValueChange={(value) =>
                          handleCustomFieldUpdate(field.id, { type: value })
                        }
                      >
                        <SelectTrigger className="w-48">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {fieldTypes.map((type) => (
                            <SelectItem key={type.value} value={type.value}>
                              {type.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <div className="flex items-center space-x-2">
                        <Checkbox
                          checked={field.required}
                          onCheckedChange={(checked) =>
                            handleCustomFieldUpdate(field.id, { required: checked })
                          }
                        />
                        <span className="text-sm text-muted-foreground">Obrigatório</span>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-end space-x-3">
              <div className="flex-1">
                <Label htmlFor="new-field-label">Adicionar Campo</Label>
                <Input
                  id="new-field-label"
                  placeholder="Nome do campo"
                  value={newFieldLabel}
                  onChange={(e) => setNewFieldLabel(e.target.value)}
                  className="mt-1"
                />
              </div>
              <div className="w-48">
                <Label htmlFor="new-field-type">Tipo</Label>
                <Select value={newFieldType} onValueChange={setNewFieldType}>
                  <SelectTrigger className="mt-1">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {fieldTypes.map((type) => (
                      <SelectItem key={type.value} value={type.value}>
                        {type.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <Button onClick={handleAddCustomField} className="bg-[#FF6B35] hover:bg-[#e55f30]">
                <Plus className="h-4 w-4 mr-2" />
                Adicionar
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-3">Fluxo de Conversação</h3>
        <Card>
          <CardContent className="p-4">
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground mb-3">
                O agente perguntará na seguinte ordem:
              </p>
              {Object.entries(standardFieldsConfig)
                .filter(([_, config]: any) => config.enabled)
                .map(([fieldId, config]: any, index) => {
                  const field = standardFields.find((f) => f.id === fieldId);
                  return (
                    <div key={fieldId} className="flex items-center space-x-2 text-sm">
                      <span className="font-mono text-muted-foreground">{index + 1}.</span>
                      <span>{field?.label}</span>
                      {config.required && (
                        <span className="text-xs text-red-500">(obrigatório)</span>
                      )}
                    </div>
                  );
                })}
              {customFields.map((field: any, index: number) => {
                const startIndex = Object.values(standardFieldsConfig).filter(
                  (c: any) => c.enabled
                ).length;
                return (
                  <div key={field.id} className="flex items-center space-x-2 text-sm">
                    <span className="font-mono text-muted-foreground">
                      {startIndex + index + 1}.
                    </span>
                    <span>{field.label}</span>
                    {field.required && (
                      <span className="text-xs text-red-500">(obrigatório)</span>
                    )}
                  </div>
                );
              })}
              {Object.values(standardFieldsConfig).filter((c: any) => c.enabled).length === 0 &&
                customFields.length === 0 && (
                  <p className="text-sm text-muted-foreground italic">
                    Nenhum campo selecionado ainda
                  </p>
                )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Step3Fields;
