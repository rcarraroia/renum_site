import React, { useState } from 'react';
import { GuardrailIntervention, ConversationMessage } from '@/types/conversation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Zap, Shield, Lock, AlertTriangle, Edit, Send, X, Eye, Copy } from 'lucide-react';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import { useAuth } from '@/context/AuthContext';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';

interface GuardrailMessageProps {
  message: ConversationMessage;
  intervention: GuardrailIntervention;
  onGuardrailDetails: (intervention: GuardrailIntervention) => void;
  onRetry: (originalMessageId: string, newContent: string) => void;
}

const GuardrailMessage: React.FC<GuardrailMessageProps> = ({ message, intervention, onGuardrailDetails, onRetry }) => {
  const { action, reason, originalContent, sanitizedContent } = intervention;
  const { role } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [editContent, setEditContent] = useState(sanitizedContent || originalContent);
  const [isOverrideDialogOpen, setIsOverrideDialogOpen] = useState(false);

  const isBlocked = action === 'blocked';
  const isSanitized = action === 'sanitized';
  const isWarned = action === 'warned';
  const isAdmin = role === 'admin';

  const getReasonText = (r: typeof reason) => {
    switch (r) {
      case 'PII': return 'Informações Pessoais (como email ou telefone)';
      case 'Secret': return 'Credenciais ou Chaves de API';
      case 'Jailbreak': return 'Tentativa de desvio de comportamento';
      case 'Keyword': return 'Palavra-chave restrita';
      case 'NSFW': return 'Conteúdo impróprio';
      case 'Topic': return 'Tópico fora do escopo';
      default: return 'Violação de política de segurança';
    }
  };

  const handleRetry = () => {
    if (editContent.trim()) {
      onRetry(message.id, editContent.trim());
      setIsEditing(false);
    } else {
      toast.error("A mensagem não pode estar vazia.");
    }
  };

  const handleOverride = () => {
    if (isAdmin) {
        setIsOverrideDialogOpen(true);
    } else {
        toast.error("Apenas administradores podem ignorar bloqueios.");
    }
  };

  const confirmOverride = () => {
    // Mock override action: send original content as an admin message
    onRetry(message.id, `[ADMIN OVERRIDE] ${originalContent}`);
    toast.warning("Bloqueio de Guardrail ignorado. Ação registrada.");
    setIsOverrideDialogOpen(false);
    setIsEditing(false);
  };

  // --- Render Logic ---

  let icon: React.ReactNode;
  let colorClass: string;
  let title: string;
  let guidance: React.ReactNode;

  if (isBlocked) {
    icon = <Lock className="h-6 w-6 text-red-500" />;
    colorClass = 'bg-red-50 dark:bg-red-900/20 border-red-500';
    title = 'Mensagem Bloqueada por Segurança';
    guidance = (
      <div className="space-y-2">
        <p className="text-sm text-red-700 dark:text-red-300">
          Motivo: Detectamos {getReasonText(reason)}.
        </p>
        <p className="text-xs text-muted-foreground">
          Por favor, remova qualquer informação sensível ou tente reformular sua pergunta.
        </p>
        <Button size="sm" className="bg-red-500 hover:bg-red-600" onClick={() => setIsEditing(true)}>
          <Edit className="h-4 w-4 mr-2" /> Editar e Tentar Novamente
        </Button>
        {isAdmin && (
            <Button variant="link" size="sm" className="p-0 h-auto text-red-500 ml-4" onClick={handleOverride}>
                <Shield className="h-4 w-4 mr-1" /> Ignorar Bloqueio (Admin)
            </Button>
        )}
      </div>
    );
  } else if (isSanitized) {
    icon = <Shield className="h-6 w-6 text-yellow-500" />;
    colorClass = 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-500';
    title = 'Conteúdo Sanitizado Automaticamente';
    guidance = (
      <div className="space-y-2">
        <p className="text-sm text-yellow-700 dark:text-yellow-300">
          Aviso: Removemos {getReasonText(reason)} da sua mensagem antes de enviá-la ao Renus.
        </p>
        <p className="text-xs text-muted-foreground">
          O Renus recebeu a versão segura da mensagem.
        </p>
        <Button variant="link" size="sm" className="p-0 h-auto text-yellow-500" onClick={() => onGuardrailDetails(intervention)}>
            <Eye className="h-4 w-4 mr-1" /> Ver Detalhes da Sanitização
        </Button>
      </div>
    );
  } else if (isWarned) {
    icon = <AlertTriangle className="h-6 w-6 text-orange-500" />;
    colorClass = 'bg-orange-50 dark:bg-orange-900/20 border-orange-500';
    title = 'Alerta de Política de Conteúdo';
    guidance = (
      <div className="space-y-2">
        <p className="text-sm text-orange-700 dark:text-orange-300">
          Aviso: Sua mensagem contém {getReasonText(reason)}, o que pode afetar a resposta do Renus.
        </p>
        <p className="text-xs text-muted-foreground">
          Você pode prosseguir ou editar para garantir uma resposta mais precisa.
        </p>
        <Button size="sm" className="bg-orange-500 hover:bg-orange-600" onClick={() => onRetry(message.id, originalContent)}>
          <Send className="h-4 w-4 mr-2" /> Prosseguir Assim Mesmo
        </Button>
        <Button variant="outline" size="sm" className="ml-2" onClick={() => setIsEditing(true)}>
          <Edit className="h-4 w-4 mr-2" /> Editar
        </Button>
      </div>
    );
  } else {
    return null;
  }

  // --- Edit/Retry Interface ---
  if (isEditing) {
    return (
      <Card className="w-full max-w-[85%] p-4 shadow-lg border-2 border-[#4e4ea8] dark:border-[#0ca7d2] my-3">
        <CardTitle className="text-lg mb-3 flex items-center text-[#4e4ea8]">
            <Edit className="h-5 w-5 mr-2" /> Editar Mensagem
        </CardTitle>
        <Label htmlFor="edit-content" className="text-sm mb-2 block">
            Corrija o conteúdo sensível (Ex: [REDACTED] ou palavras bloqueadas).
        </Label>
        <Textarea
          id="edit-content"
          rows={4}
          value={editContent}
          onChange={(e) => setEditContent(e.target.value)}
          className="font-mono text-sm"
        />
        <div className="flex justify-end space-x-2 mt-4">
          <Button variant="outline" onClick={() => setIsEditing(false)}>
            <X className="h-4 w-4 mr-2" /> Cancelar
          </Button>
          <Button onClick={handleRetry} className="bg-[#FF6B35] hover:bg-[#e55f30]">
            <Send className="h-4 w-4 mr-2" /> Enviar Corrigido
          </Button>
        </div>
      </Card>
    );
  }

  // --- Default Display ---
  return (
    <Card className={cn("w-full max-w-[85%] p-4 shadow-md border-2 my-3", colorClass)}>
      <CardHeader className="p-0 mb-3">
        <CardTitle className="text-xl flex items-center space-x-2">
          {icon}
          <span className="font-bold">{title}</span>
        </CardTitle>
      </CardHeader>
      <div className="text-sm">
        {guidance}
      </div>

      {/* Admin Override Dialog */}
      <Dialog open={isOverrideDialogOpen} onOpenChange={setIsOverrideDialogOpen}>
        <DialogContent>
            <DialogHeader>
                <DialogTitle className="text-red-500 flex items-center"><AlertTriangle className="h-5 w-5 mr-2" /> Confirmação de Override</DialogTitle>
            </DialogHeader>
            <p className="text-sm">
                Você está prestes a ignorar o bloqueio de segurança do Guardrail. Esta ação pode expor dados sensíveis ou desviar o comportamento do agente.
            </p>
            <p className="font-semibold">Motivo: {getReasonText(reason)}</p>
            <p className="text-xs text-muted-foreground">Esta ação será registrada no log de auditoria.</p>
            <DialogFooter>
                <Button variant="outline" onClick={() => setIsOverrideDialogOpen(false)}>Cancelar</Button>
                <Button variant="destructive" onClick={confirmOverride}>
                    <Shield className="h-4 w-4 mr-2" /> Confirmar Override
                </Button>
            </DialogFooter>
        </DialogContent>
      </Dialog>
    </Card>
  );
};

export default GuardrailMessage;