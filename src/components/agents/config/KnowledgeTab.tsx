import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { UploadCloud, FileText, Search, Trash2, Loader2, Database } from 'lucide-react';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import agentService from '@/services/agentService';
import { knowledgeService, KnowledgeDocument, SearchResult } from '@/services/knowledgeService';

const KnowledgeTab: React.FC = () => {
  const [agent, setAgent] = useState<any>(null);
  const [documents, setDocuments] = useState<KnowledgeDocument[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  const [testQuery, setTestQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setIsLoading(true);
      // Load Agent (Try getting Renus)
      let agentData;
      try {
        // Try strictly renus first
        agentData = await agentService.getAgentBySlug('renus');
      } catch {
        // Fallback to first available if renus not found
        const agents = await agentService.listAgents();
        agentData = agents.find((a: any) => a.slug === 'renus' || a.role === 'system_orchestrator');
      }

      if (agentData) {
        setAgent(agentData);
        // Load Documents
        const docs = await knowledgeService.listDocuments(agentData.id);
        setDocuments(docs || []);
      }
    } catch (error) {
      console.error(error);
      toast.error("Erro ao carregar base de conhecimento.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!agent) return;
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];

      // Validate file type locally
      if (!file.name.endsWith('.pdf') && !file.name.endsWith('.txt') && !file.name.endsWith('.md')) {
        toast.error("Apenas arquivos PDF, TXT ou MD são permitidos no momento.");
        return;
      }

      try {
        setIsUploading(true);
        const newDoc = await knowledgeService.uploadDocument(agent.id, file);
        setDocuments(prev => [newDoc, ...prev]);
        toast.success(`Documento '${file.name}' indexado com sucesso.`);
      } catch (error) {
        console.error(error);
        toast.error("Erro ao fazer upload do documento.");
      } finally {
        setIsUploading(false);
        // Reset input
        e.target.value = '';
      }
    }
  };

  const handleDelete = async (docId: string) => {
    if (!agent) return;
    try {
      await knowledgeService.deleteDocument(agent.id, docId);
      setDocuments(prev => prev.filter(d => d.id !== docId));
      toast.success("Documento removido.");
    } catch (error) {
      toast.error("Erro ao remover documento.");
    }
  };

  const handleTestQuery = async () => {
    if (!agent || !testQuery) return;
    try {
      setIsSearching(true);
      const results = await knowledgeService.searchKnowledge(agent.id, testQuery);
      setSearchResults(results);
      if (results.length === 0) {
        toast.info("Nenhum resultado relevante encontrado.");
      }
    } catch (error) {
      toast.error("Erro ao realizar busca.");
    } finally {
      setIsSearching(false);
    }
  };

  if (isLoading) {
    return <div className="flex justify-center p-8"><Loader2 className="animate-spin h-8 w-8 text-primary" /></div>;
  }

  if (!agent) {
    return <div className="text-red-500 p-4">Agente não encontrado. Verifique a configuração.</div>;
  }

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Upload Section */}
        <Card className="md:col-span-1">
          <CardHeader>
            <CardTitle className="text-primary flex items-center gap-2">
              <UploadCloud className="h-5 w-5" />
              Upload de Conhecimento
            </CardTitle>
            <CardDescription>Envie manuais, relatórios em PDF ou TXT. O agente aprenderá o conteúdo automaticamente.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className={cn(
              "border-2 border-dashed border-border rounded-lg p-8 text-center cursor-pointer hover:border-primary/50 transition-colors relative",
              isUploading ? "opacity-50 pointer-events-none" : ""
            )}>
              <input
                type="file"
                className="hidden"
                id="file-upload"
                onChange={handleFileUpload}
                accept=".pdf,.txt,.md"
                disabled={isUploading}
              />
              <label htmlFor="file-upload" className="flex flex-col items-center justify-center w-full h-full cursor-pointer">
                {isUploading ? (
                  <Loader2 className="h-10 w-10 text-primary animate-spin mb-2" />
                ) : (
                  <UploadCloud className="h-10 w-10 text-muted-foreground mb-2" />
                )}
                <p className="text-sm font-medium">
                  {isUploading ? "Processando e Indexando..." : "Clique para selecionar arquivo"}
                </p>
                <p className="text-xs text-muted-foreground mt-1">PDF, TXT, MD (máx 10MB)</p>
              </label>
            </div>
          </CardContent>
        </Card>

        {/* Tester Section */}
        <Card className="md:col-span-1">
          <CardHeader>
            <CardTitle className="text-blue-500 flex items-center gap-2">
              <Search className="h-5 w-5" />
              Testar RAG
            </CardTitle>
            <CardDescription>Simule uma pergunta para verificar o que o agente encontra.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex gap-2">
              <Input
                placeholder="Ex: Qual a política de reembolso?"
                value={testQuery}
                onChange={(e) => setTestQuery(e.target.value)}
                disabled={isSearching}
                onKeyDown={(e) => e.key === 'Enter' && handleTestQuery()}
              />
              <Button onClick={handleTestQuery} disabled={isSearching || !testQuery} className="bg-blue-600 hover:bg-blue-700">
                {isSearching ? <Loader2 className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
              </Button>
            </div>

            {searchResults.length > 0 && (
              <div className="bg-muted/50 rounded-md p-3 max-h-[200px] overflow-y-auto space-y-2 text-sm">
                {searchResults.map((res, idx) => (
                  <div key={idx} className="bg-background p-2 rounded border">
                    <div className="flex justify-between text-xs text-muted-foreground mb-1">
                      <span>Similiaridade: {(res.similarity * 100).toFixed(1)}%</span>
                      <span>Fonte: {res.metadata?.source || 'Desconhecida'}</span>
                    </div>
                    <p className="text-muted-foreground italic">"{res.content.substring(0, 150)}..."</p>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Documents List */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Database className="h-5 w-5" />
            Base de Conhecimento ({documents.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          {documents.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              <Database className="h-12 w-12 mx-auto mb-3 opacity-20" />
              <p>Nenhum documento indexado.</p>
            </div>
          ) : (
            <div className="space-y-2">
              {documents.map(doc => (
                <div key={doc.id} className="flex items-center justify-between p-3 border rounded-lg hover:bg-accent/50 transition-colors">
                  <div className="flex items-center gap-3 overflow-hidden">
                    <div className="bg-primary/10 p-2 rounded">
                      <FileText className="h-5 w-5 text-primary" />
                    </div>
                    <div className="min-w-0">
                      <h4 className="font-medium truncate pr-4">{doc.title}</h4>
                      <div className="flex gap-2 text-xs text-muted-foreground">
                        <span>{new Date(doc.created_at).toLocaleDateString()}</span>
                        <span>•</span>
                        <span className="uppercase">{doc.file_type}</span>
                        <span>•</span>
                        <span>{doc.chunk_count} chunks</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <Badge variant={doc.status === 'ready' ? 'default' : 'secondary'} className={
                      doc.status === 'ready' ? 'bg-green-500 hover:bg-green-600' :
                        doc.status === 'error' ? 'bg-red-500' : 'bg-yellow-500'
                    }>
                      {doc.status}
                    </Badge>
                    <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-red-500" onClick={() => handleDelete(doc.id)}>
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default KnowledgeTab;