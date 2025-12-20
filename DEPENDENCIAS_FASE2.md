# Dependências Necessárias - Fase 2

## Backend (Python)

### Instalar via pip:
```bash
cd backend
pip install stripe
pip install httpx  # Se não tiver
```

### Adicionar ao requirements.txt:
```
stripe==7.0.0
httpx==0.25.2
```

## Frontend (Node.js)

### Instalar via npm:
```bash
cd renum_site
npm install @stripe/stripe-js @stripe/react-stripe-js
```

### Adicionar ao package.json:
```json
{
  "dependencies": {
    "@stripe/stripe-js": "^2.4.0",
    "@stripe/react-stripe-js": "^2.4.0"
  }
}
```

## Variáveis de Ambiente

### Backend (.env)
```env
# Asaas
ASAAS_API_KEY=your_asaas_api_key_here
ASAAS_BASE_URL=https://www.asaas.com/api/v3

# Stripe
STRIPE_API_KEY=sk_test_your_stripe_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

### Frontend (.env ou .env.local)
```env
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here
```

## Configuração do Stripe

1. Acessar https://dashboard.stripe.com
2. Criar produtos e preços:
   - B2C Basic: R$ 49,90/mês (criar price_id)
   - B2C Pro: R$ 99,90/mês (criar price_id)
   - B2B Starter: R$ 299,90/mês (criar price_id)
   - B2B Business: R$ 599,90/mês (criar price_id)
3. Atualizar `payment_service.py` com os `stripe_price_id` corretos

## Configuração do Asaas

1. Acessar https://www.asaas.com
2. Criar conta e obter API Key
3. Configurar webhook para notificações de pagamento
4. URL do webhook: `https://seu-dominio.com/api/payment/webhook/asaas`

## Notas Importantes

- As chaves acima são de TESTE
- Antes de produção, substituir por chaves LIVE
- Configurar webhooks em ambos os gateways
- Testar fluxo completo com cartões de teste
