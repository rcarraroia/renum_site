# 🎯 RENUM - Documentação do Produto

## Visão Geral do Negócio

**Nome:** RENUM  
**Segmento:** Agência de automações e agentes de IA  
**Modelo:** B2B (venda de agentes para empresas)  
**Proposta de Valor:** Desenvolvimento e venda de agentes de IA especializados para diferentes nichos de mercado

---

## 🤖 Produtos e Serviços

### Agente Principal: RENUS
Sistema de agente conversacional inteligente que serve como base para todos os sub-agentes especializados.

**Características:**
- Orquestração via LangGraph/LangChain
- Integração com WhatsApp
- Sistema de pesquisas e entrevistas automatizadas
- Análise de dados com IA
- Multi-canal (WhatsApp, SMS, Email)

### Sub-agentes Especializados
Cada sub-agente é uma versão customizada do RENUS para nichos específicos:

1. **Agente MMN (Marketing Multinível)**
   - Gestão de redes de distribuidores
   - Acompanhamento de performance
   - Comunicação automatizada com equipe

2. **Agente Vereadores**
   - Gestão de relacionamento com eleitores
   - Pesquisas de opinião
   - Comunicação política

3. **Agente Clínicas**
   - Agendamento de consultas
   - Follow-up de pacientes
   - Pesquisas de satisfação

4. **Sistema de Pesquisas/Entrevistas**
   - Criação de questionários dinâmicos
   - Coleta automatizada via WhatsApp
   - Análise de respostas com IA
   - Relatórios e insights

---

## 💰 Modelo de Negócio

### Clientes-Alvo
- **Empresas MLM:** Gestão de redes de distribuição
- **Políticos:** Relacionamento com eleitores e pesquisas
- **Clínicas e Consultórios:** Atendimento e follow-up
- **Empresas B2C:** Pesquisas de satisfação e NPS

### Como Funciona a Venda
1. Cliente contrata um agente especializado
2. RENUM cria sistema dedicado para o cliente
3. Cliente recebe acesso ao painel administrativo próprio
4. Sistema é configurado com branding e regras do cliente
5. Agente começa a operar de forma autônoma

### Diferença: Sistema Admin vs Sistemas Cliente

**Sistema Admin (RENUM):**
- Gerencia todos os clientes
- Cria e configura novos sistemas
- Monitora performance global
- Gerencia leads e projetos internos
- Acesso total ao banco de dados

**Sistemas Cliente:**
- Criados sob demanda para cada cliente
- Isolamento total de dados (multi-tenant)
- Branding personalizado
- Configurações específicas do negócio
- Cliente só vê seus próprios dados

---

## 🎯 Estratégia de Operação

### Sistema Administrativo
**Responsabilidades:**
- Gestão de leads (potenciais clientes)
- Gestão de clientes ativos
- Criação de projetos
- Configuração de agentes
- Monitoramento de uso e performance
- Suporte técnico

### Sistemas dos Clientes
**Responsabilidades:**
- Gestão de contatos/leads do cliente
- Execução de pesquisas e entrevistas
- Conversas automatizadas
- Relatórios e análises
- Configurações do agente

### Leads (Usuários Finais)
**Características importantes:**
- **NÃO precisam de login**
- **NÃO acessam sistema web**
- Interagem apenas via WhatsApp
- Respondem pesquisas e conversam com agente
- Dados armazenados de forma anônima/pseudônima

---

## ✅ Regras de Negócio Críticas

### 1. Multi-tenant Separado
- Cada cliente tem sistema completamente isolado
- Dados de um cliente NUNCA aparecem para outro
- Configurações independentes por cliente
- Possibilidade de white-label

### 2. Arquitetura de Entrevistas
**CRÍTICO:** `interview_messages` em tabela separada!

**Motivo:** Performance com 1000+ entrevistas ativas simultâneas

**Estrutura:**
```
interviews (metadados)
  ├── id
  ├── lead_id
  ├── status
  ├── created_at
  └── metadata

interview_messages (mensagens individuais) - 1:N
  ├── id
  ├── interview_id (FK)
  ├── role (user/assistant)
  ├── content
  └── timestamp
```

### 3. Integração WhatsApp
- Gateway de WhatsApp (API a ser definida por projeto)
- Fallback para SMS se WhatsApp falhar
- Fallback para Email como última opção
- Fila de mensagens com Celery + Redis

### 4. Orquestração de Agentes
- **LangGraph** para fluxos complexos
- **LangChain** para componentes reutilizáveis
- Cada sub-agente tem configuração própria em `renus_config`
- Tools dinâmicas carregadas da tabela `tools`

### 5. Sistema de Filas
- Todas operações assíncronas via Celery
- Redis como message broker
- Priorização de mensagens críticas
- Retry automático em caso de falha

### 6. Comandos ISA
- Sistema de comandos especiais para administradores
- Tabela `isa_commands` armazena histórico
- Permite intervenção manual em conversas
- Auditoria completa de ações

---

## 🔄 Fluxos Principais

### Fluxo de Pesquisa/Entrevista
1. Cliente cria pesquisa no painel
2. Sistema envia convite via WhatsApp para leads
3. Lead responde perguntas via chat
4. Respostas armazenadas em `interview_messages`
5. IA analisa respostas em tempo real
6. Relatório gerado automaticamente
7. Cliente recebe notificação de conclusão

### Fluxo de Conversão Lead → Cliente
1. Lead demonstra interesse em produto/serviço
2. Agente qualifica lead com perguntas
3. Lead qualificado vira "cliente" na tabela `clients`
4. Sistema cria projeto específico
5. Agente continua relacionamento personalizado

### Fluxo de Notificações
1. Evento dispara notificação (nova mensagem, pesquisa concluída, etc)
2. Sistema tenta WhatsApp
3. Se falhar, tenta SMS
4. Se falhar, envia Email
5. Log completo em `conversations` e `messages`

---

## 📊 Métricas de Sucesso

### Para RENUM (Admin)
- Número de clientes ativos
- Número de agentes vendidos
- Taxa de retenção de clientes
- Uptime do sistema
- Tempo de resposta médio

### Para Clientes
- Taxa de resposta em pesquisas
- Tempo médio de conclusão de entrevistas
- Satisfação dos leads
- Conversões (lead → cliente)
- ROI do agente

---

## 🚀 Roadmap

### Fase Atual
- Sistema admin funcional
- Agente RENUS base operacional
- Integração WhatsApp estável
- Sistema de pesquisas MVP

### Próximos Passos
- Sub-agentes especializados (MMN, Vereadores, Clínicas)
- White-label completo
- Dashboard analytics avançado
- Integração com CRMs externos
- API pública para integrações

---

## ⚠️ Pontos de Atenção

### Escalabilidade
- Sistema deve suportar 10.000+ leads simultâneos
- Filas devem processar 1000+ mensagens/minuto
- Banco otimizado para queries em tabelas grandes

### Segurança
- Dados sensíveis criptografados
- RLS (Row Level Security) em todas tabelas
- Auditoria completa de acessos
- Compliance com LGPD

### Confiabilidade
- Uptime mínimo de 99.5%
- Backup automático diário
- Disaster recovery plan
- Monitoramento 24/7

---

**Última atualização:** 2025-11-25  
**Versão:** 1.0  
**Responsável:** Equipe RENUM
