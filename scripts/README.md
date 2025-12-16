# 🔧 Scripts de Desenvolvimento RENUM

Esta pasta contém scripts de teste, validação, backup e análise utilizados durante o desenvolvimento.

## 📂 Estrutura

```
scripts/
├── backups/          # Arquivos JSON de backup
├── test_*.py         # Scripts de teste de funcionalidades
├── validate_*.py     # Scripts de validação
├── check_*.py        # Scripts de verificação
├── verify_*.py       # Scripts de verificação de estado
└── README.md         # Este arquivo
```

---

## 🐍 Scripts Python

### Testes de Funcionalidade
- `test_agents_api.py` - Testa API de agentes
- `test_auth_token.py` - Testa autenticação/tokens
- `test_backend_connection.py` - Testa conexão backend
- `test_backend_fixed.py` - Testa correções backend
- `test_cors.py` / `test_cors_real.py` - Testa configuração CORS
- `test_new_token.py` - Testa novos tokens
- `test_sicc_integration.py` - Testa integração SICC

### Validações
- `validate_agent_improvements.py` - Valida melhorias em agentes
- `validate_agent_tabs.py` - Valida abas de agentes
- `validate_chat_functionality.py` - Valida funcionalidade chat
- `validate_fase1_automatic.py` - Validação automática Fase 1
- `validate_frontend_fix.py` - Valida correções frontend
- `validate_isa_real_functionality.py` - Valida ISA real
- `validate_preview_chat_locations.py` - Valida localizações preview
- `validate_preview_chat_removal.py` - Valida remoção preview
- `validate_sicc_frontend.py` - Valida SICC frontend
- `validate_sicc_frontend_mocks.py` - Valida mocks SICC
- `validate_sicc_integration_final.py` - Validação final SICC
- `validate_sprint_10_sicc.py` - Valida Sprint 10 SICC
- `validate_system_integration.py` - Valida integração sistema

### Verificações
- `check_agents.py` - Verifica agentes
- `check_agents_structure.py` - Verifica estrutura agentes
- `check_agents_v2.py` - Verifica agentes v2
- `check_database_agents.py` - Verifica agentes no DB
- `check_system_agents_db_real.py` - Verifica sistema real
- `verify_agent_service.py` - Verifica serviço agentes
- `verify_database_state.py` - Verifica estado DB
- `verify_isa_real.py` - Verifica ISA real
- `verify_renus_real.py` - Verifica Renus real

### Análises
- `analyze_renus_isa_modules.py` - Analisa módulos Renus/ISA
- `debug_chat_renus.py` - Debug chat Renus
- `find_renus_slug.py` - Encontra slug Renus
- `inspect_agents.py` - Inspeciona agentes
- `list_clients.py` - Lista clientes

### Backup e Migração
- `backup_agents_conflict.py` - Backup conflitos agentes
- `backup_data.py` - Backup dados gerais
- `restore_test.py` - Teste de restore
- `apply_migration.py` - Aplica migrações
- `clean_and_migrate.py` - Limpa e migra
- `create_test_agent.py` - Cria agente de teste

### Database
- `audit_database.py` - Audita banco de dados
- `audit_db_real.py` - Audita DB real
- `check_users.sql` - Verifica usuários (SQL)

---

## 🟦 Scripts PowerShell

- `START_SERVER_AQUI.ps1` - Inicia servidor local
- `test_backend_startup.ps1` - Testa startup backend

---

## 🌐 Scripts JavaScript/HTML

- `apply_fix_now.js` - Aplica correção imediata
- `fix_auth_frontend.html` - Corrige autenticação frontend
- `validate_task_41.html` - Valida tarefa 41
- `validate_tasks_42_43.html` - Valida tarefas 42 e 43

---

## 💾 Pasta backups/

Contém arquivos JSON de backup:
- `audit_database_results.json` - Resultados auditoria DB
- `audit_db_final.json` - Auditoria DB final
- `backup_agents_conflict_*.json` - Backups conflitos
- `backup_isa_commands_*.json` - Backup comandos ISA
- `backup_renus_config_*.json` - Backup config Renus
- `backup_sub_agents_*.json` - Backup sub-agentes

---

## 🚀 Como Usar

### Executar Testes
```bash
# Python
python scripts/test_agents_api.py

# PowerShell
.\scripts\START_SERVER_AQUI.ps1
```

### Validar Funcionalidades
```bash
python scripts/validate_system_integration.py
```

### Fazer Backup
```bash
python scripts/backup_data.py
```

---

**Nota:** Scripts são usados para desenvolvimento/debugging. Produção usa Docker.

**Última Atualização:** 2025-12-16
