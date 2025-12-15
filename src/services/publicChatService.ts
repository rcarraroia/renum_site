
import { apiClient } from './api';

export interface ChatMessage {
    id: string; // Changed to string to support backend IDs if needed
    sender: 'user' | 'renus';
    text: string;
    timestamp?: string;
    isThinking?: boolean;
}

export interface ChatResponse {
    message: string;
    interview_id: string;
    is_complete: boolean;
    progress: any;
}

export const publicChatService = {
    async sendMessage(slug: string, message: string, interviewId?: string | null) {
        // Note: endpoint is /chat/{slug}/message without /api prefix in apiClient if baseURL includes /api
        // Wait, apiClient usually has baseURL = localhost:8000/api ? No, it was localhost:8000
        // But public_chat.py uses @router with no prefix in main.py? 
        // main.py: app.include_router(public_chat.router, prefix="/api")
        // public_chat.py: @router.post("/chat/{agent_slug}/message")
        // So full URL is /api/chat/{slug}/message

        const payload = {
            message,
            interview_id: interviewId || null
        };

        const { data } = await apiClient.post<ChatResponse>(`/api/chat/${slug}/message`, payload);
        return data;
    },

    async getHistory(slug: string, interviewId: string) {
        const { data } = await apiClient.get<{ messages: any[] }>(`/api/chat/${slug}/interview/${interviewId}`);
        return data;
    },

    async getAgentPublicInfo(slug: string) {
        const { data } = await apiClient.get<any>(`/api/chat/${slug}`);
        return data;
    }
};
