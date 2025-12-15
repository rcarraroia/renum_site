# Requirements Document - SICC (Sistema de Inteligência Corporativa Contínua)

## Introduction

O Sistema de Inteligência Corporativa Contínua (SICC) é uma camada cognitiva adaptativa que permite aos agentes Renum aprenderem continuamente com interações reais, consolidarem conhecimento corporativo e evoluírem suas capacidades sem necessidade de modificação manual de prompts. O sistema captura padrões de conversas, transforma dados em memórias estruturadas validadas pela ISA (assistente supervisora) e aplica esse conhecimento de forma controlada e versionada.

O SICC opera em três camadas hierárquicas:
1. **Agente Base do Nicho** - Conhecimento fundamental do setor (MMN, Gabinete, Clínicas)
2. **Camada Empresa/Equipe** - Planos de negócio, processos e propriedade intelectual da empresa
3. **Configuração Individual** - Ajustes leves por distribuidor/usuário

Este documento define os requisitos para implementação do SICC como diferencial competitivo nativo da plataforma Renum.

## Glossary

- **SICC**: Sistema de Inteligência Corporativa Contínua - camada de aprendizado adaptativo
- **ISA**: Intelligent Supervisor Agent - agente supervisor que valida aprendizados
- **Memory Chunk**: Unidade de conhecimento armazenada (termo, processo, FAQ, produto)
- **Behavior Pattern**: Padrão comportamental que define estratégias de resposta
- **Learning Log**: Registro de aprendizado pendente de aprovação
- **Embedding**: Representação vetorial de texto para similarity search
- **pgvector**: Extensão PostgreSQL para armazenamento e busca de vetores
- **GTE-small**: Modelo de embedding local (padrão)
- **MiniLM-L6-v2**: Modelo de embedding local (fallback)
- **Confidence Score**: Pontuação de confiança de um aprendizado (0.0-1.0)
- **DNA Cognitivo**: Configuração imutável do agente (função, princípios, restrições)
- **Snapshot**: Backup versionado do estado de conhecimento do agente
- **RLS**: Row Level Security - isolamento de dados por cliente no banco
- **Whisper**: Modelo de transcrição de áudio local
- **Similarity Search**: Busca por similaridade semântica usando embeddings

## Requirements

### Requirement 1: Infraestrutura de Vector Database

**User Story:** Como desenvolvedor do sistema, eu preciso de uma infraestrutura de vector database funcional, para que o SICC possa armazenar e buscar embeddings de forma eficiente.

#### Acceptance Criteria

1. WHEN o sistema é inicializado THEN a extensão pgvector SHALL estar instalada e ativa no banco de dados Supabase
2. WHEN embeddings são armazenados THEN o sistema SHALL utilizar dimensão 384 para GTE-small ou 384 para MiniLM-L6-v2
3. WHEN buscas por similaridade são executadas THEN o sistema SHALL retornar resultados em menos de 500ms para até 100.000 embeddings
4. WHEN índices são criados THEN o sistema SHALL utilizar ivfflat ou hnsw conforme volume de dados
5. WHEN o banco de dados é consultado THEN o sistema SHALL aplicar RLS garantindo isolamento entre clientes

### Requirement 2: Serviço de Embeddings Local

**User Story:** Como sistema SICC, eu preciso gerar embeddings localmente na VPS, para que não haja custos de API externa e os dados permaneçam privados.

#### Acceptance Criteria

1. WHEN o serviço de embeddings é iniciado THEN o sistema SHALL carregar o modelo GTE-small localmente na VPS
2. IF o modelo GTE-small falhar ao carregar THEN o sistema SHALL utilizar MiniLM-L6-v2 como fallback
3. WHEN texto é enviado para embedding THEN o sistema SHALL retornar vetor em menos de 100ms para textos de até 512 tokens
4. WHEN múltiplos textos são processados THEN o sistema SHALL suportar batch processing de até 32 textos simultaneamente
5. WHEN embeddings idênticos são solicitados THEN o sistema SHALL utilizar cache para evitar reprocessamento

### Requirement 3: DNA Cognitivo do Agente

**User Story:** Como administrador, eu quero definir o DNA cognitivo imutável de cada agente, para que sua função, princípios e restrições fundamentais não sejam alterados por aprendizado automático.

#### Acceptance Criteria

1. WHEN um agente é criado THEN o sistema SHALL criar registro de DNA cognitivo contendo função, princípios, restrições, tom de voz e políticas de segurança
2. WHEN o DNA cognitivo é definido THEN o sistema SHALL impedir modificações automáticas pelo processo de aprendizado
3. WHEN o DNA cognitivo precisa ser alterado THEN o sistema SHALL exigir permissão de administrador
4. WHEN o DNA é modificado THEN o sistema SHALL criar nova versão mantendo histórico completo
5. WHEN o agente processa mensagens THEN o sistema SHALL sempre respeitar as restrições definidas no DNA

### Requirement 4: Memória Adaptativa

**User Story:** Como agente Renum, eu preciso armazenar e consultar conhecimento aprendido, para que minhas respostas sejam enriquecidas com informações específicas do negócio do cliente.

#### Acceptance Criteria

1. WHEN conhecimento novo é identificado THEN o sistema SHALL criar memory_chunk com tipo, conteúdo, embedding e metadados
2. WHEN uma consulta é feita THEN o sistema SHALL executar similarity search retornando top 5 memórias mais relevantes
3. WHEN memórias são utilizadas THEN o sistema SHALL incrementar usage_count e atualizar last_used_at
4. WHEN memórias antigas não são usadas por 90 dias THEN o sistema SHALL marcar como candidatas a arquivamento
5. WHEN o limite de memórias é atingido THEN o sistema SHALL arquivar memórias menos utilizadas mantendo as mais relevantes

### Requirement 5: Padrões Comportamentais

**User Story:** Como agente Renum, eu preciso aplicar padrões comportamentais aprendidos, para que estratégias bem-sucedidas sejam reutilizadas em contextos similares.

#### Acceptance Criteria

1. WHEN um padrão comportamental é detectado THEN o sistema SHALL armazenar trigger_context e action_config
2. WHEN o contexto de uma conversa corresponde a um padrão THEN o sistema SHALL aplicar a ação configurada
3. WHEN um padrão é aplicado THEN o sistema SHALL registrar aplicação e resultado (sucesso/falha)
4. WHEN a taxa de sucesso de um padrão cai abaixo de 40% THEN o sistema SHALL desativar o padrão automaticamente
5. WHEN padrões são consultados THEN o sistema SHALL priorizar padrões com maior taxa de sucesso

### Requirement 6: Ciclo de Aprendizado Supervisionado pela ISA

**User Story:** Como ISA (supervisor), eu preciso analisar conversas periodicamente e extrair aprendizados, para que o conhecimento dos agentes evolua de forma controlada.

#### Acceptance Criteria

1. WHEN o ciclo de análise é executado THEN a ISA SHALL processar conversas das últimas 24 horas
2. WHEN padrões são detectados THEN a ISA SHALL criar learning_log com tipo, dados de origem, análise e confidence score
3. WHEN confidence score é maior que 0.8 THEN o sistema SHALL aprovar aprendizado automaticamente
4. WHEN confidence score está entre 0.5 e 0.8 THEN o sistema SHALL marcar para revisão humana
5. WHEN confidence score é menor que 0.5 THEN o sistema SHALL descartar aprendizado automaticamente

### Requirement 7: Modelo Híbrido de Aprovação

**User Story:** Como administrador, eu quero controlar quais aprendizados são aplicados aos agentes, para que apenas conhecimento validado seja incorporado.

#### Acceptance Criteria

1. WHEN aprendizados de alta confiança são gerados THEN o sistema SHALL aplicar automaticamente sem intervenção humana
2. WHEN aprendizados de média confiança são gerados THEN o sistema SHALL apresentar na fila de revisão
3. WHEN um humano aprova aprendizado THEN o sistema SHALL criar memory_chunk ou behavior_pattern correspondente
4. WHEN um humano rejeita aprendizado THEN o sistema SHALL marcar como rejeitado e registrar motivo
5. WHEN threshold de auto-aprovação é configurado THEN o sistema SHALL respeitar valor entre 0.0 e 1.0

### Requirement 8: Enriquecimento de Prompts

**User Story:** Como agente Renum, eu preciso enriquecer meus prompts com memórias e padrões relevantes, para que minhas respostas sejam mais precisas e contextualizadas.

#### Acceptance Criteria

1. WHEN uma mensagem é recebida THEN o sistema SHALL executar similarity search nas memórias do agente
2. WHEN memórias relevantes são encontradas THEN o sistema SHALL incluir top 5 no contexto do prompt
3. WHEN padrões aplicáveis são identificados THEN o sistema SHALL incluir instruções do padrão no prompt
4. WHEN o prompt enriquecido é gerado THEN o sistema SHALL manter tamanho total abaixo de 8000 tokens
5. WHEN nenhuma memória relevante é encontrada THEN o sistema SHALL processar com prompt base sem falhar

### Requirement 9: Snapshots e Rollback

**User Story:** Como administrador, eu preciso criar snapshots do estado de conhecimento dos agentes, para que seja possível reverter aprendizados problemáticos.

#### Acceptance Criteria

1. WHEN consolidação diária é executada THEN o sistema SHALL criar snapshot automático do estado do agente
2. WHEN snapshot é criado THEN o sistema SHALL armazenar contagem de memórias, padrões, interações e taxa de sucesso
3. WHEN rollback é solicitado THEN o sistema SHALL restaurar estado de snapshot específico
4. WHEN rollback é executado THEN o sistema SHALL desativar memórias e padrões criados após o snapshot
5. WHEN snapshots antigos acumulam THEN o sistema SHALL manter últimos 30 dias e arquivar anteriores

### Requirement 10: Métricas de Performance

**User Story:** Como administrador, eu preciso visualizar métricas de performance dos agentes, para que seja possível avaliar evolução e ROI do SICC.

#### Acceptance Criteria

1. WHEN interações ocorrem THEN o sistema SHALL registrar total, sucessos, tempo de resposta e satisfação
2. WHEN memórias são utilizadas THEN o sistema SHALL contabilizar uso em métricas diárias
3. WHEN padrões são aplicados THEN o sistema SHALL registrar aplicações e resultados
4. WHEN novos aprendizados são consolidados THEN o sistema SHALL incrementar contador de learnings
5. WHEN métricas são consultadas THEN o sistema SHALL agregar por dia, semana e mês

### Requirement 11: Transcrição de Áudio Local

**User Story:** Como sistema SICC, eu preciso transcrever áudios localmente, para que conversas em áudio sejam processadas mantendo privacidade dos dados.

#### Acceptance Criteria

1. WHEN arquivo de áudio é enviado THEN o sistema SHALL utilizar Whisper local para transcrição
2. WHEN transcrição é concluída THEN o sistema SHALL detectar idioma automaticamente
3. WHEN áudio contém silêncios longos THEN o sistema SHALL segmentar em chunks lógicos
4. WHEN transcrição é gerada THEN o sistema SHALL criar memory_chunks com embeddings do conteúdo
5. WHEN arquivo original é processado THEN o sistema SHALL arquivar com política de retenção configurável

### Requirement 12: Interface de Evolução do Agente

**User Story:** Como usuário, eu quero visualizar a evolução do conhecimento do meu agente, para que eu possa acompanhar seu aprendizado ao longo do tempo.

#### Acceptance Criteria

1. WHEN a página de evolução é acessada THEN o sistema SHALL exibir gráfico temporal de memórias criadas
2. WHEN métricas são exibidas THEN o sistema SHALL mostrar total de memórias, padrões, interações e taxa de sucesso
3. WHEN velocidade de aprendizado é calculada THEN o sistema SHALL mostrar novos aprendizados por dia
4. WHEN top memórias são listadas THEN o sistema SHALL ordenar por usage_count decrescente
5. WHEN padrões ativos são exibidos THEN o sistema SHALL mostrar taxa de sucesso de cada padrão

### Requirement 13: Interface de Gestão de Memória

**User Story:** Como usuário, eu quero gerenciar as memórias do meu agente, para que eu possa editar, desativar ou adicionar conhecimento manualmente.

#### Acceptance Criteria

1. WHEN a página de memória é acessada THEN o sistema SHALL listar todas as memórias com paginação
2. WHEN filtros são aplicados THEN o sistema SHALL filtrar por tipo (termo, processo, FAQ, produto, objeção)
3. WHEN busca é realizada THEN o sistema SHALL buscar por conteúdo usando full-text search
4. WHEN memória é editada THEN o sistema SHALL criar nova versão mantendo histórico
5. WHEN memória é desativada THEN o sistema SHALL marcar is_active como false sem deletar

### Requirement 14: Interface de Fila de Aprendizados

**User Story:** Como usuário, eu quero revisar aprendizados pendentes, para que eu possa aprovar ou rejeitar conhecimento antes de ser aplicado ao agente.

#### Acceptance Criteria

1. WHEN a fila é acessada THEN o sistema SHALL listar learning_logs com status pending
2. WHEN aprendizado é exibido THEN o sistema SHALL mostrar análise da ISA, confidence score e dados de origem
3. WHEN usuário aprova em lote THEN o sistema SHALL processar múltiplos aprendizados simultaneamente
4. WHEN usuário rejeita THEN o sistema SHALL solicitar motivo opcional
5. WHEN aprendizado é processado THEN o sistema SHALL atualizar status e registrar reviewed_by

### Requirement 15: Interface de Configurações de Aprendizado

**User Story:** Como usuário, eu quero configurar como meu agente aprende, para que eu possa controlar frequência, thresholds e limites de aprendizado.

#### Acceptance Criteria

1. WHEN configurações são acessadas THEN o sistema SHALL exibir frequência de análise (hourly, daily, weekly)
2. WHEN threshold é ajustado THEN o sistema SHALL permitir valores entre 0.0 e 1.0 para auto-aprovação
3. WHEN tipos de aprendizado são configurados THEN o sistema SHALL permitir habilitar/desabilitar por tipo
4. WHEN limite de memórias é definido THEN o sistema SHALL aplicar quota máxima por agente
5. WHEN aprendizado é desativado THEN o sistema SHALL pausar ciclo de análise mantendo memórias existentes

### Requirement 16: Isolamento Multi-tenant

**User Story:** Como sistema, eu preciso garantir isolamento total entre clientes, para que dados de um cliente nunca sejam acessíveis por outro.

#### Acceptance Criteria

1. WHEN tabelas SICC são criadas THEN o sistema SHALL habilitar RLS em todas as tabelas
2. WHEN políticas RLS são definidas THEN o sistema SHALL exigir client_id em todas as queries
3. WHEN similarity search é executado THEN o sistema SHALL filtrar apenas embeddings do cliente
4. WHEN snapshots são criados THEN o sistema SHALL isolar por client_id
5. WHEN testes de isolamento são executados THEN o sistema SHALL comprovar zero vazamento entre clientes

### Requirement 17: Arquitetura em Camadas

**User Story:** Como sistema, eu preciso implementar arquitetura em três camadas, para que conhecimento seja organizado hierarquicamente (Nicho → Empresa → Individual).

#### Acceptance Criteria

1. WHEN agente é criado THEN o sistema SHALL associar a um nicho base (MMN, Gabinete, Clínicas)
2. WHEN memórias são criadas THEN o sistema SHALL classificar em camada (base, empresa, individual)
3. WHEN consulta é feita THEN o sistema SHALL priorizar camada individual, depois empresa, depois base
4. WHEN plano de negócio é adicionado THEN o sistema SHALL armazenar exclusivamente na camada empresa
5. WHEN agente base é atualizado THEN o sistema SHALL propagar conhecimento para todos os agentes do nicho

### Requirement 18: Auditoria e Rastreabilidade

**User Story:** Como administrador, eu preciso auditar todas as ações do SICC, para que seja possível rastrear origem de aprendizados e decisões tomadas.

#### Acceptance Criteria

1. WHEN aprendizado é criado THEN o sistema SHALL registrar fonte de dados completa
2. WHEN aprovação ocorre THEN o sistema SHALL registrar reviewed_by e reviewed_at
3. WHEN memória é utilizada THEN o sistema SHALL registrar em qual conversa foi aplicada
4. WHEN padrão é aplicado THEN o sistema SHALL registrar contexto e resultado
5. WHEN logs são consultados THEN o sistema SHALL permitir filtrar por agente, data e tipo

### Requirement 19: Observabilidade e Monitoramento

**User Story:** Como desenvolvedor, eu preciso monitorar saúde do SICC, para que problemas sejam detectados e resolvidos rapidamente.

#### Acceptance Criteria

1. WHEN sistema está operando THEN o sistema SHALL expor endpoint /sicc/status com métricas de saúde
2. WHEN filas estão congestionadas THEN o sistema SHALL emitir alerta quando tamanho exceder threshold
3. WHEN jobs falham THEN o sistema SHALL registrar erro com stack trace completo
4. WHEN pgvector está lento THEN o sistema SHALL alertar quando queries excederem 1 segundo
5. WHEN logs são gerados THEN o sistema SHALL usar formato estruturado (JSON) para parsing

### Requirement 20: Integração com Módulos Existentes

**User Story:** Como sistema, eu preciso integrar SICC com Renus, ISA e módulo de criação de agentes, para que funcionalidades existentes sejam enriquecidas com aprendizado contínuo.

#### Acceptance Criteria

1. WHEN Renus processa mensagem THEN o sistema SHALL consultar memórias e padrões antes de gerar resposta
2. WHEN ISA executa comando THEN o sistema SHALL ter acesso a learning_service para análise
3. WHEN agente é criado THEN o sistema SHALL inicializar DNA, memória vazia e ciclo de aprendizado
4. WHEN sub-agente é criado THEN o sistema SHALL herdar conhecimento base do agente pai
5. WHEN integração falha THEN o sistema SHALL operar em modo degradado sem bloquear funcionalidades existentes
