/**
 * Task 25: Template Marketplace - IMPLEMENTAÇÃO REAL
 * Navegação, filtros e seleção de templates
 */

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Search, Star, Download, Eye, Filter } from 'lucide-react';
import { Link } from 'react-router-dom';

interface Template {
    id: string;
    name: string;
    description: string;
    category: 'b2b' | 'b2c';
    niche: string;
    rating: number;
    usage_count: number;
    preview_image?: string;
    config: Record<string, unknown>;
}

export const TemplateMarketplace: React.FC = () => {
    const [templates, setTemplates] = useState<Template[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [categoryFilter, setCategoryFilter] = useState<string>('all');
    const [nicheFilter, setNicheFilter] = useState<string>('all');

    useEffect(() => {
        loadTemplates();
    }, [categoryFilter, nicheFilter]);

    const loadTemplates = async () => {
        try {
            setLoading(true);
            let url = '/api/agents/wizard/templates?';
            if (categoryFilter !== 'all') url += `category=${categoryFilter}&`;
            if (nicheFilter !== 'all') url += `niche=${nicheFilter}&`;

            const res = await fetch(url);
            const data = await res.json();
            setTemplates(data);
        } catch (error) {
            console.error('Erro ao carregar templates:', error);
        } finally {
            setLoading(false);
        }
    };

    const filteredTemplates = templates.filter(t =>
        t.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.description.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const niches = ['vendas', 'suporte', 'marketing', 'rh', 'financeiro', 'saude', 'educacao'];

    return (
        <div className="p-6 space-y-6">
            {/* Header */}
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold">Marketplace de Templates</h1>
                    <p className="text-muted-foreground">
                        Encontre templates prontos para acelerar a criação do seu agente
                    </p>
                </div>
                <Link to="/dashboard/agents/wizard/new">
                    <Button>Criar do Zero</Button>
                </Link>
            </div>

            {/* Filtros */}
            <div className="flex flex-wrap gap-4">
                <div className="flex-1 min-w-[300px]">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                        <Input
                            placeholder="Buscar templates..."
                            className="pl-10"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>
                </div>

                <select
                    className="border rounded-md px-4 py-2"
                    value={categoryFilter}
                    onChange={(e) => setCategoryFilter(e.target.value)}
                >
                    <option value="all">Todas Categorias</option>
                    <option value="b2b">B2B</option>
                    <option value="b2c">B2C</option>
                </select>

                <select
                    className="border rounded-md px-4 py-2"
                    value={nicheFilter}
                    onChange={(e) => setNicheFilter(e.target.value)}
                >
                    <option value="all">Todos os Nichos</option>
                    {niches.map(niche => (
                        <option key={niche} value={niche}>{niche.charAt(0).toUpperCase() + niche.slice(1)}</option>
                    ))}
                </select>
            </div>

            {/* Grid de Templates */}
            {loading ? (
                <div className="text-center py-12">Carregando templates...</div>
            ) : filteredTemplates.length === 0 ? (
                <Card>
                    <CardContent className="py-12 text-center">
                        <p className="text-muted-foreground">Nenhum template encontrado.</p>
                        <p className="text-sm mt-2">Tente ajustar os filtros ou criar um agente do zero.</p>
                    </CardContent>
                </Card>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredTemplates.map((template) => (
                        <Card key={template.id} className="hover:shadow-lg transition-shadow">
                            <CardHeader>
                                <div className="flex justify-between items-start">
                                    <div>
                                        <CardTitle>{template.name}</CardTitle>
                                        <div className="flex items-center gap-2 mt-1">
                                            <span className="px-2 py-0.5 bg-blue-100 text-blue-800 rounded text-xs uppercase">
                                                {template.category}
                                            </span>
                                            <span className="px-2 py-0.5 bg-gray-100 text-gray-800 rounded text-xs">
                                                {template.niche}
                                            </span>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-1 text-yellow-500">
                                        <Star className="h-4 w-4 fill-current" />
                                        <span className="text-sm">{template.rating.toFixed(1)}</span>
                                    </div>
                                </div>
                                <CardDescription className="line-clamp-2">
                                    {template.description}
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="flex items-center justify-between text-sm text-muted-foreground mb-4">
                                    <span className="flex items-center gap-1">
                                        <Download className="h-4 w-4" />
                                        {template.usage_count} usos
                                    </span>
                                </div>
                                <div className="flex gap-2">
                                    <Link to={`/dashboard/marketplace/template/${template.id}/preview`} className="flex-1">
                                        <Button variant="outline" className="w-full">
                                            <Eye className="h-4 w-4 mr-2" />
                                            Preview
                                        </Button>
                                    </Link>
                                    <Link to={`/dashboard/agents/wizard/new?template=${template.id}`} className="flex-1">
                                        <Button className="w-full">
                                            Usar Template
                                        </Button>
                                    </Link>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}
        </div>
    );
};

export default TemplateMarketplace;
