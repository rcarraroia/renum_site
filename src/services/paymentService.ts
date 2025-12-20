/**
 * Payment Service(Frontend)
 * Serviço para operações de pagamento no frontend
 */

import { apiClient } from './api';

export interface Plan {
    key: string;
    name: string;
    category: 'b2c' | 'b2b';
    price_brl: number | null;
    price_usd: number | null;
    stripe_price_id: string | null;
    features: string[];
}

export interface SubscriptionCreate {
    plan_key: string;
    template_id: string;
    payment_method?: 'credit_card' | 'boleto' | 'pix';
}

export interface SubscriptionResponse {
    gateway: 'asaas' | 'stripe';
    subscription_id: string;
    status: string;
    payment_url?: string;
    client_secret?: string;
}

/**
 * Lista planos disponíveis
 */
export async function listPlans(category?: 'b2c' | 'b2b'): Promise<Plan[]> {
    const params = category ? { category } : {};
    const { data } = await apiClient.get<Plan[]>('/api/payment/plans', { params });
    return data;
}

/**
 * Cria assinatura para um template
 */
export async function createSubscription(
    subscriptionData: SubscriptionCreate
): Promise<SubscriptionResponse> {
    const { data } = await apiClient.post<SubscriptionResponse>(
        '/api/payment/subscribe',
        subscriptionData
    );
    return data;
}

/**
 * Cancela assinatura ativa
 */
export async function cancelSubscription(): Promise<{ status: string; gateway: string }> {
    const { data } = await apiClient.post('/api/payment/cancel');
    return data;
}

/**
 * Busca status da assinatura atual
 */
export async function getSubscriptionStatus(): Promise<any> {
    const { data } = await apiClient.get('/api/payment/subscription');
    return data;
}

export const paymentService = {
    listPlans,
    createSubscription,
    cancelSubscription,
    getSubscriptionStatus,
};

export default paymentService;
