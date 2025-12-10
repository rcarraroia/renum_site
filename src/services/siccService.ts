import { EvolutionStats, RecentActivity, Memory, MemoryListResponse, Learning, LearningQueueResponse, LearningStatus, AgentSettings, Snapshot } from "@/types/sicc";
import { mockAgents } from "@/mocks/agents.mock";

// Mock data generation utility
const generateMockData = (days: number, baseValue: number, key: 'count' | 'rate') => {
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
};

const MOCK_ACTIVITY: RecentActivity[] = [
    {
        type: 'memory',
        description: 'Nova memória: "Processo de onboarding"',
        timestamp: new Date(Date.now() - 7200000).toISOString(), // 2 hours ago
        metadata: { agent_id: '1', layer: 'Empresa' }
    },
    {
        type: 'pattern',
        description: 'Padrão detectado: "Saudação personalizada"',
        timestamp: new Date(Date.now() - 18000000).toISOString(), // 5 hours ago
        metadata: { agent_id: '1', confidence: 0.92 }
    },
    {
        type: 'consolidation',
        description: '12 aprendizados consolidados',
        timestamp: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
        metadata: { agent_id: '1', approval_rate: 0.85 }
    },
    {
        type: 'memory',
        description: 'Memória atualizada: "Política de preços"',
        timestamp: new Date(Date.now() - 172800000).toISOString(), // 2 days ago
        metadata: { agent_id: '1', layer: 'Global' }
    },
];

const MOCK_STATS: EvolutionStats = {
    total_memories: 1234,
    total_memories_change: 15, // +15%
    auto_approved_rate: 89,
    auto_approved_rate_change: 5, // +5%
    success_rate: 94.5,
    success_rate_change: 2.1, // +2.1%
    learning_velocity: 12.3,
    learning_velocity_change: 0.8, // +0.8
    memory_growth: generateMockData(30, 45, 'count'),
    success_trend: generateMockData(30, 90, 'rate'),
    recent_activity: MOCK_ACTIVITY,
};

const MOCK_MEMORIES: Memory[] = [
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
    },
    {
        id: 'm3',
        content: 'Se o cliente perguntar sobre o concorrente X, a resposta padrão é focar nos diferenciais de qualidade e suporte da RENUM.',
        chunk_type: 'Response Strategy',
        layer: 'individual',
        quality_score: 0.75,
        usage_count: 32,
        created_at: new Date(Date.now() - 86400000 * 2).toISOString(),
        is_active: true,
        embedding: [0.01, 0.02, 0.03, 0.04, 0.05],
        history: ['Criado por Bruno Costa'],
    },
    {
        id: 'm4',
        content: 'O horário de atendimento é de segunda a sexta, das 9h às 18h.',
        chunk_type: 'FAQ',
        layer: 'base',
        quality_score: 0.99,
        usage_count: 200,
        created_at: new Date(Date.now() - 86400000 * 50).toISOString(),
        is_active: false,
        embedding: [0.99, 0.88, 0.77, 0.66, 0.55],
        history: ['Criado por Sistema'],
    },
];

const MOCK_LEARNINGS: Learning[] = [
    {
        id: 'l1',
        learning_type: 'memory_added',
        title: 'Novo termo: "onboarding personalizado"',
        source_data: {
            conversations: [{ id: 'c4521', date: '2025-01-20' }, { id: 'c4489', date: '2025-01-19' }],
            impact_estimate: '+15% precisão em respostas sobre onboarding',
        },
        analysis: 'A ISA detectou que o termo "onboarding personalizado" foi usado 12 vezes em conversas de alto valor nos últimos 7 dias, mas não estava na base de conhecimento. A sugestão é adicionar este termo como um Business Term para melhorar a precisão.',
        quality_score: 0.75,
        status: 'pending',
        created_at: new Date(Date.now() - 3600000).toISOString(), // 1 hour ago
    },
    {
        id: 'l2',
        learning_type: 'pattern_detected',
        title: 'Padrão detectado: "Saudação personalizada"',
        source_data: {
            conversations: [{ id: 'c4500', date: '2025-01-21' }, { id: 'c4490', date: '2025-01-20' }, { id: 'c4480', date: '2025-01-19' }],
            impact_estimate: '+5% na satisfação do usuário (CSAT)',
        },
        analysis: 'A ISA identificou que saudações que incluem o nome do cliente e o nome do agente (ex: "Olá [Nome], aqui é o Renus") resultam em uma taxa de continuação de conversa 10% maior. Sugere-se atualizar o comportamento padrão de saudação.',
        quality_score: 0.68,
        status: 'pending',
        created_at: new Date(Date.now() - 7200000).toISOString(), // 2 hours ago
    },
    {
        id: 'l3',
        learning_type: 'behavior_updated',
        title: 'Comportamento atualizado: Foco em ROI',
        source_data: {
            conversations: [{ id: 'c4000', date: '2025-01-01' }],
            impact_estimate: 'N/A',
        },
        analysis: 'Atualização de comportamento aprovada pelo Admin. Foco em métricas de ROI.',
        quality_score: 0.99,
        status: 'approved',
        created_at: new Date(Date.now() - 86400000 * 5).toISOString(),
        reviewed_at: new Date(Date.now() - 86400000 * 4).toISOString(),
        reviewed_by: 'Admin Renum',
    },
    {
        id: 'l4',
        learning_type: 'memory_added',
        title: 'Termo rejeitado: "preço fixo"',
        source_data: {
            conversations: [{ id: 'c3900', date: '2024-12-25' }],
            impact_estimate: 'N/A',
        },
        analysis: 'A ISA sugeriu adicionar o termo "preço fixo", mas foi rejeitado.',
        quality_score: 0.55,
        status: 'rejected',
        created_at: new Date(Date.now() - 86400000 * 10).toISOString(),
        reviewed_at: new Date(Date.now() - 86400000 * 9).toISOString(),
        reviewed_by: 'Ana Silva',
        rejection_reason: 'A política de preços é dinâmica e não deve ser fixada na memória base.',
    },
];

const MOCK_SETTINGS: AgentSettings = {
    agent_id: '1',
    learning_mode: 'active',
    analysis_frequency: 'hourly',
    auto_approve_threshold: 0.80,
    manual_review_threshold: 0.50,
    auto_reject_threshold: 0.30,
    max_memories: 10000,
    max_pending_learnings: 500,
    snapshot_retention_days: 90,
    auto_archive_days: 365,
    layer_base_enabled: true,
    layer_company_enabled: true,
    layer_individual_enabled: true,
    audio_retention_days: 30,
    anonymization_enabled: true,
    multi_tenant_isolation: true,
    updated_at: new Date(Date.now() - 7200000).toISOString(), // 2 hours ago
    updated_by: 'admin@renum.ai',
};

const MOCK_SNAPSHOTS: Snapshot[] = [
    { id: 'snap1', name: 'Configuração Inicial', created_at: new Date(Date.now() - 86400000 * 30).toISOString(), size_mb: 120 },
    { id: 'snap2', name: 'Após Treinamento Q1', created_at: new Date(Date.now() - 86400000 * 10).toISOString(), size_mb: 155 },
];

// Mock current usage stats (for display purposes)
const CURRENT_USAGE = {
    memories: 1234,
    pending_learnings: 15,
};


export const siccService = {
    getEvolutionStats: async (agentId: string, periodDays: number): Promise<EvolutionStats> => {
        console.log(`[SICC Service] Fetching evolution stats for agent ${agentId} over ${periodDays} days.`);
        
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 800));

        if (agentId === 'error') {
            throw new Error("Falha ao carregar dados do agente.");
        }
        
        // Adjust mock data based on period (simple simulation)
        const adjustedStats = {
            ...MOCK_STATS,
            total_memories: MOCK_STATS.total_memories + (periodDays === 7 ? -500 : 0),
            memory_growth: generateMockData(periodDays, 45, 'count'),
            success_trend: generateMockData(periodDays, 90, 'rate'),
        };

        return adjustedStats;
    },
    
    getAgents: async () => {
        // Simulate fetching agents available for SICC
        await new Promise(resolve => setTimeout(resolve, 200));
        return mockAgents.map(a => ({ id: a.id, name: a.name, client_id: a.client_id }));
    },

    listMemories: async (agentId: string, page: number, perPage: number, search: string, filters: any): Promise<MemoryListResponse> => {
        console.log(`[SICC Service] Listing memories for agent ${agentId}. Page: ${page}, Search: ${search}, Filters:`, filters);
        
        await new Promise(resolve => setTimeout(resolve, 500));

        let filteredData = MOCK_MEMORIES.filter(m => {
            const matchesSearch = search === '' || m.content.toLowerCase().includes(search.toLowerCase());
            const matchesType = filters.chunk_type === 'all' || m.chunk_type === filters.chunk_type;
            const matchesLayer = filters.layer === 'all' || m.layer === filters.layer;
            const matchesStatus = filters.is_active === 'all' || m.is_active.toString() === filters.is_active;
            const matchesScore = filters.quality_score === 'all' || m.quality_score >= parseFloat(filters.quality_score);
            
            return matchesSearch && matchesType && matchesLayer && matchesStatus && matchesScore;
        });

        const startIndex = (page - 1) * perPage;
        const endIndex = startIndex + perPage;

        return {
            data: filteredData.slice(startIndex, endIndex),
            total: filteredData.length,
            page,
            per_page: perPage,
        };
    },

    getMemoryDetails: async (id: string): Promise<Memory> => {
        await new Promise(resolve => setTimeout(resolve, 300));
        const memory = MOCK_MEMORIES.find(m => m.id === id);
        if (!memory) throw new Error("Memória não encontrada.");
        return memory;
    },

    updateMemory: async (id: string, data: Partial<Memory>): Promise<Memory> => {
        await new Promise(resolve => setTimeout(resolve, 500));
        const index = MOCK_MEMORIES.findIndex(m => m.id === id);
        if (index === -1) throw new Error("Memória não encontrada.");
        
        const updatedMemory = { ...MOCK_MEMORIES[index], ...data, created_at: MOCK_MEMORIES[index].created_at };
        MOCK_MEMORIES[index] = updatedMemory;
        return updatedMemory;
    },

    deleteMemory: async (id: string): Promise<void> => {
        await new Promise(resolve => setTimeout(resolve, 300));
        const index = MOCK_MEMORIES.findIndex(m => m.id === id);
        if (index === -1) throw new Error("Memória não encontrada.");
        
        // Simulate archiving instead of deleting
        MOCK_MEMORIES[index].is_active = false;
    },
    
    // --- Learning Queue Mocks ---
    
    getLearningQueue: async (agentId: string, status: LearningStatus): Promise<LearningQueueResponse> => {
        console.log(`[SICC Service] Fetching learning queue for agent ${agentId} with status: ${status}`);
        await new Promise(resolve => setTimeout(resolve, 500));
        
        const filteredData = MOCK_LEARNINGS.filter(l => l.status === status);
        
        return {
            data: filteredData,
            stats: {
                pending: MOCK_LEARNINGS.filter(l => l.status === 'pending').length,
                approved: MOCK_LEARNINGS.filter(l => l.status === 'approved').length,
                rejected: MOCK_LEARNINGS.filter(l => l.status === 'rejected').length,
                approval_rate: 89, // Mock rate
            }
        };
    },
    
    approveLearning: async (id: string): Promise<void> => {
        await new Promise(resolve => setTimeout(resolve, 300));
        const learning = MOCK_LEARNINGS.find(l => l.id === id);
        if (learning) {
            learning.status = 'approved';
            learning.reviewed_at = new Date().toISOString();
            learning.reviewed_by = 'Admin Mock';
        }
    },
    
    rejectLearning: async (id: string, reason: string): Promise<void> => {
        await new Promise(resolve => setTimeout(resolve, 300));
        const learning = MOCK_LEARNINGS.find(l => l.id === id);
        if (learning) {
            learning.status = 'rejected';
            learning.reviewed_at = new Date().toISOString();
            learning.reviewed_by = 'Admin Mock';
            learning.rejection_reason = reason;
        }
    },
    
    batchApproveLearning: async (ids: string[]): Promise<void> => {
        await new Promise(resolve => setTimeout(resolve, 500));
        ids.forEach(id => {
            const learning = MOCK_LEARNINGS.find(l => l.id === id);
            if (learning) {
                learning.status = 'approved';
                learning.reviewed_at = new Date().toISOString();
                learning.reviewed_by = 'Admin Mock';
            }
        });
    },
    
    batchRejectLearning: async (ids: string[], reason: string): Promise<void> => {
        await new Promise(resolve => setTimeout(resolve, 500));
        ids.forEach(id => {
            const learning = MOCK_LEARNINGS.find(l => l.id === id);
            if (learning) {
                learning.status = 'rejected';
                learning.reviewed_at = new Date().toISOString();
                learning.reviewed_by = 'Admin Mock';
                learning.rejection_reason = reason;
            }
        });
    },

    // --- Settings Mocks ---
    getSettings: async (agentId: string): Promise<AgentSettings> => {
        console.log(`[SICC Service] Fetching settings for agent ${agentId}`);
        await new Promise(resolve => setTimeout(resolve, 500));
        return { ...MOCK_SETTINGS, agent_id: agentId };
    },

    saveSettings: async (agentId: string, settings: Partial<AgentSettings>): Promise<AgentSettings> => {
        console.log(`[SICC Service] Saving settings for agent ${agentId}`, settings);
        await new Promise(resolve => setTimeout(resolve, 800));
        
        // Update mock settings globally (simple state management)
        Object.assign(MOCK_SETTINGS, settings, {
            updated_at: new Date().toISOString(),
            updated_by: 'Current User',
        });
        return MOCK_SETTINGS;
    },

    resetSettings: async (agentId: string): Promise<void> => {
        console.log(`[SICC Service] Resetting settings for agent ${agentId}`);
        await new Promise(resolve => setTimeout(resolve, 500));
        // Simulate reset logic (e.g., reverting to default values)
        Object.assign(MOCK_SETTINGS, {
            auto_approve_threshold: 0.80,
            manual_review_threshold: 0.50,
            auto_reject_threshold: 0.30,
            max_memories: 10000,
            max_pending_learnings: 500,
            snapshot_retention_days: 90,
            auto_archive_days: 365,
            layer_base_enabled: true,
            layer_company_enabled: true,
            layer_individual_enabled: true,
            audio_retention_days: 30,
            anonymization_enabled: true,
            multi_tenant_isolation: true,
            updated_at: new Date().toISOString(),
            updated_by: 'System Reset',
        });
    },

    createSnapshot: async (agentId: string, name: string): Promise<Snapshot> => {
        console.log(`[SICC Service] Creating snapshot for agent ${agentId} with name: ${name}`);
        await new Promise(resolve => setTimeout(resolve, 1000));
        const newSnapshot: Snapshot = {
            id: `snap${MOCK_SNAPSHOTS.length + 1}`,
            name: name || `Snapshot Manual ${new Date().toLocaleDateString()}`,
            created_at: new Date().toISOString(),
            size_mb: Math.floor(Math.random() * 50) + 100,
        };
        MOCK_SNAPSHOTS.push(newSnapshot);
        return newSnapshot;
    },

    listSnapshots: async (agentId: string): Promise<Snapshot[]> => {
        console.log(`[SICC Service] Listing snapshots for agent ${agentId}`);
        await new Promise(resolve => setTimeout(resolve, 300));
        return MOCK_SNAPSHOTS;
    },

    restoreSnapshot: async (snapshotId: string): Promise<void> => {
        console.log(`[SICC Service] Restoring snapshot ${snapshotId}`);
        await new Promise(resolve => setTimeout(resolve, 1500));
        // Simulate restoration affecting settings
        MOCK_SETTINGS.updated_by = `Restored from ${snapshotId}`;
    },

    purgeMemories: async (agentId: string): Promise<void> => {
        console.log(`[SICC Service] Purging all memories for agent ${agentId}`);
        await new Promise(resolve => setTimeout(resolve, 2000));
        // Simulate memory purge
        CURRENT_USAGE.memories = 0;
    },
    
    // Helper to get current usage stats (mocked)
    getCurrentUsageStats: async (agentId: string) => {
        await new Promise(resolve => setTimeout(resolve, 100));
        return CURRENT_USAGE;
    }
};