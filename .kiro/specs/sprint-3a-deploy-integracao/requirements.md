# Requirements Document - Sprint 3A: Deploy e Integração

## Introduction

Este sprint tem como objetivo integrar o frontend React com o backend FastAPI existente, estabelecendo um sistema funcional end-to-end em ambiente de desenvolvimento local. O foco é substituir dados mock por integrações reais com a API e banco de dados Supabase, além de preparar a infraestrutura Docker para deploy futuro em produção.

## Scope

### In Scope
- Configuração e execução do backend FastAPI localmente (sem Docker)
- Integração completa do frontend com backend via API REST
- Autenticação real usando Supabase Auth
- CRUD completo de clientes, leads e projetos integrado
- Preparação de infraestrutura Docker (não utilizada ainda)
- Validação end-to-end do sistema

### Out of Scope
- Deploy em produção (VPS)
- Configuração de domínio e SSL/HTTPS
- Sistema de conversas em tempo real (WebSocket)
- Sistema de entrevistas automatizadas
- Integração com WhatsApp
- Execução de Celery/Redis em desenvolvimento
- Sub-agentes especializados

## Stakeholders

- **Desenvolvedor Backend**: Responsável por configurar e rodar backend localmente
- **Desenvolvedor Frontend**: Responsável por integrar frontend com API real
- **DevOps**: Responsável por preparar infraestrutura Docker
- **QA**: Responsável por validar sistema end-to-end

## User Stories

### Epic 1: Backend Local em Execução

#### US-3A-001: Configurar Ambiente Python
**Como** desenvolvedor backend  
**Quero** configurar ambiente virtual Python com todas dependências  
**Para que** eu possa rodar o backend localmente sem conflitos

**Acceptance Criteria:**
- WHEN ambiente virtual é criado THEN Python 3.11+ está disponível
- WHEN requirements.txt é instalado THEN todas dependências são instaladas sem erros
- WHEN dependências são verificadas THEN fastapi, uvicorn, supabase, pydantic estão presentes
- WHEN ambiente é ativado THEN comandos python e pip apontam para venv

#### US-3A-002: Configurar Variáveis de Ambiente
**Como** desenvolvedor backend  
**Quero** configurar arquivo .env com credenciais Supabase  
**Para que** o backend possa conectar ao banco de dados

**Acceptance Criteria:**
- WHEN .env é criado THEN contém SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_KEY
- WHEN .env é carregado THEN variáveis estão acessíveis via settings
- WHEN credenciais são inválidas THEN erro claro é exibido
- WHEN .env está no .gitignore THEN não é commitado

#### US-3A-003: Iniciar Backend FastAPI
**Como** desenvolvedor backend  
**Quero** iniciar servidor FastAPI localmente  
**Para que** endpoints estejam disponíveis para o frontend

**Acceptance Criteria:**
- WHEN uvicorn é executado THEN servidor inicia na porta 8000
- WHEN servidor está rodando THEN logs aparecem no console
- WHEN /health é acessado THEN retorna status 200
- WHEN /docs é acessado THEN Swagger UI é exibido
- WHEN código é alterado THEN servidor recarrega automaticamente (--reload)

#### US-3A-004: Validar Conexão com Supabase
**Como** desenvolvedor backend  
**Quero** validar conexão com Supabase  
**Para que** operações de banco de dados funcionem corretamente

**Acceptance Criteria:**
- WHEN backend inicia THEN conexão com Supabase é estabelecida
- WHEN query é executada THEN dados são retornados do banco
- WHEN conexão falha THEN erro claro é logado
- WHEN RLS está ativo THEN políticas são respeitadas

### Epic 2: Frontend Integrado com Backend

#### US-3A-005: Criar API Client
**Como** desenvolvedor frontend  
**Quero** criar cliente HTTP para comunicação com backend  
**Para que** eu possa fazer requisições à API de forma padronizada

**Acceptance Criteria:**
- WHEN API client é criado THEN base URL aponta para http://localhost:8000
- WHEN requisição é feita THEN headers corretos são enviados
- WHEN token JWT existe THEN é incluído automaticamente no header Authorization
- WHEN erro de rede ocorre THEN é tratado adequadamente

#### US-3A-006: Implementar Autenticação Real
**Como** usuário do sistema  
**Quero** fazer login com credenciais reais  
**Para que** eu possa acessar o sistema de forma segura

**Acceptance Criteria:**
- WHEN credenciais válidas são enviadas THEN token JWT é retornado
- WHEN token é recebido THEN é armazenado no localStorage
- WHEN token é armazenado THEN usuário é redirecionado para dashboard
- WHEN credenciais inválidas são enviadas THEN erro claro é exibido
- WHEN logout é feito THEN token é removido e usuário redirecionado para login

#### US-3A-007: Integrar CRUD de Clientes
**Como** usuário admin  
**Quero** gerenciar clientes via interface integrada com backend  
**Para que** dados sejam persistidos no banco de dados real

**Acceptance Criteria:**
- WHEN página de clientes carrega THEN lista de clientes vem da API
- WHEN novo cliente é criado THEN POST /api/clients é chamado e cliente aparece na lista
- WHEN cliente é editado THEN PUT /api/clients/{id} é chamado e dados são atualizados
- WHEN cliente é deletado THEN DELETE /api/clients/{id} é chamado e cliente é removido
- WHEN operação está em andamento THEN loading state é exibido
- WHEN erro ocorre THEN mensagem de erro é exibida

#### US-3A-008: Integrar CRUD de Leads
**Como** usuário admin  
**Quero** gerenciar leads via interface integrada com backend  
**Para que** dados sejam persistidos no banco de dados real

**Acceptance Criteria:**
- WHEN página de leads carrega THEN lista de leads vem da API
- WHEN novo lead é criado THEN POST /api/leads é chamado e lead aparece na lista
- WHEN lead é editado THEN PUT /api/leads/{id} é chamado e dados são atualizados
- WHEN lead é deletado THEN DELETE /api/leads/{id} é chamado e lead é removido
- WHEN operação está em andamento THEN loading state é exibido
- WHEN erro ocorre THEN mensagem de erro é exibida

#### US-3A-009: Integrar CRUD de Projetos
**Como** usuário admin  
**Quero** gerenciar projetos via interface integrada com backend  
**Para que** dados sejam persistidos no banco de dados real

**Acceptance Criteria:**
- WHEN página de projetos carrega THEN lista de projetos vem da API
- WHEN novo projeto é criado THEN POST /api/projects é chamado e projeto aparece na lista
- WHEN projeto é editado THEN PUT /api/projects/{id} é chamado e dados são atualizados
- WHEN projeto é deletado THEN DELETE /api/projects/{id} é chamado e projeto é removido
- WHEN operação está em andamento THEN loading state é exibido
- WHEN erro ocorre THEN mensagem de erro é exibida

#### US-3A-010: Configurar CORS
**Como** desenvolvedor backend  
**Quero** configurar CORS no backend  
**Para que** frontend possa fazer requisições sem bloqueios

**Acceptance Criteria:**
- WHEN frontend faz requisição THEN CORS headers são retornados
- WHEN origem é http://localhost:5173 THEN requisição é permitida
- WHEN método é OPTIONS THEN preflight é tratado corretamente
- WHEN credenciais são enviadas THEN são aceitas

### Epic 3: Infraestrutura Docker Preparada

#### US-3A-011: Criar Dockerfile do Backend
**Como** DevOps  
**Quero** criar Dockerfile para o backend  
**Para que** aplicação possa ser containerizada no futuro

**Acceptance Criteria:**
- WHEN Dockerfile é criado THEN usa imagem Python 3.11+
- WHEN build é executado THEN imagem é criada sem erros
- WHEN container é iniciado THEN backend roda corretamente
- WHEN dependências são instaladas THEN requirements.txt é usado

#### US-3A-012: Criar docker-compose.yml
**Como** DevOps  
**Quero** criar docker-compose.yml com todos serviços  
**Para que** stack completa possa ser iniciada com um comando

**Acceptance Criteria:**
- WHEN docker-compose.yml é criado THEN inclui backend, redis, nginx
- WHEN docker-compose up é executado THEN todos serviços iniciam
- WHEN serviços estão rodando THEN comunicam entre si corretamente
- WHEN volumes são definidos THEN dados persistem

#### US-3A-013: Configurar Nginx como Proxy Reverso
**Como** DevOps  
**Quero** configurar nginx como proxy reverso  
**Para que** requisições sejam roteadas corretamente em produção

**Acceptance Criteria:**
- WHEN nginx.conf é criado THEN rotas para backend estão definidas
- WHEN requisição chega THEN é encaminhada para backend
- WHEN headers são necessários THEN são adicionados corretamente
- WHEN SSL for configurado THEN nginx está preparado

#### US-3A-014: Documentar Uso do Docker
**Como** desenvolvedor  
**Quero** documentação clara de como usar Docker  
**Para que** eu possa fazer deploy em produção no futuro

**Acceptance Criteria:**
- WHEN README é criado THEN comandos de build estão documentados
- WHEN README é lido THEN comandos de execução estão claros
- WHEN README é seguido THEN sistema roda em Docker
- WHEN troubleshooting é necessário THEN soluções estão documentadas

### Epic 4: Validação End-to-End

#### US-3A-015: Validar Fluxo de Autenticação
**Como** QA  
**Quero** validar fluxo completo de autenticação  
**Para que** login/logout funcionem corretamente

**Acceptance Criteria:**
- WHEN usuário faz login THEN é autenticado e redirecionado
- WHEN usuário está autenticado THEN pode acessar páginas protegidas
- WHEN usuário não está autenticado THEN é redirecionado para login
- WHEN usuário faz logout THEN sessão é encerrada

#### US-3A-016: Validar CRUD Completo
**Como** QA  
**Quero** validar operações CRUD de todas entidades  
**Para que** dados sejam persistidos corretamente

**Acceptance Criteria:**
- WHEN cliente é criado THEN aparece no banco Supabase
- WHEN lead é criado THEN aparece no banco Supabase
- WHEN projeto é criado THEN aparece no banco Supabase
- WHEN entidade é atualizada THEN mudanças são salvas
- WHEN entidade é deletada THEN é removida do banco

#### US-3A-017: Validar RLS (Row Level Security)
**Como** QA  
**Quero** validar que RLS está funcionando  
**Para que** usuários vejam apenas dados permitidos

**Acceptance Criteria:**
- WHEN admin faz requisição THEN vê todos os dados
- WHEN cliente faz requisição THEN vê apenas seus dados
- WHEN usuário não autenticado faz requisição THEN recebe 401
- WHEN usuário tenta acessar dados de outro THEN recebe 403

#### US-3A-018: Validar Performance
**Como** QA  
**Quero** validar performance do sistema  
**Para que** operações sejam rápidas

**Acceptance Criteria:**
- WHEN página carrega THEN tempo < 2s
- WHEN operação CRUD é executada THEN tempo < 1s
- WHEN múltiplas requisições são feitas THEN sistema responde adequadamente
- WHEN erro ocorre THEN é tratado em < 500ms

## Functional Requirements

### FR-001: Backend Local
**WHILE** backend está em desenvolvimento  
**THE SYSTEM SHALL** rodar localmente sem Docker  
**AND** conectar ao Supabase em produção

### FR-002: Autenticação JWT
**WHILE** usuário faz login  
**THE SYSTEM SHALL** retornar token JWT válido  
**AND** armazenar token no cliente

### FR-003: Interceptor de Token
**WHILE** requisição é feita ao backend  
**THE SYSTEM SHALL** incluir token JWT no header Authorization  
**AND** renovar token se expirado

### FR-004: CRUD Completo
**WHILE** usuário gerencia entidades  
**THE SYSTEM SHALL** permitir criar, ler, atualizar e deletar  
**AND** persistir dados no Supabase

### FR-005: Loading States
**WHILE** operação assíncrona está em andamento  
**THE SYSTEM SHALL** exibir indicador de loading  
**AND** desabilitar ações duplicadas

### FR-006: Error Handling
**WHILE** erro ocorre  
**THE SYSTEM SHALL** exibir mensagem clara ao usuário  
**AND** logar erro para debugging

### FR-007: CORS Configurado
**WHILE** frontend faz requisição  
**THE SYSTEM SHALL** permitir origem http://localhost:5173  
**AND** aceitar credenciais

### FR-008: Docker Preparado
**WHILE** infraestrutura Docker é criada  
**THE SYSTEM SHALL** incluir Dockerfile, docker-compose.yml, nginx.conf  
**AND** documentar uso

## Non-Functional Requirements

### NFR-001: Performance
**WHILE** sistema está em operação  
**THE SYSTEM SHALL** responder requisições em < 1s  
**AND** carregar páginas em < 2s

### NFR-002: Segurança
**WHILE** dados são transmitidos  
**THE SYSTEM SHALL** usar HTTPS em produção  
**AND** validar tokens JWT

### NFR-003: Confiabilidade
**WHILE** erro ocorre  
**THE SYSTEM SHALL** tratar gracefully  
**AND** não quebrar aplicação

### NFR-004: Usabilidade
**WHILE** usuário interage com sistema  
**THE SYSTEM SHALL** fornecer feedback claro  
**AND** exibir mensagens compreensíveis

### NFR-005: Manutenibilidade
**WHILE** código é desenvolvido  
**THE SYSTEM SHALL** seguir padrões definidos  
**AND** incluir documentação

### NFR-006: Escalabilidade
**WHILE** infraestrutura Docker é preparada  
**THE SYSTEM SHALL** suportar múltiplas instâncias  
**AND** permitir load balancing

## Constraints

### Technical Constraints
- Backend deve usar Python 3.11+
- Frontend deve usar React 18+
- Banco de dados deve ser Supabase (PostgreSQL)
- Autenticação deve usar Supabase Auth
- Docker deve usar imagens oficiais

### Business Constraints
- Sistema deve funcionar em ambiente local primeiro
- Deploy em produção é sprint futuro
- Integrações externas (WhatsApp, SMS) são sprints futuros

### Time Constraints
- Sprint deve ser concluído em 5-7 dias
- Validação end-to-end deve ser feita antes de considerar completo

## Assumptions

- Python 3.11+ está instalado na máquina de desenvolvimento
- Node.js 18+ está instalado na máquina de desenvolvimento
- Git está configurado
- Credenciais Supabase estão disponíveis em docs/SUPABASE_CREDENTIALS.md
- Banco de dados Supabase já tem estrutura criada (Sprint 01)
- Backend FastAPI já tem código base implementado
- Frontend React já tem estrutura base implementada

## Dependencies

### Sprint Dependencies
- Sprint 01 - Fundação e Autenticação deve estar concluído
- Tabelas do banco de dados devem existir
- RLS deve estar habilitado
- Usuário admin deve existir no Supabase

### External Dependencies
- Supabase deve estar acessível
- Internet deve estar disponível para instalar dependências
- Portas 8000 (backend) e 5173 (frontend) devem estar livres

## Acceptance Criteria (Sprint Level)

### Backend Local
- [ ] Backend roda com `uvicorn src.main:app --reload`
- [ ] Endpoints acessíveis em http://localhost:8000
- [ ] Swagger UI funcionando em http://localhost:8000/docs
- [ ] Health check retorna 200
- [ ] Conecta no Supabase corretamente
- [ ] Logs sendo gerados sem erros

### Frontend Integrado
- [ ] Login funciona com backend real
- [ ] Token JWT salvo e enviado em requisições
- [ ] CRUD de clientes funciona completamente
- [ ] CRUD de leads funciona completamente
- [ ] CRUD de projetos funciona completamente
- [ ] Loading states implementados
- [ ] Error handling implementado
- [ ] CORS funcionando

### Docker Preparado
- [ ] Dockerfile criado e testado
- [ ] docker-compose.yml criado
- [ ] nginx.conf configurado
- [ ] .dockerignore criado
- [ ] README com instruções de Docker
- [ ] Build funciona sem erros

### Validação End-to-End
- [ ] Login → CRUD → Logout funciona
- [ ] Dados persistem no Supabase
- [ ] RLS aplicado corretamente
- [ ] Performance < 1s por operação
- [ ] Console sem erros críticos

## Risks

### Risk 1: Dependências Incompatíveis
**Probability:** Medium  
**Impact:** High  
**Mitigation:** Usar requirements.txt com versões fixas, testar instalação em ambiente limpo

### Risk 2: CORS Bloqueando Requisições
**Probability:** High  
**Impact:** High  
**Mitigation:** Configurar CORS corretamente no backend, testar com diferentes origens

### Risk 3: RLS Bloqueando Operações Legítimas
**Probability:** Medium  
**Impact:** High  
**Mitigation:** Validar políticas RLS, usar SERVICE_KEY quando necessário

### Risk 4: Token JWT Expirando
**Probability:** Medium  
**Impact:** Medium  
**Mitigation:** Implementar refresh token, tratar expiração gracefully

### Risk 5: Performance Lenta
**Probability:** Low  
**Impact:** Medium  
**Mitigation:** Adicionar índices no banco, otimizar queries, implementar cache

## Glossary

- **RLS**: Row Level Security - Segurança em nível de linha no PostgreSQL
- **JWT**: JSON Web Token - Token de autenticação
- **CORS**: Cross-Origin Resource Sharing - Compartilhamento de recursos entre origens
- **CRUD**: Create, Read, Update, Delete - Operações básicas de banco de dados
- **API**: Application Programming Interface - Interface de programação de aplicações
- **Supabase**: Plataforma de backend como serviço baseada em PostgreSQL
- **FastAPI**: Framework web Python moderno e rápido
- **Uvicorn**: Servidor ASGI para Python
- **Docker**: Plataforma de containerização
- **Nginx**: Servidor web e proxy reverso