import { EvolutionStats, RecentActivity, Memory, MemoryListResponse } from "@/types/sicc";
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
    }
};