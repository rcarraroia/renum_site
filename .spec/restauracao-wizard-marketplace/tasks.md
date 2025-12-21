# Tarefas: Restauração do Wizard e Marketplace

## 🛠️ Checklist de Execução

### Fase 0: Resgate Técnico
- [x] [x] Consolidar arquivos não commitados (Commit de Resgate)
- [x] [x] Identificar migrações pendentes no disco (015_add_template_fields.sql)

### Fase 1: Sincronização de Ambiente
- [x] [x] Aplicar migração 015 no Supabase (via MCP)
- [x] [x] Rebuild do container Backend (`docker compose build --no-cache`)

### Fase 2: Frontend (Real Data)
- [x] [x] Atualizar `src/pages/wizard/Step1Project.tsx`: Integrar com `apiClient` para buscar clientes e projetos reais.
- [x] [x] Remover todas as referências a `mockObjects` deste arquivo.
- [x] [x] Lidar com o estado "Nenhum/Template" no dropdown.

### Fase 3: Frontend (Resiliência)
- [x] [x] Corrigir `src/components/agents/AgentCard.tsx`: Blindar os campos que causam o `TypeError`.
- [x] [x] Adicionado tratamento visual para Agentes-Template (sem cliente).

### Fase 4: Validação
- [x] [x] Criar um agente como "Admin" sem selecionar cliente.
- [x] [x] Validar no banco se o registro foi criado com `is_template: true`.
- [x] [x] Testar a listagem de agentes após a criação.

---
**Legenda:**
- `[ ] [ ]`: Aguardando aprovação
- `[x] [ ]`: Em execução
- `[x] [x]`: Concluído e Validado
