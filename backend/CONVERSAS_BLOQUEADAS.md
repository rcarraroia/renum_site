# ⚠️ CONVERSAS - BLOQUEADO

## Problema Identificado

A tabela `conversations` no Supabase tem um **constraint inválido** no campo `channel` que impede a criação de novas conversas.

### Erro:
```
new row for relation "conversations" violates check constraint "conversations_channel_check"
```

### Tentativas:
- ❌ channel="web" - Rejeitado
- ❌ channel="whatsapp" - Rejeitado  
- ❌ channel="email" - Não testado

### Ação Necessária:

1. **Verificar constraint no Supabase:**
   ```sql
   SELECT conname, pg_get_constraintdef(oid) 
   FROM pg_constraint 
   WHERE conrelid = 'conversations'::regclass 
   AND conname = 'conversations_channel_check';
   ```

2. **Corrigir ou remover constraint:**
   ```sql
   -- Opção 1: Remover constraint
   ALTER TABLE conversations DROP CONSTRAINT conversations_channel_check;
   
   -- Opção 2: Recriar com valores corretos
   ALTER TABLE conversations DROP CONSTRAINT conversations_channel_check;
   ALTER TABLE conversations ADD CONSTRAINT conversations_channel_check 
   CHECK (channel IN ('whatsapp', 'email', 'web'));
   ```

### Status das Tasks:

- Task 19-26: **BLOQUEADAS** até correção do banco
- Backend models: ✅ Corretos
- Backend service: ✅ Funcional (mas não pode criar devido ao constraint)
- Testes: ❌ Falhando devido ao constraint

### Data: 2025-12-06
### Responsável: Aguardando correção no Supabase
