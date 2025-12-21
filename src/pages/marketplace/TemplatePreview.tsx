/**
 * Task 25 (continuação): Template Preview Page
 */

import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowLeft, Star, Download, Settings } from 'lucide-react';

interface TemplateDetails {
    id: string;
    name: string;
    description: string;
    category: string;
    niche: string;
    rating: number;
    usage_count: number;
    config: {
        instructions?: { system_prompt?: string; persona?: string };
        intelligence?: { model?: string; temperature?: number };
        tools?: { enabled_tools?: string[] };
    };
}

export const TemplatePreview: React.FC = () => {
    const { templateId } = useParams<{ templateId: string }>();
    const [template, setTemplate] = useState<TemplateDetails | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadTemplate();
    }, [templateId]);

    const loadTemplate = async () => {
        try {
            const res = await fetch(`/api/agents/${templateId}`);
            const data = await res.json();
            setTemplate(data);
        } catch (error) {
            console.error('Erro ao carregar template:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="p-6">Carregando...</div>;
    if (!template) return <div className="p-6">Template não encontrado</div>;

    return (
        <div className="p-6 space-y-6">
            <Link to="/dashboard/marketplace" className="flex items-center gap-2 text-muted-foreground hover:text-foreground">
                <ArrowLeft className="h-4 w-4" />
                Voltar ao Marketplace
            </Link>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Info Principal */}
                <div className="lg:col-span-2 space-y-6">
                    <Card>
                        <CardHeader>
                            <div className="flex justify-between items-start">
                                <div>
                                    <CardTitle className="text-2xl">{template.name}</CardTitle>
                                    <div className="flex items-center gap-2 mt-2">
                                        <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm uppercase">
                                            {template.category}
                                        </span>
                                        <span className="px-2 py-1 bg-gray-100 text-gray-800 rounded text-sm">
                                            {template.niche}
                                        </span>
                                        <div className="flex items-center gap-1 text-yellow-500">
                                            <Star className="h-4 w-4 fill-current" />
                                            <span>{template.rating.toFixed(1)}</span>
                                        </div>
                                    </div>
                                </div>
                                <div className="flex items-center gap-1 text-muted-foreground">
                                    <Download className="h-4 w-4" />
                                    <span>{template.usage_count} usos</span>
                                </div>
                            </div>
                        </CardHeader>
                        <CardContent>
                            <p className="text-muted-foreground">{template.description}</p>
                        </CardContent>
                    </Card>

                    {/* Preview do System Prompt */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-lg">System Prompt</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="bg-gray-50 p-4 rounded-md font-mono text-sm whitespace-pre-wrap">
                                {template.config.instructions?.system_prompt || 'Não definido'}
                            </div>
                        </CardContent>
                    </Card>

                    {/* Configurações */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-lg flex items-center gap-2">
                                <Settings className="h-5 w-5" />
                                Configurações Incluídas
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <p className="font-medium">Modelo</p>
                                    <p className="text-muted-foreground">{template.config.intelligence?.model || 'gpt-4o-mini'}</p>
                                </div>
                                <div>
                                    <p className="font-medium">Temperatura</p>
                                    <p className="text-muted-foreground">{template.config.intelligence?.temperature || 0.7}</p>
                                </div>
                                <div className="col-span-2">
                                    <p className="font-medium">Ferramentas</p>
                                    <div className="flex flex-wrap gap-2 mt-2">
                                        {template.config.tools?.enabled_tools?.map(tool => (
                                            <span key={tool} className="px-2 py-1 bg-green-100 text-green-800 rounded text-sm">
                                                {tool}
                                            </span>
                                        )) || <span className="text-muted-foreground">Nenhuma ferramenta configurada</span>}
                                    </div>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Sidebar */}
                <div className="space-y-4">
                    <Card>
                        <CardContent className="p-6">
                            <Link to={`/dashboard/agents/wizard/new?template=${template.id}`}>
                                <Button className="w-full mb-4" size="lg">
                                    Usar este Template
                                </Button>
                            </Link>
                            <p className="text-sm text-muted-foreground text-center">
                                Você poderá personalizar todas as configurações após selecionar o template
                            </p>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
};

export default TemplatePreview;
