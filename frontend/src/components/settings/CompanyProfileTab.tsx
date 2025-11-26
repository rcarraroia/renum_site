import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Building, Mail, Phone, MapPin, Clock, Upload, Save } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { toast } from 'sonner';

const MOCK_PROFILE = {
    name: 'Renum Tech Agency',
    cnpj: '00.000.000/0001-00',
    email: 'contato@renum.tech',
    phone: '(11) 98765-4321',
    address: 'Rua da Inovação, 123, São Paulo - SP',
    hours: 'Seg - Sex, 9h - 18h',
    logoUrl: '/public/placeholder.svg',
};

const CompanyProfileTab: React.FC = () => {
    const [profile, setProfile] = useState(MOCK_PROFILE);
    const [isSaving, setIsSaving] = useState(false);

    const handleSave = () => {
        setIsSaving(true);
        setTimeout(() => {
            setIsSaving(false);
            toast.success("Perfil da empresa atualizado com sucesso!");
        }, 1000);
    };

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#4e4ea8]"><Building className="h-5 w-5 mr-2" /> Informações Básicas</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <div className="grid md:grid-cols-2 gap-4">
                        <div><Label htmlFor="name">Nome da Empresa</Label><Input id="name" value={profile.name} onChange={(e) => setProfile({...profile, name: e.target.value})} /></div>
                        <div><Label htmlFor="cnpj">CNPJ</Label><Input id="cnpj" value={profile.cnpj} onChange={(e) => setProfile({...profile, cnpj: e.target.value})} /></div>
                        <div><Label htmlFor="email">Email de Contato</Label><Input id="email" type="email" value={profile.email} onChange={(e) => setProfile({...profile, email: e.target.value})} /></div>
                        <div><Label htmlFor="phone">Telefone</Label><Input id="phone" value={profile.phone} onChange={(e) => setProfile({...profile, phone: e.target.value})} /></div>
                    </div>
                    <div><Label htmlFor="address">Endereço Completo</Label><Textarea id="address" rows={2} value={profile.address} onChange={(e) => setProfile({...profile, address: e.target.value})} /></div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#FF6B35]"><Clock className="h-5 w-5 mr-2" /> Horário de Funcionamento</CardTitle></CardHeader>
                <CardContent>
                    <div><Label htmlFor="hours">Horário</Label><Input id="hours" value={profile.hours} onChange={(e) => setProfile({...profile, hours: e.target.value})} placeholder="Seg - Sex, 9h - 18h" /></div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#0ca7d2]"><Upload className="h-5 w-5 mr-2" /> Branding e Logo</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center space-x-4">
                        <img src={profile.logoUrl} alt="Logo Preview" className="h-16 w-16 object-contain border p-1 rounded-md dark:bg-white" />
                        <Button variant="outline"><Upload className="h-4 w-4 mr-2" /> Upload Novo Logo</Button>
                    </div>
                    <Separator />
                    <div><Label>Cor Primária (Mock)</Label><Input type="color" defaultValue="#4e4ea8" className="w-24 h-10 p-1" /></div>
                </CardContent>
            </Card>
            
            <div className="flex justify-end">
                <Button onClick={handleSave} disabled={isSaving} className="bg-[#FF6B35] hover:bg-[#e55f30]">
                    <Save className="h-4 w-4 mr-2" /> {isSaving ? 'Salvando...' : 'Salvar Perfil'}
                </Button>
            </div>
        </div>
    );
};

export default CompanyProfileTab;