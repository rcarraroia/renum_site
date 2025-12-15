# Sprint 06 - Database Migrations

## Overview

This directory contains all database migrations for Sprint 06 - Wizard de Criação de Agentes.

## Migrations

### 006: Add Wizard Fields to sub_agents
**File:** `006_add_wizard_fields_to_sub_agents.sql`  
**Executed:** ✅ Yes  
**Purpose:** Add wizard-specific fields to sub_agents table

**Changes:**
- Added `client_id` column (UUID, FK → clients)
- Added `template_type` column (VARCHAR(50) with CHECK constraint)
- Added `status` column (VARCHAR(20) with CHECK constraint)
- Created indexes for performance
- Updated RLS policies for multi-tenant security

**Rollback:** See rollback section in migration file

---

### 006b: Add config Column
**File:** `006b_add_config_column.sql`  
**Executed:** ✅ Yes  
**Purpose:** Add JSONB config column for wizard session data

**Changes:**
- Added `config` column (JSONB, default '{}')
- Created GIN index for JSONB queries

**Why Needed:** Original migration 006 didn't include this column, but wizard_service requires it to store wizard session data.

---

### 006c: Add channel Column to messages
**File:** `006c_add_channel_to_messages.sql`  
**Executed:** ✅ Yes  
**Purpose:** Add channel column to messages table for sandbox messaging

**Changes:**
- Added `channel` column (TEXT, nullable)

**Why Needed:** Sandbox service needs to track which channel messages came from (Web, WhatsApp, Email, API).

---

## Execution Scripts

### execute_migration_006.py
Executes migration 006 (wizard fields).

**Usage:**
```bash
cd backend
python execute_migration_006.py
```

### execute_migration_006b.py
Executes migration 006b (config column).

**Usage:**
```bash
cd backend
python execute_migration_006b.py
```

### execute_migration_006c.py
Executes migration 006c (channel column).

**Usage:**
```bash
cd backend
python execute_migration_006c.py
```

---

## Verification Scripts

### check_constraints.py
Checks CHECK constraints on conversations table.

**Usage:**
```bash
cd backend
python check_constraints.py
```

### check_messages_schema.py
Displays full schema of messages table.

**Usage:**
```bash
cd backend
python check_messages_schema.py
```

### check_messages_constraints.py
Checks CHECK constraints on messages table.

**Usage:**
```bash
cd backend
python check_messages_constraints.py
```

### check_messages_tables.py
Lists all messages tables across schemas and shows current schema.

**Usage:**
```bash
cd backend
python check_messages_tables.py
```

---

## Important Notes

### CHECK Constraints

**conversations table:**
- `channel`: Must be 'WhatsApp', 'Web', 'Email', or 'API' (case-sensitive!)
- `status`: Must be 'Nova', 'Em Andamento', 'Resolvida', 'Fechada', or 'Pendente'
- `priority`: Must be 'Low', 'Medium', or 'High'

**messages table:**
- `sender`: Must be 'client', 'renus', 'admin', or 'system'

**sub_agents table:**
- `channel`: Must be 'site' or 'whatsapp'
- `template_type`: Must be 'customer_service', 'sales', 'support', 'recruitment', or 'custom'
- `status`: Must be 'draft', 'active', 'paused', or 'inactive'

### Supabase Cache Issues

When adding new columns, Supabase PostgREST may cache the old schema. Solutions:

1. **Restart backend:** Clears local cache
2. **Use direct SQL:** Bypass Supabase client (psycopg2)
3. **Wait:** Cache refreshes automatically after ~5 minutes

### RLS Policies

All tables have Row Level Security enabled:
- Admins have full access
- Clients can only access their own data
- Public agents are viewable by anonymous users

---

## Rollback Procedures

### Rollback 006
```sql
DROP POLICY IF EXISTS "Admins have full access to sub_agents" ON sub_agents;
DROP POLICY IF EXISTS "Clients can view own agents" ON sub_agents;
DROP POLICY IF EXISTS "Clients can create own agents" ON sub_agents;
DROP POLICY IF EXISTS "Clients can update own agents" ON sub_agents;
DROP POLICY IF EXISTS "Clients can delete own agents" ON sub_agents;
DROP POLICY IF EXISTS "Public agents are viewable" ON sub_agents;

DROP INDEX IF EXISTS idx_sub_agents_client_id;
DROP INDEX IF EXISTS idx_sub_agents_status;
DROP INDEX IF EXISTS idx_sub_agents_template_type;
DROP INDEX IF EXISTS idx_sub_agents_slug;
DROP INDEX IF EXISTS idx_sub_agents_client_status;

ALTER TABLE sub_agents DROP COLUMN IF EXISTS client_id;
ALTER TABLE sub_agents DROP COLUMN IF EXISTS template_type;
ALTER TABLE sub_agents DROP COLUMN IF EXISTS status;
```

### Rollback 006b
```sql
DROP INDEX IF EXISTS idx_sub_agents_config;
ALTER TABLE sub_agents DROP COLUMN IF EXISTS config;
```

### Rollback 006c
```sql
ALTER TABLE messages DROP COLUMN IF EXISTS channel;
```

---

## Testing

After running migrations, verify with:

```bash
cd backend
python test_wizard_api_direct.py
```

Expected result: **15/15 tests passing (100%)**

---

**Last Updated:** 2025-12-04  
**Sprint:** 06 - Wizard de Criação de Agentes  
**Status:** ✅ All migrations executed successfully
