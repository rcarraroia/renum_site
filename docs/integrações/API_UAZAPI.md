# API Uazapi - Documentação Completa

**Título:** uazapiGO -  WhatsApp API (v2.0)

**Versão:** 1.0.0

**Descrição:** API para gerenciamento de instâncias do WhatsApp e comunicações.

## ⚠️ Recomendação Importante: WhatsApp Business
**É ALTAMENTE RECOMENDADO usar contas do WhatsApp Business** em vez do WhatsApp normal para integração, o WhatsApp normal pode apresentar inconsistências, desconexões, limitações e instabilidades durante o uso com a nossa API.

## Autenticação
- Endpoints regulares requerem um header 'token' com o token da instância
- Endpoints administrativos requerem um header 'admintoken'

## Estados da Instância
As instâncias podem estar nos seguintes estados:
- `disconnected`: Desconectado do WhatsApp
- `connecting`: Em processo de conexão
- `connected`: Conectado e autenticado com sucesso

## Limites de Uso
- O servidor possui um limite máximo de instâncias conectadas
- Quando o limite é atingido, novas tentativas receberão erro 429
- Servidores gratuitos/demo podem ter restrições adicionais de tempo de vida


## Servidores

- URL: `https://{subdomain}.uazapi.com`
  - subdomain: Subdomínio da sua empresa (padrão: free)

## Esquemas de Segurança

### token

- **Tipo:** apiKey
- **Localização:** header

### admintoken

- **Tipo:** apiKey
- **Localização:** header
- **Descrição:** Token de administrador para endpoints administrativos

## Schemas

### Instance

Representa uma instância do WhatsApp

**Tipo:** object


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string (uuid) | Não | ID único gerado automaticamente |
| token | string | Não | Token de autenticação da instância |
| status | string | Não | Status atual da conexão |
| paircode | string | Não | Código de pareamento |
| qrcode | string | Não | QR Code em base64 para autenticação |
| name | string | Não | Nome da instância |
| profileName | string | Não | Nome do perfil WhatsApp |
| profilePicUrl | string (uri) | Não | URL da foto do perfil |
| isBusiness | boolean | Não | Indica se é uma conta business |
| plataform | string | Não | Plataforma de origem (iOS/Android/Web) |
| systemName | string | Não | Nome do sistema operacional |
| owner | string | Não | Proprietário da instância |
| lastDisconnect | string (date-time) | Não | Data/hora da última desconexão |
| lastDisconnectReason | string | Não | Motivo da última desconexão |
| adminField01 | string | Não | Campo administrativo 01 |
| adminField02 | string | Não | Campo administrativo 02 |
| openai_apikey | string | Não | Chave da API OpenAI |
| chatbot_enabled | boolean | Não | Habilitar chatbot automático |
| chatbot_ignoreGroups | boolean | Não | Ignorar mensagens de grupos |
| chatbot_stopConversation | string | Não | Palavra-chave para parar conversa |
| chatbot_stopMinutes | integer | Não | Por quanto tempo ficará pausado o chatbot ao usar stop conversation |
| chatbot_stopWhenYouSendMsg | integer | Não | Por quanto tempo ficará pausada a conversa quando você enviar mensagem manualmente |
| created | string (date-time) | Não | Data de criação da instância |
| updated | string (date-time) | Não | Data da última atualização |
| msg_delay_min | integer (int64) | Não | Delay mínimo em segundos entre mensagens diretas |
| msg_delay_max | integer (int64) | Não | Delay máximo em segundos entre mensagens diretas (deve ser maior que delayMin) |


### Webhook

Configuração completa de webhook com filtros e opções avançadas

**Tipo:** object


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string (uuid) | Não | ID único gerado automaticamente |
| instance_id | string | Não | ID da instância associada |
| enabled | boolean | Não | Webhook ativo/inativo |
| url | string (uri) | Sim | URL de destino dos eventos |
| events | array | Sim | Tipos de eventos monitorados |
| AddUrlTypesMessages | boolean | Não | Incluir na URLs o tipo de mensagem |
| addUrlEvents | boolean | Não | Incluir na URL o nome do evento |
| excludeMessages | array | Não | Filtros para excluir tipos de mensagens |
| created | string (date-time) | Não | Data de criação (automática) |
| updated | string (date-time) | Não | Data da última atualização (automática) |


### Chat

Representa uma conversa/chamado no sistema

**Tipo:** object


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Não | ID único da conversa (r + 7 bytes aleatórios em hex) |
| wa_fastid | string | Não | Identificador rápido do WhatsApp |
| wa_chatid | string | Não | ID completo do chat no WhatsApp |
| wa_archived | boolean | Não | Indica se o chat está arquivado |
| wa_contactName | string | Não | Nome do contato no WhatsApp |
| wa_name | string | Não | Nome do WhatsApp |
| name | string | Não | Nome exibido do chat |
| image | string | Não | URL da imagem do chat |
| imagePreview | string | Não | URL da miniatura da imagem |
| wa_ephemeralExpiration | integer (int64) | Não | Tempo de expiração de mensagens efêmeras |
| wa_isBlocked | boolean | Não | Indica se o contato está bloqueado |
| wa_isGroup | boolean | Não | Indica se é um grupo |
| wa_isGroup_admin | boolean | Não | Indica se o usuário é admin do grupo |
| wa_isGroup_announce | boolean | Não | Indica se é um grupo somente anúncios |
| wa_isGroup_community | boolean | Não | Indica se é uma comunidade |
| wa_isGroup_member | boolean | Não | Indica se é membro do grupo |
| wa_isPinned | boolean | Não | Indica se o chat está fixado |
| wa_label | string | Não | Labels do chat em JSON |
| wa_lastMessageTextVote | string | Não | Texto/voto da última mensagem |
| wa_lastMessageType | string | Não | Tipo da última mensagem |
| wa_lastMsgTimestamp | integer (int64) | Não | Timestamp da última mensagem |
| wa_lastMessageSender | string | Não | Remetente da última mensagem |
| wa_muteEndTime | integer (int64) | Não | Timestamp do fim do silenciamento |
| owner | string | Não | Dono da instância |
| wa_unreadCount | integer (int64) | Não | Contador de mensagens não lidas |
| phone | string | Não | Número de telefone |
| wa_common_groups | string | Não | Grupos em comum separados por vírgula, formato: (nome_grupo)id_grupo |
| lead_name | string | Não | Nome do lead |
| lead_fullName | string | Não | Nome completo do lead |
| lead_email | string | Não | Email do lead |
| lead_personalid | string | Não | Documento de identificação |
| lead_status | string | Não | Status do lead |
| lead_tags | string | Não | Tags do lead em JSON |
| lead_notes | string | Não | Anotações sobre o lead |
| lead_isTicketOpen | boolean | Não | Indica se tem ticket aberto |
| lead_assignedAttendant_id | string | Não | ID do atendente responsável |
| lead_kanbanOrder | integer (int64) | Não | Ordem no kanban |
| lead_field01 | string | Não |  |
| lead_field02 | string | Não |  |
| lead_field03 | string | Não |  |
| lead_field04 | string | Não |  |
| lead_field05 | string | Não |  |
| lead_field06 | string | Não |  |
| lead_field07 | string | Não |  |
| lead_field08 | string | Não |  |
| lead_field09 | string | Não |  |
| lead_field10 | string | Não |  |
| lead_field11 | string | Não |  |
| lead_field12 | string | Não |  |
| lead_field13 | string | Não |  |
| lead_field14 | string | Não |  |
| lead_field15 | string | Não |  |
| lead_field16 | string | Não |  |
| lead_field17 | string | Não |  |
| lead_field18 | string | Não |  |
| lead_field19 | string | Não |  |
| lead_field20 | string | Não |  |
| chatbot_agentResetMemoryAt | integer (int64) | Não | Timestamp do último reset de memória |
| chatbot_lastTrigger_id | string | Não | ID do último gatilho executado |
| chatbot_lastTriggerAt | integer (int64) | Não | Timestamp do último gatilho |
| chatbot_disableUntil | integer (int64) | Não | Timestamp até quando chatbot está desativado |
| created | string | Não | Data de criação |
| updated | string | Não | Data da última atualização |


### Message

Representa uma mensagem trocada no sistema

**Tipo:** object


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string (uuid) | Não | ID único interno da mensagem (formato r + 7 caracteres hex aleatórios) |
| messageid | string | Não | ID original da mensagem no provedor |
| chatid | string | Não | ID da conversa relacionada |
| fromMe | boolean | Não | Indica se a mensagem foi enviada pelo usuário |
| isGroup | boolean | Não | Indica se é uma mensagem de grupo |
| messageType | string | Não | Tipo de conteúdo da mensagem |
| messageTimestamp | integer | Não | Timestamp original da mensagem em milissegundos |
| edited | string | Não | Histórico de edições da mensagem |
| quoted | string | Não | ID da mensagem citada/respondida |
| reaction | string | Não | ID da mensagem reagida |
| sender | string | Não | ID do remetente da mensagem |
| senderName | string | Não | Nome exibido do remetente |
| source | string | Não | Plataforma de origem da mensagem |
| status | string | Não | Status do ciclo de vida da mensagem |
| text | string | Não | Texto original da mensagem |
| vote | string | Não | Dados de votação de enquete e listas |
| buttonOrListid | string | Não | ID do botão ou item de lista selecionado |
| convertOptions | string | Não | Conversão de opções de da mensagem, lista, enquete e botões |
| fileURL | string (uri) | Não | URL para download de arquivos de mídia |
| content | string | Não | Conteúdo completo da mensagem em formato JSON |
| owner | string | Não | Dono da mensagem |
| track_source | string | Não | Origem do rastreamento da mensagem |
| track_id | string | Não | ID para rastreamento da mensagem (aceita valores duplicados) |
| created | string (date-time) | Não | Data de criação no sistema (formato SQLite YYYY-MM-DD HH:MM:SS.FFF) |
| updated | string (date-time) | Não | Data da última atualização (formato SQLite YYYY-MM-DD HH:MM:SS.FFF) |
| ai_metadata | object | Não | Metadados do processamento por IA |


### Label

Representa uma etiqueta/categoria no sistema

**Tipo:** object


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string (uuid) | Não | ID único da etiqueta |
| name | string | Não | Nome da etiqueta |
| color | integer | Não | Índice numérico da cor (0-19) |
| colorHex | string | Não | Cor hexadecimal correspondente ao índice |
| createdAt | string (date-time) | Não | Data de criação |


### Attendant

Modelo de atendente do sistema

**Tipo:** object


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string (uuid) | Não | ID único gerado automaticamente |
| name | string | Não | Nome do atendente |
| phone | string | Não | Número de telefone |
| email | string (email) | Não | Endereço de e-mail |
| department | string | Não | Departamento de atuação |
| customField01 | string | Não | Campo personalizável 01 |
| customField02 | string | Não | Campo personalizável 02 |
| owner | string | Não | Responsável pelo cadastro |
| created | string (date-time) | Não | Data de criação automática |
| updated | string (date-time) | Não | Data de atualização automática |


### ChatbotTrigger

**Tipo:** object


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Não | Identificador único do trigger. Se definido, você irá editar ou deletar o trigger. Se vazio, um novo trigger será criado.  |
| active | boolean | Não | Define se o trigger está ativo e disponível para uso. Triggers inativos não serão executados pelo sistema.  |
| type | string | Sim | Tipo do trigger: * agent - aciona um agente de IA * quickreply - aciona respostas rápidas predefinidas  |
| agent_id | string | Sim | ID do agente de IA. Obrigatório quando type='agent' |
| quickReply_id | string | Não | ID da resposta rápida. Obrigatório quando type='quickreply' |
| ignoreGroups | boolean | Não | Define se o trigger deve ignorar mensagens de grupos |
| lead_field | string | Não | Campo do lead usado para condição do trigger |
| lead_operator | string | Não | Operador de comparação para condição do lead: * equals - igual a * not_equals - diferente de * contains - contém * not_contains - não contém * greater - maior que * less - menor que * empty - vazio * not_empty - não vazio  |
| lead_value | string | Não | Valor para comparação com o campo do lead. Usado em conjunto com lead_field e lead_operator |
| priority | integer (int64) | Não | Prioridade do trigger. Quando existem múltiplos triggers que poderiam ser acionados, APENAS o trigger com maior prioridade será executado. Se houver múltiplos triggers com a mesma prioridade mais alta, um será escolhido aleatoriamente.  |
| wordsToStart | string | Não | Palavras-chave ou frases que ativam o trigger. Múltiplas entradas separadas por pipe (|). Exemplo: olá|bom dia|qual seu nome  |
| responseDelay_seconds | integer (int64) | Não | Tempo de espera em segundos antes de executar o trigger |
| owner | string | Não | Identificador do proprietário do trigger |
| created | string (date-time) | Não | Data e hora de criação |
| updated | string (date-time) | Não | Data e hora da última atualização |


### ChatbotAIAgent

Configuração de um agente de IA para atendimento de conversas

**Tipo:** object


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string (uuid) | Não | ID único gerado pelo sistema |
| name | string | Sim | Nome de exibição do agente |
| provider | string | Sim | Provedor do serviço de IA |
| model | string | Sim | Nome do modelo LLM a ser utilizado |
| apikey | string | Sim | Chave de API para autenticação no provedor |
| basePrompt | string | Não | Prompt base para orientar o comportamento do agente |
| maxTokens | integer | Não | Número máximo de tokens por resposta |
| temperature | integer | Não | Controle de criatividade (0-100) |
| diversityLevel | integer | Não | Nível de diversificação das respostas |
| frequencyPenalty | integer | Não | Penalidade para repetição de frases |
| presencePenalty | integer | Não | Penalidade para manter foco no tópico |
| signMessages | boolean | Não | Adiciona identificação do agente nas mensagens |
| readMessages | boolean | Não | Marca mensagens como lidas automaticamente |
| maxMessageLength | integer | Não | Tamanho máximo permitido para mensagens (caracteres) |
| typingDelay_seconds | integer | Não | Atraso simulado de digitação em segundos |
| contextTimeWindow_hours | integer | Não | Janela temporal para contexto da conversa |
| contextMaxMessages | integer | Não | Número máximo de mensagens no contexto |
| contextMinMessages | integer | Não | Número mínimo de mensagens para iniciar contexto |
| owner | string | Não | Responsável/Proprietário do agente |
| created | string (date-time) | Não | Data de criação do registro |
| updated | string (date-time) | Não | Data da última atualização |


### ChatbotAIFunction

**Tipo:** object


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Não | ID único da função gerado automaticamente |
| name | string | Sim | Nome da função |
| description | string | Sim | Descrição da função |
| active | boolean | Não | Indica se a função está ativa |
| method | string | Sim | Método HTTP da requisição |
| endpoint | string | Sim | Endpoint da API |
| headers | string | Não | Cabeçalhos da requisição |
| body | string | Não | Corpo da requisição |
| parameters | string | Não | Parâmetros da função |
| undocumentedParameters | string | Não | Parâmetros não documentados |
| header_error | boolean | Não | Indica erro de formatação nos cabeçalhos |
| body_error | boolean | Não | Indica erro de formatação no corpo |
| owner | string | Não | Proprietário da função |
| created | string (date-time) | Não | Data de criação |
| updated | string (date-time) | Não | Data de atualização |


### ChatbotAIKnowledge

**Tipo:** object


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Sim | ID único gerado automaticamente |
| active | boolean | Sim | Indica se o conhecimento está ativo |
| tittle | string | Sim | Título do conhecimento |
| content | string | Sim | Conteúdo textual do conhecimento |
| vectorStatus | string | Não | Status da vetorização no sistema |
| isVectorized | boolean | Não | Indica se o conteúdo foi vetorizado |
| lastVectorizedAt | integer (int64) | Não | Timestamp da última vetorização |
| owner | string | Não | Proprietário do conhecimento |
| priority | integer (int64) | Não | Prioridade de uso do conhecimento |
| created | string (date-time) | Não | Data de criação |
| updated | string (date-time) | Não | Data de atualização |


### MessageQueueFolder

Pasta para organização de campanhas de mensagens em massa

**Tipo:** object


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Não | Identificador único |
| info | string | Não | Informações adicionais sobre a pasta |
| status | string | Não | Status atual da pasta |
| scheduled_for | integer (int64) | Não | Timestamp Unix para execução agendada |
| delayMax | integer (int64) | Não | Atraso máximo entre mensagens em milissegundos |
| delayMin | integer (int64) | Não | Atraso mínimo entre mensagens em milissegundos |
| log_delivered | integer (int64) | Não | Contagem de mensagens entregues |
| log_failed | integer (int64) | Não | Contagem de mensagens com falha |
| log_played | integer (int64) | Não | Contagem de mensagens reproduzidas (para áudio/vídeo) |
| log_read | integer (int64) | Não | Contagem de mensagens lidas |
| log_sucess | integer (int64) | Não | Contagem de mensagens enviadas com sucesso |
| log_total | integer (int64) | Não | Contagem total de mensagens |
| owner | string | Não | Identificador do proprietário da instância |
| created | string (date-time) | Não | Data e hora de criação |
| updated | string (date-time) | Não | Data e hora da última atualização |


### QuickReply

**Tipo:** object


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string (uuid) | Não | ID único da resposta rápida |
| shortcut | string | Sim | Atalho para acionar a resposta |
| content | string | Sim | Conteúdo da mensagem pré-definida |
| category | string | Não | Categoria para organização |
| createdAt | string (date-time) | Não | Data de criação |
| updatedAt | string (date-time) | Não | Data da última atualização |


### Group

Representa um grupo/conversa coletiva

**Tipo:** object


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| JID | string (jid) | Não | Identificador único do grupo |
| OwnerJID | string (jid) | Não | JID do proprietário do grupo |
| Name | string | Não | Nome do grupo |
| NameSetAt | string (date-time) | Não | Data da última alteração do nome |
| NameSetBy | string (jid) | Não | JID do usuário que definiu o nome |
| Topic | string | Não | Descrição do grupo |
| IsLocked | boolean | Não | Indica se apenas administradores podem editar informações do grupo - true = apenas admins podem editar - false = todos podem editar  |
| IsAnnounce | boolean | Não | Indica se apenas administradores podem enviar mensagens |
| AnnounceVersionID | string | Não | Versão da configuração de anúncios |
| IsEphemeral | boolean | Não | Indica se as mensagens são temporárias |
| DisappearingTimer | integer | Não | Tempo em segundos para desaparecimento de mensagens |
| IsIncognito | boolean | Não | Indica se o grupo é incognito |
| IsParent | boolean | Não | Indica se é um grupo pai (comunidade) |
| IsJoinApprovalRequired | boolean | Não | Indica se requer aprovação para novos membros |
| LinkedParentJID | string (jid) | Não | JID da comunidade vinculada |
| IsDefaultSubGroup | boolean | Não | Indica se é um subgrupo padrão da comunidade |
| GroupCreated | string (date-time) | Não | Data de criação do grupo |
| ParticipantVersionID | string | Não | Versão da lista de participantes |
| Participants | array | Não | Lista de participantes do grupo |
| MemberAddMode | string | Não | Modo de adição de novos membros |
| OwnerCanSendMessage | boolean | Não | Verifica se é possível você enviar mensagens |
| OwnerIsAdmin | boolean | Não | Verifica se você adminstrador do grupo |
| DefaultSubGroupId | string | Não | Se o grupo atual for uma comunidade, nesse campo mostrará o ID do subgrupo de avisos |
| invite_link | string | Não | Link de convite para entrar no grupo |
| request_participants | string | Não | Lista de solicitações de entrada, separados por vírgula |


### GroupParticipant

Participante de um grupo

**Tipo:** object


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| JID | string (jid) | Não | Identificador do participante |
| LID | string (jid) | Não | Identificador local do participante |
| IsAdmin | boolean | Não | Indica se é administrador |
| IsSuperAdmin | boolean | Não | Indica se é super administrador |
| DisplayName | string | Não | Nome exibido no grupo (para usuários anônimos) |
| Error | integer | Não | Código de erro ao adicionar participante |
| AddRequest | object | Não | Informações da solicitação de entrada |


### WebhookEvent

**Tipo:** object


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| event | string | Sim | Tipo do evento recebido |
| instance | string | Sim | ID da instância que gerou o evento |
| data | object | Sim |  |


## Endpoints

### Admininstração


### POST /instance/init

**Resumo:** Criar Instancia

Cria uma nova instância do WhatsApp. Para criar uma instância você precisa:

1. Ter um admintoken válido
2. Enviar pelo menos o nome da instância
3. A instância será criada desconectada
4. Será gerado um token único para autenticação

Após criar a instância, guarde o token retornado pois ele será necessário
para todas as outras operações.

Estados possíveis da instância:

- `disconnected`: Desconectado do WhatsApp
- `connecting`: Em processo de conexão
- `connected`: Conectado e autenticado

Campos administrativos (adminField01/adminField02) são opcionais e podem ser usados para armazenar metadados personalizados. 
OS valores desses campos são vísiveis para o dono da instancia via token, porém apenas o administrador da api (via admin token) pode editá-los.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| name | string | Sim | Nome da instância |
| systemName | string | Não | Nome do sistema (opcional, padrão 'uazapiGO' se não informado) |
| adminField01 | string | Não | Campo administrativo 1 para metadados personalizados (opcional) |
| adminField02 | string | Não | Campo administrativo 2 para metadados personalizados (opcional) |


**Respostas:**

#### 200

Sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não |  |
| instance | object | Não |  |
| connected | boolean | Não |  |
| loggedIn | boolean | Não |  |
| name | string | Não |  |
| token | string | Não |  |
| info | string | Não |  |

#### 401

Token inválido/expirado

#### 404

Instância não encontrada

#### 500

Erro interno


### GET /instance/all

**Resumo:** Listar todas as instâncias

Retorna uma lista completa de todas as instâncias do sistema, incluindo:
- ID e nome de cada instância
- Status atual (disconnected, connecting, connected)
- Data de criação
- Última desconexão e motivo
- Informações de perfil (se conectado)

Requer permissões de administrador.


**Respostas:**

#### 200

Lista de instâncias retornada com sucesso

Content-Type: `application/json`

#### 401

Token inválido ou expirado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 403

Token de administrador inválido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /instance/updateAdminFields

**Resumo:** Atualizar campos administrativos

Atualiza os campos administrativos (adminField01/adminField02) de uma instância.

Campos administrativos são opcionais e podem ser usados para armazenar metadados personalizados. 
Estes campos são persistidos no banco de dados e podem ser utilizados para integrações com outros sistemas ou para armazenamento de informações internas.
OS valores desses campos são vísiveis para o dono da instancia via token, porém apenas o administrador da api (via admin token) pode editá-los.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Sim | ID da instância |
| adminField01 | string | Não | Campo administrativo 1 |
| adminField02 | string | Não | Campo administrativo 2 |


**Respostas:**

#### 200

Campos atualizados com sucesso

Content-Type: `application/json`

Schema: `Instance`

#### 401

Token de administrador inválido

#### 404

Instância não encontrada

#### 500

Erro interno


### GET /globalwebhook

**Resumo:** Ver Webhook Global

Retorna a configuração atual do webhook global, incluindo:
- URL configurada
- Eventos ativos
- Filtros aplicados
- Configurações adicionais

Exemplo de resposta:
```json
{
  "enabled": true,
  "url": "https://example.com/webhook",
  "events": ["messages", "messages_update"],
  "excludeMessages": ["wasSentByApi", "isGroupNo"],
  "addUrlEvents": true,
  "addUrlTypesMessages": true
}
```


**Respostas:**

#### 200

Configuração atual do webhook global

Content-Type: `application/json`

Schema: `Webhook`

#### 401

Token de administrador não fornecido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 403

Token de administrador inválido ou servidor demo

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 404

Webhook global não encontrado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /globalwebhook

**Resumo:** Configurar Webhook Global

Configura um webhook global que receberá eventos de todas as instâncias.

### 🚀 Configuração Simples (Recomendada)

**Para a maioria dos casos de uso**:
- Configure apenas URL e eventos desejados
- Modo simples por padrão (sem complexidade)
- **Recomendado**: Sempre use `"excludeMessages": ["wasSentByApi"]` para evitar loops
- **Exemplo**: `{"url": "https://webhook.cool/global", "events": ["messages", "connection"], "excludeMessages": ["wasSentByApi"]}`

### 🧪 Sites para Testes (ordenados por qualidade)

**Para testar webhooks durante desenvolvimento**:
1. **https://webhook.cool/** - ⭐ Melhor opção (sem rate limit, interface limpa)
2. **https://rbaskets.in/** - ⭐ Boa alternativa (confiável, baixo rate limit)
3. **https://webhook.site/** - ⚠️ Evitar se possível (rate limit agressivo)

### Funcionalidades Principais:
- Configuração de URL para recebimento de eventos
- Seleção granular de tipos de eventos
- Filtragem avançada de mensagens
- Parâmetros adicionais na URL

**Eventos Disponíveis**:
- `connection`: Alterações no estado da conexão
- `history`: Recebimento de histórico de mensagens
- `messages`: Novas mensagens recebidas
- `messages_update`: Atualizações em mensagens existentes
- `call`: Eventos de chamadas VoIP
- `contacts`: Atualizações na agenda de contatos
- `presence`: Alterações no status de presença
- `groups`: Modificações em grupos
- `labels`: Gerenciamento de etiquetas
- `chats`: Eventos de conversas
- `chat_labels`: Alterações em etiquetas de conversas
- `blocks`: Bloqueios/desbloqueios
- `leads`: Atualizações de leads
- `sender`: Atualizações de campanhas, quando inicia, e quando completa

**Remover mensagens com base nos filtros**:
- `wasSentByApi`: Mensagens originadas pela API ⚠️ **IMPORTANTE:** Use sempre este filtro para evitar loops em automações
- `wasNotSentByApi`: Mensagens não originadas pela API
- `fromMeYes`: Mensagens enviadas pelo usuário
- `fromMeNo`: Mensagens recebidas de terceiros
- `isGroupYes`: Mensagens em grupos
- `isGroupNo`: Mensagens em conversas individuais

💡 **Prevenção de Loops Globais**: O webhook global recebe eventos de TODAS as instâncias. Se você tem automações que enviam mensagens via API, sempre inclua `"excludeMessages": ["wasSentByApi"]`. Caso prefira receber esses eventos, certifique-se de que sua automação detecta mensagens enviadas pela própria API para não criar loops infinitos em múltiplas instâncias.

**Parâmetros de URL**:
- `addUrlEvents` (boolean): Quando ativo, adiciona o tipo do evento como path parameter na URL.
  Exemplo: `https://api.example.com/webhook/{evento}`
- `addUrlTypesMessages` (boolean): Quando ativo, adiciona o tipo da mensagem como path parameter na URL.
  Exemplo: `https://api.example.com/webhook/{tipo_mensagem}`

**Combinações de Parâmetros**:
- Ambos ativos: `https://api.example.com/webhook/{evento}/{tipo_mensagem}`
  Exemplo real: `https://api.example.com/webhook/message/conversation`
- Apenas eventos: `https://api.example.com/webhook/message`
- Apenas tipos: `https://api.example.com/webhook/conversation`

**Notas Técnicas**:
1. Os parâmetros são adicionados na ordem: evento → tipo mensagem
2. A URL deve ser configurada para aceitar esses parâmetros dinâmicos
3. Funciona com qualquer combinação de eventos/mensagens


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| url | string (uri) | Sim | URL para receber os eventos |
| events | array | Sim | Lista de eventos monitorados |
| excludeMessages | array | Não | Filtros para excluir tipos de mensagens |
| addUrlEvents | boolean | Não | Adiciona o tipo do evento como parâmetro na URL. - `false` (padrão): URL normal - `true`: Adiciona evento na URL (ex: `/webhook/message`)  |
| addUrlTypesMessages | boolean | Não | Adiciona o tipo da mensagem como parâmetro na URL. - `false` (padrão): URL normal   - `true`: Adiciona tipo da mensagem (ex: `/webhook/conversation`)  |


**Respostas:**

#### 200

Webhook global configurado com sucesso

Content-Type: `application/json`

Schema: `Webhook`

#### 400

Payload inválido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Token de administrador não fornecido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 403

Token de administrador inválido ou servidor demo

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

### Ações na mensagem e Buscar


### POST /message/download

**Resumo:** Baixar arquivo de uma mensagem

Baixa o arquivo associado a uma mensagem de mídia (imagem, vídeo, áudio, documento ou sticker).

## Parâmetros

- **id** (string, obrigatório): ID da mensagem
- **return_base64** (boolean, default: false): Retorna arquivo em base64
- **generate_mp3** (boolean, default: true): Para áudios, define formato de retorno
  - `true`: Retorna MP3
  - `false`: Retorna OGG
- **return_link** (boolean, default: true): Retorna URL pública do arquivo
- **transcribe** (boolean, default: false): Transcreve áudios para texto
- **openai_apikey** (string, opcional): Chave OpenAI para transcrição
  - Se não informada, usa a chave salva na instância
  - Se informada, atualiza e salva na instância para próximas chamadas
- **download_quoted** (boolean, default: false): Baixa mídia da mensagem citada
  - Útil para baixar conteúdo original de status do WhatsApp
  - Quando uma mensagem é resposta a um status, permite baixar a mídia do status original
  - **Contextualização**: Ao baixar a mídia citada, você identifica o contexto da conversa
    - Exemplo: Se alguém responde a uma promoção, baixando a mídia você saberá que a pergunta é sobre aquela promoção específica

## Exemplos

### Baixar áudio como MP3:
```json
{
  "id": "7EB0F01D7244B421048F0706368376E0",
  "generate_mp3": true
}
```

### Transcrever áudio:
```json
{
  "id": "7EB0F01D7244B421048F0706368376E0",
  "transcribe": true
}
```

### Apenas base64 (sem salvar):
```json
{
  "id": "7EB0F01D7244B421048F0706368376E0",
  "return_base64": true,
  "return_link": false
}
```

### Baixar mídia de status (mensagem citada):
```json
{
  "id": "7EB0F01D7244B421048F0706368376E0",
  "download_quoted": true
}
```
*Útil quando o cliente responde a uma promoção/status - você baixa a mídia original para entender sobre qual produto/oferta ele está perguntando.*

## Resposta

```json
{
  "fileURL": "https://api.exemplo.com/files/arquivo.mp3",
  "mimetype": "audio/mpeg",
  "base64Data": "UklGRkj...",
  "transcription": "Texto transcrito"
}
```

**Nota**: 
- Por padrão, se não definido o contrário:
  1. áudios são retornados como MP3. 
  2. E todos os pedidos de download são retornados com URL pública.
- Transcrição requer chave OpenAI válida. A chave pode ser configurada uma vez na instância e será reutilizada automaticamente.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Sim | ID da mensagem contendo o arquivo |
| return_base64 | boolean | Não | Se verdadeiro, retorna o conteúdo em base64 |
| generate_mp3 | boolean | Não | Para áudios, define formato de retorno (true=MP3, false=OGG) |
| return_link | boolean | Não | Salva e retorna URL pública do arquivo |
| transcribe | boolean | Não | Se verdadeiro, transcreve áudios para texto |
| openai_apikey | string | Não | Chave da API OpenAI para transcrição (opcional) |
| download_quoted | boolean | Não | Se verdadeiro, baixa mídia da mensagem citada ao invés da mensagem principal |


**Respostas:**

#### 200

Successful file download

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| fileURL | string | Não | URL pública para acessar o arquivo (se return_link=true) |
| mimetype | string | Sim | Tipo MIME do arquivo |
| base64Data | string | Não | Conteúdo do arquivo em base64 (se return_base64=true) |
| transcription | string | Não | Texto transcrito do áudio (se transcribe=true) |

#### 400

Bad Request

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Unauthorized

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 404

Not Found

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Internal Server Error

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /message/find

**Resumo:** Buscar mensagens em um chat

Busca mensagens com múltiplos filtros disponíveis. Este endpoint permite:

1. **Busca por ID específico**: Use `id` para encontrar uma mensagem exata
2. **Filtrar por chat**: Use `chatid` para mensagens de uma conversa específica
3. **Filtrar por rastreamento**: Use `track_source` e `track_id` para mensagens com dados de tracking
4. **Limitar resultados**: Use `limit` para controlar quantas mensagens retornar
5. **Ordenação**: Resultados ordenados por data (mais recentes primeiro)


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Não | ID específico da mensagem para busca exata |
| chatid | string | Não | ID do chat no formato internacional |
| track_source | string | Não | Origem do rastreamento para filtrar mensagens |
| track_id | string | Não | ID de rastreamento para filtrar mensagens |
| limit | integer | Não | Numero maximo de mensagens a retornar (padrao 100) |
| offset | integer | Não | Deslocamento para paginacao (0 retorna as mensagens mais recentes) |


**Respostas:**

#### 200

Lista de mensagens encontradas com metadados de paginacao

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| returnedMessages | integer | Não | Quantidade de mensagens retornadas nesta pagina |
| messages | array | Não |  |
| limit | integer | Não | Limite aplicado na busca |
| offset | integer | Não | Offset usado para recuperar os resultados |
| nextOffset | integer | Não | Offset sugerido para a proxima pagina |
| hasMore | boolean | Não | Indica se existem mais mensagens apos esta pagina |

#### 400

Parametros invalidos

#### 401

Token invalido ou expirado

#### 404

Chat nao encontrado

#### 500

Erro interno do servidor


### POST /message/markread

**Resumo:** Marcar mensagens como lidas

Marca uma ou mais mensagens como lidas. Este endpoint permite:
1. Marcar múltiplas mensagens como lidas de uma vez
2. Atualizar o status de leitura no WhatsApp
3. Sincronizar o status de leitura entre dispositivos

Exemplo de requisição básica:
```json
{
  "id": [
    "62AD1AD844E518180227BF68DA7ED710",
    "ECB9DE48EB41F77BFA8491BFA8D6EF9B"  
  ]
}
```

Exemplo de resposta:
```json
{
  "success": true,
  "message": "Messages marked as read",
  "markedMessages": [
    {
      "id": "62AD1AD844E518180227BF68DA7ED710",
      "timestamp": 1672531200000
    },
    {
      "id": "ECB9DE48EB41F77BFA8491BFA8D6EF9B",
      "timestamp": 1672531300000
    }
  ]
}
```

Parâmetros disponíveis:
- id: Lista de IDs das mensagens a serem marcadas como lidas

Erros comuns:
- 401: Token inválido ou expirado
- 400: Lista de IDs vazia ou inválida
- 404: Uma ou mais mensagens não encontradas
- 500: Erro ao marcar mensagens como lidas


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | array | Sim | Lista de IDs das mensagens a serem marcadas como lidas |


**Respostas:**

#### 200

Messages successfully marked as read

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| results | array | Não |  |

#### 400

Invalid request payload or missing required fields

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Unauthorized - invalid or missing token

#### 500

Server error while processing the request


### POST /message/react

**Resumo:** Enviar reação a uma mensagem

Envia uma reação (emoji) a uma mensagem específica. Este endpoint permite:

1. Adicionar ou remover reações em mensagens

2. Usar qualquer emoji Unicode válido

3. Reagir a mensagens em chats individuais ou grupos

4. Remover reações existentes

5. Verificar o status da reação enviada


Tipos de reações suportados:

- Qualquer emoji Unicode válido (👍, ❤️, 😂, etc)

- String vazia para remover reação


Exemplo de requisição básica:

```json

{
  "number": "5511999999999@s.whatsapp.net",
  "text": "👍",
  "id": "3EB0538DA65A59F6D8A251"
}

```


Exemplo de requisição para remover reação:

```json

{
  "number": "5511999999999@s.whatsapp.net",
  "text": "",
  "id": "3EB0538DA65A59F6D8A251"
}

```


Exemplo de resposta:

```json

{
  "success": true,
  "message": "Reaction sent",
  "reaction": {
    "id": "3EB0538DA65A59F6D8A251",
    "emoji": "👍",
    "timestamp": 1672531200000,
    "status": "sent"
  }
}

```


Exemplo de resposta ao remover reação:

```json

{
  "success": true,
  "message": "Reaction removed",
  "reaction": {
    "id": "3EB0538DA65A59F6D8A251",
    "emoji": null,
    "timestamp": 1672531200000,
    "status": "removed"
  }
}

```


Parâmetros disponíveis:

- number: Número do chat no formato internacional (ex:
5511999999999@s.whatsapp.net)

- text: Emoji Unicode da reação (ou string vazia para remover reação)

- id: ID da mensagem que receberá a reação


Erros comuns:

- 401: Token inválido ou expirado

- 400: Número inválido ou emoji não suportado

- 404: Mensagem não encontrada

- 500: Erro ao enviar reação


Limitações:

- Só é possível reagir a mensagens enviadas por outros usuários

- Não é possível reagir a mensagens antigas (mais de 7 dias)

- O mesmo usuário só pode ter uma reação ativa por mensagem


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do chat no formato internacional |
| text | string | Sim | Emoji Unicode da reação (ou string vazia para remover reação) |
| id | string | Sim | ID da mensagem que receberá a reação |


**Respostas:**

#### 200

Reação enviada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Não | ID único da mensagem de reação |
| messageid | string | Não | ID gerado para a mensagem de reação |
| content | object | Não | Detalhes da reação |
| messageTimestamp | number | Não | Timestamp da mensagem em milissegundos |
| messageType | string | Não | Tipo da mensagem |
| status | string | Não | Status atual da mensagem |
| owner | string | Não | Proprietário da instância |

#### 400

Erro nos dados da requisição

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Não autorizado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 404

Mensagem não encontrada

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /message/delete

**Resumo:** Apagar Mensagem Para Todos

Apaga uma mensagem para todos os participantes da conversa.

### Funcionalidades:
- Apaga mensagens em conversas individuais ou grupos
- Funciona com mensagens enviadas pelo usuário ou recebidas
- Atualiza o status no banco de dados
- Envia webhook de atualização

**Notas Técnicas**:
1. O ID da mensagem pode ser fornecido em dois formatos:
   - ID completo (contém ":"): usado diretamente
   - ID curto: concatenado com o owner para busca
2. Gera evento webhook do tipo "messages_update"
3. Atualiza o status da mensagem para "Deleted"


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Sim | ID da mensagem a ser apagada |


**Respostas:**

#### 200

Mensagem apagada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| timestamp | string (date-time) | Não |  |
| id | string | Não |  |

#### 400

Payload inválido ou ID de chat/sender inválido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Token não fornecido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 404

Mensagem não encontrada

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor ou sessão não iniciada

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /message/edit

**Resumo:** Edita uma mensagem enviada

Edita o conteúdo de uma mensagem já enviada usando a funcionalidade nativa do WhatsApp.

O endpoint realiza:
- Busca a mensagem original no banco de dados usando o ID fornecido
- Edita o conteúdo da mensagem para o novo texto no WhatsApp
- Gera um novo ID para a mensagem editada
- Retorna objeto de mensagem completo seguindo o padrão da API
- Dispara eventos SSE/Webhook automaticamente

**Importante**: 
- Só é possível editar mensagens enviadas pela própria instância
- A mensagem deve existir no banco de dados
- O ID pode ser fornecido no formato completo (owner:messageid) ou apenas messageid
- A mensagem deve estar dentro do prazo permitido pelo WhatsApp para edição


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Sim | ID único da mensagem que será editada (formato owner:messageid ou apenas messageid) |
| text | string | Sim | Novo conteúdo de texto da mensagem |


**Respostas:**

#### 200

Mensagem editada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Não | ID único da mensagem no formato owner:messageid |
| messageid | string | Não | ID da mensagem no WhatsApp |
| content | string | Não | Conteúdo da mensagem editada |
| messageTimestamp | integer | Não | Timestamp da mensagem (Unix timestamp em milissegundos) |
| messageType | string | Não | Tipo da mensagem |
| status | string | Não | Status da mensagem |
| owner | string | Não | Proprietário da instância |

#### 400

Dados inválidos na requisição

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Sem sessão ativa

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 404

Mensagem não encontrada

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

### Bloqueios


### POST /chat/block

**Resumo:** Bloqueia ou desbloqueia contato do WhatsApp

Bloqueia ou desbloqueia um contato do WhatsApp. Contatos bloqueados não podem enviar mensagens 
para a instância e a instância não pode enviar mensagens para eles.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do WhatsApp no formato internacional (ex. 5511999999999) |
| block | boolean | Sim | True para bloquear, False para desbloquear |


**Respostas:**

#### 200

Operação realizada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não | Mensagem de confirmação |
| blockList | array | Não | Lista atualizada de contatos bloqueados |

#### 401

Não autorizado - token inválido

#### 404

Contato não encontrado

#### 500

Erro do servidor ao processar a requisição


### GET /chat/blocklist

**Resumo:** Lista contatos bloqueados

Retorna a lista completa de contatos que foram bloqueados pela instância.
Esta lista é atualizada em tempo real conforme contatos são bloqueados/desbloqueados.


**Respostas:**

#### 200

Lista de contatos bloqueados recuperada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| blockList | array | Não |  |

#### 401

Token inválido ou não fornecido

#### 500

Erro interno do servidor ou instância não conectada

### CRM


### POST /instance/updateFieldsMap

**Resumo:** Atualizar campos personalizados de leads

Atualiza os campos personalizados (custom fields) de uma instância. 
Permite configurar até 20 campos personalizados para armazenamento de 
informações adicionais sobre leads.

Cada campo pode armazenar até 255 caracteres e aceita qualquer tipo de dado.

Campos disponíveis:
- lead_field01 a lead_field20

Exemplo de uso:
1. Armazenar informações adicionais sobre leads
2. Criar campos personalizados para integração com outros sistemas
3. Armazenar tags ou categorias personalizadas
4. Manter histórico de interações com o lead

Exemplo de requisição:
```json
{
  "lead_field01": "nome",
  "lead_field02": "email",
  "lead_field03": "telefone",
  "lead_field04": "cidade",
  "lead_field05": "estado",
  "lead_field06": "idade",
  "lead_field07": "interesses",
  "lead_field08": "origem",
  "lead_field09": "status",
  "lead_field10": "valor",
  "lead_field11": "observacoes",
  "lead_field12": "ultima_interacao",
  "lead_field13": "proximo_contato",
  "lead_field14": "vendedor",
  "lead_field15": "produto_interesse",
  "lead_field16": "fonte_captacao",
  "lead_field17": "score",
  "lead_field18": "tags",
  "lead_field19": "historico",
  "lead_field20": "custom"
}
```

Exemplo de resposta:
```json
{
  "success": true,
  "message": "Custom fields updated successfully",
  "instance": {
    "id": "r183e2ef9597845",
    "name": "minha-instancia",
    "fieldsMap": {
      "lead_field01": "nome",
      "lead_field02": "email",
      "lead_field03": "telefone",
      "lead_field04": "cidade",
      "lead_field05": "estado",
      "lead_field06": "idade",
      "lead_field07": "interesses",
      "lead_field08": "origem",
      "lead_field09": "status",
      "lead_field10": "valor",
      "lead_field11": "observacoes",
      "lead_field12": "ultima_interacao",
      "lead_field13": "proximo_contato",
      "lead_field14": "vendedor",
      "lead_field15": "produto_interesse",
      "lead_field16": "fonte_captacao",
      "lead_field17": "score",
      "lead_field18": "tags",
      "lead_field19": "historico",
      "lead_field20": "custom"
    }
  }
}
```

Erros comuns:
- 400: Campos inválidos ou payload mal formatado
- 401: Token inválido ou expirado
- 404: Instância não encontrada
- 500: Erro ao atualizar campos no banco de dados

Restrições:
- Cada campo pode ter no máximo 255 caracteres
- Campos vazios serão mantidos com seus valores atuais
- Apenas os campos enviados serão atualizados


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| lead_field01 | string | Não | Campo personalizado 01 |
| lead_field02 | string | Não | Campo personalizado 02 |
| lead_field03 | string | Não | Campo personalizado 03 |
| lead_field04 | string | Não | Campo personalizado 04 |
| lead_field05 | string | Não | Campo personalizado 05 |
| lead_field06 | string | Não | Campo personalizado 06 |
| lead_field07 | string | Não | Campo personalizado 07 |
| lead_field08 | string | Não | Campo personalizado 08 |
| lead_field09 | string | Não | Campo personalizado 09 |
| lead_field10 | string | Não | Campo personalizado 10 |
| lead_field11 | string | Não | Campo personalizado 11 |
| lead_field12 | string | Não | Campo personalizado 12 |
| lead_field13 | string | Não | Campo personalizado 13 |
| lead_field14 | string | Não | Campo personalizado 14 |
| lead_field15 | string | Não | Campo personalizado 15 |
| lead_field16 | string | Não | Campo personalizado 16 |
| lead_field17 | string | Não | Campo personalizado 17 |
| lead_field18 | string | Não | Campo personalizado 18 |
| lead_field19 | string | Não | Campo personalizado 19 |
| lead_field20 | string | Não | Campo personalizado 20 |


**Respostas:**

#### 200

Sucesso

Content-Type: `application/json`

Schema: `Instance`

#### 401

Token inválido/expirado

#### 404

Instância não encontrada

#### 500

Erro interno


### POST /chat/editLead

**Resumo:** Edita informações de lead

Atualiza as informações de lead associadas a um chat. Permite modificar status do ticket, 
atribuição de atendente, posição no kanban, tags e outros campos customizados.

As alterações são refletidas imediatamente no banco de dados e disparam eventos webhook/SSE
para manter a aplicação sincronizada.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Sim | Identificador do chat. Pode ser: - wa_chatid (ex: "5511999999999@s.whatsapp.net") - wa_fastid (ex: "5511888888888:5511999999999")  |
| chatbot_disableUntil | integer (int64) | Não | Timestamp UTC até quando o chatbot deve ficar desativado para este chat. Use 0 para reativar imediatamente.  |
| lead_isTicketOpen | boolean | Não | Status do ticket associado ao lead. - true: Ticket está aberto/em atendimento - false: Ticket está fechado/resolvido  |
| lead_assignedAttendant_id | string | Não | ID do atendente atribuído ao lead. Use string vazia ("") para remover a atribuição.  |
| lead_kanbanOrder | integer (int64) | Não | Posição do card no quadro kanban. Valores maiores aparecem primeiro.  |
| lead_tags | array | Não | Lista de tags associadas ao lead. Tags inexistentes são criadas automaticamente. Envie array vazio ([]) para remover todas as tags.  |
| lead_name | string | Não | Nome principal do lead |
| lead_fullName | string | Não | Nome completo do lead |
| lead_email | string (email) | Não | Email do lead |
| lead_personalId | string | Não | Documento de identificação (CPF/CNPJ) Apenas números ou formatado  |
| lead_status | string | Não | Status do lead no funil de vendas |
| lead_notes | string | Não | Anotações sobre o lead |
| lead_field01 | string | Não | Campo personalizado 1 |
| lead_field02 | string | Não | Campo personalizado 2 |
| lead_field03 | string | Não | Campo personalizado 3 |
| lead_field04 | string | Não | Campo personalizado 4 |
| lead_field05 | string | Não | Campo personalizado 5 |
| lead_field06 | string | Não | Campo personalizado 6 |
| lead_field07 | string | Não | Campo personalizado 7 |
| lead_field08 | string | Não | Campo personalizado 8 |
| lead_field09 | string | Não | Campo personalizado 9 |
| lead_field10 | string | Não | Campo personalizado 10 |
| lead_field11 | string | Não | Campo personalizado 11 |
| lead_field12 | string | Não | Campo personalizado 12 |
| lead_field13 | string | Não | Campo personalizado 13 |
| lead_field14 | string | Não | Campo personalizado 14 |
| lead_field15 | string | Não | Campo personalizado 15 |
| lead_field16 | string | Não | Campo personalizado 16 |
| lead_field17 | string | Não | Campo personalizado 17 |
| lead_field18 | string | Não | Campo personalizado 18 |
| lead_field19 | string | Não | Campo personalizado 19 |
| lead_field20 | string | Não | Campo personalizado 20 |


**Respostas:**

#### 200

Lead atualizado com sucesso

Content-Type: `application/json`

Schema: `Chat`

#### 400

Payload inválido

#### 404

Chat não encontrado

#### 500

Erro interno do servidor

### Chamadas


### POST /call/make

**Resumo:** Iniciar chamada de voz

Inicia uma chamada de voz para um contato específico. Este endpoint permite:
1. Iniciar chamadas de voz para contatos
2. Funciona apenas com números válidos do WhatsApp
3. O contato receberá uma chamada de voz

**Nota**: O telefone do contato tocará normalmente, mas ao contato atender, ele não ouvirá nada, e você também não ouvirá nada. 
Este endpoint apenas inicia a chamada, não estabelece uma comunicação de voz real.

Exemplo de requisição:
```json
{
  "number": "5511999999999"
}
```

Exemplo de resposta:
```json
{
  "response": "Call successful"
}
```

Erros comuns:
- 401: Token inválido ou expirado
- 400: Número inválido ou ausente
- 500: Erro ao iniciar chamada


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do contato no formato internacional (ex: 5511999999999) |


**Respostas:**

#### 200

Chamada iniciada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não | Mensagem de confirmação |

#### 400

Requisição inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Descrição do erro |

#### 401

Token inválido ou expirado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Descrição do erro de autenticação |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Descrição do erro interno |


### POST /call/reject

**Resumo:** Rejeitar chamada recebida

Rejeita uma chamada recebida do WhatsApp. Este endpoint permite:
1. Rejeitar chamadas de voz ou vídeo recebidas
2. Necessita do número do contato que está ligando
3. Necessita do ID da chamada para identificação

Exemplo de requisição:
```json
{
  "number": "5511999999999",
  "id": "ABEiGmo8oqkAcAKrBYQAAAAA_1"
}
```

Exemplo de resposta:
```json
{
  "response": "Call rejected"
}
```

Erros comuns:
- 401: Token inválido ou expirado
- 400: Número inválido ou ID da chamada ausente
- 500: Erro ao rejeitar chamada


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do contato no formato internacional (ex: 5511999999999) |
| id | string | Sim | ID único da chamada a ser rejeitada |


**Respostas:**

#### 200

Chamada rejeitada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não | Mensagem de confirmação |

#### 400

Requisição inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Descrição do erro |

#### 401

Token inválido ou expirado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Descrição do erro de autenticação |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Descrição do erro interno |

### Chatbot Configurações


### POST /instance/updatechatbotsettings

**Resumo:** Chatbot Configurações

Explicação dos campos:


- `openai_apikey`: Chave da API OpenAI (começa com "sk-")  

- `chatbot_enabled`: Habilita/desabilita o chatbot  

- `chatbot_ignoreGroups`: Define se o chatbot deve ignorar mensagens de grupos  

- `chatbot_stopConversation`: Palavra-chave que os usuários podem usar para parar o chatbot  

- `chatbot_stopMinutes`: Por quantos minutos o chatbot deve ficar desativado após receber o comando de parada  

- `chatbot_stopWhenYouSendMsg`: Por quantos minutos o chatbot deve ficar desativado após você enviar uma mensagem fora da API, 0 desliga.


**Request Body:**

Content-Type: `application/json`


**Respostas:**

#### 200

Sucesso

Content-Type: `application/json`

Schema: `Instance`

#### 401

Token inválido/expirado

#### 404

Instância não encontrada

#### 500

Erro interno

### Chatbot Trigger


### POST /trigger/edit

**Resumo:** Criar, atualizar ou excluir um trigger do chatbot

Endpoint para gerenciar triggers do chatbot. Suporta:
- Criação de novos triggers
- Atualização de triggers existentes
- Exclusão de triggers por ID


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Não | ID do trigger. Vazio para criação, obrigatório para atualização/exclusão |
| delete | boolean | Não | Quando verdadeiro, exclui o trigger especificado pelo id |
| trigger | object | Sim |  |


**Respostas:**

#### 200

Trigger atualizado com sucesso

Content-Type: `application/json`

Schema: `ChatbotTrigger`

#### 201

Trigger criado com sucesso

Content-Type: `application/json`

Schema: `ChatbotTrigger`

#### 400

Corpo da requisição inválido ou campos obrigatórios ausentes

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 404

Trigger não encontrado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro no servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### GET /trigger/list

**Resumo:** Listar todos os triggers do chatbot

Retorna a lista completa de triggers configurados para a instância atual

**Parâmetros:**

| Nome | Localização | Tipo | Obrigatório | Descrição |
|------|-------------|------|-------------|----------|

**Respostas:**

#### 200

Lista de triggers retornada com sucesso

Content-Type: `application/json`

#### 401

Não autorizado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro no servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

### Chats


### POST /chat/delete

**Resumo:** Deleta chat

Deleta um chat e/ou suas mensagens do WhatsApp e/ou banco de dados. 
Você pode escolher deletar:
- Apenas do WhatsApp
- Apenas do banco de dados
- Apenas as mensagens do banco de dados
- Qualquer combinação das opções acima


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do chat no formato internacional. Para grupos use o ID completo do grupo.  |
| deleteChatDB | boolean | Não | Se true, deleta o chat do banco de dados |
| deleteMessagesDB | boolean | Não | Se true, deleta todas as mensagens do chat do banco de dados |
| deleteChatWhatsApp | boolean | Não | Se true, deleta o chat do WhatsApp |


**Respostas:**

#### 200

Operação realizada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não | Mensagem de sucesso |
| actions | array | Não | Lista de ações realizadas |
| errors | array | Não | Lista de erros ocorridos, se houver |

#### 400

Erro nos parâmetros da requisição

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Token inválido ou não fornecido

#### 404

Chat não encontrado

#### 500

Erro interno do servidor


### POST /chat/archive

**Resumo:** Arquivar/desarquivar chat

Altera o estado de arquivamento de um chat do WhatsApp.
- Quando arquivado, o chat é movido para a seção de arquivados no WhatsApp
- A ação é sincronizada entre todos os dispositivos conectados
- Não afeta as mensagens ou o conteúdo do chat


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do telefone (formato E.164) ou ID do grupo |
| archive | boolean | Sim | true para arquivar, false para desarquivar |


**Respostas:**

#### 200

Chat arquivado/desarquivado com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não |  |

#### 400

Dados da requisição inválidos

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Token de autenticação ausente ou inválido

#### 500

Erro ao executar a operação

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /chat/read

**Resumo:** Marcar chat como lido/não lido

Atualiza o status de leitura de um chat no WhatsApp.

Quando um chat é marcado como lido:
- O contador de mensagens não lidas é zerado
- O indicador visual de mensagens não lidas é removido
- O remetente recebe confirmação de leitura (se ativado)

Quando marcado como não lido:
- O chat aparece como pendente de leitura
- Não afeta as confirmações de leitura já enviadas


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Identificador do chat no formato: - Para usuários: [número]@s.whatsapp.net (ex: 5511999999999@s.whatsapp.net) - Para grupos: [id-grupo]@g.us (ex: 123456789-987654321@g.us)  |
| read | boolean | Sim | - true: marca o chat como lido - false: marca o chat como não lido  |


**Respostas:**

#### 200

Status de leitura atualizado com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não |  |

#### 401

Token de autenticação ausente ou inválido

#### 404

Chat não encontrado

#### 500

Erro ao atualizar status de leitura


### POST /chat/mute

**Resumo:** Silenciar chat

Silencia notificações de um chat por um período específico. 
As opções de silenciamento são:
* 0 - Remove o silenciamento
* 8 - Silencia por 8 horas
* 168 - Silencia por 1 semana (168 horas)
* -1 - Silencia permanentemente


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | ID do chat no formato 123456789@s.whatsapp.net ou 123456789-123456@g.us |
| muteEndTime | integer | Sim | Duração do silenciamento: * 0 = Remove silenciamento * 8 = Silencia por 8 horas * 168 = Silencia por 1 semana * -1 = Silencia permanentemente  |


**Respostas:**

#### 200

Chat silenciado com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não |  |

#### 400

Duração inválida ou formato de número incorreto

#### 401

Token inválido ou ausente

#### 404

Chat não encontrado


### POST /chat/pin

**Resumo:** Fixar/desafixar chat

Fixa ou desafixa um chat no topo da lista de conversas. Chats fixados permanecem 
no topo mesmo quando novas mensagens são recebidas em outros chats.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do chat no formato internacional completo (ex: "5511999999999")  ou ID do grupo (ex: "123456789-123456@g.us")  |
| pin | boolean | Sim | Define se o chat deve ser fixado (true) ou desafixado (false)  |


**Respostas:**

#### 200

Chat fixado/desafixado com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não | Mensagem de confirmação |

#### 400

Erro na requisição

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Descrição do erro |

#### 401

Não autorizado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Mensagem de erro de autenticação |


### POST /chat/find

**Resumo:** Busca chats com filtros

Busca chats com diversos filtros e ordenação. Suporta filtros em todos os campos do chat, 
paginação e ordenação customizada.

Operadores de filtro:
- `~` : LIKE (contém)
- `!~` : NOT LIKE (não contém)
- `!=` : diferente
- `>=` : maior ou igual
- `>` : maior que
- `<=` : menor ou igual
- `<` : menor que
- Sem operador: LIKE (contém)


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| operator | string | Não | Operador lógico entre os filtros |
| sort | string | Não | Campo para ordenação (+/-campo). Ex -wa_lastMsgTimestamp |
| limit | integer | Não | Limite de resultados por página |
| offset | integer | Não | Offset para paginação |
| wa_fastid | string | Não |  |
| wa_chatid | string | Não |  |
| wa_archived | boolean | Não |  |
| wa_contactName | string | Não |  |
| wa_name | string | Não |  |
| name | string | Não |  |
| wa_isBlocked | boolean | Não |  |
| wa_isGroup | boolean | Não |  |
| wa_isGroup_admin | boolean | Não |  |
| wa_isGroup_announce | boolean | Não |  |
| wa_isGroup_member | boolean | Não |  |
| wa_isPinned | boolean | Não |  |
| wa_label | string | Não |  |
| lead_tags | string | Não |  |
| lead_isTicketOpen | boolean | Não |  |
| lead_assignedAttendant_id | string | Não |  |
| lead_status | string | Não |  |


**Respostas:**

#### 200

Lista de chats encontrados

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| chats | array | Não |  |
| totalChatsStats | object | Não | Contadores totais de chats |
| pagination | object | Não |  |

### Configuração do Agente de IA


### POST /agent/edit

**Resumo:** Criar/Editar Agente

# Documentação dos Campos de Configuração

## Campos Básicos

### Nome e Identificação

O agente precisa ser configurado com informações básicas que determinam sua identidade e funcionamento.

#### Nome do Agente
**name**: Define como o agente será identificado nas conversas.

Exemplos válidos:
- "Assistente de Vendas"
- "Suporte Técnico" 
- "João"
- "Maria"

#### Provedor do Serviço
**provider**: Especifica qual serviço de IA será utilizado.

Provedores disponíveis:
- "openai" (ChatGPT)
- "anthropic" (Claude)
- "gemini" (Google)
- "deepseek" (DeepSeek)

#### Chave de API
**apikey**: Credencial necessária para autenticação com o provedor escolhido.
- Deve ser obtida através do site oficial do provedor selecionado
- Mantenha esta chave em segurança e nunca a compartilhe

### Configuração do Modelo

#### Seleção do Modelo
**model**: Especifica qual modelo de IA será utilizado. A disponibilidade depende do provedor selecionado.

##### OpenAI
Documentação: https://platform.openai.com/docs/models
- gpt-4o
- gpt-4o-mini
- gpt-3.5-turbo

##### Claude
Documentação: https://docs.anthropic.com/en/docs/about-claude/models
- claude-3-5-sonnet-latest
- claude-3-5-haiku-latest
- claude-3-opus-latest

##### Gemini
Documentação: https://ai.google.dev/models/gemini
- gemini-2.0-flash-exp
- gemini-1.5-pro
- gemini-1.5-flash

##### DeepSeek
Documentação: https://api-docs.deepseek.com/quick_start/pricing
- deepseek-chat
- deepseek-reasoner

        

## Configurações de Comportamento


### Prompt Base (**basePrompt**)


Instruções iniciais para definir o comportamento do agente
    
Exemplo para assistente de vendas:

"Você é um assistente especializado em vendas, focado em ajudar clientes a encontrar os produtos ideais. Mantenha um tom profissional e amigável."
        
Exemplo para suporte:

"Você é um agente de suporte técnico especializado em nossos produtos. Forneça respostas claras e objetivas para ajudar os clientes a resolverem seus problemas."

        

### Parâmetros de Geração


- **temperature**: Controla a criatividade das respostas (0-100)
    
    - 0-30: Respostas mais conservadoras e precisas
        
    - 30-70: Equilíbrio entre criatividade e precisão
        
    - 70-100: Respostas mais criativas e variadas

        
- **maxTokens**: Limite máximo de tokens por resposta
    
    - Recomendado: 1000-4000 para respostas detalhadas
        
    - Para respostas curtas: 500-1000
        
    - Limite máximo varia por modelo

        
- **diversityLevel**: Controla a diversidade das respostas (0-100)
    
    - Valores mais altos geram respostas mais variadas
        
    - Recomendado: 30-70 para uso geral

        
- **frequencyPenalty**: Penalidade para repetição de palavras (0-100)
    
    - Valores mais altos reduzem repetições
        
    - Recomendado: 20-50 para comunicação natural

        
- **presencePenalty**: Penalidade para manter foco no tópico (0-100)
    
    - Valores mais altos incentivam mudanças de tópico
        
    - Recomendado: 10-30 para manter coerência

        

## Configurações de Interação


### Mensagens


- **signMessages**: Se verdadeiro, adiciona a assinatura do agente nas mensagens
    
    - Útil para identificar quem está enviando a mensagem

        
- **readMessages**: Se verdadeiro, marca as mensagens como lidas ao responder
    
    - Recomendado para simular comportamento humano

        

## Exemplos de Configuração


### Assistente de Vendas


``` json

{
  "name": "Assistente de Vendas",
  "provider": "openai",
  "model": "gpt-4",
  "basePrompt": "Você é um assistente de vendas especializado...",
  "temperature": 70,
  "maxTokens": 2000,
  "diversityLevel": 50,
  "frequencyPenalty": 30,
  "presencePenalty": 20,
  "signMessages": true,
  "readMessages": true
}

  ```

### Suporte Técnico


``` json

{
  "name": "Suporte Técnico",
  "provider": "anthropic",
  "model": "claude-3-sonnet-20240229",
  "basePrompt": "Você é um agente de suporte técnico...",
  "temperature": 30,
  "maxTokens": 3000,
  "diversityLevel": 40,
  "frequencyPenalty": 40,
  "presencePenalty": 15,
  "signMessages": true,
  "readMessages": true
}

  ```

## Dicas de Otimização


1. **Ajuste Gradual**: Comece com valores moderados e ajuste conforme necessário
    
2. **Teste o Base Prompt**: Verifique se as instruções estão claras e completas
    
3. **Monitore o Desempenho**: Observe as respostas e ajuste os parâmetros para melhor adequação
    
4. **Backup**: Mantenha um backup das configurações que funcionaram bem
    
5. **Documentação**: Registre as alterações e seus impactos para referência futura


**Request Body:**

Content-Type: `application/json`


**Respostas:**

#### 200

Agente atualizado com sucesso

Content-Type: `application/json`

Schema: `ChatbotAIAgent`

#### 201

Novo agente criado com sucesso

Content-Type: `application/json`

Schema: `ChatbotAIAgent`

#### 400

Erro na requisição

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Não autorizado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 404

Agente não encontrado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### GET /agent/list

**Resumo:** Todos os agentes

**Parâmetros:**

| Nome | Localização | Tipo | Obrigatório | Descrição |
|------|-------------|------|-------------|----------|

**Respostas:**

#### 200

Lista de todos os agentes de IA

Content-Type: `application/json`

#### 401

Sessão não encontrada

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro ao buscar agentes

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

### Conhecimento dos Agentes


### POST /knowledge/edit

**Resumo:** Criar/Editar Conhecimento do Agente

Gerencia o conhecimento base usado pelos agentes de IA para responder consultas.
O conhecimento pode ser fornecido como texto direto ou através de arquivos PDF/CSV.

Características principais:
- Suporta criação, edição e exclusão de conhecimento
- Aceita conteúdo em:
  - Texto puro
  - URLs públicas
  - Base64 encoded de arquivos
  - Upload direto de arquivos
- Formatos suportados: PDF, CSV, TXT, HTML
- Processa automaticamente qualquer formato de entrada
- Vetoriza automaticamente o conteúdo para busca semântica

Nota sobre URLs e Base64:
- URLs devem ser públicas e acessíveis
- Para PDFs/CSVs, especifique fileType se não for detectável da extensão
- Base64 deve incluir o encoding completo do arquivo
- O servidor detecta e processa automaticamente conteúdo Base64


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Não | ID do conhecimento (vazio para criar novo) |
| delete | boolean | Não | Define se é uma operação de exclusão |
| knowledge | object | Não |  |
| fileType | string | Não | Tipo do arquivo quando não detectado automaticamente |


**Respostas:**

#### 200

Conhecimento atualizado com sucesso

Content-Type: `application/json`

Schema: `ChatbotAIKnowledge`

#### 201

Novo conhecimento criado com sucesso

Content-Type: `application/json`

Schema: `ChatbotAIKnowledge`

#### 400

Requisição inválida

#### 404

Conhecimento não encontrado

#### 500

Erro interno do servidor


### GET /knowledge/list

**Resumo:** Listar Base de Conhecimento

Retorna todos os conhecimentos cadastrados para o agente de IA da instância.
Estes conhecimentos são utilizados pelo chatbot para responder perguntas
e interagir com os usuários de forma contextualizada.


**Parâmetros:**

| Nome | Localização | Tipo | Obrigatório | Descrição |
|------|-------------|------|-------------|----------|

**Respostas:**

#### 200

Lista de conhecimentos recuperada com sucesso

Content-Type: `application/json`

#### 401

Token de autenticação ausente ou inválido

#### 500

Erro interno do servidor ao buscar conhecimentos

### Contatos


### GET /contacts

**Resumo:** Retorna lista de contatos do WhatsApp

Retorna a lista de contatos salvos na agenda do celular e que estão no WhatsApp.

O endpoint realiza:
- Busca todos os contatos armazenados
- Retorna dados formatados incluindo JID e informações de nome


**Respostas:**

#### 200

Lista de contatos retornada com sucesso

Content-Type: `application/json`

#### 401

Sem sessão ativa

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /contacts/list

**Resumo:** Listar todos os contatos com paginacao

Retorna uma lista paginada de contatos da instancia do WhatsApp. 
Use este endpoint (POST) para controlar pagina, tamanho e offset via corpo da requisicao.
A rota GET `/contacts` continua disponivel para quem prefere a lista completa sem paginacao.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| page | integer | Não | Numero da pagina para paginacao (padrao 1) |
| pageSize | integer | Não | Quantidade de resultados por pagina (padrao 100, maximo 1000) |
| limit | integer | Não | Alias opcional para `pageSize` |
| offset | integer | Não | Deslocamento base zero para paginacao; se informado recalcula a pagina |


**Respostas:**

#### 200

Lista de contatos recuperada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| contacts | array | Não |  |
| pagination | object | Não |  |

#### 401

Token nao fornecido ou invalido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor ao recuperar contatos

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Mensagem detalhando o erro encontrado |


### POST /contact/add

**Resumo:** Adiciona um contato à agenda

Adiciona um novo contato à agenda do celular.

O endpoint realiza:
- Adiciona o contato à agenda usando o WhatsApp
- Usa o campo 'name' tanto para o nome completo quanto para o primeiro nome
- Salva as informações do contato na agenda do WhatsApp
- Retorna informações do contato adicionado


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| phone | string | Sim | Número de telefone no formato internacional com código do país obrigatório.  Para Brasil, deve começar com 55. Aceita variações com/sem símbolo +,  com/sem parênteses, com/sem hífen e com/sem espaços. Também aceita formato  JID do WhatsApp (@s.whatsapp.net). Não aceita contatos comerciais (@lid)  nem grupos (@g.us).  |
| name | string | Sim | Nome completo do contato (será usado como primeiro nome e nome completo) |


**Respostas:**

#### 200

Contato adicionado com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| success | boolean | Não |  |
| message | string | Não |  |
| contact | object | Não |  |

#### 400

Dados inválidos na requisição

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Sem sessão ativa

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /contact/remove

**Resumo:** Remove um contato da agenda

Remove um contato da agenda do celular.

O endpoint realiza:
- Remove o contato da agenda usando o WhatsApp AppState
- Atualiza a lista de contatos sincronizada
- Retorna confirmação da remoção


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| phone | string | Sim | Número de telefone no formato internacional com código do país obrigatório.  Para Brasil, deve começar com 55. Aceita variações com/sem símbolo +,  com/sem parênteses, com/sem hífen e com/sem espaços. Também aceita formato  JID do WhatsApp (@s.whatsapp.net). Não aceita contatos comerciais (@lid)  nem grupos (@g.us).  |


**Respostas:**

#### 200

Contato removido com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| success | boolean | Não |  |
| message | string | Não |  |
| removed_contact | object | Não |  |

#### 400

Dados inválidos na requisição

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Sem sessão ativa

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 404

Contato não encontrado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /chat/details

**Resumo:** Obter Detalhes Completos

Retorna informações **completas** sobre um contato ou chat, incluindo **todos os campos disponíveis** do modelo Chat.

### Funcionalidades:
- **Retorna chat completo**: Todos os campos do modelo Chat (mais de 60 campos)
- **Busca informações para contatos individuais e grupos**
- **URLs de imagem em dois tamanhos**: preview (menor) ou full (original)
- **Combina informações de diferentes fontes**: WhatsApp, contatos salvos, leads
- **Atualiza automaticamente dados desatualizados** no banco

### Campos Retornados:
- **Informações básicas**: id, wa_fastid, wa_chatid, owner, name, phone
- **Dados do WhatsApp**: wa_name, wa_contactName, wa_archived, wa_isBlocked, etc.
- **Dados de lead/CRM**: lead_name, lead_email, lead_status, lead_field01-20, etc.
- **Informações de grupo**: wa_isGroup, wa_isGroup_admin, wa_isGroup_announce, etc.
- **Chatbot**: chatbot_summary, chatbot_lastTrigger_id, chatbot_disableUntil, etc.
- **Configurações**: wa_muteEndTime, wa_isPinned, wa_unreadCount, etc.

**Comportamento**:
- Para contatos individuais:
  - Busca nome verificado do WhatsApp
  - Verifica nome salvo nos contatos
  - Formata número internacional
  - Calcula grupos em comum
- Para grupos:
  - Busca nome do grupo
  - Verifica status de comunidade


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do telefone ou ID do grupo |
| preview | boolean | Não | Controla o tamanho da imagem de perfil retornada: - `true`: Retorna imagem em tamanho preview (menor, otimizada para listagens) - `false` (padrão): Retorna imagem em tamanho full (resolução original, maior qualidade)  |


**Respostas:**

#### 200

Informações completas do chat retornadas com sucesso

Content-Type: `application/json`

#### 400

Payload inválido ou número inválido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Token não fornecido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor ou sessão não iniciada

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /chat/check

**Resumo:** Verificar Números no WhatsApp

Verifica se números fornecidos estão registrados no WhatsApp e retorna informações detalhadas.

### Funcionalidades:
- Verifica múltiplos números simultaneamente
- Suporta números individuais e IDs de grupo
- Retorna nome verificado quando disponível
- Identifica grupos e comunidades
- Verifica subgrupos de comunidades

**Comportamento específico**:
- Para números individuais:
  - Verifica registro no WhatsApp
  - Retorna nome verificado se disponível
  - Normaliza formato do número
- Para grupos:
  - Verifica existência
  - Retorna nome do grupo
  - Retorna id do grupo de anúncios se buscado por id de comunidade


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| numbers | array | Não | Lista de números ou IDs de grupo para verificar |


**Respostas:**

#### 200

Resultado da verificação

Content-Type: `application/json`

#### 400

Payload inválido ou sem números

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Sem sessão ativa

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

### Enviar Mensagem


### POST /send/text

**Resumo:** Enviar mensagem de texto

Envia uma mensagem de texto para um contato ou grupo.

## Recursos Específicos

- **Preview de links** com suporte a personalização automática ou customizada
- **Formatação básica** do texto
- **Substituição automática de placeholders** dinâmicos

## Campos Comuns

Este endpoint suporta todos os **campos opcionais comuns** documentados na tag **"Enviar Mensagem"**, incluindo:
`delay`, `readchat`, `readmessages`, `replyid`, `mentions`, `forward`, `track_source`, `track_id`, placeholders e envio para grupos.

## Preview de Links

### Preview Automático
```json
{
  "number": "5511999999999",
  "text": "Confira: https://exemplo.com",
  "linkPreview": true
}
```

### Preview Personalizado
```json
{
  "number": "5511999999999",
  "text": "Confira nosso site! https://exemplo.com",
  "linkPreview": true,
  "linkPreviewTitle": "Título Personalizado",
  "linkPreviewDescription": "Uma descrição personalizada do link",
  "linkPreviewImage": "https://exemplo.com/imagem.jpg",
  "linkPreviewLarge": true
}
```


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do destinatário (formato internacional) |
| text | string | Sim | Texto da mensagem (aceita placeholders) |
| linkPreview | boolean | Não | Ativa/desativa preview de links. Se true, procura automaticamente um link no texto para gerar preview.  Comportamento: - Se apenas linkPreview=true: gera preview automático do primeiro link encontrado no texto - Se fornecidos campos personalizados (title, description, image): usa os valores fornecidos - Se campos personalizados parciais: combina com dados automáticos do link como fallback  |
| linkPreviewTitle | string | Não | Define um título personalizado para o preview do link |
| linkPreviewDescription | string | Não | Define uma descrição personalizada para o preview do link |
| linkPreviewImage | string | Não | URL ou Base64 da imagem para usar no preview do link |
| linkPreviewLarge | boolean | Não | Se true, gera um preview grande com upload da imagem. Se false, gera um preview pequeno sem upload |
| replyid | string | Não | ID da mensagem para responder |
| mentions | string | Não | Números para mencionar (separados por vírgula) |
| readchat | boolean | Não | Marca conversa como lida após envio |
| readmessages | boolean | Não | Marca últimas mensagens recebidas como lidas |
| delay | integer | Não | Atraso em milissegundos antes do envio, durante o atraso apacerá 'Digitando...' |
| forward | boolean | Não | Marca a mensagem como encaminhada no WhatsApp |
| track_source | string | Não | Origem do rastreamento da mensagem |
| track_id | string | Não | ID para rastreamento da mensagem (aceita valores duplicados) |


**Respostas:**

#### 200

Mensagem enviada com sucesso

Content-Type: `application/json`

#### 400

Requisição inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Não autorizado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 429

Limite de requisições excedido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /send/media

**Resumo:** Enviar mídia (imagem, vídeo, áudio ou documento)

Envia diferentes tipos de mídia para um contato ou grupo. Suporta URLs ou arquivos base64.

## Tipos de Mídia Suportados
- **`image`**: Imagens (JPG preferencialmente)
- **`video`**: Vídeos (apenas MP4)
- **`document`**: Documentos (PDF, DOCX, XLSX, etc)
- **`audio`**: Áudio comum (MP3 ou OGG)
- **`myaudio`**: Mensagem de voz (alternativa ao PTT)
- **`ptt`**: Mensagem de voz (Push-to-Talk)
- **`sticker`**: Figurinha/Sticker

## Recursos Específicos
- **Upload por URL ou base64**
- **Caption/legenda** opcional com suporte a placeholders
- **Nome personalizado** para documentos (`docName`)
- **Geração automática de thumbnails**
- **Compressão otimizada** conforme o tipo

## Campos Comuns

Este endpoint suporta todos os **campos opcionais comuns** documentados na tag **"Enviar Mensagem"**, incluindo:
`delay`, `readchat`, `readmessages`, `replyid`, `mentions`, `forward`, `track_source`, `track_id`, placeholders e envio para grupos.

## Exemplos Básicos

### Imagem Simples
```json
{
  "number": "5511999999999",
  "type": "image",
  "file": "https://exemplo.com/foto.jpg"
}
```

### Documento com Nome
```json
{
  "number": "5511999999999",
  "type": "document",
  "file": "https://exemplo.com/contrato.pdf",
  "docName": "Contrato.pdf",
  "text": "Segue o documento solicitado"
}
```


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do destinatário (formato internacional) |
| type | string | Sim | Tipo de mídia (image, video, document, audio, myaudio, ptt, sticker) |
| file | string | Sim | URL ou base64 do arquivo |
| text | string | Não | Texto descritivo (caption) - aceita placeholders |
| docName | string | Não | Nome do arquivo (apenas para documents) |
| replyid | string | Não | ID da mensagem para responder |
| mentions | string | Não | Números para mencionar (separados por vírgula) |
| readchat | boolean | Não | Marca conversa como lida após envio |
| readmessages | boolean | Não | Marca últimas mensagens recebidas como lidas |
| delay | integer | Não | Atraso em milissegundos antes do envio, durante o atraso apacerá 'Digitando...' ou 'Gravando áudio...' |
| forward | boolean | Não | Marca a mensagem como encaminhada no WhatsApp |
| track_source | string | Não | Origem do rastreamento da mensagem |
| track_id | string | Não | ID para rastreamento da mensagem (aceita valores duplicados) |


**Respostas:**

#### 200

Mídia enviada com sucesso

Content-Type: `application/json`

#### 400

Requisição inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Não autorizado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 413

Arquivo muito grande

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 415

Formato de mídia não suportado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /send/contact

**Resumo:** Enviar cartão de contato (vCard)

Envia um cartão de contato (vCard) para um contato ou grupo.

## Recursos Específicos

- **vCard completo** com nome, telefones, organização, email e URL
- **Múltiplos números de telefone** (separados por vírgula)
- **Cartão clicável** no WhatsApp para salvar na agenda
- **Informações profissionais** (organização/empresa)

## Campos Comuns

Este endpoint suporta todos os **campos opcionais comuns** documentados na tag **"Enviar Mensagem"**, incluindo:
`delay`, `readchat`, `readmessages`, `replyid`, `mentions`, `forward`, `track_source`, `track_id`, placeholders e envio para grupos.

## Exemplo Básico
```json
{
  "number": "5511999999999",
  "fullName": "João Silva",
  "phoneNumber": "5511999999999,5511888888888",
  "organization": "Empresa XYZ",
  "email": "joao.silva@empresa.com",
  "url": "https://empresa.com/joao"
}
```


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do destinatário (formato internacional) |
| fullName | string | Sim | Nome completo do contato |
| phoneNumber | string | Sim | Números de telefone (separados por vírgula) |
| organization | string | Não | Nome da organização/empresa |
| email | string | Não | Endereço de email |
| url | string | Não | URL pessoal ou da empresa |
| replyid | string | Não | ID da mensagem para responder |
| mentions | string | Não | Números para mencionar (separados por vírgula) |
| readchat | boolean | Não | Marca conversa como lida após envio |
| readmessages | boolean | Não | Marca últimas mensagens recebidas como lidas |
| delay | integer | Não | Atraso em milissegundos antes do envio, durante o atraso apacerá 'Digitando...' |
| forward | boolean | Não | Marca a mensagem como encaminhada no WhatsApp |
| track_source | string | Não | Origem do rastreamento da mensagem |
| track_id | string | Não | ID para rastreamento da mensagem (aceita valores duplicados) |


**Respostas:**

#### 200

Cartão de contato enviado com sucesso

Content-Type: `application/json`

#### 400

Requisição inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Não autorizado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 429

Limite de requisições excedido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /send/location

**Resumo:** Enviar localização geográfica

Envia uma localização geográfica para um contato ou grupo.

## Recursos Específicos

- **Coordenadas precisas** (latitude e longitude obrigatórias)
- **Nome do local** para identificação
- **Mapa interativo** no WhatsApp para navegação
- **Pin personalizado** com nome do local

## Campos Comuns

Este endpoint suporta todos os **campos opcionais comuns** documentados na tag **"Enviar Mensagem"**, incluindo:
`delay`, `readchat`, `readmessages`, `replyid`, `mentions`, `forward`, `track_source`, `track_id`, placeholders e envio para grupos.

## Exemplo Básico
```json
{
  "number": "5511999999999",
  "name": "Maracanã",
  "address": "Av. Pres. Castelo Branco, Portão 3 - Maracanã, Rio de Janeiro - RJ, 20271-130",
  "latitude": -22.912982815767986,
  "longitude": -43.23028153499254
}
```


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do destinatário (formato internacional) |
| name | string | Não | Nome do local |
| address | string | Não | Endereço completo do local |
| latitude | number | Sim | Latitude (-90 a 90) |
| longitude | number | Sim | Longitude (-180 a 180) |
| replyid | string | Não | ID da mensagem para responder |
| mentions | string | Não | Números para mencionar (separados por vírgula) |
| readchat | boolean | Não | Marca conversa como lida após envio |
| readmessages | boolean | Não | Marca últimas mensagens recebidas como lidas |
| delay | integer | Não | Atraso em milissegundos antes do envio, durante o atraso apacerá 'Digitando...' |
| forward | boolean | Não | Marca a mensagem como encaminhada no WhatsApp |
| track_source | string | Não | Origem do rastreamento da mensagem |
| track_id | string | Não | ID para rastreamento da mensagem (aceita valores duplicados) |


**Respostas:**

#### 200

Localização enviada com sucesso

Content-Type: `application/json`

#### 400

Requisição inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Não autorizado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 429

Limite de requisições excedido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /message/presence

**Resumo:** Enviar atualização de presença

Envia uma atualização de presença para um contato ou grupo de forma **assíncrona**.

## 🔄 Comportamento Assíncrono:
- **Execução independente**: A presença é gerenciada em background, não bloqueia o retorno da API
- **Limite máximo**: 5 minutos de duração (300 segundos)
- **Tick de atualização**: Reenvia a presença a cada 10 segundos
- **Cancelamento automático**: Presença é cancelada automaticamente ao enviar uma mensagem para o mesmo chat

## 📱 Tipos de presença suportados:
- **composing**: Indica que você está digitando uma mensagem
- **recording**: Indica que você está gravando um áudio
- **paused**: Remove/cancela a indicação de presença atual

## ⏱️ Controle de duração:
- **Sem delay**: Usa limite padrão de 5 minutos
- **Com delay**: Usa o valor especificado (máximo 5 minutos)
- **Cancelamento**: Envio de mensagem cancela presença automaticamente

## 📋 Exemplos de uso:

### Digitar por 30 segundos:
```json
{
  "number": "5511999999999",
  "presence": "composing",
  "delay": 30000
}
```

### Gravar áudio por 1 minuto:
```json
{
  "number": "5511999999999",
  "presence": "recording",
  "delay": 60000
}
```

### Cancelar presença atual:
```json
{
  "number": "5511999999999",
  "presence": "paused"
}
```

### Usar limite máximo (5 minutos):
```json
{
  "number": "5511999999999",
  "presence": "composing"
}
```


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do destinatário no formato internacional (ex: 5511999999999) |
| presence | string | Sim | Tipo de presença a ser enviada |
| delay | integer | Não | Duração em milissegundos que a presença ficará ativa (máximo 5 minutos = 300000ms). Se não informado ou valor maior que 5 minutos, usa o limite padrão de 5 minutos. A presença é reenviada a cada 10 segundos durante este período.  |


**Respostas:**

#### 200

Presença atualizada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não | Mensagem de confirmação |

#### 400

Requisição inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Descrição do erro |

#### 401

Token inválido ou expirado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Descrição do erro de autenticação |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Descrição do erro interno |


### POST /send/status

**Resumo:** Enviar Stories (Status)

Envia um story (status) com suporte para texto, imagem, vídeo e áudio.

**Suporte a campos de rastreamento**: Este endpoint também suporta `track_source` e `track_id` documentados na tag **"Enviar Mensagem"**.

## Tipos de Status
- text: Texto com estilo e cor de fundo
- image: Imagens com legenda opcional
- video: Vídeos com thumbnail e legenda
- audio: Áudio normal ou mensagem de voz (PTT)

## Cores de Fundo
- 1-3: Tons de amarelo
- 4-6: Tons de verde
- 7-9: Tons de azul
- 10-12: Tons de lilás
- 13: Magenta
- 14-15: Tons de rosa
- 16: Marrom claro
- 17-19: Tons de cinza (19 é o padrão)

## Fontes (para texto)
- 0: Padrão 
- 1-8: Estilos alternativos

## Limites
- Texto: Máximo 656 caracteres
- Imagem: JPG, PNG, GIF
- Vídeo: MP4, MOV
- Áudio: MP3, OGG, WAV (convertido para OGG/OPUS)

## Exemplo
```json
{
  "type": "text",
  "text": "Novidades chegando!",
  "background_color": 7,
  "font": 1
}
```


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| type | string | Sim | Tipo do status |
| text | string | Não | Texto principal ou legenda |
| background_color | integer | Não | Código da cor de fundo |
| font | integer | Não | Estilo da fonte (apenas para type=text) |
| file | string | Não | URL ou Base64 do arquivo de mídia |
| thumbnail | string | Não | URL ou Base64 da miniatura (opcional para vídeos) |
| mimetype | string | Não | MIME type do arquivo (opcional) |
| track_source | string | Não | Origem do rastreamento da mensagem |
| track_id | string | Não | ID para rastreamento da mensagem (aceita valores duplicados) |


**Respostas:**

#### 200

Status enviado com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| Id | string | Não |  |
| content | object | Não | Conteúdo processado da mensagem |
| messageTimestamp | integer | Não |  |
| status | string | Não |  |

#### 400

Requisição inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Não autorizado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /send/menu

**Resumo:** Enviar menu interativo (botões, carrosel, lista ou enquete)

Este endpoint oferece uma interface unificada para envio de quatro tipos principais de mensagens interativas:
- Botões: Para ações rápidas e diretas
- Carrosel de Botões: Para uma lista horizontal de botões com imagens
- Listas: Para menus organizados em seções
- Enquetes: Para coleta de opiniões e votações

**Suporte a campos de rastreamento**: Este endpoint também suporta `track_source` e `track_id` documentados na tag **"Enviar Mensagem"**.

## Estrutura Base do Payload

Todas as requisições seguem esta estrutura base:

```json
{
  "number": "5511999999999",
  "type": "button|list|poll|carousel",
  "text": "Texto principal da mensagem",
  "choices": ["opções baseadas no tipo escolhido"],
  "footerText": "Texto do rodapé (opcional para botões e listas)",
  "listButton": "Texto do botão (para listas)",
  "selectableCount": "Número de opções selecionáveis (apenas para enquetes)"
}
```

## Tipos de Mensagens Interativas

### 1. Botões (type: "button")

Cria botões interativos com diferentes funcionalidades de ação.

#### Campos Específicos
- `footerText`: Texto opcional exibido abaixo da mensagem principal
- `choices`: Array de opções que serão convertidas em botões

#### Formatos de Botões
Cada botão pode ser configurado usando `|` (pipe) ou `\n` (quebra de linha) como separadores:

- **Botão de Resposta**: 
  - `"texto|id"` ou 
  - `"texto\nid"` ou 
  - `"texto"` (ID será igual ao texto)

- **Botão de Cópia**: 
  - `"texto|copy:código"` ou 
  - `"texto\ncopy:código"`

- **Botão de Chamada**: 
  - `"texto|call:+5511999999999"` ou 
  - `"texto\ncall:+5511999999999"`

- **Botão de URL**: 
  - `"texto|https://exemplo.com"` ou 
  - `"texto|url:https://exemplo.com"`

#### Botões com Imagem
Para adicionar uma imagem aos botões, use o campo `imageButton` no payload:

#### Exemplo com Imagem
```json
{
  "number": "5511999999999",
  "type": "button",
  "text": "Escolha um produto:",
  "imageButton": "https://exemplo.com/produto1.jpg",
  "choices": [
    "Produto A|prod_a",
    "Mais Info|https://exemplo.com/produto-a",
    "Produto B|prod_b",
    "Ligar|call:+5511999999999"
  ],
  "footerText": "Produtos em destaque"
}
```

> **Suporte**: O campo `imageButton` aceita URLs ou imagens em base64.

#### Exemplo Completo
```json
{
  "number": "5511999999999",
  "type": "button",
  "text": "Como podemos ajudar?",
  "choices": [
    "Suporte Técnico|suporte",
    "Fazer Pedido|pedido",
    "Nosso Site|https://exemplo.com",
    "Falar Conosco|call:+5511999999999"
  ],
  "footerText": "Escolha uma das opções abaixo"
}
```

#### Limitações e Compatibilidade
> **Importante**: Ao combinar botões de resposta com outros tipos (call, url, copy) na mesma mensagem, será exibido o aviso: "Não é possível exibir esta mensagem no WhatsApp Web. Abra o WhatsApp no seu celular para visualizá-la."

### 2. Listas (type: "list")

Cria menus organizados em seções com itens selecionáveis.

#### Campos Específicos
- `listButton`: Texto do botão que abre a lista
- `footerText`: Texto opcional do rodapé
- `choices`: Array com seções e itens da lista

#### Formato das Choices
- `"[Título da Seção]"`: Inicia uma nova seção
- `"texto|id|descrição"`: Item da lista com:
  - texto: Label do item
  - id: Identificador único, opcional
  - descrição: Texto descritivo adicional e opcional

#### Exemplo Completo
```json
{
  "number": "5511999999999",
  "type": "list",
  "text": "Catálogo de Produtos",
  "choices": [
    "[Eletrônicos]",
    "Smartphones|phones|Últimos lançamentos",
    "Notebooks|notes|Modelos 2024",
    "[Acessórios]",
    "Fones|fones|Bluetooth e com fio",
    "Capas|cases|Proteção para seu device"
  ],
  "listButton": "Ver Catálogo",
  "footerText": "Preços sujeitos a alteração"
}
```

### 3. Enquetes (type: "poll")

Cria enquetes interativas para votação.

#### Campos Específicos
- `selectableCount`: Número de opções que podem ser selecionadas (padrão: 1)
- `choices`: Array simples com as opções de voto

#### Exemplo Completo
```json
{
  "number": "5511999999999",
  "type": "poll",
  "text": "Qual horário prefere para atendimento?",
  "choices": [
    "Manhã (8h-12h)",
    "Tarde (13h-17h)",
    "Noite (18h-22h)"
  ],
  "selectableCount": 1
}
```

### 4. Carousel (type: "carousel")

Cria um carrossel de cartões com imagens e botões interativos.

#### Campos Específicos
- `choices`: Array com elementos do carrossel na seguinte ordem:
  - `[Texto do cartão]`: Texto do cartão entre colchetes
  - `{URL ou base64 da imagem}`: Imagem entre chaves
  - Botões do cartão (um por linha):
    - `"texto|copy:código"` para botão de copiar
    - `"texto|https://url"` para botão de link
    - `"texto|call:+número"` para botão de ligação

#### Exemplo Completo
```json
{
  "number": "5511999999999",
  "type": "carousel",
  "text": "Conheça nossos produtos",
  "choices": [
    "[Smartphone XYZ\nO mais avançado smartphone da linha]",
    "{https://exemplo.com/produto1.jpg}",
    "Copiar Código|copy:PROD123",
    "Ver no Site|https://exemplo.com/xyz",
    "Fale Conosco|call:+5511999999999",
    "[Notebook ABC\nO notebook ideal para profissionais]",
    "{https://exemplo.com/produto2.jpg}",
    "Copiar Código|copy:NOTE456",
    "Comprar Online|https://exemplo.com/abc",
    "Suporte|call:+5511988888888"
  ]
}
```

> **Nota**: Criamos outro endpoint para carrossel: `/send/carousel`, funciona da mesma forma, mas com outro formato de payload. Veja o que é mais fácil para você.

## Termos de uso

Os recursos de botões interativos e listas podem ser descontinuados a qualquer momento sem aviso prévio. Não nos responsabilizamos por quaisquer alterações ou indisponibilidade destes recursos.

### Alternativas e Compatibilidade

Considerando a natureza dinâmica destes recursos, nosso endpoint foi projetado para facilitar a migração entre diferentes tipos de mensagens (botões, listas e enquetes). 

Recomendamos criar seus fluxos de forma flexível, preparados para alternar entre os diferentes tipos.

Em caso de descontinuidade de algum recurso, você poderá facilmente migrar para outro tipo de mensagem apenas alterando o campo "type" no payload, mantendo a mesma estrutura de choices.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do destinatário (formato internacional) |
| type | string | Sim | Tipo do menu (button, list, poll, carousel) |
| text | string | Sim | Texto principal (aceita placeholders) |
| footerText | string | Não | Texto do rodapé (opcional) |
| listButton | string | Não | Texto do botão principal |
| selectableCount | integer | Não | Número máximo de opções selecionáveis (para enquetes) |
| choices | array | Sim | Lista de opções. Use [Título] para seções em listas |
| imageButton | string | Não | URL da imagem para botões (recomendado para type: button) |
| replyid | string | Não | ID da mensagem para responder |
| mentions | string | Não | Números para mencionar (separados por vírgula) |
| readchat | boolean | Não | Marca conversa como lida após envio |
| readmessages | boolean | Não | Marca últimas mensagens recebidas como lidas |
| delay | integer | Não | Atraso em milissegundos antes do envio, durante o atraso apacerá 'Digitando...' |
| track_source | string | Não | Origem do rastreamento da mensagem |
| track_id | string | Não | ID para rastreamento da mensagem (aceita valores duplicados) |


**Respostas:**

#### 200

Menu enviado com sucesso

Content-Type: `application/json`

#### 400

Requisição inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Não autorizado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 429

Limite de requisições excedido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /send/carousel

**Resumo:** Enviar carrossel de mídia com botões

Este endpoint permite enviar um carrossel com imagens e botões interativos.
Funciona de maneira igual ao endpoint `/send/menu` com type: carousel, porém usando outro formato de payload.

## Campos Comuns

Este endpoint suporta todos os **campos opcionais comuns** documentados na tag **"Enviar Mensagem"**, incluindo:
`delay`, `readchat`, `readmessages`, `replyid`, `mentions`, `forward`, `track_source`, `track_id`, placeholders e envio para grupos.

## Estrutura do Payload

```json
{
  "number": "5511999999999",
  "text": "Texto principal",
  "carousel": [
    {
      "text": "Texto do cartão",
      "image": "URL da imagem",
      "buttons": [
        {
          "id": "resposta1",
          "text": "Texto do botão",
          "type": "REPLY"
        }
      ]
    }
  ],
  "delay": 1000,
  "readchat": true
}
```

## Tipos de Botões

- `REPLY`: Botão de resposta rápida
  - Quando clicado, envia o valor do id como resposta ao chat
  - O id será o texto enviado como resposta

- `URL`: Botão com link
  - Quando clicado, abre a URL especificada
  - O id deve conter a URL completa (ex: https://exemplo.com)

- `COPY`: Botão para copiar texto
  - Quando clicado, copia o texto para a área de transferência
  - O id será o texto que será copiado

- `CALL`: Botão para realizar chamada
  - Quando clicado, inicia uma chamada telefônica
  - O id deve conter o número de telefone

## Exemplo de Botões
```json
{
  "buttons": [
    {
      "id": "Sim, quero comprar!",
      "text": "Confirmar Compra",
      "type": "REPLY"
    },
    {
      "id": "https://exemplo.com/produto",
      "text": "Ver Produto",
      "type": "URL"
    },
    {
      "id": "CUPOM20",
      "text": "Copiar Cupom",
      "type": "COPY"
    },
    {
      "id": "5511999999999",
      "text": "Falar com Vendedor",
      "type": "CALL"
    }
  ]
}
```

## Exemplo Completo de Carrossel
```json
{
  "number": "5511999999999",
  "text": "Nossos Produtos em Destaque",
  "carousel": [
    {
      "text": "Smartphone XYZ\nO mais avançado smartphone da linha",
      "image": "https://exemplo.com/produto1.jpg",
      "buttons": [
        {
          "id": "SIM_COMPRAR_XYZ",
          "text": "Comprar Agora",
          "type": "REPLY"
        },
        {
          "id": "https://exemplo.com/xyz",
          "text": "Ver Detalhes",
          "type": "URL"
        }
      ]
    },
    {
      "text": "Cupom de Desconto\nGanhe 20% OFF em qualquer produto",
      "image": "https://exemplo.com/cupom.jpg",
      "buttons": [
        {
          "id": "DESCONTO20",
          "text": "Copiar Cupom",
          "type": "COPY"
        },
        {
          "id": "5511999999999",
          "text": "Falar com Vendedor",
          "type": "CALL"
        }
      ]
    }
  ],
  "delay": 0,
  "readchat": true
}
```


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do destinatário (formato internacional) |
| text | string | Sim | Texto principal da mensagem |
| carousel | array | Sim | Array de cartões do carrossel |
| track_source | string | Não | Origem do rastreamento da mensagem |
| track_id | string | Não | ID para rastreamento da mensagem (aceita valores duplicados) |


**Respostas:**

#### 200

Carrossel enviado com sucesso

Content-Type: `application/json`

#### 400

Requisição inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Não autorizado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /send/location-button

**Resumo:** Solicitar localização do usuário

Este endpoint envia uma mensagem com um botão que solicita a localização do usuário.
Quando o usuário clica no botão, o WhatsApp abre a interface para compartilhar a localização atual.

## Campos Comuns

Este endpoint suporta todos os **campos opcionais comuns** documentados na tag **"Enviar Mensagem"**, incluindo:
`delay`, `readchat`, `readmessages`, `replyid`, `mentions`, `forward`, `track_source`, `track_id`, placeholders e envio para grupos.

## Estrutura do Payload

```json
{
  "number": "5511999999999",
  "text": "Por favor, compartilhe sua localização",
  "delay": 0,
  "readchat": true
}
```

## Exemplo de Uso

```json
{
  "number": "5511999999999",
  "text": "Para continuar o atendimento, clique no botão abaixo e compartilhe sua localização"
}
```

> **Nota**: O botão de localização é adicionado automaticamente à mensagem


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do destinatário (formato internacional) |
| text | string | Sim | Texto da mensagem que será exibida |
| delay | integer | Não | Atraso em milissegundos antes do envio |
| readchat | boolean | Não | Se deve marcar a conversa como lida após envio |
| track_source | string | Não | Origem do rastreamento da mensagem |
| track_id | string | Não | ID para rastreamento da mensagem (aceita valores duplicados) |


**Respostas:**

#### 200

Localização enviada com sucesso

Content-Type: `application/json`

#### 400

Requisição inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Não autorizado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /send/request-payment

**Resumo:** Solicitar pagamento

Envia uma solicitação de pagamento com o botão nativo **"Revisar e pagar"** do WhatsApp.
O fluxo suporta PIX (estático, dinâmico ou desabilitado), boleto, link de pagamento e cartão,
combinando tudo em uma única mensagem interativa.

## Como funciona
- Define o valor em `amount` (BRL por padrão) e opcionalmente personaliza título, texto e nota adicional.
- Por padrão exige `pixKey`.
- O arquivo apontado por `fileUrl` é anexado como documento (boleto ou fatura em PDF, por exemplo).
- `paymentLink` habilita o botão externo.

### Links suportados (`paymentLink`)
O WhatsApp apenas aceita URLs de provedores homologados. Utilize os padrões abaixo:
- Mercado Pago: `mpago.la/*`, `mpago.li/*`, `mercadopago.com.br/*`
- PicPay: `picpay.me/*`, `link.picpay.com/*`, `app.picpay.com/user/*`
- Stone: `payment-link.stone.com.br/*`
- Cielo: `cielolink.com.br/*`, `cielo.mystore.com.br/*`
- Getnet: `pag.getnet.com.br/*`
- Rede: `userede.com.br/pagamentos/*`
- SumUp: `pay.sumup.com/b2c/*`
- Pagar.me: `payment-link.pagar.me/*`
- TON: `payment-link.ton.com.br/*`
- PagBank: `sacola.pagbank.com.br/*`, `pag.ae/*`
- Nubank: `nubank.com.br/cobrar/*`, `checkout.nubank.com.br/*`
- InfinitePay: `pay.infinitepay.io/*`
- VTEX: `*.vtexpayments.com/*`, `*.myvtex.com/*`
- EBANX: `payment.ebanx.com/*`
- Asaas: `asaas.com/*`
- Vindi: `pagar.vindi.com.br/*`
- Adyen: `eu.adyen.link/*`
- EFI (Gerencianet): `sejaefi.link/*`, `pagamento.sejaefi.com.br/*`
- SafraPay: `portal.safrapay.com.br/*`, `safrapay.aditum.com.br/*`
- Stripe: `buy.stripe.com/*`
- Hotmart: `pay.hotmart.com/*`


## Campos comuns
Este endpoint também suporta os campos padrão: `delay`, `readchat`, `readmessages`, `replyid`,
`mentions`, `track_source`, `track_id` e `async`.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do destinatário (DDD + número, formato internacional) |
| title | string | Não | Título que aparece no cabeçalho do fluxo |
| text | string | Não | Mensagem exibida no corpo do fluxo |
| footer | string | Não | Texto do rodapé da mensagem |
| itemName | string | Não | Nome do item principal listado no fluxo |
| invoiceNumber | string | Não | Identificador ou número da fatura |
| amount | number (float) | Sim | Valor da cobrança (em BRL por padrão) |
| pixKey | string | Não | Chave PIX estático (CPF/CNPJ/telefone/email/EVP) |
| pixType | string | Não | Tipo da chave PIX (`CPF`, `CNPJ`, `PHONE`, `EMAIL`, `EVP`). Padrão `EVP` |
| pixName | string | Não | Nome do recebedor exibido no fluxo (padrão usa o nome do perfil da instância) |
| paymentLink | string | Não | URL externa para checkout (somente dominios homologados; veja lista acima) |
| fileUrl | string | Não | URL ou caminho (base64) do documento a ser anexado (ex.: boleto PDF) |
| fileName | string | Não | Nome do arquivo exibido no WhatsApp ao anexar `fileUrl` |
| boletoCode | string | Não | Linha digitável do boleto (habilita o método boleto automaticamente) |
| replyid | string | Não | ID da mensagem que será respondida |
| mentions | string | Não | Números mencionados separados por vírgula |
| delay | integer | Não | Atraso em milissegundos antes do envio (exibe "digitando..." no WhatsApp) |
| readchat | boolean | Não | Marca o chat como lido após enviar a mensagem |
| readmessages | boolean | Não | Marca mensagens recentes como lidas após o envio |
| async | boolean | Não | Enfileira o envio para processamento assíncrono |
| track_source | string | Não | Origem de rastreamento (ex.: chatwoot, crm-interno) |
| track_id | string | Não | Identificador de rastreamento (aceita valores duplicados) |


**Respostas:**

#### 200

Solicitação de pagamento enviada com sucesso

Content-Type: `application/json`

#### 400

Requisição inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Não autorizado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /send/pix-button

**Resumo:** Enviar botão PIX

Envia um botão nativo do WhatsApp que abre para pagamento PIX com a chave informada.
O usuário visualiza o detalhe do recebedor, nome e chave.

## Regras principais
- `pixType` aceita: `CPF`, `CNPJ`, `PHONE`, `EMAIL`, `EVP` (case insensitive)
- `pixName` padrão: `"Pix"` quando não informado - nome de quem recebe o pagamento


## Campos comuns
Este endpoint herda os campos opcionais padronizados da tag **"Enviar Mensagem"**:
`delay`, `readchat`, `readmessages`, `replyid`, `mentions`, `track_source`, `track_id` e `async`.

## Exemplo de payload
```json
{
  "number": "5511999999999",
  "pixType": "EVP",
  "pixKey": "123e4567-e89b-12d3-a456-426614174000",
  "pixName": "Loja Exemplo"
}
```


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do destinatário (DDD + número, formato internacional) |
| pixType | string | Sim | Tipo da chave PIX. Valores aceitos: CPF, CNPJ, PHONE, EMAIL ou EVP |
| pixKey | string | Sim | Valor da chave PIX (CPF/CNPJ/telefone/email/EVP) |
| pixName | string | Não | Nome exibido como recebedor do PIX (padrão "Pix" se vazio) |
| async | boolean | Não | Enfileira o envio para processamento assíncrono |
| delay | integer | Não | Atraso em milissegundos antes do envio (exibe "digitando..." no WhatsApp) |
| readchat | boolean | Não | Marca o chat como lido após enviar a mensagem |
| readmessages | boolean | Não | Marca mensagens recentes como lidas após o envio |
| replyid | string | Não | ID da mensagem que será respondida |
| mentions | string | Não | Lista de números mencionados separados por vírgula |
| track_source | string | Não | Origem de rastreamento (ex.: chatwoot, crm-interno) |
| track_id | string | Não | Identificador de rastreamento (aceita valores duplicados) |


**Respostas:**

#### 200

Botão PIX enviado com sucesso

Content-Type: `application/json`

#### 400

Requisição inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Não autorizado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

### Etiquetas


### POST /chat/labels

**Resumo:** Gerencia labels de um chat

Atualiza as labels associadas a um chat específico. Este endpoint oferece três modos de operação:

1. **Definir todas as labels** (labelids): Define o conjunto completo de labels para o chat, substituindo labels existentes
2. **Adicionar uma label** (add_labelid): Adiciona uma única label ao chat sem afetar as existentes
3. **Remover uma label** (remove_labelid): Remove uma única label do chat sem afetar as outras

**Importante**: Use apenas um dos três parâmetros por requisição. Labels inexistentes serão rejeitadas.

As labels devem ser fornecidas no formato id ou labelid encontradas na função get labels.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| number | string | Sim | Número do chat ou grupo |
| labelids | array | Não | Lista de IDs das labels a serem aplicadas ao chat (define todas as labels) |
| add_labelid | string | Não | ID da label a ser adicionada ao chat |
| remove_labelid | string | Não | ID da label a ser removida do chat |


**Respostas:**

#### 200

Labels atualizadas com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não | Mensagem de confirmação |
| editions | array | Não | Lista de operações realizadas (apenas para operação labelids) |

#### 400

Erro na requisição

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 404

Chat não encontrado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /label/edit

**Resumo:** Editar etiqueta

Edita uma etiqueta existente na instância.
Permite alterar nome, cor ou deletar a etiqueta.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| labelid | string | Sim | ID da etiqueta a ser editada |
| name | string | Não | Novo nome da etiqueta |
| color | integer | Não | Código numérico da nova cor (0-19) |
| delete | boolean | Não | Indica se a etiqueta deve ser deletada |


**Respostas:**

#### 200

Etiqueta editada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não |  |

#### 400

Payload inválido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor ou sessão inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### GET /labels

**Resumo:** Buscar todas as etiquetas

Retorna a lista completa de etiquetas da instância.


**Respostas:**

#### 200

Lista de etiquetas retornada com sucesso

Content-Type: `application/json`

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

### Funções API dos Agentes


### POST /function/edit

**Resumo:** Criar/Editar função para integração com APIs externas

# Configuração de Funções de API para Agentes IA

Documentação para criar/editar funções utilizadas pelos agentes de IA para integração com APIs externas. Inclui validação automática e controle de ativação.

## 1. Estrutura Base da Função

### Campos Principais
```json
{
  "name": "nomeDaFuncao",
  "description": "Descrição detalhada",
  "isActive": true,
  "method": "POST",
  "endpoint": "https://api.exemplo.com/recurso",
  "headers": {},
  "body": {},
  "parameters": []
}
```

### Detalhamento dos Campos

#### `name`
- Identificador único e descritivo
- Sem espaços ou caracteres especiais
- Ex: "createProduct", "updateUserStatus"

#### `description`
- Propósito e funcionamento da função
- Inclua casos de uso e resultados esperados
- Ex: "Cria produto no catálogo com nome, preço e categoria"

#### `isActive`
- Controla disponibilidade da função
- Desativa automaticamente se houver erros
- Default: false

#### `method`
- GET: buscar dados
- POST: criar recurso
- PUT: atualizar completo
- PATCH: atualização parcial
- DELETE: remover recurso

#### `endpoint`
- URL completa da API
- Aceita placeholders: {{variavel}}
- Exemplos:
  ```
  https://api.exemplo.com/produtos
  https://api.exemplo.com/usuarios/{{userId}}
  https://api.exemplo.com/busca?q={{query}}&limit={{limit}}
  ```

#### `headers`
```json
{
  "Authorization": "Bearer {{apiKey}}",
  "Content-Type": "application/json",
  "Accept": "application/json"
}
```

#### `body` (POST/PUT/PATCH)
```json
{
  "name": "{{productName}}",
  "price": "{{price}}",
  "metadata": {
    "tags": "{{tags}}"
  }
}
```

## 2. Configuração de Parâmetros

### Estrutura do Parâmetro
```json
{
  "name": "nomeParametro",
  "type": "string",
  "description": "Descrição do uso",
  "required": true,
  "enum": "valor1,valor2,valor3",
  "minimum": 0,
  "maximum": 100
}
```

### Tipos de Parâmetros

#### String
```json
{
  "name": "status",
  "type": "string",
  "description": "Status do pedido",
  "required": true,
  "enum": "pending,processing,completed"
}
```

#### Número
```json
{
  "name": "price",
  "type": "number",
  "description": "Preço em reais",
  "required": true,
  "minimum": 0.01,
  "maximum": 99999.99
}
```

#### Inteiro
```json
{
  "name": "quantity",
  "type": "integer",
  "description": "Quantidade",
  "minimum": 0,
  "maximum": 1000
}
```

#### Boolean
```json
{
  "name": "active",
  "type": "boolean",
  "description": "Status de ativação"
}
```

## 3. Sistema de Validação

### Validações Automáticas
1. JSON
  - Headers e body devem ser válidos
  - Erros desativam a função

2. Placeholders ({{variavel}})
  - Case-sensitive
  - Devem ter parâmetro correspondente

3. Parâmetros
  - Nomes únicos
  - Tipos corretos
  - Limites numéricos válidos
  - Enums sem valores vazios

### Erros e Avisos
- Função desativa se houver:
  - JSON inválido
  - Parâmetros não documentados
  - Violações de tipo
- Erros aparecem em `undocumentedParameters`

## 4. Exemplo Completo

```json
{
  "name": "createProduct",
  "description": "Criar novo produto no catálogo",
  "isActive": true,
  "method": "POST",
  "endpoint": "https://api.store.com/v1/products",
  "headers": {
    "Authorization": "Bearer {{apiKey}}",
    "Content-Type": "application/json"
  },
  "body": {
    "name": "{{productName}}",
    "price": "{{price}}",
    "category": "{{category}}"
  },
  "parameters": [
    {
      "name": "apiKey",
      "type": "string",
      "description": "Chave de API",
      "required": true
    },
    {
      "name": "productName",
      "type": "string",
      "description": "Nome do produto",
      "required": true
    },
    {
      "name": "price",
      "type": "number",
      "description": "Preço em reais",
      "required": true,
      "minimum": 0.01
    },
    {
      "name": "category",
      "type": "string",
      "description": "Categoria do produto",
      "required": true,
      "enum": "electronics,clothing,books"
    }
  ]
}
```


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Sim | ID da função. Vazio para criar nova, preenchido para editar existente. |
| delete | boolean | Sim | Se true, deleta a função especificada pelo ID. |
| function | object | Sim |  |


**Respostas:**

#### 200

Função atualizada com sucesso

Content-Type: `application/json`

Schema: `ChatbotAIFunction`

#### 201

Nova função criada com sucesso

Content-Type: `application/json`

Schema: `ChatbotAIFunction`

#### 400

Erro de validação nos dados fornecidos

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 404

Função não encontrada

#### 500

Erro interno do servidor


### GET /function/list

**Resumo:** Lista todas as funções de API

Retorna todas as funções de API configuradas para a instância atual

**Respostas:**

#### 200

Lista de funções recuperada com sucesso

Content-Type: `application/json`

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

### Grupos e Comunidades


### POST /group/create

**Resumo:** Criar um novo grupo

Cria um novo grupo no WhatsApp com participantes iniciais.

### Detalhes
- Requer autenticação via token da instância
- Os números devem ser fornecidos sem formatação (apenas dígitos)

### Limitações
- Mínimo de 1 participante além do criador
  
### Comportamento
- Retorna informações detalhadas do grupo criado
- Inclui lista de participantes adicionados com sucesso/falha


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| name | string | Sim | Nome do grupo |
| participants | array | Sim | Lista de números de telefone dos participantes iniciais |


**Respostas:**

#### 200

Grupo criado com sucesso

Content-Type: `application/json`

Schema: `Group`

#### 400

Erro de payload inválido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /group/info

**Resumo:** Obter informações detalhadas de um grupo

Recupera informações completas de um grupo do WhatsApp, incluindo:
- Detalhes do grupo
- Participantes
- Configurações
- Link de convite (opcional)


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| groupjid | string | Sim | Identificador único do grupo (JID) |
| getInviteLink | boolean | Não | Recuperar link de convite do grupo |
| getRequestsParticipants | boolean | Não | Recuperar lista de solicitações pendentes de participação |
| force | boolean | Não | Forçar atualização, ignorando cache |


**Respostas:**

#### 200

Informações do grupo obtidas com sucesso

Content-Type: `application/json`

Schema: `Group`

#### 400

Código de convite inválido ou mal formatado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 404

Grupo não encontrado ou link de convite expirado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /group/inviteInfo

**Resumo:** Obter informações de um grupo pelo código de convite

Retorna informações detalhadas de um grupo usando um código de convite ou URL completo do WhatsApp.

Esta rota permite:
- Recuperar informações básicas sobre um grupo antes de entrar
- Validar um link de convite
- Obter detalhes como nome do grupo, número de participantes e restrições de entrada


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| inviteCode | string | Sim | Código de convite ou URL completo do grupo. Pode ser um código curto ou a URL completa do WhatsApp.  |


**Respostas:**

#### 200

Informações do grupo obtidas com sucesso

Content-Type: `application/json`

Schema: `Group`

#### 400

Código de convite inválido ou mal formatado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 404

Grupo não encontrado ou link de convite expirado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### GET /group/invitelink/:groupJID

**Resumo:** Gerar link de convite para um grupo

Retorna o link de convite para o grupo especificado. 
Esta operação requer que o usuário seja um administrador do grupo.


**Parâmetros:**

| Nome | Localização | Tipo | Obrigatório | Descrição |
|------|-------------|------|-------------|----------|
| groupJID | path | string | Sim |  |

**Respostas:**

#### 200

Link de convite gerado com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| inviteLink | string | Não | Link de convite completo para o grupo |

#### 400

Erro ao processar a solicitação

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Descrição do erro |

#### 403

Usuário não tem permissão para gerar link

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Mensagem indicando falta de permissão |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Detalhes do erro interno |


### POST /group/join

**Resumo:** Entrar em um grupo usando código de convite

Permite entrar em um grupo do WhatsApp usando um código de convite ou URL completo. 

Características:
- Suporta código de convite ou URL completo
- Valida o código antes de tentar entrar no grupo
- Retorna informações básicas do grupo após entrada bem-sucedida
- Trata possíveis erros como convite inválido ou expirado


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| inviteCode | string | Sim | Código de convite ou URL completo do grupo.  Formatos aceitos: - Código completo: "IYnl5Zg9bUcJD32rJrDzO7" - URL completa: "https://chat.whatsapp.com/IYnl5Zg9bUcJD32rJrDzO7"  |


**Respostas:**

#### 200

Entrada no grupo realizada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não |  |
| group | object | Não |  |

#### 400

Código de convite inválido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 403

Usuário já está no grupo ou não tem permissão para entrar

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /group/leave

**Resumo:** Sair de um grupo

Remove o usuário atual de um grupo específico do WhatsApp.

Requisitos:
- O usuário deve estar conectado a uma instância válida
- O usuário deve ser um membro do grupo

Comportamentos:
- Se o usuário for o último administrador, o grupo será dissolvido
- Se o usuário for um membro comum, será removido do grupo


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| groupjid | string | Sim | Identificador único do grupo (JID) - Formato: número@g.us - Exemplo válido: 120363324255083289@g.us  |


**Respostas:**

#### 200

Saída do grupo realizada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não |  |

#### 400

Erro de payload inválido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor ou falha na conexão

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### GET /group/list

**Resumo:** Listar todos os grupos

Retorna uma lista com todos os grupos disponíveis para a instância atual do WhatsApp.

Recursos adicionais:
- Suporta atualização forçada do cache de grupos
- Recupera informações detalhadas de grupos conectados


**Parâmetros:**

| Nome | Localização | Tipo | Obrigatório | Descrição |
|------|-------------|------|-------------|----------|
| force | query | boolean | Não | Se definido como `true`, força a atualização do cache de grupos. Útil para garantir que as informações mais recentes sejam recuperadas.  Comportamentos: - `false` (padrão): Usa informações em cache - `true`: Busca dados atualizados diretamente do WhatsApp  |
| noparticipants | query | boolean | Não | Se definido como `true`, retorna a lista de grupos sem incluir os participantes. Útil para otimizar a resposta quando não há necessidade dos dados dos participantes.  Comportamentos: - `false` (padrão): Retorna grupos com lista completa de participantes - `true`: Retorna grupos sem incluir os participantes  |

**Respostas:**

#### 200

Lista de grupos recuperada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| groups | array | Não | Lista detalhada de grupos |

#### 500

Erro interno do servidor ao recuperar grupos

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Mensagem detalhando o erro encontrado |


### POST /group/list

**Resumo:** Listar todos os grupos com filtros e paginacao

Retorna uma lista com todos os grupos disponiveis para a instancia atual do WhatsApp, com opcoes de filtros e paginacao via corpo (POST).
A rota GET continua para quem prefere a listagem direta sem paginacao.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| page | integer | Não | Numero da pagina para paginacao (padrao 1) |
| pageSize | integer | Não | Quantidade de resultados por pagina (padrao 50, maximo 1000) |
| limit | integer | Não | Alias opcional para `pageSize` |
| offset | integer | Não | Deslocamento base zero; se informado recalcula a pagina |
| search | string | Não | Texto para filtrar grupos por nome/JID |
| force | boolean | Não | Se definido como `true`, forca a atualizacao do cache de grupos. Util para garantir que as informacoes mais recentes sejam recuperadas.  |
| noParticipants | boolean | Não | Se definido como `true`, retorna a lista de grupos sem incluir os participantes. Util para otimizar a resposta quando nao ha necessidade dos dados dos participantes.  |


**Respostas:**

#### 200

Lista de grupos recuperada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| groups | array | Não | Lista detalhada de grupos |
| pagination | object | Não |  |

#### 500

Erro interno do servidor ao recuperar grupos

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Mensagem detalhando o erro encontrado |


### POST /group/resetInviteCode

**Resumo:** Resetar código de convite do grupo

Gera um novo código de convite para o grupo, invalidando o código de convite anterior. 
Somente administradores do grupo podem realizar esta ação.

Principais características:
- Invalida o link de convite antigo
- Cria um novo link único
- Retorna as informações atualizadas do grupo


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| groupjid | string | Sim | Identificador único do grupo (JID) |


**Respostas:**

#### 200

Código de convite resetado com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| InviteLink | string | Não | Novo link de convite gerado |
| group | object | Não |  |

#### 400

Erro de validação

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 403

Usuário sem permissão

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /group/updateAnnounce

**Resumo:** Configurar permissões de envio de mensagens no grupo

Define as permissões de envio de mensagens no grupo, permitindo restringir o envio apenas para administradores.

Quando ativado (announce=true):
- Apenas administradores podem enviar mensagens
- Outros participantes podem apenas ler
- Útil para anúncios importantes ou controle de spam

Quando desativado (announce=false):
- Todos os participantes podem enviar mensagens
- Configuração padrão para grupos normais

Requer que o usuário seja administrador do grupo para fazer alterações.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| groupjid | string | Sim | Identificador único do grupo no formato xxxx@g.us |
| announce | boolean | Sim | Controla quem pode enviar mensagens no grupo |


**Respostas:**

#### 200

Configuração atualizada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não |  |
| group | object | Não |  |

#### 401

Token de autenticação ausente ou inválido

#### 403

Usuário não é administrador do grupo

#### 404

Grupo não encontrado

#### 500

Erro interno do servidor ou falha na API do WhatsApp


### POST /group/updateDescription

**Resumo:** Atualizar descrição do grupo

Altera a descrição (tópico) do grupo WhatsApp especificado.
Requer que o usuário seja administrador do grupo.
A descrição aparece na tela de informações do grupo e pode ser visualizada por todos os participantes.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| groupjid | string | Sim | JID (ID) do grupo no formato xxxxx@g.us |
| description | string | Sim | Nova descrição/tópico do grupo |


**Respostas:**

#### 200

Descrição atualizada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não |  |
| group | object | Não |  |

#### 401

Token inválido ou ausente

#### 403

Usuário não é administrador do grupo

#### 404

Grupo não encontrado

#### 413

Descrição excede o limite máximo permitido


### POST /group/updateImage

**Resumo:** Atualizar imagem do grupo

Altera a imagem do grupo especificado. A imagem pode ser enviada como URL ou como string base64.

Requisitos da imagem:
- Formato: JPEG
- Resolução máxima: 640x640 pixels
- Imagens maiores ou diferente de JPEG não são aceitas pelo WhatsApp

Para remover a imagem atual, envie "remove" ou "delete" no campo image.


**Parâmetros:**

| Nome | Localização | Tipo | Obrigatório | Descrição |
|------|-------------|------|-------------|----------|

**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| groupjid | string | Sim | JID do grupo |
| image | string | Sim | URL da imagem, string base64 ou "remove"/"delete" para remover. A imagem deve estar em formato JPEG e ter resolução máxima de 640x640.  |


**Respostas:**

#### 200

Imagem atualizada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não |  |
| group | object | Não |  |

#### 400

Erro nos parâmetros da requisição

#### 401

Token inválido ou expirado

#### 403

Usuário não é administrador do grupo

#### 413

Imagem muito grande

#### 415

Formato de imagem inválido


### POST /group/updateLocked

**Resumo:** Configurar permissão de edição do grupo

Define se apenas administradores podem editar as informações do grupo. 
Quando bloqueado (locked=true), apenas administradores podem alterar nome, descrição, 
imagem e outras configurações do grupo. Quando desbloqueado (locked=false), 
qualquer participante pode editar as informações.

Importante:
- Requer que o usuário seja administrador do grupo
- Afeta edições de nome, descrição, imagem e outras informações do grupo
- Não controla permissões de adição de membros


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| groupjid | string | Sim | Identificador único do grupo (JID) |
| locked | boolean | Sim | Define permissões de edição: - true = apenas admins podem editar infos do grupo - false = qualquer participante pode editar infos do grupo  |


**Respostas:**

#### 200

Operação realizada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não |  |
| group | object | Não |  |

#### 403

Usuário não é administrador do grupo

#### 404

Grupo não encontrado


### POST /group/updateName

**Resumo:** Atualizar nome do grupo

Altera o nome de um grupo do WhatsApp. Apenas administradores do grupo podem realizar esta operação.
O nome do grupo deve seguir as diretrizes do WhatsApp e ter entre 1 e 25 caracteres.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| groupjid | string | Sim | Identificador único do grupo no formato JID |
| name | string | Sim | Novo nome para o grupo |


**Respostas:**

#### 200

Nome do grupo atualizado com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não |  |
| group | object | Não |  |

#### 400

Erro de validação na requisição

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Token de autenticação ausente ou inválido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 403

Usuário não é administrador do grupo

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 404

Grupo não encontrado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /group/updateParticipants

**Resumo:** Gerenciar participantes do grupo

Gerencia participantes do grupo através de diferentes ações:
- Adicionar ou remover participantes
- Promover ou rebaixar administradores
- Aprovar ou rejeitar solicitações pendentes

Requer que o usuário seja administrador do grupo para executar as ações.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| groupjid | string | Sim | JID (identificador) do grupo |
| action | string | Sim | Ação a ser executada: - add: Adicionar participantes ao grupo - remove: Remover participantes do grupo - promote: Promover participantes a administradores - demote: Remover privilégios de administrador - approve: Aprovar solicitações pendentes de entrada - reject: Rejeitar solicitações pendentes de entrada  |
| participants | array | Sim | Lista de números de telefone ou JIDs dos participantes. Para números de telefone, use formato internacional sem '+' ou espaços.  |


**Respostas:**

#### 200

Sucesso na operação

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| groupUpdated | array | Não | Status da operação para cada participante |
| group | object | Não | Informações atualizadas do grupo |

#### 400

Erro nos parâmetros da requisição

#### 403

Usuário não é administrador do grupo

#### 500

Erro interno do servidor


### POST /community/create

**Resumo:** Criar uma comunidade

Cria uma nova comunidade no WhatsApp. Uma comunidade é uma estrutura que permite agrupar múltiplos grupos relacionados sob uma única administração. 

A comunidade criada inicialmente terá apenas o grupo principal (announcements), e grupos adicionais podem ser vinculados posteriormente usando o endpoint `/community/updategroups`.

**Observações importantes:**
- O número que cria a comunidade torna-se automaticamente o administrador
- A comunidade terá um grupo principal de anúncios criado automaticamente


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| name | string | Sim | Nome da comunidade |


**Respostas:**

#### 200

Comunidade criada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| group | object | Não |  |
| failed | array | Não | Lista de JIDs que falharam ao serem adicionados |

#### 400

Erro na requisição

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Token inválido ou não fornecido

#### 403

Sem permissão para criar comunidades

#### 429

Limite de criação de comunidades atingido

#### 500

Erro interno do servidor


### POST /community/editgroups

**Resumo:** Gerenciar grupos em uma comunidade

Adiciona ou remove grupos de uma comunidade do WhatsApp. Apenas administradores da comunidade podem executar estas operações.

## Funcionalidades
- Adicionar múltiplos grupos simultaneamente a uma comunidade
- Remover grupos de uma comunidade existente
- Suporta operações em lote

## Limitações
- Os grupos devem existir previamente
- A comunidade deve existir e o usuário deve ser administrador
- Grupos já vinculados não podem ser adicionados novamente
- Grupos não vinculados não podem ser removidos

## Ações Disponíveis
- `add`: Adiciona os grupos especificados à comunidade
- `remove`: Remove os grupos especificados da comunidade


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| community | string | Sim | JID (identificador único) da comunidade |
| action | string | Sim | Tipo de operação a ser realizada: * add - Adiciona grupos à comunidade * remove - Remove grupos da comunidade  |
| groupjids | array | Sim | Lista de JIDs dos grupos para adicionar ou remover |


**Respostas:**

#### 200

Operação realizada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| message | string | Não |  |
| success | array | Não | Lista de JIDs dos grupos processados com sucesso |
| failed | array | Não | Lista de JIDs dos grupos que falharam no processamento |

#### 400

Requisição inválida

#### 401

Não autorizado

#### 403

Usuário não é administrador da comunidade

### Instancia


### POST /instance/connect

**Resumo:** Conectar instância ao WhatsApp

Inicia o processo de conexão de uma instância ao WhatsApp. Este endpoint:
1. Requer o token de autenticação da instância
2. Recebe o número de telefone associado à conta WhatsApp
3. Gera um QR code caso não passe o campo `phone`
4. Ou Gera código de pareamento se passar o o campo `phone`
5. Atualiza o status da instância para "connecting"

O processo de conexão permanece pendente até que:
- O QR code seja escaneado no WhatsApp do celular, ou
- O código de pareamento seja usado no WhatsApp
- Timeout de 2 minutos para QRCode seja atingido ou 5 minutos para o código de pareamento

Use o endpoint /instance/status para monitorar o progresso da conexão.

Estados possíveis da instância:
- `disconnected`: Desconectado do WhatsApp
- `connecting`: Em processo de conexão
- `connected`: Conectado e autenticado

Exemplo de requisição:
```json
{
  "phone": "5511999999999"
}
```


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| phone | string | Sim | Número de telefone no formato internacional (ex: 5511999999999) |


**Respostas:**

#### 200

Sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| connected | boolean | Não | Estado atual da conexão |
| loggedIn | boolean | Não | Estado do login |
| jid | object | Não | ID do WhatsApp (quando logado) |
| instance | object | Não | Detalhes completos da instância |

#### 401

Token inválido/expirado

#### 404

Instância não encontrada

#### 429

Limite de conexões simultâneas atingido

#### 500

Erro interno


### POST /instance/disconnect

**Resumo:** Desconectar instância

Desconecta a instância do WhatsApp, encerrando a sessão atual.
Esta operação:

- Encerra a conexão ativa

- Requer novo QR code para reconectar


Diferenças entre desconectar e hibernar:

- Desconectar: Encerra completamente a sessão, exigindo novo login

- Hibernar: Mantém a sessão ativa, apenas pausa a conexão


Use este endpoint para:

1. Encerrar completamente uma sessão

2. Forçar uma nova autenticação

3. Limpar credenciais de uma instância

4. Reiniciar o processo de conexão


Estados possíveis após desconectar:

- `disconnected`: Desconectado do WhatsApp

- `connecting`: Em processo de reconexão (após usar /instance/connect)



### GET /instance/status

**Resumo:** Verificar status da instância

Retorna o status atual de uma instância, incluindo:
- Estado da conexão (disconnected, connecting, connected)
- QR code atualizado (se em processo de conexão)
- Código de pareamento (se disponível)
- Informações da última desconexão
- Detalhes completos da instância

Este endpoint é particularmente útil para:
1. Monitorar o progresso da conexão
2. Obter QR codes atualizados durante o processo de conexão
3. Verificar o estado atual da instância
4. Identificar problemas de conexão

Estados possíveis:
- `disconnected`: Desconectado do WhatsApp
- `connecting`: Em processo de conexão (aguardando QR code ou código de pareamento)
- `connected`: Conectado e autenticado com sucesso


**Respostas:**

#### 200

Sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| instance | object | Não |  |
| status | object | Não |  |

#### 401

Token inválido/expirado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 404

Instância não encontrada

#### 500

Erro interno


### POST /instance/updateInstanceName

**Resumo:** Atualizar nome da instância

Atualiza o nome de uma instância WhatsApp existente.
O nome não precisa ser único.	


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| name | string | Sim | Novo nome para a instância |


**Respostas:**

#### 200

Sucesso

Content-Type: `application/json`

Schema: `Instance`

#### 401

Token inválido/expirado

#### 404

Instância não encontrada

#### 500

Erro interno


### DELETE /instance

**Resumo:** Deletar instância

Remove a instância do sistema.


**Respostas:**

#### 200

Instância deletada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não |  |
| info | string | Não |  |

#### 401

Falha na autenticação

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 404

Instância não encontrada

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### GET /instance/privacy

**Resumo:** Buscar configurações de privacidade

Busca as configurações de privacidade atuais da instância do WhatsApp.

**Importante - Diferença entre Status e Broadcast:**

- **Status**: Refere-se ao recado personalizado que aparece embaixo do nome do usuário (ex: "Disponível", "Ocupado", texto personalizado)
- **Broadcast**: Refere-se ao envio de "stories/reels" (fotos/vídeos temporários)

**Limitação**: As configurações de privacidade do broadcast (stories/reels) não estão disponíveis para alteração via API.

Retorna todas as configurações de privacidade como quem pode:
- Adicionar aos grupos
- Ver visto por último
- Ver status (recado embaixo do nome)
- Ver foto de perfil
- Receber confirmação de leitura
- Ver status online
- Fazer chamadas


**Respostas:**

#### 200

Configurações de privacidade obtidas com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| groupadd | string | Não | Quem pode adicionar aos grupos. Valores - all, contacts, contact_blacklist, none |
| last | string | Não | Quem pode ver visto por último. Valores - all, contacts, contact_blacklist, none |
| status | string | Não | Quem pode ver status (recado embaixo do nome). Valores - all, contacts, contact_blacklist, none |
| profile | string | Não | Quem pode ver foto de perfil. Valores - all, contacts, contact_blacklist, none |
| readreceipts | string | Não | Confirmação de leitura. Valores - all, none |
| online | string | Não | Quem pode ver status online. Valores - all, match_last_seen |
| calladd | string | Não | Quem pode fazer chamadas. Valores - all, known |

#### 401

Token de autenticação inválido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /instance/privacy

**Resumo:** Alterar configurações de privacidade

Altera uma ou múltiplas configurações de privacidade da instância do WhatsApp de forma otimizada.

**Importante - Diferença entre Status e Broadcast:**

- **Status**: Refere-se ao recado personalizado que aparece embaixo do nome do usuário (ex: "Disponível", "Ocupado", texto personalizado)
- **Broadcast**: Refere-se ao envio de "stories/reels" (fotos/vídeos temporários)

**Limitação**: As configurações de privacidade do broadcast (stories/reels) não estão disponíveis para alteração via API.

**Características:**
- ✅ **Eficiência**: Altera apenas configurações que realmente mudaram
- ✅ **Flexibilidade**: Pode alterar uma ou múltiplas configurações na mesma requisição
- ✅ **Feedback completo**: Retorna todas as configurações atualizadas

**Formato de entrada:**
```json
{
  "groupadd": "contacts",
  "last": "none",
  "status": "contacts"
}
```

**Tipos de privacidade disponíveis:**
- `groupadd`: Quem pode adicionar aos grupos
- `last`: Quem pode ver visto por último
- `status`: Quem pode ver status (recado embaixo do nome)
- `profile`: Quem pode ver foto de perfil
- `readreceipts`: Confirmação de leitura
- `online`: Quem pode ver status online
- `calladd`: Quem pode fazer chamadas

**Valores possíveis:**
- `all`: Todos
- `contacts`: Apenas contatos
- `contact_blacklist`: Contatos exceto bloqueados
- `none`: Ninguém
- `match_last_seen`: Corresponder ao visto por último (apenas para online)
- `known`: Números conhecidos (apenas para calladd)


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| groupadd | string | Não | Quem pode adicionar aos grupos. Valores - all, contacts, contact_blacklist, none |
| last | string | Não | Quem pode ver visto por último. Valores - all, contacts, contact_blacklist, none |
| status | string | Não | Quem pode ver status (recado embaixo do nome). Valores - all, contacts, contact_blacklist, none |
| profile | string | Não | Quem pode ver foto de perfil. Valores - all, contacts, contact_blacklist, none |
| readreceipts | string | Não | Confirmação de leitura. Valores - all, none |
| online | string | Não | Quem pode ver status online. Valores - all, match_last_seen |
| calladd | string | Não | Quem pode fazer chamadas. Valores - all, known |


**Respostas:**

#### 200

Configuração de privacidade alterada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| groupadd | string | Não | Quem pode adicionar aos grupos. Valores - all, contacts, contact_blacklist, none |
| last | string | Não | Quem pode ver visto por último. Valores - all, contacts, contact_blacklist, none |
| status | string | Não | Quem pode ver status (recado embaixo do nome). Valores - all, contacts, contact_blacklist, none |
| profile | string | Não | Quem pode ver foto de perfil. Valores - all, contacts, contact_blacklist, none |
| readreceipts | string | Não | Confirmação de leitura. Valores - all, none |
| online | string | Não | Quem pode ver status online. Valores - all, match_last_seen |
| calladd | string | Não | Quem pode fazer chamadas. Valores - all, known |

#### 400

Dados de entrada inválidos

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Token de autenticação inválido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /instance/presence

**Resumo:** Atualizar status de presença da instância

Atualiza o status de presença global da instância do WhatsApp. Este endpoint permite:
1. Definir se a instância está disponível (Aparece "online") ou indisponível
2. Controlar o status de presença para todos os contatos
3. Salvar o estado atual da presença na instância

Tipos de presença suportados:
- available: Marca a instância como disponível/online
- unavailable: Marca a instância como indisponível/offline

**Atenção**:
- O status de presença pode ser temporariamente alterado para "available" (online) em algumas situações internas da API, e com isso o visto por último também pode ser atualizado.
- Caso isso for um problema, considere alterar suas configurações de privacidade no WhatsApp para não mostrar o visto por último e/ou quem pode ver seu status "online".

**⚠️ Importante - Limitação do Presence "unavailable"**:
- **Quando a API é o único dispositivo ativo**: Confirmações de entrega/leitura (ticks cinzas/azuis) não são enviadas nem recebidas
- **Impacto**: Eventos `message_update` com status de entrega podem não ser recebidos
- **Solução**: Se precisar das confirmações, mantenha WhatsApp Web ou aplicativo móvel ativo ou use presence "available" 

Exemplo de requisição:
```json
{
  "presence": "available"
}
```

Exemplo de resposta:
```json
{
  "response": "Presence updated successfully"
}
```

Erros comuns:
- 401: Token inválido ou expirado
- 400: Valor de presença inválido
- 500: Erro ao atualizar presença


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| presence | string | Sim | Status de presença da instância |


**Respostas:**

#### 200

Presença atualizada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| response | string | Não | Mensagem de confirmação |

#### 400

Requisição inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Descrição do erro |

#### 401

Token inválido ou expirado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Descrição do erro de autenticação |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Descrição do erro interno |

### Integração Chatwoot


### GET /chatwoot/config

**Resumo:** Obter configuração do Chatwoot

Retorna a configuração atual da integração com Chatwoot para a instância.

### Funcionalidades:
- Retorna todas as configurações do Chatwoot incluindo credenciais
- Mostra status de habilitação da integração
- Útil para verificar configurações atuais antes de fazer alterações


**Respostas:**

#### 200

Configuração obtida com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| chatwoot_enabled | boolean | Não | Se a integração com Chatwoot está habilitada |
| chatwoot_url | string | Não | URL base da instância Chatwoot |
| chatwoot_account_id | integer (int64) | Não | ID da conta no Chatwoot |
| chatwoot_inbox_id | integer (int64) | Não | ID da inbox no Chatwoot |
| chatwoot_access_token | string | Não | Token de acesso da API Chatwoot |
| chatwoot_ignore_groups | boolean | Não | Se deve ignorar mensagens de grupos na sincronização |
| chatwoot_sign_messages | boolean | Não | Se deve assinar mensagens enviadas para o WhatsApp |
| chatwoot_create_new_conversation | boolean | Não | Sempre criar nova conversa ao invés de reutilizar conversas existentes |

#### 401

Token inválido/expirado

#### 500

Erro interno do servidor


### PUT /chatwoot/config

**Resumo:** Atualizar configuração do Chatwoot

Atualiza a configuração da integração com Chatwoot para a instância.

### Funcionalidades:
- Configura todos os parâmetros da integração Chatwoot
- Reinicializa automaticamente o cliente Chatwoot quando habilitado
- Retorna URL do webhook para configurar no Chatwoot
- Sincronização bidirecional de mensagens novas entre WhatsApp e Chatwoot
- Sincronização automática de contatos (nome e telefone)
- Atualização automática LID → PN (Local ID para Phone Number)
- Sistema de nomes inteligentes com til (~)

### Configuração no Chatwoot:
1. Após configurar via API, use a URL retornada no webhook settings da inbox no Chatwoot
2. Configure como webhook URL na sua inbox do Chatwoot
3. A integração ficará ativa e sincronizará mensagens e contatos automaticamente

### 🏷️ Sistema de Nomes Inteligentes:
- **Nomes com til (~)**: São atualizados automaticamente quando o contato modifica seu nome no WhatsApp
- **Nomes específicos**: Para definir um nome fixo, remova o til (~) do nome no Chatwoot
- **Exemplo**: "~João Silva" será atualizado automaticamente, "João Silva" (sem til) permanecerá fixo
- **Atualização LID→PN**: Contatos migram automaticamente de Local ID para Phone Number quando disponível
- **Sem duplicação**: Durante a migração LID→PN, não haverá duplicação de conversas
- **Respostas nativas**: Todas as respostas dos agentes aparecem nativamente no Chatwoot

### 🚧 AVISO IMPORTANTE - INTEGRAÇÃO BETA:
- **Fase Beta**: Esta integração está em fase de desenvolvimento e testes
- **Uso por conta e risco**: O usuário assume total responsabilidade pelo uso
- **Recomendação**: Teste em ambiente não-produtivo antes de usar em produção
- **Suporte limitado**: Funcionalidades podem mudar sem aviso prévio

### ⚠️ Limitações Conhecidas:
- **Sincronização de histórico**: Não implementada - apenas mensagens novas são sincronizadas


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| enabled | boolean | Sim | Habilitar/desabilitar integração com Chatwoot |
| url | string | Sim | URL base da instância Chatwoot (sem barra final) |
| access_token | string | Sim | Token de acesso da API Chatwoot (obtido em Profile Settings > Access Token) |
| account_id | integer (int64) | Sim | ID da conta no Chatwoot (visível na URL da conta) |
| inbox_id | integer (int64) | Sim | ID da inbox no Chatwoot (obtido nas configurações da inbox) |
| ignore_groups | boolean | Não | Ignorar mensagens de grupos do WhatsApp na sincronização |
| sign_messages | boolean | Não | Assinar mensagens enviadas para WhatsApp com identificação do agente |
| create_new_conversation | boolean | Não | Sempre criar nova conversa ao invés de reutilizar conversas existentes |


**Respostas:**

#### 200

Configuração atualizada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| message | string | Não | Mensagem de confirmação |
| chatwoot_inbox_webhook_url | string | Não | URL do webhook para configurar na inbox do Chatwoot |

#### 400

Dados inválidos no body da requisição

#### 401

Token inválido/expirado

#### 500

Erro interno ao salvar configuração

### Mensagem em massa


### POST /sender/simple

**Resumo:** Criar nova campanha (Simples)

Cria uma nova campanha de envio com configurações básicas

**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| numbers | array | Sim | Lista de números para envio |
| type | string | Sim | Tipo da mensagem |
| delayMin | integer | Sim | Delay mínimo entre mensagens em segundos |
| delayMax | integer | Sim | Delay máximo entre mensagens em segundos |
| scheduled_for | integer | Sim | Timestamp em milissegundos ou minutos a partir de agora para agendamento |
| info | string | Não | Informações adicionais sobre a campanha |
| delay | integer | Não | Delay fixo entre mensagens (opcional) |
| mentions | string | Não | Menções na mensagem em formato JSON |
| text | string | Não | Texto da mensagem |
| linkPreview | boolean | Não | Habilitar preview de links em mensagens de texto. O preview será gerado automaticamente a partir da URL contida no texto. |
| linkPreviewTitle | string | Não | Título personalizado para o preview do link (opcional) |
| linkPreviewDescription | string | Não | Descrição personalizada para o preview do link (opcional) |
| linkPreviewImage | string | Não | URL ou dados base64 da imagem para o preview do link (opcional) |
| linkPreviewLarge | boolean | Não | Se deve usar preview grande ou pequeno (opcional, padrão false) |
| file | string | Não | URL da mídia ou arquivo (quando type é image, video, audio, document, etc.) |
| docName | string | Não | Nome do arquivo (quando type é document) |
| fullName | string | Não | Nome completo (quando type é contact) |
| phoneNumber | string | Não | Número do telefone (quando type é contact) |
| organization | string | Não | Organização (quando type é contact) |
| email | string | Não | Email (quando type é contact) |
| url | string | Não | URL (quando type é contact) |
| latitude | number | Não | Latitude (quando type é location) |
| longitude | number | Não | Longitude (quando type é location) |
| name | string | Não | Nome do local (quando type é location) |
| address | string | Não | Endereço (quando type é location) |
| footerText | string | Não | Texto do rodapé (quando type é list, button, poll ou carousel) |
| buttonText | string | Não | Texto do botão (quando type é list, button, poll ou carousel) |
| listButton | string | Não | Texto do botão da lista (quando type é list) |
| selectableCount | integer | Não | Quantidade de opções selecionáveis (quando type é poll) |
| choices | array | Não | Lista de opções (quando type é list, button, poll ou carousel). Para carousel, use formato específico com [texto], {imagem} e botões |
| imageButton | string | Não | URL da imagem para o botão (quando type é button) |


**Respostas:**

#### 200

campanha criada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| folder_id | string | Não | ID único da campanha criada |
| count | integer | Não | Quantidade de mensagens agendadas |
| status | string | Não | Status da operação |

#### 400

Erro nos parâmetros da requisição

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Erro de autenticação

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 409

Conflito - campanha já existe

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /sender/advanced

**Resumo:** Criar envio em massa avançado

Cria um novo envio em massa com configurações avançadas, permitindo definir
múltiplos destinatários e mensagens com delays personalizados.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| delayMin | integer | Não | Delay mínimo entre mensagens (segundos) |
| delayMax | integer | Não | Delay máximo entre mensagens (segundos) |
| info | string | Não | Descrição ou informação sobre o envio em massa |
| scheduled_for | integer | Não | Timestamp em milissegundos (date unix) ou minutos a partir de agora para agendamento |
| messages | array | Sim | Lista de mensagens a serem enviadas |


**Respostas:**

#### 200

Mensagens adicionadas à fila com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| folder_id | string | Não | ID da pasta/lote criado |
| count | integer | Não | Total de mensagens adicionadas à fila |
| status | string | Não | Status da operação |

#### 400

Erro nos parâmetros da requisição

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Descrição do erro |

#### 401

Não autorizado - token inválido ou ausente

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Mensagem de erro |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Detalhes do erro interno |


### POST /sender/edit

**Resumo:** Controlar campanha de envio em massa

Permite controlar campanhas de envio de mensagens em massa através de diferentes ações:

## Ações Disponíveis:

**🛑 stop** - Pausar campanha
- Pausa uma campanha ativa ou agendada
- Altera o status para "paused" 
- Use quando quiser interromper temporariamente o envio
- Mensagens já enviadas não são afetadas

**▶️ continue** - Continuar campanha  
- Retoma uma campanha pausada
- Altera o status para "scheduled"
- Use para continuar o envio após pausar uma campanha
- Não funciona em campanhas já concluídas ("done")

**🗑️ delete** - Deletar campanha
- Remove completamente a campanha
- Deleta apenas mensagens NÃO ENVIADAS (status "scheduled")
- Mensagens já enviadas são preservadas no histórico
- Operação é executada de forma assíncrona

## Status de Campanhas:
- **scheduled**: Agendada para envio
- **sending**: Enviando mensagens  
- **paused**: Pausada pelo usuário
- **done**: Concluída (não pode ser alterada)
- **deleting**: Sendo deletada (operação em andamento)


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| folder_id | string | Sim | Identificador único da campanha de envio |
| action | string | Sim | Ação a ser executada na campanha: - **stop**: Pausa a campanha (muda para status "paused") - **continue**: Retoma campanha pausada (muda para status "scheduled")  - **delete**: Remove campanha e mensagens não enviadas (assíncrono)  |


**Respostas:**

#### 200

Ação realizada com sucesso

Content-Type: `application/json`

#### 400

Requisição inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /sender/cleardone

**Resumo:** Limpar mensagens enviadas

Inicia processo de limpeza de mensagens antigas em lote que já foram enviadas com sucesso. Por padrão, remove mensagens mais antigas que 7 dias.

**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| hours | integer | Não | Quantidade de horas para manter mensagens. Mensagens mais antigas que esse valor serão removidas. |


**Respostas:**

#### 200

Limpeza iniciada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| status | string | Não | Status da operação |


### DELETE /sender/clearall

**Resumo:** Limpar toda fila de mensagens

Remove todas as mensagens da fila de envio em massa, incluindo mensagens pendentes e já enviadas.
Esta é uma operação irreversível.


**Respostas:**

#### 200

Fila de mensagens limpa com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| info | string | Não | Mensagem de confirmação |

#### 401

Não autorizado - token inválido ou ausente

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Mensagem de erro |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Detalhes do erro interno |


### GET /sender/listfolders

**Resumo:** Listar campanhas de envio

Retorna todas as campanhas de mensagens em massa com possibilidade de filtro por status

**Parâmetros:**

| Nome | Localização | Tipo | Obrigatório | Descrição |
|------|-------------|------|-------------|----------|
| status | query | string | Não | Filtrar campanhas por status |

**Respostas:**

#### 200

Lista de campanhas retornada com sucesso

Content-Type: `application/json`

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /sender/listmessages

**Resumo:** Listar mensagens de uma campanha

Retorna a lista de mensagens de uma campanha específica, com opções de filtro por status e paginação

**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| folder_id | string | Sim | ID da campanha a ser consultada |
| messageStatus | string | Não | Status das mensagens para filtrar |
| page | integer | Não | Número da página para paginação |
| pageSize | integer | Não | Quantidade de itens por página |


**Respostas:**

#### 200

Lista de mensagens retornada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| messages | array | Não |  |
| pagination | object | Não |  |

#### 400

Requisição inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

### Perfil


### POST /profile/name

**Resumo:** Altera o nome do perfil do WhatsApp

Altera o nome de exibição do perfil da instância do WhatsApp.

O endpoint realiza:
- Atualiza o nome do perfil usando o WhatsApp AppState
- Sincroniza a mudança com o servidor do WhatsApp
- Retorna confirmação da alteração

**Importante**: 
- A instância deve estar conectada ao WhatsApp
- O nome será visível para todos os contatos
- Pode haver um limite de alterações por período (conforme WhatsApp)


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| name | string | Sim | Novo nome do perfil do WhatsApp |


**Respostas:**

#### 200

Nome do perfil alterado com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| success | boolean | Não |  |
| message | string | Não |  |
| profile | object | Não |  |

#### 400

Dados inválidos na requisição

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Sem sessão ativa

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 403

Ação não permitida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /profile/image

**Resumo:** Altera a imagem do perfil do WhatsApp

Altera a imagem de perfil da instância do WhatsApp.

O endpoint realiza:
- Atualiza a imagem do perfil usando 
- Processa a imagem (URL, base64 ou comando de remoção)
- Sincroniza a mudança com o servidor do WhatsApp
- Retorna confirmação da alteração

**Importante**: 
- A instância deve estar conectada ao WhatsApp
- A imagem será visível para todos os contatos
- A imagem deve estar em formato JPEG e tamanho 640x640 pixels


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| image | string | Sim | Imagem do perfil. Pode ser: - URL da imagem (http/https) - String base64 da imagem - "remove" ou "delete" para remover a imagem atual  |


**Respostas:**

#### 200

Imagem do perfil alterada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| success | boolean | Não |  |
| message | string | Não |  |
| profile | object | Não |  |

#### 400

Dados inválidos na requisição

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Sem sessão ativa

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 403

Ação não permitida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 413

Imagem muito grande

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

### Proxy


### GET /instance/proxy

**Resumo:** Obter configuração de proxy da instância

A uazapiGO já utiliza um proxy gerenciado por padrão. Para dar liberdade ao cliente, é possível informar um proxy próprio.
Retorna o estado atual do proxy, com a URL mascarada e informações do último teste de conectividade.


**Respostas:**

#### 200

Configuração de proxy recuperada com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| enabled | boolean | Não | Indica se o proxy está habilitado |
| proxy_url | string | Não | URL do proxy (mascarada na resposta) |
| last_test_at | integer | Não | Timestamp (ms) do último teste |
| last_test_error | string | Não | Último erro de teste (se houver) |
| validation_error | boolean | Não | Indica se o último teste resultou em erro |

#### 401

Token inválido ou expirado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor ao recuperar a configuração

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Mensagem detalhando o erro encontrado |


### POST /instance/proxy

**Resumo:** Configurar ou alterar o proxy

Permite habilitar ou trocar para um proxy próprio. A URL é validada antes de salvar.
Quando já usamos o proxy gerenciado padrão, você pode substituí-lo enviando seu `proxy_url`.
A conexão pode ser reiniciada automaticamente para aplicar a mudança.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| enable | boolean | Sim | Define se o proxy deve ser habilitado; se `false`, remove o proxy atual |
| proxy_url | string | Não | URL do proxy a ser usado (obrigatória se `enable=true`) |


**Respostas:**

#### 200

Proxy configurado com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| details | string | Não |  |
| proxy | object | Não |  |
| restart_requested | boolean | Não | Indica se uma reinicialização da conexão foi solicitada para aplicar o proxy |

#### 400

Payload inválido ou falha na validação do proxy

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Token inválido ou expirado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor ao configurar o proxy

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Mensagem detalhando o erro encontrado |


### DELETE /instance/proxy

**Resumo:** Remover o proxy configurado

Desativa e apaga o proxy personalizado, voltando ao comportamento padrão (proxy gerenciado).
Pode reiniciar a conexão para aplicar a remoção.


**Respostas:**

#### 200

Configuração de proxy removida com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| details | string | Não |  |
| proxy | object | Não |  |
| restart_requested | boolean | Não | Indica se a conexão foi reiniciada para aplicar a mudança |

#### 401

Token inválido ou expirado

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor ao deletar a configuração de proxy

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não | Mensagem detalhando o erro encontrado |

### Respostas Rápidas


### POST /quickreply/edit

**Resumo:** Criar, atualizar ou excluir resposta rápida

Gerencia templates de respostas rápidas para agilizar o atendimento. Suporta mensagens de texto e mídia.

- Para criar: não inclua o campo `id`
- Para atualizar: inclua o `id` existente
- Para excluir: defina `delete: true` e inclua o `id`

Observação: Templates originados do WhatsApp (onWhatsApp=true) não podem ser modificados ou excluídos.


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Não | Necessário para atualizações/exclusões, omitir para criação |
| delete | boolean | Não | Definir como true para excluir o template |
| shortCut | string | Sim | Atalho para acesso rápido ao template |
| type | string | Sim | Tipo da mensagem |
| text | string | Não | Obrigatório para mensagens do tipo texto |
| file | string | Não | URL ou Base64 para tipos de mídia |
| docName | string | Não | Nome do arquivo opcional para tipo documento |


**Respostas:**

#### 200

Operação concluída com sucesso

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| message | string | Não |  |
| quickReplies | array | Não |  |

#### 400

Requisição inválida (erro de validação)

#### 403

Não é possível modificar template originado do WhatsApp

#### 404

Template não encontrado

#### 500

Erro no servidor


### GET /quickreply/showall

**Resumo:** Listar todas as respostas rápidas

Retorna todas as respostas rápidas cadastradas para a instância autenticada

**Respostas:**

#### 200

Lista de respostas rápidas

Content-Type: `application/json`

#### 500

Erro no servidor

### Webhooks e SSE


### GET /webhook

**Resumo:** Ver Webhook da Instância

Retorna a configuração atual do webhook da instância, incluindo:
- URL configurada
- Eventos ativos
- Filtros aplicados
- Configurações adicionais

Exemplo de resposta:
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "enabled": true,
    "url": "https://example.com/webhook",
    "events": ["messages", "messages_update"],
    "excludeMessages": ["wasSentByApi", "isGroupNo"],
    "addUrlEvents": true,
    "addUrlTypesMessages": true
  },
  {
    "id": "987fcdeb-51k3-09j8-x543-864297539100",
    "enabled": true,
    "url": "https://outro-endpoint.com/webhook",
    "events": ["connection", "presence"],
    "excludeMessages": [],
    "addUrlEvents": false,
    "addUrlTypesMessages": false
  }
]
```

A resposta é sempre um array, mesmo quando há apenas um webhook configurado.


**Respostas:**

#### 200

Configuração do webhook retornada com sucesso

Content-Type: `application/json`

#### 401

Token inválido ou não fornecido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### POST /webhook

**Resumo:** Configurar Webhook da Instância

Gerencia a configuração de webhooks para receber eventos em tempo real da instância.
Permite gerenciar múltiplos webhooks por instância através do campo ID e action.

### 🚀 Modo Simples (Recomendado)

**Uso mais fácil - sem complexidade de IDs**:
- Não inclua `action` nem `id` no payload
- Gerencia automaticamente um único webhook por instância
- Cria novo ou atualiza o existente automaticamente
- **Recomendado**: Sempre use `"excludeMessages": ["wasSentByApi"]` para evitar loops
- **Exemplo**: `{"url": "https://meusite.com/webhook", "events": ["messages"], "excludeMessages": ["wasSentByApi"]}`

### 🧪 Sites para Testes (ordenados por qualidade)

**Para testar webhooks durante desenvolvimento**:
1. **https://webhook.cool/** - ⭐ Melhor opção (sem rate limit, interface limpa)
2. **https://rbaskets.in/** - ⭐ Boa alternativa (confiável, baixo rate limit)
3. **https://webhook.site/** - ⚠️ Evitar se possível (rate limit agressivo)

### ⚙️ Modo Avançado (Para múltiplos webhooks)

**Para usuários que precisam de múltiplos webhooks por instância**:

💡 **Dica**: Mesmo precisando de múltiplos webhooks, considere usar `addUrlEvents` no modo simples.
Um único webhook pode receber diferentes tipos de eventos em URLs específicas 
(ex: `/webhook/message`, `/webhook/connection`), eliminando a necessidade de múltiplos webhooks.

1. **Criar Novo Webhook**:
   - Use `action: "add"`
   - Não inclua `id` no payload
   - O sistema gera ID automaticamente

2. **Atualizar Webhook Existente**:
   - Use `action: "update"`
   - Inclua o `id` do webhook no payload
   - Todos os campos serão atualizados

3. **Remover Webhook**:
   - Use `action: "delete"`
   - Inclua apenas o `id` do webhook
   - Outros campos são ignorados



### Eventos Disponíveis
- `connection`: Alterações no estado da conexão
- `history`: Recebimento de histórico de mensagens
- `messages`: Novas mensagens recebidas
- `messages_update`: Atualizações em mensagens existentes
- `call`: Eventos de chamadas VoIP
- `contacts`: Atualizações na agenda de contatos
- `presence`: Alterações no status de presença
- `groups`: Modificações em grupos
- `labels`: Gerenciamento de etiquetas
- `chats`: Eventos de conversas
- `chat_labels`: Alterações em etiquetas de conversas
- `blocks`: Bloqueios/desbloqueios
- `leads`: Atualizações de leads
- `sender`: Atualizações de campanhas, quando inicia, e quando completa

**Remover mensagens com base nos filtros**:
- `wasSentByApi`: Mensagens originadas pela API ⚠️ **IMPORTANTE:** Use sempre este filtro para evitar loops em automações
- `wasNotSentByApi`: Mensagens não originadas pela API
- `fromMeYes`: Mensagens enviadas pelo usuário
- `fromMeNo`: Mensagens recebidas de terceiros
- `isGroupYes`: Mensagens em grupos
- `isGroupNo`: Mensagens em conversas individuais

💡 **Prevenção de Loops**: Se você tem automações que enviam mensagens via API, sempre inclua `"excludeMessages": ["wasSentByApi"]` no seu webhook. Caso prefira receber esses eventos, certifique-se de que sua automação detecta mensagens enviadas pela própria API para não criar loops infinitos.

**Ações Suportadas**:
- `add`: Registrar novo webhook
- `delete`: Remover webhook existente

**Parâmetros de URL**:
- `addUrlEvents` (boolean): Quando ativo, adiciona o tipo do evento como path parameter na URL.
  Exemplo: `https://api.example.com/webhook/{evento}`
- `addUrlTypesMessages` (boolean): Quando ativo, adiciona o tipo da mensagem como path parameter na URL.
  Exemplo: `https://api.example.com/webhook/{tipo_mensagem}`

**Combinações de Parâmetros**:
- Ambos ativos: `https://api.example.com/webhook/{evento}/{tipo_mensagem}`
  Exemplo real: `https://api.example.com/webhook/message/conversation`
- Apenas eventos: `https://api.example.com/webhook/message`
- Apenas tipos: `https://api.example.com/webhook/conversation`

**Notas Técnicas**:
1. Os parâmetros são adicionados na ordem: evento → tipo mensagem
2. A URL deve ser configurada para aceitar esses parâmetros dinâmicos
3. Funciona com qualquer combinação de eventos/mensagens


**Request Body:**

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| id | string | Não | ID único do webhook (necessário para update/delete) |
| enabled | boolean | Não | Habilita/desabilita o webhook |
| url | string | Sim | URL para receber os eventos |
| events | array | Não | Lista de eventos monitorados |
| excludeMessages | array | Não | Filtros para excluir tipos de mensagens |
| addUrlEvents | boolean | Não | Adiciona o tipo do evento como parâmetro na URL. - `false` (padrão): URL normal - `true`: Adiciona evento na URL (ex: `/webhook/message`)  |
| addUrlTypesMessages | boolean | Não | Adiciona o tipo da mensagem como parâmetro na URL. - `false` (padrão): URL normal   - `true`: Adiciona tipo da mensagem (ex: `/webhook/conversation`)  |
| action | string | Não | Ação a ser executada: - add: criar novo webhook - update: atualizar webhook existente (requer id) - delete: remover webhook (requer apenas id) Se não informado, opera no modo simples (único webhook)  |


**Respostas:**

#### 200

Webhook configurado ou atualizado com sucesso

Content-Type: `application/json`

#### 400

Requisição inválida

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 401

Token inválido ou não fornecido

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |

#### 500

Erro interno do servidor

Content-Type: `application/json`


**Propriedades:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|----------|
| error | string | Não |  |


### GET /sse

**Resumo:** Server-Sent Events (SSE)

Receber eventos em tempo real via Server-Sent Events (SSE)

### Funcionalidades Principais:
- Configuração de URL para recebimento de eventos
- Seleção granular de tipos de eventos
- Filtragem avançada de mensagens
- Parâmetros adicionais na URL
- Gerenciamento múltiplo de webhooks

**Eventos Disponíveis**:
- `connection`: Alterações no estado da conexão
- `history`: Recebimento de histórico de mensagens
- `messages`: Novas mensagens recebidas
- `messages_update`: Atualizações em mensagens existentes
- `call`: Eventos de chamadas VoIP
- `contacts`: Atualizações na agenda de contatos
- `presence`: Alterações no status de presença
- `groups`: Modificações em grupos
- `labels`: Gerenciamento de etiquetas
- `chats`: Eventos de conversas
- `chat_labels`: Alterações em etiquetas de conversas
- `blocks`: Bloqueios/desbloqueios
- `leads`: Atualizações de leads


Estabelece uma conexão persistente para receber eventos em tempo real. Este
endpoint:

1. Requer autenticação via token

2. Mantém uma conexão HTTP aberta com o cliente

3. Envia eventos conforme ocorrem no servidor

4. Suporta diferentes tipos de eventos

Exemplo de uso:

```javascript

const eventSource = new
EventSource('/sse?token=SEU_TOKEN&events=chats,messages');


eventSource.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Novo evento:', data);
};


eventSource.onerror = function(error) {
  console.error('Erro na conexão SSE:', error);
};

```


Estrutura de um evento:

```json

{
  "type": "message",
  "data": {
    "id": "3EB0538DA65A59F6D8A251",
    "from": "5511999999999@s.whatsapp.net",
    "to": "5511888888888@s.whatsapp.net",
    "text": "Olá!",
    "timestamp": 1672531200000
  }
}

```

**Parâmetros:**

| Nome | Localização | Tipo | Obrigatório | Descrição |
|------|-------------|------|-------------|----------|
| token | query | string | Sim | Token de autenticação da instância |
| events | query | string | Sim | Tipos de eventos a serem recebidos (separados por vírgula) |

