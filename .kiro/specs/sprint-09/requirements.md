# SPRINT 09 - REQUIREMENTS

## OBJETIVO GERAL

Este sprint tem dois objetivos principais:

1. **Completar WebSocket (Sprint 08 pendente):** Implementar comunicação em tempo real para conversas, permitindo que mensagens apareçam instantaneamente sem refresh da página.

2. **Corrigir Arquitetura Agents/Sub-Agents:** Criar a tabela `agents` e estabelecer a hierarquia correta `clients → agents → sub_agents`, migrando os 12 registros existentes e atualizando o RENUS para carregamento dinâmico.

---

## PARTE 1: WEBSOCKET (Completar Sprint 08)

### Contexto

O Sprint 08 implementou a estrutura básica de conversas, mas deixou pendente a comunicação em tempo real via WebSocket. Atualmente, as mensagens só aparecem após refresh manual da página.

### Requisitos Funcionais

#### RF-WS-01: Conexão WebSocket Autenticada
**User Story:** Como usuário logado, quero que o sistema estabeleça conexão WebSocket automaticamente ao acessar conversas, para receber atualizações em tempo real.

**Acceptance Criteria:**
1. WHEN o usuário acessa página de conversas THEN o sistema SHALL estabelecer conexão WebSocket com token JWT
2. WHEN a conexão falha THEN o sistema SHALL tentar reconectar automaticamente com backoff exponencial
3. WHEN o token expira THEN o sistema SHALL renovar token e reconectar
4. WHEN o usuário faz logout THEN o sistema SHALL fechar conexão WebSocket graciosamente

#### RF-WS-02: Recebimento de Mensagens em Tempo Real
**User Story:** Como usuário em uma conversa, quero ver novas mensagens instantaneamente, sem precisar atualizar a página.

**Acceptance Criteria:**
1. WHEN outra pessoa envia mensagem THEN a mensagem SHALL aparecer na tela em menos de 1 segundo
2. WHEN múltiplas mensagens chegam THEN todas SHALL ser exibidas na ordem correta
3. WHEN mensagem chega em conversa não aberta THEN contador de não lidas SHALL incrementar
4. WHEN mensagem chega em conversa aberta THEN mensagem SHALL ser marcada como lida automaticamente

#### RF-WS-03: Indicadores de Presença
**User Story:** Como usuário, quero ver quando outros usuários estão online, para saber se posso esperar resposta rápida.

**Acceptance Criteria:**
1. WHEN usuário conecta THEN status SHALL mudar para "online" para outros usuários
2. WHEN usuário desconecta THEN status SHALL mudar para "offline" após 30 segundos
3. WHEN usuário está inativo por 5 minutos THEN status SHALL mudar para "away"
4. WHEN usuário volta a interagir THEN status SHALL voltar para "online"

#### RF-WS-04: Indicadores de Digitação
**User Story:** Como usuário em uma conversa, quero ver quando a outra pessoa está digitando, para saber que ela está respondendo.

**Acceptance Criteria:**
1. WHEN usuário digita THEN indicador "digitando..." SHALL aparecer para outros participantes
2. WHEN usuário para de digitar por 3 segundos THEN indicador SHALL desaparecer
3. WHEN usuário envia mensagem THEN indicador SHALL desaparecer imediatamente
4. WHEN múltiplos usuários digitam THEN todos os nomes SHALL ser exibidos

#### RF-WS-05: Reconexão Automática
**User Story:** Como usuário, quero que o sistema reconecte automaticamente se a conexão cair, sem perder mensagens.

**Acceptance Criteria:**
1. WHEN conexão cai THEN sistema SHALL tentar reconectar após 1 segundo
2. WHEN reconexão falha THEN sistema SHALL tentar novamente com backoff exponencial (2s, 4s, 8s, 16s, max 30s)
3. WHEN reconecta com sucesso THEN sistema SHALL sincronizar mensagens perdidas
4. WHEN reconexão falha após 5 tentativas THEN sistema SHALL notificar usuário e sugerir refresh

### Comportamento Esperado

**Fluxo Normal:**
1. Usuário faz login → Token JWT gerado
2. Usuário acessa conversas → WebSocket conecta com token
3. Conexão estabelecida → Status "online" broadcast
4. Mensagem recebida → Aparece instantaneamente
5. Usuário digita → Indicador enviado via WebSocket
6. Usuário envia mensagem → Broadcast para participantes
7. Usuário sai → Conexão fecha, status "offline"

**Fluxo de Erro:**
1. Conexão cai → Tentativa de reconexão após 1s
2. Falha → Tentativa após 2s
3. Falha → Tentativa após 4s
4. Sucesso → Sincroniza mensagens perdidas
5. Se 5 falhas → Notifica usuário

---

## PARTE 2: ARQUITETURA AGENTS/SUB-AGENTS

### Contexto

**Problema Atual:**
- Tabela `agents` não existe no banco de dados
- Wizard salva agentes em `sub_agents` (incorreto)
- `sub_agents` tem FK `client_id` (deveria ser `agent_id`)
- RENUS usa registry estático em memória (não carrega do banco)
- 12 agentes existentes funcionando, mas em estrutura incorreta

**Arquitetura Correta:**
```
clients (empresas que pagam)
    ↓ 1:N
agents (agentes principais - criados via Wizard)
    ↓ 1:N (opcional)
sub_agents (especializações opcionais)
```

### Casos de Uso

#### Caso 1: Agente Simples (Sem Sub-Agents)
**Exemplo:** Clínica Veterinária - Atendimento WhatsApp 24/7

**Estrutura:**
- 1 client: "Clínica Veterinária Dr. Pet"
- 1 agent: "Atendente Virtual"
- 0 sub_agents

**Comportamento:**
- Cliente cria agente via Wizard
- Agente responde todas as mensagens diretamente
- Não há roteamento para sub-agents
- RENUS não precisa rotear, apenas responde

#### Caso 2: Agente Complexo (Com Sub-Agents)
**Exemplo:** Empresa MMN - Gestão Completa

**Estrutura:**
- 1 client: "Empresa MMN XYZ"
- 1 agent: "Assistente Principal"
- 4 sub_agents:
  - "Recrutamento" (tópicos: recrutamento, cadastro, onboarding)
  - "Treinamento" (tópicos: cursos, certificação, dúvidas)
  - "Cobrança" (tópicos: pagamento, comissão, fatura)
  - "Suporte" (tópicos: problema, bug, ajuda)

**Comportamento:**
- Cliente cria agente principal via Wizard
- Admin cria 4 sub-agents especializados
- Mensagem chega → RENUS analisa tópico
- RENUS roteia para sub-agent apropriado
- Sub-agent responde com expertise específica

### Requisitos Funcionais

#### RF-AG-01: Tabela Agents
**User Story:** Como sistema, preciso de uma tabela `agents` para armazenar agentes principais criados via Wizard.

**Acceptance Criteria:**
1. WHEN tabela é criada THEN SHALL ter estrutura completa (id, client_id, name, description, config, status, etc)
2. WHEN tabela é criada THEN SHALL ter FK para `clients`
3. WHEN tabela é criada THEN SHALL ter RLS habilitado
4. WHEN tabela é criada THEN SHALL ter políticas de acesso (admin full, client own)
5. WHEN tabela é criada THEN SHALL ter índices em client_id, status, slug

#### RF-AG-02: Migração de Dados Existentes
**User Story:** Como sistema, preciso migrar os 12 agentes existentes de `sub_agents` para `agents`, mantendo funcionalidade.

**Acceptance Criteria:**
1. WHEN migration executa THEN 12 registros SHALL ser copiados de `sub_agents` para `agents`
2. WHEN migration executa THEN dados SHALL manter integridade (IDs, slugs, URLs)
3. WHEN migration executa THEN agentes migrados SHALL continuar funcionando
4. WHEN migration executa THEN registros originais em `sub_agents` SHALL ser deletados
5. WHEN migration falha THEN rollback SHALL restaurar estado anterior

#### RF-AG-03: Alteração de Sub-Agents
**User Story:** Como sistema, preciso que `sub_agents` referencie `agents` (não `clients`).

**Acceptance Criteria:**
1. WHEN tabela é alterada THEN FK `client_id` SHALL ser removida
2. WHEN tabela é alterada THEN FK `agent_id` SHALL ser adicionada
3. WHEN tabela é alterada THEN RLS SHALL ser atualizado para usar `agent_id`
4. WHEN tabela é alterada THEN índices SHALL ser recriados
5. WHEN sub-agent é criado THEN SHALL requerer `agent_id` válido

#### RF-AG-04: Wizard Salva em Agents
**User Story:** Como usuário criando agente via Wizard, quero que ele seja salvo em `agents` (não `sub_agents`).

**Acceptance Criteria:**
1. WHEN wizard inicia THEN registro SHALL ser criado em `agents` com status='draft'
2. WHEN wizard salva step THEN dados SHALL ser salvos em `agents.config`
3. WHEN wizard publica THEN status SHALL mudar para 'active' em `agents`
4. WHEN wizard publica THEN slug, public_url, qr_code SHALL ser gerados em `agents`
5. WHEN wizard é abandonado THEN registro draft em `agents` SHALL ser deletado

#### RF-AG-05: Routes de Sub-Agents por Agent
**User Story:** Como admin, quero gerenciar sub-agents de um agente específico via API.

**Acceptance Criteria:**
1. WHEN chamo GET /agents/{agent_id}/sub-agents THEN SHALL retornar lista de sub-agents daquele agent
2. WHEN chamo POST /agents/{agent_id}/sub-agents THEN SHALL criar sub-agent vinculado ao agent
3. WHEN chamo PUT /agents/{agent_id}/sub-agents/{id} THEN SHALL atualizar sub-agent
4. WHEN chamo DELETE /agents/{agent_id}/sub-agents/{id} THEN SHALL deletar sub-agent
5. WHEN agent_id não existe THEN SHALL retornar 404

#### RF-AG-06: RENUS Carregamento Dinâmico
**User Story:** Como RENUS, preciso carregar agents e sub-agents do banco automaticamente ao iniciar.

**Acceptance Criteria:**
1. WHEN RENUS inicia THEN SHALL carregar todos agents ativos do banco
2. WHEN RENUS inicia THEN SHALL carregar sub-agents de cada agent
3. WHEN novo agent é criado THEN RENUS SHALL detectar em até 60 segundos
4. WHEN agent é desativado THEN RENUS SHALL remover do registry em até 60 segundos
5. WHEN sub-agent é criado THEN RENUS SHALL adicionar ao agent correspondente

#### RF-AG-07: Roteamento Dinâmico por Tópicos
**User Story:** Como RENUS, preciso rotear mensagens para sub-agents baseado em tópicos.

**Acceptance Criteria:**
1. WHEN mensagem chega THEN RENUS SHALL analisar tópico da mensagem
2. WHEN tópico corresponde a sub-agent THEN SHALL rotear para aquele sub-agent
3. WHEN tópico não corresponde THEN agent principal SHALL responder
4. WHEN múltiplos sub-agents correspondem THEN SHALL escolher o mais específico
5. WHEN sub-agent falha THEN SHALL fazer fallback para agent principal

#### RF-AG-08: Frontend Agents/Sub-Agents
**User Story:** Como admin, quero gerenciar agents e sub-agents via interface web.

**Acceptance Criteria:**
1. WHEN acesso /agents THEN SHALL listar todos agents do client
2. WHEN clico em agent THEN SHALL abrir detalhes com lista de sub-agents
3. WHEN clico "Adicionar Sub-Agent" THEN SHALL abrir formulário
4. WHEN salvo sub-agent THEN SHALL aparecer na lista
5. WHEN deleto sub-agent THEN SHALL remover da lista

### Comportamento Esperado

**Fluxo de Criação de Agent:**
1. Admin clica "Criar Agente"
2. Wizard inicia → Cria registro em `agents` (status='draft')
3. Admin preenche steps → Dados salvos em `agents.config`
4. Admin testa sandbox → Usa agent draft
5. Admin publica → Status muda para 'active', gera slug/URL
6. RENUS detecta novo agent → Carrega em registry
7. Agent está pronto para receber mensagens

**Fluxo de Criação de Sub-Agent:**
1. Admin acessa agent existente
2. Admin clica "Adicionar Sub-Agent"
3. Admin preenche formulário (nome, tópicos, prompt)
4. Sistema salva em `sub_agents` com `agent_id`
5. RENUS detecta novo sub-agent → Adiciona ao agent
6. Sub-agent está pronto para roteamento

**Fluxo de Roteamento:**
1. Mensagem chega para agent
2. RENUS analisa conteúdo da mensagem
3. RENUS identifica tópico (ex: "pagamento")
4. RENUS busca sub-agent com tópico "pagamento"
5. RENUS roteia para sub-agent "Cobrança"
6. Sub-agent processa e responde
7. Resposta enviada ao usuário

---

## VALIDAÇÃO FINAL

### Parte 1: WebSocket

**Teste Manual:**
1. Abrir 2 navegadores com usuários diferentes
2. Iniciar conversa entre eles
3. Enviar mensagem no navegador 1
4. Verificar que aparece instantaneamente no navegador 2
5. Digitar no navegador 2
6. Verificar indicador "digitando..." no navegador 1
7. Desconectar internet no navegador 1
8. Reconectar internet
9. Verificar que reconexão automática funciona
10. Enviar mensagem durante desconexão
11. Verificar que mensagem é sincronizada após reconexão

**Resultado Esperado:**
- ✅ Mensagens aparecem em < 1 segundo
- ✅ Indicador de digitação funciona
- ✅ Reconexão automática funciona
- ✅ Mensagens não são perdidas

### Parte 2: Arquitetura Agents

**Teste Manual:**
1. Criar novo agent via Wizard
2. Verificar que foi salvo em `agents` (não `sub_agents`)
3. Publicar agent
4. Verificar que slug e URL foram gerados
5. Acessar agent publicado
6. Criar sub-agent para o agent
7. Verificar que foi salvo em `sub_agents` com `agent_id`
8. Enviar mensagem com tópico do sub-agent
9. Verificar que RENUS roteou corretamente
10. Verificar que 12 agents migrados continuam funcionando

**Resultado Esperado:**
- ✅ Wizard salva em `agents`
- ✅ Sub-agents têm `agent_id` correto
- ✅ RENUS carrega do banco automaticamente
- ✅ Roteamento por tópicos funciona
- ✅ Agents migrados funcionam normalmente

---

## GLOSSARY

- **Agent:** Agente principal criado via Wizard, vinculado a um client
- **Sub-Agent:** Especialização opcional de um agent, com tópicos específicos
- **RENUS:** Orquestrador principal que roteia mensagens para agents/sub-agents
- **Wizard:** Interface de criação de agents em 4 steps
- **WebSocket:** Protocolo de comunicação bidirecional em tempo real
- **Typing Indicator:** Indicador visual de que alguém está digitando
- **Presence:** Status de conexão de um usuário (online, offline, away)
- **Backoff Exponencial:** Estratégia de retry com intervalos crescentes
- **Registry:** Estrutura em memória que armazena agents/sub-agents carregados
- **Tópico:** Palavra-chave usada para rotear mensagens para sub-agents

---

**Versão:** 1.0  
**Data:** 2025-12-06  
**Responsável:** Kiro (Agente de IA)
