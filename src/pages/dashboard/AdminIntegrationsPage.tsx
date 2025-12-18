import React, { useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import IntegrationsTab from '@/components/agents/config/IntegrationsTab';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { RefreshCw, Zap, Clock, Search } from 'lucide-react';

const AdminIntegrationsPage: React.FC = () => {
    return (
        <DashboardLayout>
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold flex items-center">
                    <RefreshCw className="h-7 w-7 mr-3 text-[#4e4ea8]" />
                    Radar de Integrações
                </h2>
                <div className="flex items-center space-x-2">
                    <Badge className="bg-blue-600 text-white">Modo Administrador</Badge>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <Card className="bg-green-50/50 border-green-200">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-green-700 flex items-center">
                            <Zap className="h-4 w-4 mr-2" /> Ativas
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-green-700">3</div>
                    </CardContent>
                </Card>
                <Card className="bg-orange-50/50 border-orange-200">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-orange-700 flex items-center">
                            <Clock className="h-4 w-4 mr-2" /> Roadmap
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-orange-700">3</div>
                    </CardContent>
                </Card>
                <Card className="bg-purple-50/50 border-purple-200">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-purple-700 flex items-center">
                            <Search className="h-4 w-4 mr-2" /> Solicitadas
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-purple-700">0</div>
                    </CardContent>
                </Card>
            </div>

            <IntegrationsTab />
        </DashboardLayout>
    );
};

export default AdminIntegrationsPage;
