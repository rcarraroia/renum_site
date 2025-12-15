# Requirements Document - Sprint 05B

## Introduction

Sprint 05B é uma auditoria completa e validação sistemática do sistema RENUM após conclusão dos Sprints 01-07A. O objetivo é:

1. Validar funcionalmente todos os componentes implementados
2. Identificar bugs e gaps remanescentes
3. Definir MVP atualizado (incluindo Wizard e Integrações)
4. Criar roadmap priorizado para Sprints 07B+

Este sprint é executado em 4 fases sequenciais: Validação Funcional, Análise de Gaps, Priorização e Roadmap, Relatório Executivo.

## Glossary

- **Sistema RENUM**: Plataforma completa (Backend FastAPI, Frontend React, Agentes IA, Supabase)
- **Validação Funcional**: Teste real via navegador, WebSocket, API
- **Gap**: Funcionalidade faltante ou incompleta
- **Bug Pendente**: Bug não corrigido de sprints anteriores
- **MVP**: Minimum Viable Product - funcionalidades mínimas para produção
- **Roadmap**: Plano priorizado de correções e melhorias
- **Wizard**: Interface de criação de agentes em 5 etapas
- **Integrações Core**: WhatsApp (Uazapi), Email (SMTP), Database (Supabase Cliente)
- **Triggers**: Sistema de automação QUANDO → SE → ENTÃO
- **Celery**: Sistema de filas assíncronas para processamento background
- **LangGraph**: Framework para orquestração de agentes IA
- **RLS**: Row Level Security - segurança nível de linha no Supabase

## Requirements

### Requirement 1: Validação Funcional de WebSocket

**User Story:** Como desenvolvedor, quero validar WebSocket em cenários reais, para garantir comunicação tempo real frontend-backend.

#### Acceptance Criteria

1. WHEN cliente WebSocket conecta com token válido THEN sistema SHALL estabelecer conexão status 101
2. WHEN cliente WebSocket conecta sem token THEN sistema SHALL rejeitar com status 401/403
3. WHEN mensagem enviada via WebSocket THEN sistema SHALL processar e responder em <2s
4. WHEN múltiplos clientes conectam THEN sistema SHALL manter todas conexões estáveis
5. WHEN conexão WebSocket fecha THEN sistema SHALL liberar recursos sem memory leak

---

### Requirement 2: Validação Funcional de Frontend

**User Story:** Como desenvolvedor, quero validar frontend no navegador, para garantir experiência adequada.

#### Acceptance Criteria

1. WHEN frontend acessado THEN sistema SHALL carregar sem erros console
2. WHEN usuário faz login THEN sistema SHALL autenticar e redirecionar dashboard
3. WHEN usuário navega entre páginas THEN sistema SHALL carregar sem tela branca
4. WHEN dados carregados do backend THEN sistema SHALL exibir corretamente
5. WHEN usuário realiza CRUD THEN sistema SHALL persistir e atualizar UI

---

### Requirement 3: Validação Funcional do Wizard (Sprint 06)

**User Story:** Como cliente, quero validar que o Wizard de Criação de Agentes funciona completamente, para criar agentes sem problemas.

#### Acceptance Criteria

1. WHEN cliente seleciona template THEN sistema SHALL preencher personalidade e campos padrão
2. WHEN cliente ajusta sliders de tom THEN sistema SHALL atualizar preview conversação em tempo real
3. WHEN cliente adiciona campos customizados THEN sistema SHALL permitir reordenação via drag-and-drop
4. WHEN cliente configura integrações THEN sistema SHALL mostrar status correto (✅ Configurado / ⚠️ Não Configurado)
5. WHEN cliente testa no sandbox THEN sistema SHALL usar WizardAgent real com LangGraph
6. WHEN cliente publica agente THEN sistema SHALL gerar slug, URL pública, embed code e QR code
7. WHEN cliente fecha wizard e reabre THEN sistema SHALL carregar progresso salvo automaticamente

---

### Requirement 4: Validação Funcional das Integrações (Sprint 07A)

**User Story:** Como cliente, quero validar que integrações (WhatsApp, Email, Database) funcionam corretamente, para usar em meus agentes.

#### Acceptance Criteria

1. WHEN cliente configura Uazapi THEN sistema SHALL testar conexão e criptografar credenciais
2. WHEN cliente configura SMTP THEN sistema SHALL enviar email teste e validar recebimento
3. WHEN cliente configura Supabase cliente THEN sistema SHALL executar SELECT 1 e validar conexão
4. WHEN cliente cria trigger THEN sistema SHALL salvar no banco e permitir toggle ativar/desativar
5. WHEN trigger dispara THEN sistema SHALL executar via Celery e logar em trigger_executions
6. WHEN mensagem WhatsApp enviada THEN sistema SHALL enfileirar no Redis e processar via Celery

---

### Requirement 5: Análise de Bugs Pendentes

**User Story:** Como desenvolvedor, quero analisar bugs pendentes de todos os sprints, para priorizar correções.

#### Acceptance Criteria

1. WHEN bugs revisados THEN sistema SHALL classificar CRITICAL, HIGH, MEDIUM, LOW
2. WHEN bugs classificados THEN sistema SHALL identificar dependências
3. WHEN bugs analisados THEN sistema SHALL estimar esforço correção
4. WHEN análise concluída THEN sistema SHALL gerar lista priorizada
5. WHEN bugs bloqueadores identificados THEN sistema SHALL marcar MUST FIX

---

### Requirement 6: Identificação de Gaps

**User Story:** Como desenvolvedor, quero identificar funcionalidades faltantes, para planejar implementação.

#### Acceptance Criteria

1. WHEN componentes auditados THEN sistema SHALL listar funcionalidades parciais
2. WHEN funcionalidades analisadas THEN sistema SHALL identificar dependências faltantes
3. WHEN gaps identificados THEN sistema SHALL classificar ESSENTIAL, IMPORTANT, NICE_TO_HAVE
4. WHEN documentação revisada THEN sistema SHALL identificar docs faltantes/desatualizadas
5. WHEN gaps mapeados THEN sistema SHALL estimar esforço implementação

---

### Requirement 7: Definição de MVP Atualizado

**User Story:** Como product owner, quero definir MVP atualizado incluindo Wizard e Integrações, para priorizar funcionalidades essenciais.

#### Acceptance Criteria

1. WHEN MVP definido THEN sistema SHALL incluir: Auth, CRUD, WebSocket, Multi-Agent, Wizard, Integrações
2. WHEN MVP validado THEN sistema SHALL garantir funcionalidades MVP sem bugs críticos
3. WHEN MVP documentado THEN sistema SHALL listar claramente incluído vs excluído (Google Workspace, Chatwoot = POST-MVP)
4. WHEN bugs priorizados THEN sistema SHALL incluir apenas correções críticas no MVP
5. WHEN MVP completo THEN sistema SHALL ser viável para operação básica

---

### Requirement 8: Criação de Roadmap Priorizado

**User Story:** Como desenvolvedor, quero roadmap priorizado, para planejar Sprints 07B e seguintes.

#### Acceptance Criteria

1. WHEN roadmap criado THEN sistema SHALL organizar por sprint (07B, 08, 09+)
2. WHEN tarefas priorizadas THEN sistema SHALL considerar valor negócio e esforço técnico
3. WHEN dependências mapeadas THEN sistema SHALL ordenar respeitando dependências
4. WHEN roadmap validado THEN sistema SHALL garantir Sprint 07B tem escopo realista (4-6h deploy)
5. WHEN roadmap apresentado THEN sistema SHALL incluir estimativas tempo e recursos

---

### Requirement 9: Relatório Executivo

**User Story:** Como stakeholder, quero relatório executivo conciso, para entender status e próximos passos.

#### Acceptance Criteria

1. WHEN relatório gerado THEN sistema SHALL incluir % funcional atual
2. WHEN relatório criado THEN sistema SHALL listar conquistas Sprints 01-07A
3. WHEN relatório compilado THEN sistema SHALL destacar bugs críticos corrigidos
4. WHEN relatório finalizado THEN sistema SHALL apresentar roadmap resumido
5. WHEN relatório apresentado THEN sistema SHALL incluir recomendações claras Sprint 07B
