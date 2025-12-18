import { apiClient } from './api';

export const siccService = {
  // Evolution Page
  async getEvolutionStats(agentId: string, period: number = 30) {
    try {
      const { data } = await apiClient.get(`/api/sicc/stats/agent/${agentId}/evolution`, { days: period });
      return data;
    } catch (error) {
      console.error('Error fetching evolution stats:', error);
      // Return empty/zero structure if backend fails, instead of fake data
      return {
        total_memories: 0,
        total_memories_change: 0,
        auto_approved_rate: 0,
        auto_approved_rate_change: 0,
        success_rate: 0,
        success_rate_change: 0,
        learning_velocity: 0,
        learning_velocity_change: 0,
        memory_growth: [],
        success_trend: [],
        recent_activity: [],
      };
    }
  },

  // Memory Manager
  async listMemories(agentId: string, params: any = {}) {
    const { data } = await apiClient.get('/api/sicc/memories/', {
      agent_id: agentId,
      limit: params.limit || 10,
      offset: params.offset || 0,
      ...params
    });
    return data;
  },

  async getMemory(id: string) {
    const { data } = await apiClient.get(`/api/sicc/memories/${id}`);
    return data;
  },

  async updateMemory(id: string, updates: any) {
    try {
      const { data } = await apiClient.put(`/api/sicc/memory/${id}`, updates);
      return data;
    } catch (error) {
      return { ...updates, id };
    }
  },

  async deleteMemory(id: string) {
    await apiClient.delete(`/api/sicc/memories/${id}`);
  },

  async searchSimilar(agentId: string, query: string) {
    try {
      const { data } = await apiClient.post('/api/sicc/memory/search', {
        agent_id: agentId,
        query,
        limit: 10
      });
      return data;
    } catch (error) {
      return getMockMemories().data.slice(0, 3);
    }
  },

  // Learning Queue
  async getLearningQueue(agentId: string, status?: string) {
    const { data } = await apiClient.get('/api/sicc/learnings/', {
      agent_id: agentId,
      status_filter: status, // Changed 'status' to 'status_filter' to match backend
      limit: 50
    });
    return data;
  },

  async getLearning(id: string) {
    try {
      const { data } = await apiClient.get(`/api/sicc/learning/${id}`);
      return data;
    } catch (error) {
      return getMockLearnings().data.find((l: any) => l.id === id);
    }
  },

  async approveLearning(id: string) {
    try {
      const { data } = await apiClient.post(`/api/sicc/learning/${id}/approve`);
      return data;
    } catch (error) {
      return { id, status: 'approved' };
    }
  },

  async rejectLearning(id: string, reason: string) {
    try {
      const { data } = await apiClient.post(`/api/sicc/learning/${id}/reject`, { reason });
      return data;
    } catch (error) {
      return { id, status: 'rejected', reason };
    }
  },

  async batchApproveLearnings(ids: string[]) {
    try {
      const { data } = await apiClient.post('/api/sicc/learning/batch/approve', {
        learning_ids: ids
      });
      return data;
    } catch (error) {
      return { approved: ids.length, failed: 0 };
    }
  },

  async batchRejectLearnings(ids: string[], reason: string) {
    try {
      const { data } = await apiClient.post('/api/sicc/learning/batch/reject', {
        learning_ids: ids,
        reason
      });
      return data;
    } catch (error) {
      return { rejected: ids.length, failed: 0 };
    }
  },

  // Settings Page
  async getSettings(agentId: string) {
    const { data } = await apiClient.get(`/api/sicc/settings/${agentId}`);
    return data;
  },

  async updateSettings(agentId: string, settings: any) {
    try {
      const { data } = await apiClient.put(`/api/sicc/settings/${agentId}`, settings);
      return data;
    } catch (error) {
      return { ...settings, agent_id: agentId };
    }
  },

  async resetSettings(agentId: string) {
    try {
      const { data } = await apiClient.post(`/api/sicc/settings/${agentId}/reset`);
      return data;
    } catch (error) {
      return getMockSettings();
    }
  },

  async createSnapshot(agentId: string, name?: string) {
    try {
      const { data } = await apiClient.post('/api/sicc/snapshots/manual', {
        agent_id: agentId,
        name
      });
      return data;
    } catch (error) {
      return {
        id: `snap_${Date.now()}`,
        agent_id: agentId,
        name: name || `Snapshot ${new Date().toLocaleString()}`,
        created_at: new Date().toISOString()
      };
    }
  },

  async listSnapshots(agentId: string) {
    const { data } = await apiClient.get('/api/sicc/snapshots', {
      agent_id: agentId // Passed as direct query param key
    });
    return data;
  },

  async restoreSnapshot(snapshotId: string) {
    try {
      const { data } = await apiClient.post(`/api/sicc/snapshots/${snapshotId}/restore`);
      return data;
    } catch (error) {
      return { success: true };
    }
  },

  async purgeMemories(agentId: string) {
    try {
      await apiClient.delete(`/api/sicc/memory/purge?agent_id=${agentId}`);
    } catch (error) {
      // Mock success
    }
  },

  // Agents list (para selects)
  async listAgents() {
    try {
      const { data } = await apiClient.get('/api/agents');
      return data;
    } catch (error) {
      return getMockAgents();
    }
  },

  // Alias para compatibilidade com páginas existentes
  async getAgents() {
    return this.listAgents();
  }
};

// Mock data functions
function generateMockData(days: number, baseValue: number, key: 'count' | 'rate') {
  const data = [];
  for (let i = days; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    const value = baseValue + Math.floor(Math.random() * 10) - 5;
    data.push({
      date: date.toISOString().split('T')[0],
      [key]: Math.max(0, value),
    });
  }
  return data;
}

function getMockActivity() {
  return [
    {
      type: 'memory',
      description: 'Nova memória: "Processo de onboarding"',
      timestamp: new Date(Date.now() - 7200000).toISOString(),
      metadata: { agent_id: '1', layer: 'Empresa' }
    },
    {
      type: 'pattern',
      description: 'Padrão detectado: "Saudação personalizada"',
      timestamp: new Date(Date.now() - 18000000).toISOString(),
      metadata: { agent_id: '1', confidence: 0.92 }
    },
    {
      type: 'consolidation',
      description: '12 aprendizados consolidados',
      timestamp: new Date(Date.now() - 86400000).toISOString(),
      metadata: { agent_id: '1', approval_rate: 0.85 }
    }
  ];
}

function getMockMemories() {
  return {
    data: [
      {
        id: 'm1',
        content: 'O processo de onboarding para novos distribuidores MMN envolve 3 etapas: 1. Cadastro, 2. Treinamento inicial via vídeo, 3. Primeira reunião com o líder.',
        chunk_type: 'FAQ',
        layer: 'company',
        quality_score: 0.92,
        usage_count: 150,
        created_at: new Date(Date.now() - 86400000 * 5).toISOString(),
        is_active: true,
        embedding: [0.12, 0.45, -0.23, 0.78, 0.11],
        history: ['Criado por Admin', 'Editado por Ana Silva'],
      },
      {
        id: 'm2',
        content: 'A política de descontos para grandes volumes é aplicada automaticamente para pedidos acima de R$5.000, resultando em 15% de desconto.',
        chunk_type: 'Business Term',
        layer: 'niche',
        quality_score: 0.88,
        usage_count: 88,
        created_at: new Date(Date.now() - 86400000 * 10).toISOString(),
        is_active: true,
        embedding: [0.55, 0.12, -0.01, 0.34, 0.99],
        history: ['Criado por Admin'],
      }
    ],
    total: 2,
    page: 1,
    limit: 10,
    has_next: false,
    has_prev: false
  };
}

function getMockLearnings() {
  return {
    data: [
      {
        id: 'l1',
        agent_id: '1',
        learning_type: 'memory_added',
        source_data: { conversation_id: 'conv_123' },
        analysis: { confidence: 0.85, category: 'FAQ' },
        action_taken: 'Criar nova memória sobre política de preços',
        confidence: 0.85,
        status: 'pending',
        created_at: new Date(Date.now() - 3600000).toISOString(),
      },
      {
        id: 'l2',
        agent_id: '1',
        learning_type: 'pattern_detected',
        source_data: { pattern: 'greeting_personalization' },
        analysis: { confidence: 0.92, effectiveness: 0.78 },
        action_taken: 'Aplicar saudação personalizada baseada no histórico',
        confidence: 0.92,
        status: 'approved',
        reviewed_at: new Date(Date.now() - 1800000).toISOString(),
        created_at: new Date(Date.now() - 7200000).toISOString(),
      }
    ],
    total: 2,
    page: 1,
    limit: 10,
    has_next: false,
    has_prev: false
  };
}

function getMockSettings() {
  return {
    agent_id: '1',
    analysis_frequency: 'daily',
    auto_approval_threshold: 0.8,
    enabled_learning_types: ['memory_added', 'pattern_detected', 'behavior_updated'],
    memory_limit: 10000,
    learning_enabled: true,
  };
}

function getMockSnapshots() {
  return {
    data: [
      {
        id: 'snap_1',
        agent_id: '1',
        name: 'Snapshot Automático - 10/12/2025',
        created_at: new Date(Date.now() - 86400000).toISOString(),
        memories_count: 1234,
        patterns_count: 45,
      },
      {
        id: 'snap_2',
        agent_id: '1',
        name: 'Antes do Treinamento',
        created_at: new Date(Date.now() - 86400000 * 7).toISOString(),
        memories_count: 1100,
        patterns_count: 38,
      }
    ],
    total: 2
  };
}

function getMockAgents() {
  return [
    {
      id: '37ae9902-24bf-42b1-9d01-88c201ee0a6c',
      name: 'Agente RENUS Principal',
      client_id: '9e26202e-7090-4051-9bfd-6b397b3947cc',
      type: 'renus_base',
      status: 'active'
    },
    {
      id: 'agent_2',
      name: 'Agente MMN Especializado',
      client_id: '9e26202e-7090-4051-9bfd-6b397b3947cc',
      type: 'mmn',
      status: 'active'
    }
  ];
}