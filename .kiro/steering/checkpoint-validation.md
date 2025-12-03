# ✅ Regra de Validação de Checkpoints

## Princípio Fundamental

**NUNCA marque um checkpoint como completo sem VALIDAÇÃO REAL.**

---

## 🔴 Problema Identificado

Durante a auditoria do sistema (02/12/2025), descobrimos que:

- Sprint 03 foi marcado como **COMPLETO** ✅
- Checkpoint final (Task 28) foi marcado como **COMPLETO** ✅
- **MAS:** WebSocket não funcionava (erro 403)
- **MAS:** Bug de configuração (`JWT_SECRET` vs `SECRET_KEY`) passou despercebido
- **MAS:** Nenhum teste automatizado validou a funcionalidade real

**Resultado:** Sistema marcado como pronto, mas não funcionava.

---

## ✅ Solução: Validação Obrigatória

### Antes de Marcar Sprint como Completo:

**1. Executar Testes Automatizados**
```bash
# Backend
pytest tests/ -v

# Frontend
npm test

# E2E
npm run test:e2e
```

**2. Executar Validação Manual dos Requisitos Críticos**

Criar script de validação para cada sprint. Exemplo:

```python
# validate_sprint_03.py
def test_websocket_connection():
    """Valida que WebSocket conecta com token válido"""
    # Tenta conectar
    # Verifica status 101 (Switching Protocols)
    # Envia mensagem
    # Recebe resposta
    assert connection_successful

def test_websocket_authentication():
    """Valida que WebSocket rejeita token inválido"""
    # Tenta conectar sem token
    # Verifica status 401 ou 403
    assert connection_rejected
```

**3. Documentar Resultados**

Criar relatório de validação:
- `VALIDACAO_SPRINT_XX.md`
- Listar todos os requisitos
- Marcar ✅ ou ❌ para cada um
- Evidências (screenshots, logs, comandos executados)

**4. Aprovar com Usuário**

Mostrar ao usuário:
- O que funciona ✅
- O que não funciona ❌
- Decisão: avançar ou corrigir?

---

## 📋 Checklist de Checkpoint

Antes de marcar Task de Checkpoint como completa:

### Backend
- [ ] Todos os endpoints retornam 200/201 (não 500)
- [ ] Testes unitários passam (pytest)
- [ ] Testes de integração passam
- [ ] Logs não mostram erros críticos
- [ ] Servidor inicia sem erros

### Frontend
- [ ] Aplicação carrega sem tela branca
- [ ] Não há erros no console do navegador
- [ ] Dados carregam do backend (não mock)
- [ ] Testes unitários passam (vitest/jest)
- [ ] Build de produção funciona

### Integração
- [ ] Frontend conecta ao backend
- [ ] Autenticação funciona
- [ ] CRUD completo funciona
- [ ] WebSocket conecta (se aplicável)
- [ ] Dados persistem no banco

### E2E
- [ ] Fluxo principal funciona (login → dashboard → ação)
- [ ] Fluxo secundário funciona
- [ ] Erros são tratados graciosamente

---

## 🚨 Se Algum Item Falhar

**NÃO marque checkpoint como completo.**

1. Documente o problema
2. Crie issue/task para correção
3. Informe o usuário
4. Corrija antes de avançar

---

## 📊 Exemplo de Validação Correta

### Sprint 03 - WebSocket (Como DEVERIA ter sido)

**Checkpoint Backend (Task 9):**
```bash
# 1. Iniciar servidor
python -m src.main

# 2. Testar WebSocket
python test_websocket.py

# Resultado esperado:
# ✅ Conecta com token válido
# ✅ Rejeita sem token
# ✅ Envia mensagem
# ✅ Recebe resposta

# Se QUALQUER teste falhar → NÃO marcar como completo
```

**Checkpoint Frontend (Task 28):**
```bash
# 1. Iniciar frontend
npm run dev

# 2. Abrir navegador
# 3. Fazer login
# 4. Abrir conversas
# 5. Enviar mensagem

# Resultado esperado:
# ✅ Página carrega
# ✅ WebSocket conecta (indicador verde)
# ✅ Mensagem envia
# ✅ Mensagem aparece na tela

# Se QUALQUER passo falhar → NÃO marcar como completo
```

---

## 💡 Lição Aprendida

**Checkpoint ≠ "Código escrito"**

**Checkpoint = "Funcionalidade validada e funcionando"**

Marcar checkpoint sem validar é **dívida técnica** que volta como bug crítico depois.

---

## 🎯 Aplicação Imediata

A partir de agora:

1. **Todo checkpoint** deve ter script de validação
2. **Todo sprint** deve ter relatório de validação
3. **Nenhum sprint** avança sem aprovação do usuário baseada em evidências reais

---

**Criado em:** 02/12/2025  
**Motivo:** Auditoria revelou checkpoints marcados sem validação  
**Impacto:** Bugs críticos descobertos tarde demais  
**Solução:** Esta regra obrigatória
