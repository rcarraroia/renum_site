# SPRINT 08 - CONEXÃO BACKEND - REQUIREMENTS

## INTRODUÇÃO

Este sprint tem como objetivo conectar 6 funcionalidades que atualmente operam com dados mock ao backend real, elevando o sistema de 41% para 75% de funcionalidade completa. As funcionalidades serão integradas ao Supabase via API REST e WebSocket, garantindo persistência de dados e operações em tempo real.

## GLOSSÁRIO

- **Sistema**: Plataforma RENUM completa (frontend + backend + banco de dados)
- **Frontend**: Aplicação React/TypeScript que roda no navegador
- **Backend**: API FastAPI que processa requisições e gerencia dados
- **Supabase**: Banco de dados PostgreSQL hospedado com RLS habilitado
- **Mock**: Dados simulados armazenados em useState sem persistência
- **CRUD**: Create, Read, Update, Delete (operações básicas de dados)
- **WebSocket**: Protocolo de comunicação bidirecional em tempo real
- **RLS**: Row Level Security (segurança em nível de linha no banco)
- **Discovery Agent**: Agente de IA que conduz entrevistas automatizadas
- **Pipeline**: Fluxo de conversão de leads através de estágios

## REQUISITOS

### Requisito 1: Gestão de Projetos

**User Story:** Como administrador do sistema, quero gerenciar projetos através do frontend conectado ao backend, para que os dados sejam persistidos no banco de dados e compartilhados entre sessões.

#### Acceptance Criteria

1. WHEN um administrador cria um projeto através do formulário THEN o Sistema SHALL enviar requisição POST ao backend e persistir os dados no Supabase
2. WHEN um administrador acessa a página de projetos THEN o Sistema SHALL carregar a lista de projetos do Supabase via requisição GET
3. WHEN um administrador edita um projeto existente THEN o Sistema SHALL enviar requisição PUT ao backend e atualizar os dados no Supabase
4. WHEN um administrador deleta um projeto THEN o Sistema SHALL enviar requisição DELETE ao backend e remover o registro do Supabase
5. WHEN uma operação de projeto falha THEN o Sistema SHALL exibir mensagem de erro apropriada e manter o estado anterior

### Requisito 2: Gestão de Leads

**User Story:** Como administrador do sistema, quero gerenciar leads através do frontend conectado ao backend, para que possa rastrear contatos e convertê-los em clientes quando apropriado.

#### Acceptance Criteria

1. WHEN um administrador cria um lead através do formulário THEN o Sistema SHALL enviar requisição POST ao backend e persistir os dados no Supabase
2. WHEN um administrador acessa a página de leads THEN o Sistema SHALL carregar a lista de leads do Supabase via requisição GET
3. WHEN um administrador edita um lead existente THEN o Sistema SHALL enviar requisição PUT ao backend e atualizar os dados no Supabase
4. WHEN um administrador deleta um lead THEN o Sistema SHALL enviar requisição DELETE ao backend e remover o registro do Supabase
5. WHEN um administrador converte um lead em cliente THEN o Sistema SHALL criar um novo registro na tabela clients e atualizar o status do lead
6. WHEN um lead é movido no pipeline THEN o Sistema SHALL atualizar o estágio do lead no Supabase e refletir a mudança visualmente

### Requisito 3: Gestão de Clientes

**User Story:** Como administrador do sistema, quero gerenciar clientes através do frontend conectado ao backend, para que possa manter registro atualizado de empresas que contrataram agentes.

#### Acceptance Criteria

1. WHEN um administrador cria um cliente através do formulário THEN o Sistema SHALL enviar requisição POST ao backend e persistir os dados no Supabase
2. WHEN um administrador acessa a página de clientes THEN o Sistema SHALL carregar a lista de clientes do Supabase via requisição GET
3. WHEN um administrador edita um cliente existente THEN o Sistema SHALL enviar requisição PUT ao backend e atualizar os dados no Supabase
4. WHEN um administrador deleta um cliente THEN o Sistema SHALL enviar requisição DELETE ao backend e remover o registro do Supabase
5. WHEN um cliente é criado a partir de um lead THEN o Sistema SHALL vincular o cliente ao lead original através de client_id

### Requisito 4: Sistema de Conversas em Tempo Real

**User Story:** Como administrador do sistema, quero que as conversas funcionem em tempo real com persistência de mensagens, para que possa acompanhar histórico completo de interações com leads.

#### Acceptance Criteria

1. WHEN um administrador abre uma conversa THEN o Sistema SHALL estabelecer conexão WebSocket com o backend e carregar histórico de mensagens do Supabase
2. WHEN um administrador envia uma mensagem THEN o Sistema SHALL transmitir via WebSocket e persistir no Supabase imediatamente
3. WHEN uma nova mensagem é recebida THEN o Sistema SHALL exibir a mensagem em tempo real sem necessidade de refresh
4. WHEN um usuário está digitando THEN o Sistema SHALL transmitir indicador de digitação via WebSocket para outros participantes
5. WHEN um usuário conecta ou desconecta THEN o Sistema SHALL atualizar status de presença (online/offline) em tempo real
6. WHEN a conexão WebSocket é perdida THEN o Sistema SHALL tentar reconectar automaticamente e exibir indicador de status de conexão

### Requisito 5: Visualização de Entrevistas

**User Story:** Como administrador do sistema, quero visualizar entrevistas conduzidas pelo Discovery Agent com dados reais do banco, para que possa analisar respostas e resultados de pesquisas.

#### Acceptance Criteria

1. WHEN um administrador acessa a página de entrevistas THEN o Sistema SHALL carregar lista de entrevistas do Supabase via requisição GET
2. WHEN um administrador clica em uma entrevista THEN o Sistema SHALL carregar detalhes completos incluindo metadados e status
3. WHEN um administrador acessa resultados de uma entrevista THEN o Sistema SHALL carregar análise gerada pelo Discovery Agent do Supabase
4. WHEN uma entrevista está em andamento THEN o Sistema SHALL exibir status "in_progress" e permitir acompanhamento em tempo real
5. WHEN uma entrevista é concluída THEN o Sistema SHALL exibir status "completed" e disponibilizar resultados completos

### Requisito 6: Relatórios e Analytics

**User Story:** Como administrador do sistema, quero visualizar relatórios com dados reais e exportá-los, para que possa analisar performance e tomar decisões baseadas em dados.

#### Acceptance Criteria

1. WHEN um administrador acessa o dashboard de relatórios THEN o Sistema SHALL carregar métricas gerais do Supabase via requisição GET
2. WHEN um administrador aplica filtros de período THEN o Sistema SHALL recarregar dados filtrados do backend
3. WHEN um administrador visualiza performance de agentes THEN o Sistema SHALL exibir métricas calculadas pelo backend baseadas em dados reais
4. WHEN um administrador visualiza funil de conversão THEN o Sistema SHALL exibir estatísticas de conversão de leads calculadas pelo backend
5. WHEN um administrador clica em exportar THEN o Sistema SHALL gerar arquivo CSV ou Excel com dados filtrados via requisição ao backend

### Requisito 7: Tratamento de Erros e Estados de Loading

**User Story:** Como usuário do sistema, quero feedback visual claro durante operações e mensagens de erro compreensíveis, para que saiba o status das minhas ações.

#### Acceptance Criteria

1. WHEN uma requisição está em andamento THEN o Sistema SHALL exibir indicador de loading apropriado (spinner, skeleton, progress bar)
2. WHEN uma requisição falha por erro de rede THEN o Sistema SHALL exibir mensagem "Erro de conexão. Verifique sua internet."
3. WHEN uma requisição falha por erro de autenticação THEN o Sistema SHALL redirecionar para login e exibir mensagem apropriada
4. WHEN uma requisição falha por erro de validação THEN o Sistema SHALL exibir mensagens de erro específicas por campo
5. WHEN uma requisição falha por erro de servidor THEN o Sistema SHALL exibir mensagem genérica e registrar erro no console para debug

### Requisito 8: Sincronização de Estado

**User Story:** Como desenvolvedor do sistema, quero que o estado do frontend seja sincronizado com o backend, para que dados sejam consistentes e atualizados.

#### Acceptance Criteria

1. WHEN dados são modificados no backend THEN o Frontend SHALL refletir mudanças após próxima requisição ou via WebSocket
2. WHEN múltiplos usuários editam o mesmo recurso THEN o Sistema SHALL aplicar estratégia de last-write-wins e notificar conflitos quando apropriado
3. WHEN dados são criados via API THEN o Frontend SHALL adicionar novo item à lista local sem necessidade de recarregar página completa
4. WHEN dados são deletados via API THEN o Frontend SHALL remover item da lista local imediatamente
5. WHEN cache local está desatualizado THEN o Sistema SHALL invalidar cache e recarregar dados do backend
