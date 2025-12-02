# 🔑 Guia de Configuração de API Keys - RENUM

Este guia explica como obter e configurar todas as API keys necessárias para o funcionamento do sistema RENUM.

---

## 📋 Checklist de Configuração

- [ ] OpenRouter API Key (Obrigatório)
- [ ] Supabase Keys (Obrigatório)
- [ ] LangSmith API Key (Opcional - Monitoramento)
- [ ] WhatsApp API (Opcional - Integração)
- [ ] Email SMTP (Opcional - Notificações)

---

## 🤖 OpenRouter API Key

O OpenRouter fornece acesso a múltiplos modelos de IA (GPT-4, Claude, Llama, etc.) através de uma única API.

### Como Obter

1. Acesse: https://openrouter.ai/
2. Clique em "Sign In" e faça login com GitHub ou Google
3. Vá para "Keys" no menu
4. Clique em "Create Key"
5. Dê um nome (ex: "RENUM Production")
6. Copie a chave gerada (começa com `sk-or-v1-`)

### Configuração

Adicione no arquivo `.env`:

```bash
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Modelos Recomendados

- **Produção:** `anthropic/claude-sonnet-4` (melhor qualidade)
- **Desenvolvimento:** `openai/gpt-4o-mini` (mais barato)
- **Testes:** `meta-llama/llama-3.1-8b-instruct:free` (gratuito)

### Custos Aproximados

| Modelo | Custo por 1M tokens |
|--------|---------------------|
| Claude Sonnet 4 | $15 |
| GPT-4o Mini | $0.15 |
| Llama 3.1 8B | FREE |

### Troubleshooting

**Erro: "Invalid API key"**
- Verifique se copiou a chave completa
- Certifique-se que não há espaços extras
- Verifique se a chave não expirou

**Erro: "Insufficient credits"**
- Adicione créditos em https://openrouter.ai/credits
- Mínimo recomendado: $10 para começar

---

## 🗄️ Supabase Keys

Supabase é o banco de dados PostgreSQL gerenciado usado pelo RENUM.

### Como Obter

1. Acesse: https://supabase.com/dashboard
2. Faça login ou crie uma conta
3. Crie um novo projeto ou selecione existente
4. Vá em "Settings" → "API"
5. Copie as seguintes informações:
   - **Project URL**
   - **anon/public key** (para frontend)
   - **service_role key** (para backend)

### Configuração

Adicione no arquivo `.env`:

```bash
# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Conexão Direta (opcional)
DATABASE_URL=postgresql://postgres:senha@db.seu-projeto.supabase.co:5432/postgres
```

### ⚠️ Segurança

- **NUNCA** exponha a `SERVICE_KEY` no frontend
- Use `ANON_KEY` no frontend (respeita RLS)
- Use `SERVICE_KEY` apenas no backend (bypassa RLS)

### Troubleshooting

**Erro: "Invalid API key"**
- Verifique se está usando a chave correta (anon vs service)
- Certifique-se que o projeto está ativo

**Erro: "Connection refused"**
- Verifique se a URL está correta
- Verifique se o projeto não foi pausado (free tier)

---

## 📊 LangSmith API Key (Opcional)

LangSmith é usado para monitoramento e debugging de agentes de IA.

### Como Obter

1. Acesse: https://smith.langchain.com/
2. Faça login com GitHub ou Google
3. Crie uma organização (se necessário)
4. Vá em "Settings" → "API Keys"
5. Clique em "Create API Key"
6. Copie a chave gerada

### Configuração

Adicione no arquivo `.env`:

```bash
# LangSmith (Opcional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LANGCHAIN_PROJECT=renum-production
```

### Benefícios

- ✅ Visualizar todas as chamadas de IA
- ✅ Debugar prompts e respostas
- ✅ Monitorar custos em tempo real
- ✅ Analisar performance dos agentes

### Troubleshooting

**Traces não aparecem**
- Verifique se `LANGCHAIN_TRACING_V2=true`
- Certifique-se que a API key está correta
- Aguarde alguns minutos (pode haver delay)

---

## 💬 WhatsApp API (Opcional)

Para integração com WhatsApp Business.

### Opções Disponíveis

#### 1. Evolution API (Recomendado)
- **Site:** https://evolution-api.com/
- **Custo:** Gratuito (self-hosted)
- **Setup:** Docker

```bash
# .env
WHATSAPP_API_URL=http://localhost:8080
WHATSAPP_API_KEY=sua-chave-aqui
```

#### 2. Twilio
- **Site:** https://www.twilio.com/
- **Custo:** Pay-as-you-go
- **Setup:** Criar conta e obter credenciais

```bash
# .env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=+14155238886
```

#### 3. Meta WhatsApp Business API
- **Site:** https://developers.facebook.com/
- **Custo:** Gratuito (1000 conversas/mês)
- **Setup:** Requer aprovação do Meta

```bash
# .env
META_WHATSAPP_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
META_WHATSAPP_PHONE_ID=123456789012345
```

### Troubleshooting

**Mensagens não são enviadas**
- Verifique se o número está no formato internacional (+5511999999999)
- Certifique-se que a API está rodando
- Verifique logs para erros específicos

---

## 📧 Email SMTP (Opcional)

Para envio de emails e notificações.

### Opções Disponíveis

#### 1. Gmail (Desenvolvimento)
```bash
# .env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=senha-de-app
SMTP_FROM=seu-email@gmail.com
```

**Nota:** Habilite "App Passwords" nas configurações do Gmail

#### 2. SendGrid (Produção)
- **Site:** https://sendgrid.com/
- **Custo:** 100 emails/dia grátis

```bash
# .env
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SENDGRID_FROM_EMAIL=noreply@renum.com
```

#### 3. AWS SES (Produção)
- **Site:** https://aws.amazon.com/ses/
- **Custo:** $0.10 por 1000 emails

```bash
# .env
AWS_ACCESS_KEY_ID=AKIAxxxxxxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AWS_REGION=us-east-1
SES_FROM_EMAIL=noreply@renum.com
```

---

## 🔒 Segurança das Chaves

### Boas Práticas

1. **Nunca commite .env no Git**
   ```bash
   # .gitignore
   .env
   .env.local
   .env.*.local
   ```

2. **Use variáveis de ambiente em produção**
   - Não armazene chaves em código
   - Use secrets do provedor de hospedagem

3. **Rotacione chaves periodicamente**
   - A cada 90 dias
   - Imediatamente se houver suspeita de vazamento

4. **Use chaves diferentes por ambiente**
   - Desenvolvimento: `.env.development`
   - Produção: `.env.production`

5. **Limite permissões**
   - Use chaves com menor privilégio possível
   - Restrinja IPs quando possível

### Gerenciadores de Senhas Recomendados

- **1Password** (Pago)
- **Bitwarden** (Gratuito/Pago)
- **LastPass** (Gratuito/Pago)

---

## ✅ Validação da Configuração

Execute este script para validar suas chaves:

```bash
cd backend
python check_api_keys.py
```

**Output esperado:**
```
✅ OpenRouter API Key: Valid
✅ Supabase URL: Valid
✅ Supabase Anon Key: Valid
✅ Supabase Service Key: Valid
⚠️  LangSmith API Key: Not configured (optional)
⚠️  WhatsApp API: Not configured (optional)
⚠️  Email SMTP: Not configured (optional)

Configuration Status: READY ✅
```

---

## 🆘 Suporte

### Problemas Comuns

**"ModuleNotFoundError: No module named 'dotenv'"**
```bash
pip install python-dotenv
```

**"Environment variable not found"**
- Verifique se o arquivo `.env` está na raiz do projeto
- Certifique-se que não há espaços antes/depois do `=`
- Reinicie o servidor após alterar `.env`

**"API key invalid after configuration"**
- Limpe o cache: `rm -rf __pycache__`
- Reinicie completamente o servidor
- Verifique se não há caracteres especiais na chave

### Contato

- **Email:** suporte@renum.com
- **Discord:** https://discord.gg/renum
- **GitHub Issues:** https://github.com/renum/renum/issues

---

**Última atualização:** 2024-01-01  
**Versão:** 1.0.0
