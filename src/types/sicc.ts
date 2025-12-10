export type ActivityType = 'memory' | 'pattern' | 'consolidation';

export interface RecentActivity {
  type: ActivityType;
  description: string;
  timestamp: string;
  metadata: {
    agent_id: string;
    confidence?: number;
    layer?: 'Empresa' | 'Agente' | 'Global';
    approval_rate?: number;
  };
}

export interface MetricData {
  date: string;
  count?: number;
  rate?: number;
}

export interface EvolutionStats {
  total_memories: number;
  total_memories_change: number;
  auto_approved_rate: number;
  auto_approved_rate_change: number;
  success_rate: number;
  success_rate_change: number;
  learning_velocity: number;
  learning_velocity_change: number;
  memory_growth: MetricData[];
  success_trend: MetricData[];
  recent_activity: RecentActivity[];
}

// --- Tipos para Gerenciador de Memórias ---

export type MemoryLayer = 'base' | 'company' | 'niche' | 'individual';
export type MemoryChunkType = 'FAQ' | 'Business Term' | 'Response Strategy' | 'Script';

export interface Memory {
  id: string;
  content: string;
  chunk_type: MemoryChunkType;
  layer: MemoryLayer;
  quality_score: number; // 0.0 to 1.0 (Confiança)
  usage_count: number;
  created_at: string; // Date string
  is_active: boolean;
  embedding?: number[]; // Mock: first 5 values
  history?: string[];
}

export interface MemoryListResponse {
  data: Memory[];
  total: number;
  page: number;
  per_page: number;
}