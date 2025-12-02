# Requirements Document - Sprint 02: CRUD Core

## Introdução

Este sprint implementa operações CRUD (Create, Read, Update, Delete) completas para as três entidades principais do sistema RENUM: Clientes, Leads e Projetos. O objetivo é criar endpoints REST no backend FastAPI, serviços de negócio com validações, e preparar a base para integração com o frontend React.

A estrutura do banco de dados já existe (criada em sprint anterior) e é mais completa que o planejamento inicial. Este sprint adapta o código à estrutura real existente.

## Glossário

- **Cliente**: Empresa que contrata agentes de IA da RENUM
- **Lead**: Contato/prospect que pode se tornar cliente ou usuário final dos agentes
- **Projeto**: Campanha, pesquisa ou iniciativa criada por um cliente
- **CRUD**: Create, Read, Update, Delete - operações básicas de banco de dados
- **RLS**: Row Level Security - segurança em nível de linha do PostgreSQL
- **Supabase**: Plataforma de backend (PostgreSQL + APIs)
- **FastAPI**: Framework web Python para criar APIs REST
- **Pydantic**: Biblioteca de validação de dados Python
- **JSONB**: Tipo de dado JSON binário do PostgreSQL

## Requirements

### Requirement 1: Gerenciamento de Clientes

**User Story:** Como administrador do sistema RENUM, eu quero gerenciar clientes (empresas que contratam agentes), para que eu possa manter um cadastro completo e atualizado de todos os clientes ativos.

#### Acceptance Criteria

1. WHEN um administrador cria um novo cliente THEN o sistema SHALL validar os dados obrigatórios (company_name, segment, status) e armazenar no banco de dados
2. WHEN um administrador lista clientes THEN o sistema SHALL retornar lista paginada com filtros por status, busca por nome e ordenação por data de criação
3. WHEN um administrador busca um cliente por ID THEN o sistema SHALL retornar todos os dados do cliente incluindo informações de contato e endereço
4. WHEN um administrador atualiza um cliente THEN o sistema SHALL validar os dados modificados e atualizar apenas os campos fornecidos
5. WHEN um administrador deleta um cliente THEN o sistema SHALL remover o registro do banco de dados
6. WHEN dados de contato são fornecidos THEN o sistema SHALL armazenar em formato JSONB com campos phone, email, whatsapp, telegram
7. WHEN dados de endereço são fornecidos THEN o sistema SHALL armazenar em formato JSONB com campos completos (rua, número, cidade, estado, CEP)
8. WHEN um documento (CPF/CNPJ) é fornecido THEN o sistema SHALL validar o formato antes de salvar

### Requirement 2: Gerenciamento de Leads

**User Story:** Como administrador do sistema RENUM, eu quero gerenciar leads (contatos/prospects), para que eu possa rastrear origem, qualificação e histórico de interações de cada lead.

#### Acceptance Criteria

1. WHEN um administrador cria um novo lead THEN o sistema SHALL validar dados obrigatórios (name, phone, source, status) e armazenar no banco de dados
2. WHEN um administrador lista leads THEN o sistema SHALL retornar lista paginada com filtros por status, source, busca por nome/telefone/email
3. WHEN um administrador busca um lead por ID THEN o sistema SHALL retornar todos os dados incluindo score, datas de contato e notas
4. WHEN um administrador atualiza um lead THEN o sistema SHALL validar os dados e atualizar campos fornecidos
5. WHEN um administrador deleta um lead THEN o sistema SHALL remover o registro do banco de dados
6. WHEN um telefone é fornecido THEN o sistema SHALL validar formato brasileiro (10-11 dígitos ou +55)
7. WHEN um email é fornecido THEN o sistema SHALL validar formato de email
8. WHEN um score é fornecido THEN o sistema SHALL validar que está entre 0 e 100

### Requirement 3: Gerenciamento de Projetos

**User Story:** Como administrador do sistema RENUM, eu quero gerenciar projetos (campanhas, pesquisas), para que eu possa acompanhar progresso, orçamento e responsáveis de cada iniciativa.

#### Acceptance Criteria

1. WHEN um administrador cria um novo projeto THEN o sistema SHALL validar dados obrigatórios (name, type, status) e armazenar no banco de dados
2. WHEN um administrador lista projetos THEN o sistema SHALL retornar lista paginada com filtros por status, type, client_id e busca por nome
3. WHEN um administrador busca um projeto por ID THEN o sistema SHALL retornar todos os dados incluindo progresso, orçamento, datas e escopo
4. WHEN um administrador atualiza um projeto THEN o sistema SHALL validar os dados e atualizar campos fornecidos
5. WHEN um administrador deleta um projeto THEN o sistema SHALL remover o registro do banco de dados
6. WHEN um progresso é fornecido THEN o sistema SHALL validar que está entre 0 e 100
7. WHEN um orçamento é fornecido THEN o sistema SHALL validar que é um valor positivo
8. WHEN datas são fornecidas THEN o sistema SHALL aceitar formato date (sem hora)

### Requirement 4: Validações de Negócio

**User Story:** Como desenvolvedor, eu quero validações consistentes em todos os endpoints, para que dados inválidos sejam rejeitados antes de chegar ao banco de dados.

#### Acceptance Criteria

1. WHEN um telefone é validado THEN o sistema SHALL aceitar formatos (11) 98765-4321, 11987654321, +55 11 98765-4321
2. WHEN um CPF é validado THEN o sistema SHALL verificar que tem 11 dígitos e não é sequência repetida
3. WHEN um CNPJ é validado THEN o sistema SHALL verificar que tem 14 dígitos e não é sequência repetida
4. WHEN um email é validado THEN o sistema SHALL verificar formato padrão (usuario@dominio.com)
5. WHEN dados obrigatórios estão faltando THEN o sistema SHALL retornar erro 400 com mensagem clara
6. WHEN dados inválidos são fornecidos THEN o sistema SHALL retornar erro 400 com detalhes da validação
7. WHEN um recurso não é encontrado THEN o sistema SHALL retornar erro 404 com mensagem clara

### Requirement 5: Paginação e Filtros

**User Story:** Como administrador, eu quero listar recursos com paginação e filtros, para que eu possa navegar eficientemente em grandes volumes de dados.

#### Acceptance Criteria

1. WHEN um administrador lista recursos THEN o sistema SHALL retornar resposta com items, total, page, limit, has_next
2. WHEN parâmetro page é fornecido THEN o sistema SHALL retornar a página solicitada (mínimo 1)
3. WHEN parâmetro limit é fornecido THEN o sistema SHALL retornar até o limite solicitado (máximo 100)
4. WHEN parâmetro search é fornecido THEN o sistema SHALL buscar em campos relevantes (nome, email, etc)
5. WHEN parâmetro status é fornecido THEN o sistema SHALL filtrar por status exato
6. WHEN nenhum filtro é fornecido THEN o sistema SHALL retornar todos os registros paginados
7. WHEN ordenação não é especificada THEN o sistema SHALL ordenar por created_at descendente (mais recente primeiro)

### Requirement 6: Segurança e Autenticação

**User Story:** Como administrador do sistema, eu quero que todos os endpoints sejam protegidos por autenticação, para que apenas usuários autorizados possam acessar os dados.

#### Acceptance Criteria

1. WHEN um endpoint é acessado sem token THEN o sistema SHALL retornar erro 401 Unauthorized
2. WHEN um endpoint é acessado com token inválido THEN o sistema SHALL retornar erro 401 Unauthorized
3. WHEN um endpoint é acessado com token válido THEN o sistema SHALL processar a requisição normalmente
4. WHEN RLS está habilitado THEN o sistema SHALL aplicar políticas de segurança automaticamente
5. WHEN um administrador acessa recursos THEN o sistema SHALL permitir acesso total (política RLS)

### Requirement 7: Documentação da API

**User Story:** Como desenvolvedor frontend, eu quero documentação automática da API, para que eu possa entender e testar os endpoints facilmente.

#### Acceptance Criteria

1. WHEN a aplicação inicia THEN o sistema SHALL disponibilizar documentação Swagger em /docs
2. WHEN a documentação é acessada THEN o sistema SHALL mostrar todos os endpoints com descrições
3. WHEN um endpoint é documentado THEN o sistema SHALL mostrar parâmetros, tipos de dados e exemplos
4. WHEN um endpoint é documentado THEN o sistema SHALL mostrar possíveis códigos de resposta (200, 201, 400, 404, etc)
5. WHEN a documentação é acessada THEN o sistema SHALL permitir testar endpoints diretamente na interface

### Requirement 8: Tratamento de Erros

**User Story:** Como desenvolvedor, eu quero tratamento consistente de erros, para que o frontend possa exibir mensagens claras aos usuários.

#### Acceptance Criteria

1. WHEN um erro de validação ocorre THEN o sistema SHALL retornar status 400 com detalhes do erro
2. WHEN um recurso não é encontrado THEN o sistema SHALL retornar status 404 com mensagem clara
3. WHEN um erro de autenticação ocorre THEN o sistema SHALL retornar status 401 com mensagem
4. WHEN um erro interno ocorre THEN o sistema SHALL retornar status 500 e logar detalhes
5. WHEN um erro ocorre THEN o sistema SHALL incluir timestamp e request_id para rastreamento
