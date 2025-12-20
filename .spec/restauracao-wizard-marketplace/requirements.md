# Requisitos: Restauração do Wizard e Marketplace

## 📌 Visão Geral
Restaurar a funcionalidade do Wizard de Agentes para que ele seja 100% funcional, baseado em dados reais (e não mocks) e que suporte a criação de **Templates do Marketplace** pelo Admin sem a obrigatoriedade de vincular a um Cliente ou Projeto específico.

## 🎯 Objetivos
1. **Wizard Agnóstico (Marketplace):** Permitir que o Admin inicie e conclua o Wizard definindo um Agente como `is_template: true` sem exigir `client_id` ou `project_id`.
2. **Eliminação de Mocks:** Substituir todos os dados estáticos (`mockProjects`, `mockClients`) por chamadas reais aos serviços `clientService` e `projectService`.
3. **Resiliência de UI (TypeError):** Garantir que a listagem de agentes (`AgentCard`) não quebre quando receber dados parciais ou nulos de relações (cliente/projeto).
4. **Persistência Real:** Garantir que todos os 6 passos do Wizard salvem o progresso no backend (`wizard_sessions` / tabela `agents` em modo `draft`).

## 📏 Regras de Negócio
- **Admin:** Pode criar agendes COM ou SEM cliente. Se sem cliente, o agente é marcado como Template.
- **Cliente B2B:** Cria agentes vinculado obrigatoriamente à sua conta.
- **Wizard Step 1:** Deve listar Clientes e Projetos Reais do banco de dados via API.
- **Marketplace:** Um template concluído deve ser visível na galeria do marketplace para outros clientes.

## ✅ Critérios de Aceite
- [ ] O Admin consegue terminar o Wizard sem selecionar um cliente.
- [ ] O `AgentCard` renderiza normalmente mesmo que `agent.client` seja nulo.
- [ ] Nenhuma variável `mock` é utilizada no fluxo de criação iniciado por `/dashboard/admin/agents/create`.
- [ ] O progresso é recuperado ao recarregar a página (via `wizard_id` na URL).
