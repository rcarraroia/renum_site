# Requirements Document - Sprint 05A: Validação e Correção Completa do Sistema

## Introduction

Este sprint foca em validar 100% do sistema RENUM, corrigir bugs encontrados e garantir que todas as funcionalidades estão operacionais antes de avançar para novos desenvolvimentos. A análise rápida inicial mostrou 82% de funcionalidade, mas apenas 30% foi testado em profundidade. Este sprint valida os 70% restantes.

## Glossary

- **System**: Sistema RENUM completo (backend + frontend + agentes + integrações)
- **CRUD**: Create, Read, Update, Delete operations
- **Endpoint**: Rota da API REST
- **Agent**: Agente de IA (RENUS, ISA, Discovery)
- **WebSocket**: Protocolo de comunicação bidirecional em tempo real
- **Health Check**: Endpoint de verificação de saúde do sistema
- **Mock Data**: Dados falsos/hardcoded (não do banco)
- **Real Data**: Dados vindos do banco de dados Supabase

## Requirements

### Requirement 1: Correção de Bugs Conhecidos

**User Story:** Como desenvolvedor, quero corrigir todos os bugs conhecidos, para que o sistema funcione corretamente.

#### Acceptance Criteria

1. WHEN o endpoint /health é chamado THEN the System SHALL responder em menos de 2 segundos com status 200
2. WHEN o ISA Agent recebe uma mensagem THEN the System SHALL processar sem erro 500 e retornar resposta válida
3. WHEN um cliente é criado via POST /api/clients THEN the System SHALL aceitar dados sem campo "segment" obrigatório
4. WHEN rotas /api/sub-agents ou /api/renus-config são acessadas THEN the System SHALL retornar 200 sem redirect 307

### Requirement 2: Validação CRUD Completa

**User Story:** Como desenvolvedor, quero validar todas as operações CRUD de todas as entidades, para garantir que create, read, update e delete funcionam.

#### Acceptance Criteria

1. WHEN operações CRUD são executadas em Clients THEN the System SHALL criar, ler, atualizar e deletar clientes com sucesso
2. WHEN operações CRUD são executadas em Leads THEN the System SHALL criar, ler, atualizar e deletar leads com sucesso
3. WHEN operações CRUD são executadas em Projects THEN the System SHALL criar, ler, atualizar e deletar projetos com sucesso
4. WHEN operações CRUD são executadas em Conversations THEN the System SHALL criar, ler e gerenciar conversas com sucesso
5. WHEN operações CRUD são executadas em Interviews THEN the System SHALL iniciar e buscar entrevistas com sucesso

### Requirement 3: Validação de Agentes

**User Story:** Como desenvolvedor, quero validar que todos os agentes de IA funcionam corretamente, para garantir a funcionalidade principal do sistema.

#### Acceptance Criteria

1. WHEN o RENUS Agent é inicializado THEN the System SHALL criar instância sem erros e responder a mensagens
2. WHEN o ISA Agent recebe comando administrativo THEN the System SHALL executar comando e salvar em isa_commands
3. WHEN o Discovery Agent processa entrevista THEN the System SHALL extrair dados obrigatórios e gerar relatório ai_analysis
4. WHEN qualquer agente é invocado THEN the System SHALL registrar trace no LangSmith para auditoria

### Requirement 4: Validação WebSocket Completa

**User Story:** Como desenvolvedor, quero validar que WebSocket funciona end-to-end, para garantir comunicação em tempo real.

#### Acceptance Criteria

1. WHEN cliente conecta via WebSocket THEN the System SHALL estabelecer conexão com status 101
2. WHEN cliente envia mensagem via WebSocket THEN the System SHALL processar e retornar resposta (não timeout)
3. WHEN mensagem é enviada via WebSocket THEN the System SHALL salvar mensagem no banco de dados
4. WHEN usuário está digitando THEN the System SHALL enviar typing indicators via WebSocket
5. WHEN usuário conecta/desconecta THEN the System SHALL atualizar presence status (online/offline)

### Requirement 5: Validação Frontend Completa

**User Story:** Como desenvolvedor, quero validar que todos os menus do frontend funcionam, para garantir experiência do usuário.

#### Acceptance Criteria

1. WHEN usuário acessa Menu Overview THEN the System SHALL mostrar métricas que batem com dados do banco
2. WHEN usuário usa Menu Clientes THEN the System SHALL permitir criar, editar e deletar clientes
3. WHEN usuário usa Menu Leads THEN the System SHALL permitir criar, editar e deletar leads
4. WHEN usuário usa Menu Projetos THEN the System SHALL permitir criar, editar e deletar projetos
5. WHEN usuário usa Menu Conversas THEN the System SHALL permitir criar e visualizar conversas
6. WHEN usuário usa Menu Entrevistas THEN the System SHALL permitir visualizar entrevistas e relatórios
7. WHEN usuário usa Menu ISA THEN the System SHALL permitir enviar comandos e receber respostas reais
8. WHEN usuário usa Menu Config Renus THEN the System SHALL permitir salvar configurações que persistem no banco
9. WHEN usuário usa Menu Relatórios THEN the System SHALL permitir gerar e exportar relatórios
10. WHEN usuário usa Menu Configurações THEN the System SHALL permitir editar perfil com mudanças salvas

### Requirement 6: Documentação de Bugs

**User Story:** Como desenvolvedor, quero documentar todos os bugs encontrados, para rastreabilidade e correção futura.

#### Acceptance Criteria

1. WHEN um bug é encontrado THEN the System SHALL documentar o que quebrou, como reproduzir e erro exato
2. WHEN um bug é documentado THEN the System SHALL estimar tempo para corrigir
3. WHEN múltiplos bugs são encontrados THEN the System SHALL priorizar por impacto (crítico/médio/baixo)

### Requirement 7: Relatório Final de Validação

**User Story:** Como desenvolvedor, quero um relatório final com status real do sistema, para decidir se pode avançar para Sprint 06.

#### Acceptance Criteria

1. WHEN validação completa é concluída THEN the System SHALL gerar relatório com % funcional de cada componente
2. WHEN relatório é gerado THEN the System SHALL listar funcionalidades 100% OK, parcialmente OK e quebradas
3. WHEN relatório é gerado THEN the System SHALL recomendar se pode avançar para Sprint 06 ou precisa correções
4. WHEN sistema está 90%+ funcional THEN the System SHALL aprovar avanço para Sprint 06
5. WHEN sistema está abaixo de 90% THEN the System SHALL listar bugs críticos que bloqueiam avanço
