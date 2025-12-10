import { EvolutionStats, RecentActivity } from "@/types/sicc";
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
    }
};