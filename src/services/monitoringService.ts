import { apiClient } from './api';
import { toast } from 'sonner';

export interface MonitoringStats {
    status: string;
    project: string;
    stats_window: string;
    total_runs_in_window: number;
    error_count: number;
    error_rate: number;
    success_rate: number;
    recent_runs: {
        id: string;
        name: string;
        status: string;
        error: string | null;
        tokens: number;
        latency: number;
        timestamp: string | null;
    }[];
}

export const monitoringService = {
    async getStats(): Promise<MonitoringStats> {
        try {
            const { data } = await apiClient.get<MonitoringStats>('/api/monitoring/stats');
            return data;
        } catch (error) {
            console.error('Failed to fetch monitoring stats:', error);
            throw error;
        }
    }
};
