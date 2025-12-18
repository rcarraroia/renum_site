import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Plus, Trash2, Globe, Database, MessageSquare, Mail, BookOpen, Upload, FileText } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';

interface Step5ToolsProps {
    formData: any;
    setFormData: (data: any) => void;
}

const standardFields = [
    { id: 'name', label: 'Nome' },
    { id: 'email', label: 'Email' },
    { id: 'phone', label: 'WhatsApp' },
];

const integrations = [
    { id: 'whatsapp', name: 'WhatsApp Business', icon: MessageSquare, color: 'bg-green-500' },
    { id: 'email', name: 'Email', icon: Mail, color: 'bg-blue-500' },
    { id: 'database', name: 'Z-API / CRM', icon: Database, color: 'bg-purple-500' },
];

const Step5Tools: React.FC<Step5ToolsProps> = ({ formData, setFormData }) => {
    const [activeTab, setActiveTab] = useState('fields');
    const [newFile, setNewFile] = useState<File | null>(null);

    const updateField = (key: string, value: any) => {
        setFormData({ ...formData, [key]: value });
    };

    const handleStandardFieldToggle = (fieldId: string, checked: boolean) => {
        const config = formData.standard_fields || {};
        updateField('standard_fields', {
            ...config,
            [fieldId]: { ...config[fieldId], enabled: checked }
        });
    };

    const handleIntegrationToggle = (id: string, checked: boolean) => {
        const config = formData.integrations || {};
        updateField('integrations', { ...config, [id]: checked });
    };

    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            setNewFile(file);
            toast.success(`Arquivo ${file.name} pronto para upload.`);
            // No futuro, isso enviaria para o knowledgeService.upload
        }
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                <TabsList className="grid grid-cols-3 w-full">
                    <TabsTrigger value="fields" className="flex items-center space-x-2">
                        <FileText className="h-4 w-4" /> <span>Campos</span>
                    </TabsTrigger>
                    <TabsTrigger value="knowledge" className="flex items-center space-x-2">
                        <BookOpen className="h-4 w-4" /> <span>Conhecimento</span>
                    </TabsTrigger>
                    <TabsTrigger value="integrations" className="flex items-center space-x-2">
                        <Globe className="h-4 w-4" /> <span>Integrações</span>
                    </TabsTrigger>
                </TabsList>

                <TabsContent value="fields" className="mt-6 space-y-4">
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-base text-[#4e4ea8]">Captura de Leads</CardTitle>
                            <CardDescription>Quais dados o agente deve solicitar ao usuário?</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-3">
                            {standardFields.map(f => (
                                <div key={f.id} className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50 transition-colors">
                                    <div className="flex items-center space-x-3">
                                        <Checkbox
                                            id={`field-${f.id}`}
                                            checked={formData.standard_fields?.[f.id]?.enabled || false}
                                            onCheckedChange={(v) => handleStandardFieldToggle(f.id, v as boolean)}
                                        />
                                        <Label htmlFor={`field-${f.id}`} className="cursor-pointer font-medium">{f.label}</Label>
                                    </div>
                                    {formData.standard_fields?.[f.id]?.enabled && (
                                        <Badge variant="secondary" className="bg-blue-100 text-blue-700">Ativo</Badge>
                                    )}
                                </div>
                            ))}
                            <Button variant="outline" className="w-full border-dashed">
                                <Plus className="h-4 w-4 mr-2" /> Adicionar Campo Personalizado
                            </Button>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="knowledge" className="mt-6 space-y-4">
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-base text-[#FF6B35]">Base de Conhecimento</CardTitle>
                            <CardDescription>Faça upload de documentos para treinar seu agente.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-xl p-8 flex flex-col items-center justify-center text-center space-y-4 hover:border-[#FF6B35]/50 transition-colors cursor-pointer relative">
                                <Input
                                    type="file"
                                    className="absolute inset-0 opacity-0 cursor-pointer"
                                    onChange={handleFileUpload}
                                    accept=".pdf,.txt,.docx"
                                />
                                <div className="bg-orange-100 p-4 rounded-full">
                                    <Upload className="h-8 w-8 text-[#FF6B35]" />
                                </div>
                                <div>
                                    <p className="font-bold">Clique ou arraste arquivos</p>
                                    <p className="text-sm text-muted-foreground">PDF, TXT ou DOCX (Max 10MB)</p>
                                </div>
                            </div>

                            {newFile && (
                                <div className="mt-4 p-3 bg-green-50 border border-green-100 rounded-lg flex items-center justify-between">
                                    <span className="text-sm font-medium text-green-700">{newFile.name}</span>
                                    <Button variant="ghost" size="sm" onClick={() => setNewFile(null)}>
                                        <Trash2 className="h-4 w-4 text-red-500" />
                                    </Button>
                                </div>
                            )}
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="integrations" className="mt-6 space-y-4">
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-base text-[#4e4ea8]">Conexões Externas</CardTitle>
                            <CardDescription>Vincule o seu agente com outras plataformas.</CardDescription>
                        </CardHeader>
                        <CardContent className="grid grid-cols-1 gap-3">
                            {integrations.map(i => (
                                <div key={i.id} className="flex items-center justify-between p-3 border rounded-lg">
                                    <div className="flex items-center space-x-3">
                                        <div className={cn("p-2 rounded-lg text-white", i.color)}>
                                            <i.icon className="h-5 w-5" />
                                        </div>
                                        <div>
                                            <p className="font-bold text-sm">{i.name}</p>
                                        </div>
                                    </div>
                                    <Checkbox
                                        checked={formData.integrations?.[i.id] || false}
                                        onCheckedChange={(v) => handleIntegrationToggle(i.id, v as boolean)}
                                    />
                                </div>
                            ))}
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
};

export default Step5Tools;
