# 🐛 BUG SISTEMÁTICO: UserProfile sendo tratado como Dict

**Severidade:** 🔴 CRÍTICA  
**Descoberto em:** 02/12/2025  
**Impacto:** Múltiplos endpoints retornando erro 500

---

## 📋 DESCRIÇÃO

O middleware `get_current_user()` retorna um objeto `UserProfile` (Pydantic model), mas várias rotas estão tentando acessá-lo usando `.get()` como se fosse um dicionário.

**Código correto:**
```python
current_user.role  # ✅ Correto
current_user.id    # ✅ Correto
```

**Código incorreto (causa erro 500):**
```python
current_user.get("role")  # ❌ Erro: 'UserProfile' object has no attribute 'get'
current_user.get("id")    # ❌ Erro
```

---

## 🔍 ENDPOINTS AFETADOS

### Confirmados com Erro 500:
1. **GET /api/dashboard/stats** - dashboard_service.py
2. **POST /api/isa/chat** - isa.py (linha ~52)

### Potencialmente Afetados (não testados ainda):
- Qualquer rota que use `current_user.get()`
- Verificar todos os arquivos em `src/api/routes/`

---

## 🔧 CORREÇÃO

### Buscar e Substituir em Todos os Arquivos:

```bash
# Buscar padrão incorreto
grep -r "current_user\.get(" backend/src/api/routes/

# Substituir:
current_user.get("role")  →  current_user.role
current_user.get("id")    →  current_user.id
current_user.get("email") →  current_user.email
```

### Arquivos que Precisam Correção:
1. `src/api/routes/isa.py` - linhas 52, 56, 68, 82
2. `src/services/dashboard_service.py` - verificar todas as ocorrências
3. Outros arquivos em `src/api/routes/` - fazer varredura completa

---

## ⚠️ IMPACTO

**Antes da correção:**
- Dashboard não funciona
- ISA não funciona
- Possivelmente outros endpoints quebrados

**Após correção:**
- Todos os endpoints voltam a funcionar
- Tempo estimado de correção: 15-30 minutos

---

## 📝 RECOMENDAÇÃO

1. **Imediato:** Fazer busca global por `current_user.get(` em todos os arquivos
2. **Substituir** todos por acesso direto ao atributo
3. **Testar** todos os endpoints afetados
4. **Adicionar** teste automatizado para prevenir regressão

---

**Status:** Identificado, aguardando correção
