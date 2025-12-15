import { apiClient } from './api';

export interface RegistryTool {
    key: string;
    name: string;
    description: string;
    icon: string;
}

export const toolService = {
    getRegistryTools: async (): Promise<RegistryTool[]> => {
        const response = await apiClient.get('/api/tools/registry');
        return response.data;
    }
};
