# Design: Restauração do Wizard e Marketplace

## 🏗️ Arquitetura Técnica

### 1. Backend: Neutralidade de Client ID
- **Arquivo:** `backend/src/services/wizard_service.py`
- **Mudança:** Alterar o método `start_wizard` para aceitar `client_id: Optional[UUID] = None`.
- **Lógica:** Se `client_id` for nulo, o agente será criado com `is_template = True` e `role = "client_agent"` (mas sem dono).

### 2. Frontend: Consumo de Dados Reais no Step 1
- **Componente:** `src/pages/wizard/Step1Project.tsx`
- **Mudança:** Substituir `mockProjects` e `mockClients` por hooks de `useEffect` que chamam `clientService.listClients()` e `projectService.listProjects()`.
- **Fallback:** Se o usuário for Admin, adicionar uma opção "Nenhum (Criar como Template de Marketplace)".

### 3. Frontend: Proteção de Tipos e Props
- **Componente:** `src/components/agents/AgentCard.tsx`
- **Mudança:** Implementar Optional Chaining (`?.`) e valores padrão para todas as propriedades de `agent`.
- **Diferenciação:** Adicionar um Badge "TEMPLATE" se o agente não tiver um `client_id`.

### 4. Sincronização de Estado
- O `useAgentWizardStore` deve persistir o `wizard_id` no `localStorage` para permitir recuperação de sessão robusta.

## 💾 Alterações no Schema (Supabase)
Nenhuma alteração de schema necessária, apenas flexibilização da restrição de `NOT NULL` na coluna `client_id` da tabela `agents` (se houver).

---
> [!NOTE]
> A integração com o SICC será mantida através do JSON de `config`, garantindo que o comportamento do agente (prompt/personalidade) seja salvo independente de quem é o dono.
