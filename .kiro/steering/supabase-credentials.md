# 🔐 Credenciais Supabase - RENUM

⚠️ **ARQUIVO CONFIDENCIAL - NÃO COMMITAR NO GIT**

---

## Credenciais do Projeto

### Informações Básicas

**Nome do Projeto:**
```
Renum_Site
```

**URL do Projeto:**
```
https://vhixvzaxswphwoymdhgg.supabase.co
```

**Project Reference:**
```
vhixvzaxswphwoymdhgg
```

**Region:**
```
us-east-1 (ou conforme configurado)
```

---

## Chaves de API

### Anon Key (Pública)
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4NTc2NTMsImV4cCI6MjA3OTQzMzY1M30.E8YARatueM44zcA8lgQBd4hi2J1P3rA3EyvH5d4Wa-4
```

**Uso:** Frontend, respeita RLS

### Service Role Key (Privada)
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw
```

**Uso:** Backend apenas, bypassa RLS

⚠️ **NUNCA expor esta chave no frontend ou em logs públicos!**

### Legacy JWT Secret
```
39864Ub2rWjFWbDUvMrbQfu4lmHe9Fiv/auohpenbEx0CTYl+Gb7flinlEIdgc9xLgfhL9BUZqCjRjs7s3yhHg==
```

**Uso:** Geração de tokens JWT customizados (se necessário)

---

## Credenciais de Acesso ao Dashboard

**Email:**
```
[seu-email@exemplo.com]
```

**Senha:**
```
[SUA-SENHA-SEGURA]
```

**2FA Habilitado:** [SIM/NÃO]

**Dashboard URL:**
```
https://supabase.com/dashboard/project/vhixvzaxswphwoymdhgg
```

---

## Credenciais de Conexão Direta (PostgreSQL)

### Senha do Banco de Dados
```
BD5yEMQ9iDMOkeGW
```

### Connection String

```
postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres
```

### Detalhes da Conexão

**Host:**
```
db.vhixvzaxswphwoymdhgg.supabase.co
```

**Port:**
```
5432
```

**Database:**
```
postgres
```

**User:**
```
postgres
```

**Password:**
```
BD5yEMQ9iDMOkeGW
```

---

## Variáveis de Ambiente (.env)

```bash
# Supabase
SUPABASE_URL=https://vhixvzaxswphwoymdhgg.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4NTc2NTMsImV4cCI6MjA3OTQzMzY1M30.E8YARatueM44zcA8lgQBd4hi2J1P3rA3EyvH5d4Wa-4
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw

# Conexão Direta (opcional)
DATABASE_URL=postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres

# JWT Secret (se necessário)
JWT_SECRET=39864Ub2rWjFWbDUvMrbQfu4lmHe9Fiv/auohpenbEx0CTYl+Gb7flinlEIdgc9xLgfhL9BUZqCjRjs7s3yhHg==
```

---

## Notas de Segurança

1. ✅ Este arquivo está no `.gitignore`
2. ✅ Nunca compartilhar em canais públicos
3. ✅ Rotacionar chaves periodicamente
4. ✅ Usar variáveis de ambiente em produção
5. ✅ Habilitar 2FA na conta Supabase

---

## Histórico de Rotação de Chaves

| Data | Tipo | Motivo | Responsável |
|------|------|--------|-------------|
| YYYY-MM-DD | Service Key | Rotação programada | [Nome] |
| YYYY-MM-DD | Anon Key | Exposição acidental | [Nome] |

---

**Última atualização:** 2025-11-25  
**Responsável:** Equipe RENUM
