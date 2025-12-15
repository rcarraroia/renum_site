/**
 * ISA Service - Assistente de IA
 */

import { apiClient } from './api';

export interface IsaMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  commandExecuted?: boolean;
}

export interface IsaCommand {
  command: string;
  result: any;
  executed_at: string;
}

export const isaService = {
  /**
   * Send message to ISA
   */
  async sendMessage(message: string): Promise<IsaMessage> {
    const { data } = await apiClient.post<{ message: string; command_executed: boolean }>('/api/isa/chat', { message });

    // Adaptador Backend -> Frontend
    return {
      role: 'assistant',
      content: data.message,
      timestamp: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }),
      commandExecuted: data.command_executed
    };
  },

  /**
   * Get command history
   */
  async getCommandHistory(): Promise<IsaCommand[]> {
    try {
      const { data } = await apiClient.get('/isa/history'); // Endpoint ajustado para o que existe no backend
      return data;
    } catch (error) {
      console.warn('Erro ao buscar histórico ISA:', error);
      return [];
    }
  },

  /**
   * Execute ISA command
   */
  async executeCommand(command: string): Promise<any> {
    try {
      const { data } = await apiClient.post('/api/isa/execute', { command });
      return data;
    } catch (error) {
      throw new Error('Erro ao executar comando');
    }
  }
};