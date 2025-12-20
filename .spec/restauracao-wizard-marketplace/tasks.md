# Tarefas: Restauração do Wizard e Marketplace

## 🛠️ Checklist de Execução

### Fase 1: Backend (Agnóstico)
- [ ] [ ] Modificar `backend/src/models/wizard.py`: Permitir `client_id` opcional no modelo `WizardSessionCreate`.
- [ ] [ ] Modificar `backend/src/services/wizard_service.py`: Ajustar `start_wizard` para lidar com ausência de `client_id`.
- [ ] [ ] Verificar no Supabase se `agents.client_id` permite valores nulos.

### Fase 2: Frontend (Real Data)
- [ ] [ ] Atualizar `src/pages/wizard/Step1Project.tsx`: Integrar com `apiClient` para buscar clientes e projetos reais.
- [ ] [ ] Remover todas as referências a `mockObjects` deste arquivo.
- [ ] [ ] Lidar com o estado "Nenhum/Template" no dropdown.

### Fase 3: Frontend (Resiliência)
- [ ] [ ] Corrigir `src/components/agents/AgentCard.tsx`: Blindar os campos que causam o `TypeError`.
- [ ] [ ] Adicionar tratamento visual para Agentes-Template (sem cliente).

### Fase 4: Validação
- [ ] [ ] Criar um agente como "Admin" sem selecionar cliente.
- [ ] [ ] Validar no banco se o registro foi criado com `is_template: true`.
- [ ] [ ] Testar a listagem de agentes após a criação.

---
**Legenda:**
- `[ ] [ ]`: Aguardando aprovação
- `[x] [ ]`: Em execução
- `[x] [x]`: Concluído e Validado
