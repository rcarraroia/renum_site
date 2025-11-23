export interface SubAgent {
  id: string;
  name: string;
  description: string;
  channel: 'site' | 'whatsapp';
  systemPrompt: string;
  topics: string[];
  isActive: boolean;
  useFineTuning?: boolean;
  fineTuneStatus?: 'none' | 'preparing' | 'training' | 'ready' | 'failed';
  fineTuneModelId?: string;
  trainingExamplesCount?: number;
  model?: string; // NOVO - modelo de IA específico
}