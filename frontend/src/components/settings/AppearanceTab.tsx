import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Palette, LayoutGrid, Globe, Save } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useTheme } from '@/context/ThemeContext';
import { toast } from 'sonner';

const AppearanceTab: React.FC = () => {
    const { theme, setTheme } = useTheme();
    const [layout, setLayout] = useState('default');
    const [language, setLanguage] = useState('pt-BR');

    const handleSave = () => {
        toast.success("Preferências de aparência salvas!");
    };

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#4e4ea8]"><Palette className="h-5 w-5 mr-2" /> Tema</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <Label>Seleção de Tema</Label>
                    <div className="grid grid-cols-3 gap-4">
                        <div 
                            className={`p-4 border rounded-lg text-center cursor-pointer ${theme === 'light' ? 'border-2 border-[#FF6B35] bg-gray-50' : 'hover:bg-gray-100 dark:hover:bg-gray-800'}`}
                            onClick={() => setTheme('light')}
                        >
                            Claro
                        </div>
                        <div 
                            className={`p-4 border rounded-lg text-center cursor-pointer ${theme === 'dark' ? 'border-2 border-[#FF6B35] bg-gray-800 text-white' : 'hover:bg-gray-800 dark:hover:bg-gray-700'}`}
                            onClick={() => setTheme('dark')}
                        >
                            Escuro
                        </div>
                        <div 
                            className={`p-4 border rounded-lg text-center cursor-pointer ${theme === 'system' ? 'border-2 border-[#FF6B35] bg-gray-50 dark:bg-gray-800' : 'hover:bg-gray-100 dark:hover:bg-gray-800'}`}
                            onClick={() => setTheme('system')}
                        >
                            Sistema
                        </div>
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader><CardTitle className="flex items-center text-[#0ca7d2]"><Globe className="h-5 w-5 mr-2" /> Regional</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <div>
                        <Label>Idioma do Dashboard</Label>
                        <Select value={language} onValueChange={setLanguage}>
                            <SelectTrigger className="w-[180px]"><SelectValue placeholder="Idioma" /></SelectTrigger>
                            <SelectContent>
                                <SelectItem value="pt-BR">Português (Brasil)</SelectItem>
                                <SelectItem value="en-US">English (US)</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div>
                        <Label>Formato de Data/Hora</Label>
                        <Select defaultValue="dd/MM/yyyy">
                            <SelectTrigger className="w-[180px]"><SelectValue placeholder="Formato" /></SelectTrigger>
                            <SelectContent>
                                <SelectItem value="dd/MM/yyyy">dd/MM/yyyy</SelectItem>
                                <SelectItem value="MM/dd/yyyy">MM/dd/yyyy</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </CardContent>
            </Card>
            
            <div className="flex justify-end">
                <Button onClick={handleSave} className="bg-[#FF6B35] hover:bg-[#e55f30]">
                    <Save className="h-4 w-4 mr-2" /> Salvar Aparência
                </Button>
            </div>
        </div>
    );
};

export default AppearanceTab;