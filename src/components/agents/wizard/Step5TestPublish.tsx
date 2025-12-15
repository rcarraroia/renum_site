import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Send, Copy, Download, ExternalLink, CheckCircle } from 'lucide-react';
import { toast } from 'sonner';

interface Step5TestPublishProps {
  formData: any;
  onPublish: () => void;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const Step5TestPublish: React.FC<Step5TestPublishProps> = ({ formData, onPublish }) => {
  const [isTesting, setIsTesting] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isPublishing, setIsPublishing] = useState(false);
  const [publishResult, setPublishResult] = useState<any>(null);
  const [showPublishModal, setShowPublishModal] = useState(false);

  const handleStartTest = () => {
    setIsTesting(true);
    setMessages([
      {
        role: 'assistant',
        content: `Olá! Sou o ${formData.name}. Como posso ajudar você hoje?`,
        timestamp: new Date(),
      },
    ]);
  };

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return;

    const userMessage: Message = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date(),
    };

    setMessages([...messages, userMessage]);
    setInputMessage('');

    // Simulate assistant response
    setTimeout(() => {
      const assistantMessage: Message = {
        role: 'assistant',
        content: 'Obrigado pela informação! Esta é uma resposta de teste do sandbox.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    }, 1000);
  };

  const handlePublish = async () => {
    setIsPublishing(true);

    // Simulate publication
    setTimeout(() => {
      const result = {
        agent_id: 'mock-agent-id',
        slug: formData.name.toLowerCase().replace(/\s+/g, '-'),
        public_url: `https://renum.com.br/chat/${formData.name.toLowerCase().replace(/\s+/g, '-')}`,
        embed_code: `<script src="https://renum.com.br/widget.js"></script>`,
        qr_code_url: 'data:image/png;base64,mock-qr-code',
      };

      setPublishResult(result);
      setShowPublishModal(true);
      setIsPublishing(false);
      toast.success('Agente publicado com sucesso!');
    }, 2000);
  };

  const handleCopy = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    toast.success(`${label} copiado!`);
  };

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Teste seu Agente</h3>
        <p className="text-sm text-muted-foreground mb-4">
          Converse com seu agente em um ambiente de teste antes de publicar
        </p>

        {!isTesting ? (
          <Card>
            <CardContent className="p-6 text-center">
              <p className="text-sm text-muted-foreground mb-4">
                Clique no botão abaixo para iniciar uma conversa de teste
              </p>
              <Button onClick={handleStartTest} className="bg-[#4e4ea8] hover:bg-[#3d3d86]">
                Iniciar Teste
              </Button>
            </CardContent>
          </Card>
        ) : (
          <Card>
            <CardContent className="p-4">
              <ScrollArea className="h-96 pr-4">
                <div className="space-y-4">
                  {messages.map((msg, index) => (
                    <div
                      key={index}
                      className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-[80%] rounded-lg p-3 ${
                          msg.role === 'user'
                            ? 'bg-[#FF6B35] text-white'
                            : 'bg-muted'
                        }`}
                      >
                        <p className="text-sm">{msg.content}</p>
                        <p className="text-xs opacity-70 mt-1">
                          {msg.timestamp.toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </ScrollArea>

              <div className="flex items-center space-x-2 mt-4">
                <Input
                  placeholder="Digite sua mensagem..."
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                />
                <Button onClick={handleSendMessage} size="icon">
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        )}
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-4">Resumo da Configuração</h3>
        <Card>
          <CardContent className="p-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Nome:</span>
              <span className="font-medium">{formData.name}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Template:</span>
              <span className="font-medium">{formData.template_type}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Personalidade:</span>
              <span className="font-medium">{formData.personality}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Campos configurados:</span>
              <span className="font-medium">
                {Object.values(formData.standard_fields || {}).filter((f: any) => f.enabled).length +
                  (formData.custom_fields || []).length}
              </span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Integrações:</span>
              <span className="font-medium">
                {Object.values(formData.integrations || {}).filter(Boolean).length}
              </span>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="flex justify-center">
        <Button
          onClick={handlePublish}
          disabled={isPublishing || !isTesting}
          className="bg-green-600 hover:bg-green-700 px-8"
          size="lg"
        >
          {isPublishing ? 'Publicando...' : 'Publicar Agente'}
        </Button>
      </div>

      <Dialog open={showPublishModal} onOpenChange={setShowPublishModal}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="flex items-center space-x-2">
              <CheckCircle className="h-6 w-6 text-green-600" />
              <span>Agente Publicado com Sucesso!</span>
            </DialogTitle>
          </DialogHeader>

          {publishResult && (
            <div className="space-y-4">
              <div>
                <Label className="text-sm font-medium">Link Público</Label>
                <div className="flex items-center space-x-2 mt-1">
                  <Input value={publishResult.public_url} readOnly />
                  <Button
                    size="icon"
                    variant="outline"
                    onClick={() => handleCopy(publishResult.public_url, 'Link')}
                  >
                    <Copy className="h-4 w-4" />
                  </Button>
                  <Button
                    size="icon"
                    variant="outline"
                    onClick={() => window.open(publishResult.public_url, '_blank')}
                  >
                    <ExternalLink className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              <div>
                <Label className="text-sm font-medium">Código de Incorporação</Label>
                <div className="flex items-center space-x-2 mt-1">
                  <Input value={publishResult.embed_code} readOnly />
                  <Button
                    size="icon"
                    variant="outline"
                    onClick={() => handleCopy(publishResult.embed_code, 'Código')}
                  >
                    <Copy className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              <div>
                <Label className="text-sm font-medium">QR Code</Label>
                <div className="flex items-center space-x-4 mt-2">
                  <img
                    src={publishResult.qr_code_url}
                    alt="QR Code"
                    className="w-32 h-32 border rounded"
                  />
                  <Button
                    variant="outline"
                    onClick={() => {
                      const link = document.createElement('a');
                      link.href = publishResult.qr_code_url;
                      link.download = `${publishResult.slug}-qrcode.png`;
                      link.click();
                    }}
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Baixar QR Code
                  </Button>
                </div>
              </div>

              <div className="flex justify-end space-x-2 pt-4">
                <Button variant="outline" onClick={() => setShowPublishModal(false)}>
                  Fechar
                </Button>
                <Button onClick={onPublish}>Ver Agente</Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

const Label: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className }) => (
  <label className={className}>{children}</label>
);

export default Step5TestPublish;
