import { apiClient } from './api';

export interface KnowledgeDocument {
    id: string;
    title: string;
    file_type: string;
    status: 'indexing' | 'ready' | 'error';
    chunk_count: number;
    created_at: string;
    updated_at: string;
    metadata: any;
}

export interface SearchResult {
    content: string;
    similarity: number;
    metadata: any;
}

export const knowledgeService = {
    listDocuments: async (agentId: string): Promise<KnowledgeDocument[]> => {
        const response = await apiClient.get('/api/knowledge/documents', { agent_id: agentId });
        return response.data;
    },

    uploadDocument: async (agentId: string, file: File): Promise<KnowledgeDocument> => {
        const formData = new FormData();
        formData.append('agent_id', agentId);
        formData.append('file', file);

        // Can't use default apiClient.post because it sets Content-Type to json
        // Using fetch wrapper is better but apiClient supports headers/body override? 
        // Our apiClient.post stringifies body.
        // We need a custom request method or modify apiClient to handle FormData.
        // For now, let's look at api.ts again.

        const token = localStorage.getItem('renum_token');
        const headers: HeadersInit = {};
        if (token) headers['Authorization'] = `Bearer ${token}`;

        // Use raw fetch for FormData
        const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/knowledge/upload`, {
            method: 'POST',
            headers: headers, // Do NOT set Content-Type for FormData, browser sets it with boundary
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to upload document');
        }

        return await response.json();
    },

    deleteDocument: async (agentId: string, documentId: string): Promise<void> => {
        await apiClient.delete(`/api/knowledge/documents/${documentId}?agent_id=${agentId}`);
    },

    searchKnowledge: async (agentId: string, query: string): Promise<SearchResult[]> => {
        const response = await apiClient.post(`/api/knowledge/search?agent_id=${agentId}`, {
            query,
            limit: 5,
            threshold: 0.6
        });
        return response.data;
    }
};
