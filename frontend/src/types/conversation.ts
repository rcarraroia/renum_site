import { User } from "./auth";
import { Client } from "./client";

export type ConversationStatus = 'Nova' | 'Em Andamento' | 'Resolvida' | 'Fechada' | 'Pendente';
export type ConversationChannel = 'WhatsApp' | 'Web' | 'Email' | 'API';
export type MessageSender = 'client' | 'renus' | 'admin' | 'system';
export type MessageType = 'text' | 'image' | 'document' | 'action' | 'guardrail'; // Adicionado 'guardrail'

export interface GuardrailIntervention {
  action: 'blocked' | 'sanitized' | 'warned';
  reason: 'PII' | 'Jailbreak' | 'Secret' | 'Keyword' | 'NSFW' | 'Topic';
  originalContent: string;
  sanitizedContent?: string;
  details: {
    validator: string;
    result: string;
    latency: string;
  }[];
}

export interface ConversationMessage {
  id: string;
  sender: MessageSender;
  type: MessageType;
  content: string;
  timestamp: Date;
  read: boolean;
  metadata?: {
    intent?: string;
    sentiment?: 'positive' | 'negative' | 'neutral';
    tool_call?: string;
    internal_note?: boolean;
    guardrail?: GuardrailIntervention; // Novo campo para intervenções
  };
}

export interface Conversation {
  id: string;
  client: Pick<Client, 'id' | 'companyName' | 'contact' | 'segment'>;
  status: ConversationStatus;
  channel: ConversationChannel;
  assignedAgent: User | null;
  messages: ConversationMessage[];
  unreadCount: number;
  priority: 'Low' | 'Medium' | 'High';
  startDate: Date;
  lastUpdate: Date;
  summary?: string;
  tags: string[];
}