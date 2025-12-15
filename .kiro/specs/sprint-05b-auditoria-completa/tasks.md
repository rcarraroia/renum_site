# Implementation Plan - Sprint 05B: Auditoria Completa

## FASE 1: VALIDAÇÃO FUNCIONAL (1.5h)

- [x] 1. Validar WebSocket funcionalidade



  - Criar script teste WebSocket com cliente real
  - Testar conexão com token válido (status 101)
  - Testar conexão sem token (rejeição 401/403)
  - Testar troca mensagens
  - Testar múltiplos clientes simultâneos
  - Documentar resultados
  - _Requirements: 1.1-1.5_

- [x] 2. Validar Frontend no navegador



  - Iniciar frontend (npm run dev)
  - Abrir navegador http://localhost:5173
  - Testar carregamento (console sem erros)
  - Testar login (auth + redirect)
  - Testar navegação (Clientes, Leads, Projetos)
  - Testar carregamento dados backend
  - Testar CRUD (criar, editar, deletar)
  - Capturar screenshots
  - Documentar resultados
  - _Requirements: 2.1-2.5_

- [x] 3. Validar Wizard de Criação de Agentes
  - **Step 1: Objetivo**
    - Selecionar cada template (Customer Service, Sales, Support, Recruitment, Custom)
    - Verificar preview slug gera corretamente
    - Validar campos obrigatórios
  - **Step 2: Personalidade**
    - Selecionar personalidades (Professional, Friendly, Technical, Casual)
    - Ajustar sliders tom
    - Verificar preview conversação atualiza
  - **Step 3: Campos**
    - Habilitar/desabilitar campos standard
    - Adicionar campos customizados
    - Testar drag-and-drop reordenação
    - Verificar preview fluxo conversa
  - **Step 4: Integrações**
    - Verificar status integrações
    - Testar checkboxes habilitar/desabilitar
    - Validar botão "Configurar Agora"
  - **Step 5: Teste e Publicação**
    - Iniciar sandbox
    - Enviar mensagens e receber respostas
    - Verificar coleta dados estruturados
    - Testar publicação
    - Validar geração: slug, URL, embed, QR
  - **Auto-save**
    - Avançar entre steps
    - Fechar e reabrir (carregar progresso)
    - Verificar indicador "Salvando.../Salvo"
  - **Dashboard Agentes**
    - Listar agentes
    - Filtrar por template_type e status
    - Testar ações: Clone, Pause, Delete
    - Verificar métricas
  - Documentar resultados
  - _Requirements: 3.1-3.7_

- [x] 4. Validar WizardAgent (LangGraph)
  - Executar: `python backend/test_wizard_agent.py`
  - Verificar processamento mensagens
  - Validar coleta dados estruturados
  - Verificar isolamento (sandbox)
  - Validar personalidade configurada
  - Documentar resultados
  - _Requirements: 3.5_

- [x] 5. Validar Integrações Core
  - **WhatsApp (Uazapi)**
    - Configurar credenciais
    - Clicar "Testar e Salvar"
    - Verificar status "✅ Configurado"
    - Validar criptografia banco
  - **Email (SMTP)**
    - Configurar SMTP
    - Enviar email teste
    - Verificar recebimento
    - Validar status "✅ Configurado"
  - **Database (Supabase Cliente)**
    - Configurar credenciais
    - Testar conexão (SELECT 1)
    - Verificar status "✅ Configurado"
  - **Endpoint Status**
    - Chamar GET /api/integrations/status
    - Verificar retorno correto
    - Validar filtro client_id (RLS)
  - Documentar resultados
  - _Requirements: 4.1-4.4_

- [x] 6. Validar Sistema de Triggers
  - **Criação Trigger**
    - Criar trigger: QUANDO → SE → ENTÃO
    - Salvar e verificar banco
  - **Execução Trigger**
    - Simular condição
    - Verificar execução Celery
    - Validar ação executada
    - Checar log trigger_executions
  - **Toggle Trigger**
    - Desativar (toggle off)
    - Verificar não executa
    - Reativar e validar funciona
  - **Delete Trigger**
    - Deletar trigger
    - Verificar remoção banco
  - Documentar resultados
  - _Requirements: 4.5_

- [x] 7. Validar Celery + Redis
  - **Celery Worker**
    - SSH VPS: `ssh root@72.60.151.78`
    - Status: `systemctl status renum-celery`
    - Logs: `journalctl -u renum-celery -f`
  - **Redis**
    - Status: `systemctl status redis`
    - Conectar: `redis-cli ping`
  - **Fila Mensagens**
    - Enviar mensagem WhatsApp via API
    - Verificar enfileiramento Redis
    - Validar processamento Celery
    - Checar logs
  - **Scheduler Triggers**
    - Verificar Celery Beat rodando
    - Validar execução cada 1 min
    - Checar logs avaliação triggers
  - Documentar resultados
  - _Requirements: 4.6_

- [x] 8. Validar Fluxo E2E Completo
  - **Criar agente completo**
    - Preencher 5 etapas wizard
    - Configurar integrações
    - Publicar agente
  - **Testar agente publicado**
    - Acessar URL pública
    - Enviar mensagem
    - Verificar resposta
    - Validar coleta dados
  - **Testar notificações**
    - Verificar cliente recebe (WhatsApp/Email)
    - Validar conteúdo notificação
  - **Testar trigger automático**
    - Criar trigger follow-up
    - Simular inatividade
    - Verificar envio automático
  - Documentar resultados
  - _Requirements: 3.1-3.7, 4.1-4.6_

- [x] 9. Consolidar resultados validação funcional
  - Compilar todos resultados testes
  - Calcular % sucesso por componente
  - Identificar novos bugs
  - Gerar relatório parcial Fase 1
  - _Requirements: 1.1-1.5, 2.1-2.5, 3.1-3.7, 4.1-4.6_

## FASE 2: ANÁLISE DE GAPS (1h)

- [x] 10. Revisar bugs pendentes Sprint 05A
  - Ler: `docs/sprint-05a-validacao-completa/BUGS_ENCONTRADOS_SPRINT05A.md`
  - Listar bugs pendentes
  - Classificar severidade
  - Estimar esforço correção
  - Identificar dependências
  - _Requirements: 5.1-5.5_

- [x] 11. Revisar bugs conhecidos Sprint 06
  - Ler: `sprint-06-wizard-criacao-agentes/KNOWN_ISSUES.md`
  - Verificar bug crítico (messages.channel) corrigido
  - Validar 42 tasks obrigatórias concluídas
  - Listar property tests opcionais (9 tests)
  - Decidir implementar agora ou depois
  - _Requirements: 5.1-5.5_

- [x] 12. Revisar bugs conhecidos Sprint 07A
  - Ler: `sprint-07a-integracoes-core/KNOWN_ISSUES.md` (se existir)
  - Verificar status correções aplicadas
  - Listar bugs pendentes
  - Priorizar críticos vs melhorias
  - _Requirements: 5.1-5.5_

- [x] 13. Identificar funcionalidades incompletas
  - Revisar: Backend, Frontend, Agentes, WebSocket, Wizard, Integrações
  - Listar funcionalidades parciais
  - Identificar dependências faltantes
  - Classificar: ESSENTIAL, IMPORTANT, NICE_TO_HAVE
  - Estimar esforço implementação
  - _Requirements: 6.1-6.5_

- [x] 14. Mapear documentação faltante
  - Revisar docs/
  - Identificar gaps documentação
  - Listar docs desatualizadas
  - Priorizar crítica vs nice-to-have
  - _Requirements: 6.4_

- [x] 15. Consolidar análise de gaps
  - Compilar bugs + gaps + docs
  - Calcular total esforço estimado
  - Gerar relatório parcial Fase 2
  - _Requirements: 5.1-5.5, 6.1-6.5_

## FASE 3: PRIORIZAÇÃO E ROADMAP (1h)

- [x] 16. Classificar bugs e gaps por prioridade
  - Para cada bug: MUST FIX vs CAN WAIT
  - Para cada gap: MVP vs POST_MVP
  - Considerar valor negócio vs esforço
  - Criar matriz priorização
  - _Requirements: 5.5, 7.1-7.2_

- [x] 17. Definir MVP mínimo atualizado
  - **MVP DEVE incluir:**
    - ✅ Auth + CRUD + WebSocket + Multi-Agent (Sprints 01-04)
    - ✅ Wizard completo (Sprint 06)
    - ✅ Integrações (WhatsApp, Email, Database, Triggers) (Sprint 07A)
  - **POST-MVP:**
    - ❌ Google Workspace
    - ❌ Chatwoot
    - ❌ Sub-agentes especializados
    - ❌ Analytics avançado
  - Validar funcionalidades MVP sem bugs críticos
  - Documentar escopo MVP
  - _Requirements: 7.1-7.5_

- [x] 18. Criar roadmap Sprint 07B (Deploy)
  - Listar tarefas: Deploy backend VPS, Celery produção, Nginx, SSL, Monitoring
  - Ordenar respeitando dependências
  - Estimar capacidade: 4-6h
  - Validar escopo realista
  - Documentar Sprint 07B
  - _Requirements: 8.1-8.5_

- [x] 19. Criar roadmap Sprints 08 e 09+
  - **Sprint 08 (1-2 sem):** Bugs encontrados 05B + Performance + Docs + Testes E2E
  - **Sprint 09 (1-2 sem):** Google Workspace + Chatwoot + SMS/Telegram
  - **Sprint 10+ (futuro):** Sub-agentes + Analytics + Fine-tuning + Marketplace
  - Estimar esforço total
  - Documentar roadmap longo prazo
  - _Requirements: 8.1-8.5_

- [x] 20. Consolidar roadmap completo
  - Compilar: Sprint 07B + 08 + 09+
  - Validar ordenação e dependências
  - Calcular estimativas totais
  - Gerar relatório parcial Fase 3
  - _Requirements: 8.1-8.5_

## FASE 4: RELATÓRIO EXECUTIVO (0.5h)

- [x] 21. Compilar status atual do sistema
  - Calcular % funcional (baseado Sprint 05A + Fase 1)
  - Listar componentes funcionais vs não-funcionais
  - Resumir métricas (bugs corrigidos, testes passando)
  - _Requirements: 9.1_

- [x] 22. Destacar conquistas Sprints 01-07A
  - Listar bugs críticos corrigidos
  - Destacar melhorias estabilidade
  - Resumir validações realizadas
  - Destacar: Wizard completo + Integrações completas
  - _Requirements: 9.2, 9.3_

- [x] 23. Apresentar roadmap resumido
  - Resumir Sprint 07B (deploy: 4-6h)
  - Resumir Sprints 08-09 (visão geral)
  - Destacar marcos importantes
  - _Requirements: 9.4_

- [x] 24. Criar recomendações Sprint 07B
  - Recomendar prioridades (deploy primeiro)
  - Recomendar abordagem (produção antes features)
  - Recomendar recursos (tempo, ferramentas)
  - Recomendar riscos mitigar
  - _Requirements: 9.5_

- [x] 25. Gerar relatório executivo final
  - Compilar seções em documento único
  - Formatar clareza e concisão
  - Incluir sumário executivo (1 página)
  - Incluir detalhes técnicos (apêndices)
  - Salvar: `docs/sprint-05b-auditoria-completa/RELATORIO_EXECUTIVO.md`
  - _Requirements: 9.1-9.5_

- [x] 26. Apresentar ao usuário e obter aprovação
  - Apresentar relatório executivo
  - Explicar conclusões
  - Responder perguntas
  - Obter aprovação iniciar Sprint 07B
  - _Requirements: 9.1-9.5_

---

## 📊 RESUMO DO SPRINT 05B

### Tempo Estimado
- Fase 1 (Validação): 1.5h
- Fase 2 (Análise): 1h
- Fase 3 (Roadmap): 1h
- Fase 4 (Relatório): 0.5h
- **Total: 4h**

### Entregas
1. ✅ Validação funcional: WebSocket, Frontend, Wizard, Integrações, E2E
2. ✅ Análise bugs: Sprint 05A + 06 + 07A
3. ✅ Identificação gaps e funcionalidades faltantes
4. ✅ MVP atualizado (incluindo Wizard + Integrações)
5. ✅ Roadmap priorizado (Sprint 07B: Deploy, 08: Bugs, 09: Google/Chatwoot)
6. ✅ Relatório executivo completo

### Decisão Final
Após Sprint 05B:
- ✅ Iniciar Sprint 07B (Deploy VPS)
- ⏳ Correções adicionais (se gaps críticos)

---

**Spec criada em:** 05/12/2025  
**Responsável:** Kiro  
**Status:** ✅ COMPLETO
