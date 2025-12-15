import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { siccService } from '@/services/siccService';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Brain, Search, Plus, Filter } from 'lucide-react';

export default function MemoryManagerPage() {
  return (
    <DashboardLayout>
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold">🧠 Gerenciador de Memórias</h1>
          <Button className="bg-purple-600 hover:bg-purple-700">
            <Plus className="h-4 w-4 mr-2" />
            Nova Memória
          </Button>
        </div>

        <div className="grid gap-6 md:grid-cols-4 mb-6">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Total Memórias</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">1,234</div>
              <Badge variant="secondary" className="mt-1">Ativas</Badge>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">FAQ</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">456</div>
              <Badge variant="outline" className="mt-1">37%</Badge>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Termos Negócio</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">321</div>
              <Badge variant="outline" className="mt-1">26%</Badge>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Estratégias</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">457</div>
              <Badge variant="outline" className="mt-1">37%</Badge>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>📋 Lista de Memórias</CardTitle>
              <div className="flex space-x-2">
                <Button variant="outline" size="sm">
                  <Search className="h-4 w-4 mr-2" />
                  Buscar
                </Button>
                <Button variant="outline" size="sm">
                  <Filter className="h-4 w-4 mr-2" />
                  Filtrar
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="border rounded-lg p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <Badge variant="secondary">FAQ</Badge>
                      <Badge variant="outline">Confiança: 92%</Badge>
                    </div>
                    <p className="text-sm font-medium mb-1">
                      O processo de onboarding para novos distribuidores MMN envolve 3 etapas...
                    </p>
                    <p className="text-xs text-muted-foreground">
                      Usado 150 vezes • Criado há 5 dias
                    </p>
                  </div>
                  <Button variant="ghost" size="sm">
                    Editar
                  </Button>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <Badge variant="secondary">Termo Negócio</Badge>
                      <Badge variant="outline">Confiança: 88%</Badge>
                    </div>
                    <p className="text-sm font-medium mb-1">
                      A política de descontos para grandes volumes é aplicada automaticamente...
                    </p>
                    <p className="text-xs text-muted-foreground">
                      Usado 88 vezes • Criado há 10 dias
                    </p>
                  </div>
                  <Button variant="ghost" size="sm">
                    Editar
                  </Button>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <Badge variant="secondary">Estratégia</Badge>
                      <Badge variant="outline">Confiança: 75%</Badge>
                    </div>
                    <p className="text-sm font-medium mb-1">
                      Se o cliente perguntar sobre o concorrente X, a resposta padrão é focar...
                    </p>
                    <p className="text-xs text-muted-foreground">
                      Usado 32 vezes • Criado há 2 dias
                    </p>
                  </div>
                  <Button variant="ghost" size="sm">
                    Editar
                  </Button>
                </div>
              </div>
            </div>

            <div className="mt-6 text-center text-muted-foreground">
              <p>Funcionalidades avançadas (busca, filtros, edição) serão implementadas em breve</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}