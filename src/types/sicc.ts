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