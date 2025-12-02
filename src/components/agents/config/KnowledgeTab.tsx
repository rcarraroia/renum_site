import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Zap, UploadCloud, FileText, Search, Edit, Trash2, Tag } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';
import { Badge } from '@/components/ui/badge';

interface KnowledgeItem {
  id: number;
  title: string;
  type: 'document' | 'text';
  date: string;
  tags: string[];
}

const MOCK_KNOWLEDGE: KnowledgeItem[] = [
  { id: 1, title: 'Manual de Branding Renum', type: 'document', date: '2024-08-01', tags: ['Branding', 'Marketing'] },
  { id: 2, title: 'FAQ de Soluções AI Native', type: 'text', date: '2024-10-25', tags: ['AI Native', 'FAQ'] },
  { id: 3, title: 'Política de Preços 2024', type: 'document', date: '2024-09-10', tags: ['Financeiro'] },
];

const KnowledgeTab: React.FC = () => {
  const [knowledgeItems, setKnowledgeItems] = useState(MOCK_KNOWLEDGE);
  const [newTextContent, setNewTextContent] = useState('');
  const [newTextTitle, setNewTextTitle] = useState('');
  const [testQuery, setTestQuery] = useState('');
  const [isTesting, setIsTesting] = useState(false);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      const newItem: KnowledgeItem = {
        id: Date.now(),
        title: file.name,
        type: 'document',
        date: new Date().toISOString().split('T')[0],
        tags: ['Novo', 'Upload'],
      };
      setKnowledgeItems([newItem, ...knowledgeItems]);
      toast.success(`Documento '${file.name}' enviado e indexado.`);
    }
  };

  const handleAddText = () => {
    if (newTextTitle && newTextContent) {
      const newItem: KnowledgeItem = {
        id: Date.now(),
        title: newTextTitle,
        type: 'text',
        date: new Date().toISOString().split('T')[0],
        tags: ['Manual', 'Criado'],
      };
      setKnowledgeItems([newItem, ...knowledgeItems]);
      setNewTextTitle('');
      setNewTextContent('');
      toast.success(`Conteúdo '${newTextTitle}' adicionado à base de conhecimento.`);
    } else {
      toast.error("Título e conteúdo são obrigatórios.");
    }
  };

  const handleTestQuery = () => {
    if (!testQuery) return;
    setIsTesting(true);
    toast.info(`Consultando base de conhecimento para: "${testQuery}"`);
    setTimeout(() => {
      setIsTesting(false);
      toast.success(`Renus encontrou 3 fontes relevantes para a consulta.`);
    }, 1500);
  };

  return (
    <div className="space-y-8">
      <Card>
        <CardHeader>
          <CardTitle className="text-[#4e4ea8]">Upload de Documentos</CardTitle>
          <CardDescription>Adicione PDFs, manuais ou outros documentos para indexação.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="border-2 border-dashed border-border dark:border-gray-700 rounded-lg p-8 text-center cursor-pointer hover:border-[#0ca7d2] transition-colors">
            <input type="file" className="hidden" id="file-upload" onChange={handleFileUpload} />
            <label htmlFor="file-upload" className="flex flex-col items-center justify-center">
              <UploadCloud className="h-8 w-8 text-muted-foreground mb-2" />
              <p className="text-sm font-medium">Arraste e solte ou clique para fazer upload</p>
              <p className="text-xs text-muted-foreground">PDF, DOCX, TXT (máx. 10MB)</p>
            </label>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-[#FF6B35]">Adicionar Conteúdo de Texto</CardTitle>
          <CardDescription>Crie entradas de conhecimento diretamente no editor.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label htmlFor="text-title">Título</Label>
            <Input id="text-title" value={newTextTitle} onChange={(e) => setNewTextTitle(e.target.value)} placeholder="Ex: Como funciona a Metodologia Frontend Primeiro" />
          </div>
          <div>
            <Label htmlFor="text-content">Conteúdo</Label>
            <Textarea id="text-content" rows={5} value={newTextContent} onChange={(e) => setNewTextContent(e.target.value)} placeholder="Insira o texto que Renus deve aprender..." />
          </div>
          <Button onClick={handleAddText} className="bg-[#FF6B35] hover:bg-[#e55f30]">
            <FileText className="h-4 w-4 mr-2" /> Salvar Conteúdo
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-[#4e4ea8]">Itens na Base de Conhecimento ({knowledgeItems.length})</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex space-x-2 mb-4">
            <Input placeholder="Buscar por título ou tag..." className="flex-grow" />
            <Button variant="outline"><Search className="h-4 w-4" /></Button>
          </div>
          {knowledgeItems.map(item => (
            <div key={item.id} className="flex items-center justify-between p-3 border rounded-lg dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
              <div className="flex-grow">
                <h4 className="font-semibold text-sm flex items-center">
                    {item.type === 'document' ? <FileText className="h-4 w-4 mr-2 text-[#0ca7d2]" /> : <Edit className="h-4 w-4 mr-2 text-[#FF6B35]" />}
                    {item.title}
                </h4>
                <div className="flex space-x-1 mt-1">
                    {item.tags.map(tag => <Badge key={tag} variant="secondary" className="text-xs"><Tag className="h-3 w-3 mr-1" />{tag}</Badge>)}
                </div>
                <p className="text-xs text-muted-foreground mt-1">Adicionado em: {item.date}</p>
              </div>
              <div className="flex space-x-2">
                <Button variant="outline" size="icon"><Edit className="h-4 w-4" /></Button>
                <Button variant="destructive" size="icon"><Trash2 className="h-4 w-4" /></Button>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-[#0ca7d2]">Testar Consulta</CardTitle>
          <CardDescription>Verifique como Renus recupera informações da base de conhecimento.</CardDescription>
        </CardHeader>
        <CardContent className="flex space-x-2">
          <Input
            placeholder="Ex: Qual é a política de preços para projetos grandes?"
            value={testQuery}
            onChange={(e) => setTestQuery(e.target.value)}
            disabled={isTesting}
          />
          <Button onClick={handleTestQuery} disabled={isTesting} className="bg-[#0ca7d2] hover:bg-[#0987a8]">
            <Search className="h-4 w-4 mr-2" /> {isTesting ? 'Testando...' : 'Testar'}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default KnowledgeTab;