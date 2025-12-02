# Tasks - Sprint 3A: Deploy e Integração

## Overview

Este documento lista todas as tarefas necessárias para completar o Sprint 3A. As tarefas estão organizadas em fases e devem ser executadas na ordem apresentada.

## Phase 1: Backend Local Setup

### TASK-001: Verificar Estado Atual do Backend
**Objective:** Entender o que já existe no backend antes de começar

**Steps:**
1. Conectar ao repositório e navegar para pasta backend/
2. Listar arquivos em backend/src/
3. Verificar quais routers existem em backend/src/api/routes/
4. Verificar quais services existem em backend/src/services/
5. Verificar quais models existem em backend/src/models/
6. Ler requirements.txt e identificar dependências
7. Verificar se .env.example existe

**Acceptance Criteria:**
- [x] Lista completa de arquivos existentes documentada
- [x] Identificado o que está implementado vs o que falta
- [x] Dependências em requirements.txt verificadas

**Estimated Time:** 30 minutes
**Status:** ✅ COMPLETO

---

### TASK-002: Criar Ambiente Virtual Python
**Objective:** Configurar ambiente isolado para o backend

**Steps:**
1. Abrir terminal na pasta backend/
2. Executar: `python -m venv venv`
3. Ativar ambiente: `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Linux/Mac)
4. Verificar Python version: `python --version` (deve ser 3.11+)
5. Atualizar pip: `python -m pip install --upgrade pip`

**Acceptance Criteria:**
- [x] Pasta venv/ criada
- [x] Ambiente virtual ativado
- [x] Python 3.11+ confirmado (3.10.11)
- [x] pip atualizado

**Estimated Time:** 10 minutes
**Status:** ✅ COMPLETO

---

### TASK-003: Instalar Dependências do Backend
**Objective:** Instalar todas as bibliotecas necessárias

**Steps:**
1. Com venv ativado, executar: `pip install -r requirements.txt`
2. Verificar instalação: `pip list`
3. Confirmar que fastapi, uvicorn, supabase, pydantic estão instalados
4. Se houver erros, corrigir e reinstalar

**Acceptance Criteria:**
- [ ] Todas dependências instaladas sem erros
- [ ] `pip list` mostra todas bibliotecas necessárias
- [ ] Nenhum warning crítico

**Estimated Time:** 15 minutes

---

### TASK-004: Configurar Variáveis de Ambiente
**Objective:** Criar arquivo .env com credenciais Supabase

**Steps:**
1. Copiar .env.example para .env: `copy .env.example .env` (Windows) ou `cp .env.example .env` (Linux/Mac)
2. Abrir docs/SUPABASE_CREDENTIALS.md
3. Copiar SUPABASE_URL para .env
4. Copiar SUPABASE_ANON_KEY para .env
5. Copiar SUPABASE_SERVICE_KEY para .env
6. Adicionar CORS_ORIGINS=http://localhost:5173
7. Verificar que .env está no .gitignore

**Acceptance Criteria:**
- [ ] Arquivo .env criado
- [ ] Todas variáveis configuradas
- [ ] .env está no .gitignore
- [ ] Credenciais válidas

**Estimated Time:** 10 minutes

---

### TASK-005: Validar Banco de Dados Supabase
**Objective:** Confirmar que estrutura do banco está correta antes de continuar

**Steps:**
1. Acessar Supabase Dashboard: https://supabase.com/dashboard
2. Fazer login e selecionar projeto RENUM
3. Ir em Table Editor
4. Verificar que tabelas existem: profiles, clients, leads, projects
5. Verificar RLS habilitado (ícone de cadeado nas tabelas)
6. Ir em Authentication → Users
7. Verificar se usuário admin existe (admin@renum.tech ou similar)
8. Ir em SQL Editor e executar query de teste: `SELECT * FROM profiles LIMIT 1;`
9. Verificar estrutura de uma tabela: `SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'clients';`

**Acceptance Criteria:**
- [ ] Todas tabelas necessárias existem (profiles, clients, leads, projects)
- [ ] RLS está habilitado em todas tabelas
- [ ] Usuário admin existe no Authentication
- [ ] Query de teste retorna dados ou executa sem erro
- [ ] Estrutura das tabelas está correta

**Estimated Time:** 15 minutes

---

### TASK-006: Verificar Estrutura do Código Backend
**Objective:** Garantir que estrutura de pastas está correta

**Steps:**
1. Verificar se existe src/main.py
2. Verificar se existe src/config/settings.py
3. Verificar se existe src/api/routes/__init__.py
4. Verificar se existe src/services/
5. Verificar se existe src/models/
6. Verificar se existe src/utils/supabase_client.py
7. Se algum arquivo faltar, criar estrutura básica

**Acceptance Criteria:**
- [ ] Estrutura de pastas completa
- [ ] Todos arquivos __init__.py existem
- [ ] main.py existe e está configurado

**Estimated Time:** 20 minutes

---

### TASK-007: Implementar/Verificar Configuração (settings.py)
**Objective:** Garantir que configurações estão corretas

**Steps:**
1. Abrir src/config/settings.py
2. Verificar se usa pydantic-settings
3. Verificar se carrega variáveis do .env
4. Verificar se tem validação de variáveis obrigatórias
5. Se necessário, atualizar código

**Acceptance Criteria:**
- [ ] Settings carrega .env corretamente
- [ ] Variáveis obrigatórias validadas
- [ ] Type hints presentes
- [ ] Código segue padrões do tech.md

**Estimated Time:** 20 minutes

---

### TASK-008: Implementar/Verificar Cliente Supabase
**Objective:** Garantir conexão com Supabase funciona

**Steps:**
1. Abrir src/utils/supabase_client.py
2. Verificar se cria cliente Supabase corretamente
3. Verificar se usa SERVICE_KEY (não ANON_KEY)
4. Adicionar função de teste de conexão
5. Testar conexão executando script de teste

**Acceptance Criteria:**
- [ ] Cliente Supabase criado corretamente
- [ ] Usa SERVICE_KEY
- [ ] Conexão testada e funcionando
- [ ] Logs claros em caso de erro

**Estimated Time:** 20 minutes

---

### TASK-009: Configurar CORS no Backend
**Objective:** Permitir requisições do frontend sem bloqueios CORS

**Steps:**
1. Abrir src/main.py
2. Importar CORSMiddleware do fastapi.middleware.cors
3. Adicionar middleware com configuração:
   - allow_origins: ["http://localhost:5173"]
   - allow_credentials: True
   - allow_methods: ["*"]
   - allow_headers: ["*"]
4. Verificar que configuração está antes dos routers
5. Salvar arquivo

**Acceptance Criteria:**
- [ ] CORSMiddleware importado
- [ ] Middleware configurado corretamente
- [ ] Origem localhost:5173 permitida
- [ ] Credentials habilitados
- [ ] Todos métodos e headers permitidos

**Estimated Time:** 10 minutes

---

### TASK-009: Implementar Health Check Endpoint
**Objective:** Criar endpoint para verificar se backend está rodando

**Steps:**
1. Criar src/api/routes/health.py
2. Implementar GET /health que retorna {"status": "ok"}
3. Adicionar teste de conexão Supabase
4. Registrar router no main.py

**Acceptance Criteria:**
- [ ] Endpoint /health criado
- [ ] Retorna 200 quando tudo ok
- [ ] Testa conexão Supabase
- [ ] Router registrado

**Estimated Time:** 15 minutes

---

### TASK-010: Iniciar Backend e Validar
**Objective:** Rodar backend localmente e verificar funcionamento

**Steps:**
1. Com venv ativado, executar: `uvicorn src.main:app --reload --port 8000`
2. Verificar logs no console
3. Acessar http://localhost:8000/health
4. Acessar http://localhost:8000/docs
5. Verificar se Swagger UI carrega
6. Testar endpoint /health no Swagger

**Acceptance Criteria:**
- [ ] Backend inicia sem erros
- [ ] Logs aparecem no console
- [ ] /health retorna 200
- [ ] /docs abre Swagger UI
- [ ] Nenhum erro crítico nos logs

**Estimated Time:** 15 minutes

---

## Phase 2: Frontend Integration

### TASK-011: Verificar Estado Atual do Frontend
**Objective:** Entender o que já existe no frontend

**Steps:**
1. Navegar para pasta frontend/
2. Listar arquivos em frontend/src/
3. Verificar se AuthContext existe
4. Verificar se usa dados mock ou API
5. Verificar quais páginas existem
6. Verificar quais componentes existem
7. Verificar se axios ou fetch está instalado

**Acceptance Criteria:**
- [ ] Lista completa de arquivos documentada
- [ ] Identificado uso de mock vs API
- [ ] Páginas existentes listadas
- [ ] HTTP client identificado

**Estimated Time:** 30 minutes

---

### TASK-012: Instalar Dependências do Frontend
**Objective:** Garantir que todas bibliotecas necessárias estão instaladas

**Steps:**
1. Abrir terminal na pasta frontend/
2. Executar: `npm install`
3. Se axios não estiver instalado: `npm install axios`
4. Se react-toastify não estiver instalado: `npm install react-toastify`
5. Verificar package.json

**Acceptance Criteria:**
- [ ] node_modules/ criado
- [ ] axios instalado
- [ ] react-toastify instalado
- [ ] Nenhum erro de instalação

**Estimated Time:** 10 minutes

---

### TASK-013: Criar API Client Base
**Objective:** Criar cliente HTTP configurado para backend

**Steps:**
1. Criar arquivo src/services/api.ts
2. Importar axios
3. Criar instância com baseURL http://localhost:8000
4. Configurar headers padrão
5. Exportar instância

**Acceptance Criteria:**
- [ ] Arquivo api.ts criado
- [ ] Instância axios configurada
- [ ] baseURL correto
- [ ] Headers configurados

**Estimated Time:** 15 minutes

---

### TASK-014: Implementar Interceptors JWT
**Objective:** Adicionar token automaticamente em requisições

**Steps:**
1. Abrir src/services/api.ts
2. Adicionar request interceptor
3. Ler token do localStorage
4. Adicionar token no header Authorization
5. Adicionar response interceptor
6. Tratar erro 401 (redirecionar para login)

**Acceptance Criteria:**
- [ ] Request interceptor adiciona token
- [ ] Response interceptor trata 401
- [ ] Token lido do localStorage
- [ ] Redirecionamento funciona

**Estimated Time:** 20 minutes

---

### TASK-015: Criar Auth Service
**Objective:** Implementar funções de autenticação

**Steps:**
1. Criar src/services/authService.ts
2. Implementar função login(email, password)
3. Implementar função logout()
4. Implementar função getCurrentUser()
5. Usar API client criado anteriormente

**Acceptance Criteria:**
- [ ] authService.ts criado
- [ ] Função login implementada
- [ ] Função logout implementada
- [ ] Função getCurrentUser implementada
- [ ] Usa API client

**Estimated Time:** 25 minutes

---

### TASK-016: Atualizar AuthContext para API Real
**Objective:** Substituir mock por chamadas API reais

**Steps:**
1. Abrir src/contexts/AuthContext.tsx
2. Importar authService
3. Substituir login mock por authService.login()
4. Substituir logout mock por authService.logout()
5. Armazenar token no localStorage
6. Carregar token ao inicializar
7. Testar login/logout

**Acceptance Criteria:**
- [ ] AuthContext usa API real
- [ ] Login chama backend
- [ ] Token armazenado
- [ ] Logout limpa token
- [ ] Estado persiste após refresh

**Estimated Time:** 30 minutes

---

### TASK-017: Criar Client Service
**Objective:** Implementar funções CRUD de clientes

**Steps:**
1. Criar src/services/clientService.ts
2. Implementar getAll()
3. Implementar getById(id)
4. Implementar create(data)
5. Implementar update(id, data)
6. Implementar delete(id)
7. Usar API client

**Acceptance Criteria:**
- [ ] clientService.ts criado
- [ ] Todas funções CRUD implementadas
- [ ] Type hints corretos
- [ ] Usa API client
- [ ] Error handling presente

**Estimated Time:** 25 minutes

---

### TASK-018: Integrar Página de Clientes
**Objective:** Conectar página de clientes com API real

**Steps:**
1. Abrir página de clientes (ClientsPage.tsx ou similar)
2. Importar clientService
3. Substituir dados mock por clientService.getAll()
4. Implementar loading state
5. Implementar error handling
6. Testar listagem

**Acceptance Criteria:**
- [ ] Página usa clientService
- [ ] Dados vêm da API
- [ ] Loading state funciona
- [ ] Erros são exibidos
- [ ] Lista atualiza corretamente

**Estimated Time:** 30 minutes

---

### TASK-019: Integrar Formulário de Cliente
**Objective:** Conectar criação/edição de clientes com API

**Steps:**
1. Abrir formulário de cliente
2. Implementar onSubmit com clientService.create() ou update()
3. Adicionar loading state no botão
4. Adicionar toast de sucesso
5. Adicionar toast de erro
6. Redirecionar após sucesso
7. Testar criação e edição

**Acceptance Criteria:**
- [ ] Formulário chama API
- [ ] Loading durante submit
- [ ] Toast de sucesso/erro
- [ ] Redirecionamento funciona
- [ ] Validação de campos

**Estimated Time:** 30 minutes

---

### TASK-020: Implementar Deleção de Cliente
**Objective:** Conectar deleção com API

**Steps:**
1. Localizar botão/ação de deletar
2. Adicionar confirmação antes de deletar
3. Chamar clientService.delete(id)
4. Atualizar lista após deleção
5. Mostrar toast de sucesso/erro
6. Testar deleção

**Acceptance Criteria:**
- [ ] Confirmação antes de deletar
- [ ] Chama API corretamente
- [ ] Lista atualiza
- [ ] Toast exibido
- [ ] Erro tratado

**Estimated Time:** 20 minutes

---

### TASK-021: Criar Lead Service
**Objective:** Implementar funções CRUD de leads

**Steps:**
1. Criar src/services/leadService.ts
2. Implementar getAll()
3. Implementar getById(id)
4. Implementar create(data)
5. Implementar update(id, data)
6. Implementar delete(id)

**Acceptance Criteria:**
- [ ] leadService.ts criado
- [ ] Todas funções CRUD implementadas
- [ ] Type hints corretos
- [ ] Usa API client

**Estimated Time:** 20 minutes

---

### TASK-022: Integrar Página de Leads
**Objective:** Conectar página de leads com API real

**Steps:**
1. Abrir página de leads
2. Importar leadService
3. Substituir mock por leadService.getAll()
4. Implementar loading e error handling
5. Testar listagem

**Acceptance Criteria:**
- [ ] Página usa leadService
- [ ] Dados vêm da API
- [ ] Loading/error funcionam
- [ ] Lista atualiza

**Estimated Time:** 25 minutes

---

### TASK-023: Integrar Formulário e Deleção de Leads
**Objective:** Conectar CRUD completo de leads

**Steps:**
1. Integrar formulário de criação/edição
2. Integrar deleção com confirmação
3. Adicionar toasts
4. Testar todos fluxos

**Acceptance Criteria:**
- [x] Criar lead funciona
- [x] Editar lead funciona
- [x] Deletar lead funciona
- [x] Toasts exibidos
- [x] Erros tratados

**Estimated Time:** 30 minutes
**Status:** ✅ COMPLETO

---

### TASK-024: Criar Project Service
**Objective:** Implementar funções CRUD de projetos

**Steps:**
1. Criar src/services/projectService.ts
2. Implementar todas funções CRUD
3. Seguir mesmo padrão dos services anteriores

**Acceptance Criteria:**
- [x] projectService.ts criado
- [x] Todas funções implementadas
- [x] Padrão consistente

**Estimated Time:** 20 minutes
**Status:** ✅ COMPLETO (já existia)

---

### TASK-025: Integrar Página de Projetos
**Objective:** Conectar página de projetos com API real

**Steps:**
1. Abrir página de projetos
2. Integrar listagem
3. Integrar formulário
4. Integrar deleção
5. Testar todos fluxos

**Acceptance Criteria:**
- [x] CRUD completo funciona
- [x] Loading/error implementados
- [x] Toasts exibidos
- [x] Dados persistem

**Estimated Time:** 35 minutes
**Status:** ✅ COMPLETO

---

## Phase 3: Docker Infrastructure

### TASK-026: Criar Dockerfile do Backend
**Objective:** Preparar imagem Docker do backend

**Steps:**
1. Criar arquivo backend/Dockerfile
2. Usar imagem base python:3.11-slim
3. Configurar WORKDIR /app
4. Copiar requirements.txt e instalar
5. Copiar código fonte
6. Expor porta 8000
7. Definir CMD para uvicorn

**Acceptance Criteria:**
- [ ] Dockerfile criado
- [ ] Usa Python 3.11+
- [ ] Instala dependências
- [ ] Expõe porta correta
- [ ] CMD configurado

**Estimated Time:** 20 minutes

---

### TASK-027: Criar .dockerignore
**Objective:** Excluir arquivos desnecessários da imagem

**Steps:**
1. Criar backend/.dockerignore
2. Adicionar venv/
3. Adicionar __pycache__/
4. Adicionar *.pyc
5. Adicionar .env
6. Adicionar .git/

**Acceptance Criteria:**
- [ ] .dockerignore criado
- [ ] Arquivos desnecessários excluídos
- [ ] .env não incluído na imagem

**Estimated Time:** 10 minutes

---

### TASK-028: Criar docker-compose.yml
**Objective:** Orquestrar todos serviços

**Steps:**
1. Criar docker-compose.yml na raiz
2. Definir serviço backend
3. Definir serviço redis
4. Definir serviço nginx
5. Configurar networks
6. Configurar volumes
7. Configurar variáveis de ambiente

**Acceptance Criteria:**
- [ ] docker-compose.yml criado
- [ ] Todos serviços definidos
- [ ] Networks configuradas
- [ ] Volumes configurados
- [ ] Env vars configuradas

**Estimated Time:** 30 minutes

---

### TASK-029: Criar nginx.conf
**Objective:** Configurar proxy reverso

**Steps:**
1. Criar nginx.conf na raiz
2. Configurar upstream para backend
3. Configurar location / para frontend
4. Configurar location /api/ para backend
5. Configurar location /docs para backend
6. Adicionar headers necessários

**Acceptance Criteria:**
- [ ] nginx.conf criado
- [ ] Rotas configuradas
- [ ] Headers configurados
- [ ] Proxy pass correto

**Estimated Time:** 25 minutes

---

### TASK-030: Documentar Uso do Docker
**Objective:** Criar documentação clara

**Steps:**
1. Criar backend/README_DOCKER.md
2. Documentar como fazer build
3. Documentar como executar
4. Documentar como parar
5. Documentar troubleshooting
6. Adicionar exemplos de comandos

**Acceptance Criteria:**
- [ ] README_DOCKER.md criado
- [ ] Comandos documentados
- [ ] Exemplos claros
- [ ] Troubleshooting incluído

**Estimated Time:** 20 minutes

---

### TASK-031: Testar Build Docker (Opcional)
**Objective:** Validar que Docker funciona

**Steps:**
1. Executar: `docker-compose build`
2. Verificar se build completa sem erros
3. Executar: `docker-compose up -d`
4. Verificar se serviços iniciam
5. Testar acesso aos endpoints
6. Executar: `docker-compose down`

**Acceptance Criteria:**
- [ ] Build completa sem erros
- [ ] Serviços iniciam corretamente
- [ ] Endpoints acessíveis
- [ ] Serviços param corretamente

**Estimated Time:** 30 minutes

---

## Phase 4: End-to-End Validation

### TASK-032: Validar Fluxo de Login
**Objective:** Testar autenticação completa

**Steps:**
1. Iniciar backend e frontend
2. Acessar página de login
3. Tentar login com credenciais inválidas
4. Verificar mensagem de erro
5. Fazer login com credenciais válidas
6. Verificar redirecionamento para dashboard
7. Verificar token no localStorage
8. Refresh página e verificar que continua logado

**Acceptance Criteria:**
- [ ] Login inválido mostra erro
- [ ] Login válido funciona
- [ ] Token armazenado
- [ ] Redirecionamento correto
- [ ] Estado persiste após refresh

**Estimated Time:** 20 minutes

---

### TASK-033: Validar CRUD de Clientes
**Objective:** Testar operações completas de clientes

**Steps:**
1. Acessar página de clientes
2. Verificar que lista carrega
3. Criar novo cliente
4. Verificar que aparece na lista
5. Editar cliente criado
6. Verificar que mudanças são salvas
7. Deletar cliente
8. Verificar que é removido da lista
9. Verificar dados no Supabase

**Acceptance Criteria:**
- [ ] Lista carrega corretamente
- [ ] Criar funciona
- [ ] Editar funciona
- [ ] Deletar funciona
- [ ] Dados persistem no banco

**Estimated Time:** 25 minutes

---

### TASK-034: Validar CRUD de Leads
**Objective:** Testar operações completas de leads

**Steps:**
1. Repetir processo do TASK-033 para leads
2. Verificar associação com cliente
3. Validar dados no Supabase

**Acceptance Criteria:**
- [ ] CRUD completo funciona
- [ ] Associação com cliente correta
- [ ] Dados persistem

**Estimated Time:** 20 minutes

---

### TASK-035: Validar CRUD de Projetos
**Objective:** Testar operações completas de projetos

**Steps:**
1. Repetir processo do TASK-033 para projetos
2. Verificar associação com cliente
3. Validar dados no Supabase

**Acceptance Criteria:**
- [ ] CRUD completo funciona
- [ ] Associação com cliente correta
- [ ] Dados persistem

**Estimated Time:** 20 minutes

---

### TASK-036: Validar RLS (Row Level Security)
**Objective:** Verificar que políticas RLS funcionam

**Steps:**
1. Conectar ao Supabase via SQL Editor
2. Verificar que RLS está habilitado em todas tabelas
3. Verificar políticas existentes
4. Tentar query como usuário não-admin (se possível)
5. Verificar que dados são filtrados corretamente

**Acceptance Criteria:**
- [ ] RLS habilitado em todas tabelas
- [ ] Políticas corretas aplicadas
- [ ] Admin vê todos dados
- [ ] Cliente vê apenas seus dados

**Estimated Time:** 20 minutes

---

### TASK-037: Validar Performance
**Objective:** Verificar que sistema é rápido

**Steps:**
1. Abrir DevTools do navegador
2. Ir para aba Network
3. Fazer login e medir tempo
4. Carregar lista de clientes e medir tempo
5. Criar cliente e medir tempo
6. Verificar que operações < 1s

**Acceptance Criteria:**
- [ ] Login < 1s
- [ ] Listagem < 1s
- [ ] Criação < 1s
- [ ] Nenhuma operação > 2s

**Estimated Time:** 15 minutes

---

### TASK-038: Validar Console sem Erros
**Objective:** Garantir que não há erros críticos

**Steps:**
1. Abrir DevTools Console
2. Navegar por todas páginas
3. Executar todas operações CRUD
4. Verificar que não há erros em vermelho
5. Warnings aceitáveis podem existir

**Acceptance Criteria:**
- [ ] Nenhum erro crítico no console
- [ ] CORS funcionando
- [ ] Requisições bem-sucedidas
- [ ] Logs claros

**Estimated Time:** 15 minutes

---

### TASK-039: Validar Logout
**Objective:** Testar encerramento de sessão

**Steps:**
1. Estar logado no sistema
2. Clicar em logout
3. Verificar que token é removido do localStorage
4. Verificar redirecionamento para login
5. Tentar acessar página protegida
6. Verificar que é redirecionado para login

**Acceptance Criteria:**
- [ ] Logout remove token
- [ ] Redireciona para login
- [ ] Páginas protegidas inacessíveis
- [ ] Pode fazer login novamente

**Estimated Time:** 10 minutes

---

### TASK-040: Documentar Estado Final
**Objective:** Criar relatório do sprint

**Steps:**
1. Listar todas funcionalidades implementadas
2. Listar todos endpoints funcionando
3. Listar todas páginas integradas
4. Documentar configurações necessárias
5. Documentar próximos passos

**Acceptance Criteria:**
- [ ] Documentação completa
- [ ] Funcionalidades listadas
- [ ] Configurações documentadas
- [ ] Próximos passos claros

**Estimated Time:** 30 minutes

---

## Summary

**Total Tasks:** 40  
**Estimated Total Time:** 14.5-16.5 hours (2-3 dias de trabalho efetivo)

**Phases:**
- Phase 1 (Backend): 10 tasks, ~3.25 hours (inclui validação de banco e CORS)
- Phase 2 (Frontend): 15 tasks, ~6.5 hours
- Phase 3 (Docker): 6 tasks, ~2.5 hours
- Phase 4 (Validation): 9 tasks, ~3 hours

**Critical Path:**
1. Backend rodando localmente (TASK-001 a TASK-010)
2. Frontend integrado (TASK-011 a TASK-025)
3. Validação end-to-end (TASK-032 a TASK-039)
4. Docker preparado (TASK-026 a TASK-031) - pode ser paralelo

**Dependencies:**
- Phase 2 depende de Phase 1 completa
- Phase 4 depende de Phase 1 e 2 completas
- Phase 3 é independente e pode ser feita em paralelo

**Checkpoints:**
- [x] Checkpoint 1: Backend rodando (após TASK-010)
- [x] Checkpoint 2: Login funcionando (após TASK-016)
- [x] Checkpoint 3: Um CRUD completo (após TASK-020)
- [x] Checkpoint 4: Todos CRUDs funcionando (após TASK-025)
- [ ] Checkpoint 5: Docker preparado (após TASK-031)
- [ ] Checkpoint 6: Validação completa (após TASK-040)
