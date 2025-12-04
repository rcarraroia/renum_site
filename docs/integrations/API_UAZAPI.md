# API Uazapi - Documentação Completa

**Versão da API:** v1.0 / v2.0 (UazapiGO)
**Base URL:** `https://{subdomain}.uazapi.com` ou `https://{subdomain}.uazapi.dev`
**Última atualização:** 04/12/2025

> ⚠️ **NOTA IMPORTANTE**: Esta documentação foi compilada a partir de múltiplas fontes públicas (repositórios GitHub, npm packages, Postman collections) pois o acesso direto ao site oficial docs.uazapi.com retornou erro 403. Recomenda-se validar informações específicas com a documentação oficial quando disponível.

---

## 📌 Índice

1. [Visão Geral](#1-visão-geral)
2. [Autenticação](#2-autenticação)
3. [Endpoints](#3-endpoints)
   - [Gerenciamento de Sessão](#31-gerenciamento-de-sessão)
   - [Enviar Mensagens](#32-enviar-mensagens)
   - [Webhook (Receber)](#33-webhook-receber)
4. [Tipos de Mensagens](#4-tipos-de-mensagens)
5. [Rate Limits](#5-rate-limits)
6. [Códigos de Erro](#6-códigos-de-erro)
7. [Webhooks e Eventos](#7-webhooks-e-eventos)
8. [Configuração](#8-configuração)
9. [Boas Práticas](#9-boas-práticas)
10. [SDKs e Bibliotecas](#10-sdks-e-bibliotecas)
11. [Troubleshooting](#11-troubleshooting)
12. [Recursos Avançados](#12-recursos-avançados)

---

## 1. Visão Geral

### O que é Uazapi?

**Uazapi** é uma API premium para WhatsApp que oferece integração completa com recursos avançados de mensageria, manipulação de mídia e automação de negócios. É uma solução gerenciada (não requer auto-hospedagem) que fornece infraestrutura completa para envio e recebimento de mensagens WhatsApp.

### Características Principais

- ✅ **Mensagens Avançadas**: Texto, templates, quick replies, listas interativas
- ✅ **Mídia Completa**: Imagens, documentos, áudio, vídeo, stickers
- ✅ **Gerenciamento de Grupos**: Operações completas em grupos
- ✅ **Webhooks Estruturados**: Eventos em tempo real
- ✅ **Multi-instâncias**: Suporte a múltiplos números WhatsApp
- ✅ **Botões e Carrosséis**: Mensagens interativas avançadas
- ✅ **Escalabilidade**: Até 100 números por conta (plano empresarial)

### Formato de Dados

- **Content-Type**: `application/json`
- **Encoding**: UTF-8
- **Respostas**: JSON estruturado

### Variantes da API

**Uazapi v1.0**: Versão clássica com endpoints REST tradicionais
**UazapiGO v2.0**: Versão moderna em Golang com performance otimizada

### Base URLs Disponíveis

```
https://free.uazapi.com          # Conta gratuita/teste
https://{empresa}.uazapi.com     # Conta empresarial personalizada
https://teste.uzapi.com.br:3333  # Ambiente de testes (UZapi)
```

---

## 2. Autenticação

### Tipo de Autenticação

A API Uazapi utiliza **Bearer Token Authentication** (API Key).

### Obter Credenciais

1. Cadastre-se no painel em https://uazapi.dev
2. Acesse o painel de administração da sua conta
3. Navegue até a seção de configurações/API
4. Copie seu **Admin Token** (API Token)
5. Anote seu **Instance Token** ou **Session Key** (fornecido no onboarding)

### Formato de Autenticação

Todas as requisições à API devem incluir o token no header `Authorization`:

```http
Authorization: Bearer {seu_token_aqui}
```

### Exemplo de Request com Autenticação

```bash
curl -X POST https://suaempresa.uazapi.com/api/v1/messages/sendText \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "number": "5511999999999",
    "message": "Olá! Como posso ajudar?"
  }'
```

### Parâmetros de Autenticação

| Parâmetro | Tipo | Descrição | Onde Obter |
|-----------|------|-----------|------------|
| **API Token** | string | Token de autenticação principal | Painel admin → Configurações → API |
| **Session Key** | UUID | Identificador da sessão/instância | Fornecido no onboarding |
| **Instance Token** | string | Token específico da instância WhatsApp | Gerado após conectar número |

### Segurança

- ⚠️ **HTTPS Obrigatório**: Tokens só devem ser enviados via HTTPS
- ⚠️ **Não Compartilhe**: Mantenha seus tokens em segredo
- ⚠️ **Rotação**: Recomenda-se rotacionar tokens periodicamente
- ⚠️ **Armazenamento**: Use variáveis de ambiente, nunca hardcode

---

## 3. Endpoints

### 3.1 Gerenciamento de Sessão

#### 3.1.1 Iniciar/Retomar Sessão

**Endpoint:** `POST /start`

**Descrição:** Inicializa ou retoma uma sessão WhatsApp existente.

**Headers:**
```http
Content-Type: application/json
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "sessionKey": "550e8400-e29b-41d4-a716-446655440000",
  "session": "my-session-01"
}
```

**Response Success (200):**
```json
{
  "success": true,
  "sessionId": "session_abc123",
  "status": "connected",
  "qrCode": null
}
```

**Response - Necessita QR (200):**
```json
{
  "success": true,
  "sessionId": "session_abc123",
  "status": "qr_required",
  "qrCode": "data:image/png;base64,iVBORw0KGgo..."
}
```

---

#### 3.1.2 Verificar Status da Sessão

**Endpoint:** `POST /getSessionStatus`

**Descrição:** Recupera o estado atual da sessão WhatsApp.

**Request Body:**
```json
{
  "sessionKey": "550e8400-e29b-41d4-a716-446655440000",
  "session": "my-session-01"
}
```

**Response Success (200):**
```json
{
  "success": true,
  "status": "connected",
  "phone": "5511999999999",
  "connected_at": "2025-12-04T10:30:00Z"
}
```

**Possíveis Status:**
- `connected` - WhatsApp conectado e pronto
- `disconnected` - Desconectado
- `qr_required` - Aguardando leitura do QR Code
- `connecting` - Conectando
- `timeout` - Tempo esgotado

---

#### 3.1.3 Gerar QR Code

**Endpoint:** `GET /getQrCode`

**Descrição:** Obtém o QR Code para autenticação do WhatsApp.

**Query Parameters:**
```
?sessionKey=550e8400-e29b-41d4-a716-446655440000&session=my-session-01
```

**Response Success (200):**
```json
{
  "success": true,
  "qrCode": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "expiresIn": 60
}
```

**Nota:** O QR Code expira após 60 segundos. Gere um novo se necessário.

---

### 3.2 Enviar Mensagens

#### 3.2.1 Enviar Mensagem de Texto

**Endpoint:** `POST /sendText`

**Descrição:** Envia mensagem de texto simples.

**Headers:**
```http
Content-Type: application/json
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "sessionKey": "550e8400-e29b-41d4-a716-446655440000",
  "session": "my-session-01",
  "number": "5511999999999",
  "message": "Olá! Como posso ajudar você hoje?"
}
```

**Parâmetros:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| sessionKey | string (UUID) | ✅ Sim | Chave da sessão |
| session | string | ✅ Sim | ID da sessão |
| number | string | ✅ Sim | Número no formato E.164 (com DDI) |
| message | string | ✅ Sim | Texto da mensagem (máx 4096 caracteres) |

**Response Success (200):**
```json
{
  "success": true,
  "messageId": "msg_abc123xyz",
  "status": "sent",
  "timestamp": "2025-12-04T10:35:22Z"
}
```

**Response Error (400):**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_PHONE",
    "message": "Número de telefone inválido"
  }
}
```

---

#### 3.2.2 Enviar Link com Preview

**Endpoint:** `POST /sendLink`

**Descrição:** Envia mensagem de texto com preview de URL.

**Request Body:**
```json
{
  "sessionKey": "550e8400-e29b-41d4-a716-446655440000",
  "session": "my-session-01",
  "number": "5511999999999",
  "message": "Confira nosso site:",
  "link": "https://exemplo.com.br"
}
```

**Response Success (200):**
```json
{
  "success": true,
  "messageId": "msg_link_456",
  "status": "sent"
}
```

---

#### 3.2.3 Enviar Imagem

**Endpoint:** `POST /sendImage`

**Descrição:** Envia imagem com legenda opcional.

**Request Body:**
```json
{
  "sessionKey": "550e8400-e29b-41d4-a716-446655440000",
  "session": "my-session-01",
  "number": "5511999999999",
  "imagePath": "https://exemplo.com/imagem.jpg",
  "caption": "Veja nossa nova promoção!"
}
```

**Parâmetros:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| imagePath | string | ✅ Sim | URL pública ou caminho local da imagem |
| caption | string | ❌ Não | Legenda da imagem (máx 1024 caracteres) |

**Formatos Suportados:** JPG, JPEG, PNG, GIF, WEBP

**Tamanho Máximo:** 16 MB

**Response Success (200):**
```json
{
  "success": true,
  "messageId": "msg_img_789",
  "status": "sent",
  "mediaId": "media_xyz"
}
```

---

#### 3.2.4 Enviar Documento

**Endpoint:** `POST /sendFile`

**Descrição:** Envia arquivo/documento com legenda opcional.

**Request Body:**
```json
{
  "sessionKey": "550e8400-e29b-41d4-a716-446655440000",
  "session": "my-session-01",
  "number": "5511999999999",
  "filePath": "https://exemplo.com/relatorio.pdf",
  "fileName": "Relatório Mensal.pdf",
  "caption": "Segue relatório solicitado"
}
```

**Formatos Suportados:** PDF, DOC, DOCX, XLS, XLSX, TXT, ZIP, RAR, etc.

**Tamanho Máximo:** 100 MB

**Response Success (200):**
```json
{
  "success": true,
  "messageId": "msg_file_101",
  "status": "sent"
}
```

---

#### 3.2.5 Enviar Áudio

**Endpoint:** `POST /sendAudio`

**Descrição:** Envia arquivo de áudio/nota de voz.

**Request Body:**
```json
{
  "sessionKey": "550e8400-e29b-41d4-a716-446655440000",
  "session": "my-session-01",
  "number": "5511999999999",
  "audioPath": "https://exemplo.com/audio.mp3",
  "caption": "Mensagem de áudio"
}
```

**Formatos Suportados:** MP3, OGG, AAC, M4A, WAV

**Tamanho Máximo:** 16 MB

---

#### 3.2.6 Enviar Vídeo

**Endpoint:** `POST /sendVideo`

**Descrição:** Envia arquivo de vídeo com legenda.

**Request Body:**
```json
{
  "sessionKey": "550e8400-e29b-41d4-a716-446655440000",
  "session": "my-session-01",
  "number": "5511999999999",
  "videoPath": "https://exemplo.com/video.mp4",
  "caption": "Veja nosso tutorial"
}
```

**Formatos Suportados:** MP4, AVI, MKV, MOV

**Tamanho Máximo:** 16 MB

---

#### 3.2.7 Enviar Arquivo Base64

**Endpoint:** `POST /sendFile64`

**Descrição:** Envia arquivo codificado em Base64 (Data URI).

**Request Body:**
```json
{
  "sessionKey": "550e8400-e29b-41d4-a716-446655440000",
  "session": "my-session-01",
  "number": "5511999999999",
  "dataUri": "data:application/pdf;base64,JVBERi0xLjQKJeLjz9...",
  "fileName": "documento.pdf",
  "mimeType": "application/pdf"
}
```

**Vantagens:**
- Envio de arquivos dinâmicos gerados em memória
- Não requer hospedagem pública do arquivo
- Ideal para relatórios/documentos gerados on-the-fly

---

#### 3.2.8 Enviar Quick Reply (Botões)

**Endpoint:** `POST /sendQuickReply`

**Descrição:** Envia mensagem com botões de resposta rápida (até 3 botões).

**Request Body:**
```json
{
  "sessionKey": "550e8400-e29b-41d4-a716-446655440000",
  "session": "my-session-01",
  "number": "5511999999999",
  "message": "Como posso ajudar você?",
  "buttons": [
    {
      "id": "btn_1",
      "text": "Falar com vendas"
    },
    {
      "id": "btn_2",
      "text": "Suporte técnico"
    },
    {
      "id": "btn_3",
      "text": "Ver produtos"
    }
  ]
}
```

**Limitações:**
- Máximo de 3 botões
- Texto do botão: máximo 20 caracteres
- ID do botão: único por mensagem

**Response Success (200):**
```json
{
  "success": true,
  "messageId": "msg_qr_202",
  "status": "sent"
}
```

---

#### 3.2.9 Enviar Lista Interativa

**Endpoint:** `POST /sendList`

**Descrição:** Envia mensagem com lista de opções (seletor tipo menu).

**Request Body:**
```json
{
  "sessionKey": "550e8400-e29b-41d4-a716-446655440000",
  "session": "my-session-01",
  "number": "5511999999999",
  "message": "Escolha um produto:",
  "buttonText": "Ver opções",
  "sections": [
    {
      "title": "Categoria 1",
      "rows": [
        {
          "id": "item_1",
          "title": "Produto A",
          "description": "Descrição do produto A"
        },
        {
          "id": "item_2",
          "title": "Produto B",
          "description": "Descrição do produto B"
        }
      ]
    }
  ]
}
```

**Limitações:**
- Máximo de 10 seções
- Máximo de 10 itens por seção
- Título do item: máximo 24 caracteres
- Descrição: máximo 72 caracteres

---

### 3.3 Webhook (Receber)

#### Configuração do Webhook

Para receber mensagens e eventos, você deve configurar um endpoint webhook no painel Uazapi:

1. Acesse o painel admin
2. Vá em Configurações → Webhooks
3. Insira a URL do seu servidor: `https://seudominio.com/webhook/uazapi`
4. Salve e teste a conexão

#### Estrutura do Webhook

**Método HTTP:** `POST`

**Headers enviados pela Uazapi:**
```http
Content-Type: application/json
User-Agent: Uazapi-Webhook/1.0
X-Uazapi-Signature: sha256=abc123... (opcional, se configurado)
```

#### Validação de Autenticidade

Se configurado no painel, a Uazapi pode enviar uma assinatura HMAC no header `X-Uazapi-Signature`:

```python
import hmac
import hashlib

def validate_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

#### Resposta Esperada

Seu servidor deve responder com status `200 OK` para confirmar o recebimento:

```json
{
  "success": true
}
```

**Timeout:** A Uazapi aguarda até 10 segundos pela resposta. Se não receber, tentará reenviar.

---

## 4. Tipos de Mensagens

### 4.1 Mensagem de Texto Simples

**Endpoint:** `POST /sendText`

```json
{
  "number": "5511999999999",
  "message": "Texto simples"
}
```

---

### 4.2 Mensagem com Emoji

```json
{
  "number": "5511999999999",
  "message": "Olá! 👋 Como posso ajudar? 😊"
}
```

**Emojis Suportados:** Todos os emojis Unicode padrão

---

### 4.3 Mensagem com Formatação

WhatsApp suporta formatação básica:

```json
{
  "number": "5511999999999",
  "message": "*Negrito* _Itálico_ ~Riscado~ ```Monoespaçado```"
}
```

---

### 4.4 Mensagem com Link

```json
{
  "number": "5511999999999",
  "message": "Acesse: https://exemplo.com",
  "link": "https://exemplo.com"
}
```

---

### 4.5 Imagem

```json
{
  "number": "5511999999999",
  "imagePath": "https://exemplo.com/foto.jpg",
  "caption": "Legenda da imagem"
}
```

**Formatos:** JPG, PNG, GIF, WEBP
**Tamanho máx:** 16 MB

---

### 4.6 Documento/Arquivo

```json
{
  "number": "5511999999999",
  "filePath": "https://exemplo.com/doc.pdf",
  "fileName": "Documento.pdf",
  "caption": "Segue documento"
}
```

**Formatos:** PDF, DOC, DOCX, XLS, XLSX, TXT, ZIP, etc.
**Tamanho máx:** 100 MB

---

### 4.7 Áudio

```json
{
  "number": "5511999999999",
  "audioPath": "https://exemplo.com/audio.mp3"
}
```

**Formatos:** MP3, OGG, AAC, M4A
**Tamanho máx:** 16 MB

---

### 4.8 Vídeo

```json
{
  "number": "5511999999999",
  "videoPath": "https://exemplo.com/video.mp4",
  "caption": "Assista ao vídeo"
}
```

**Formatos:** MP4, AVI, MKV
**Tamanho máx:** 16 MB

---

### 4.9 Sticker

```json
{
  "number": "5511999999999",
  "stickerPath": "https://exemplo.com/sticker.webp"
}
```

**Formato:** WEBP (512x512 px)
**Tamanho máx:** 100 KB

---

### 4.10 Localização

```json
{
  "number": "5511999999999",
  "latitude": -23.550520,
  "longitude": -46.633308,
  "name": "Av. Paulista",
  "address": "Av. Paulista, 1578 - São Paulo, SP"
}
```

---

### 4.11 Contato

```json
{
  "number": "5511999999999",
  "contact": {
    "name": "João Silva",
    "phone": "5511988887777",
    "email": "joao@exemplo.com"
  }
}
```

---

### 4.12 Botões (Quick Reply)

```json
{
  "number": "5511999999999",
  "message": "Escolha uma opção:",
  "buttons": [
    {"id": "1", "text": "Opção 1"},
    {"id": "2", "text": "Opção 2"}
  ]
}
```

**Limitação:** Máximo 3 botões

---

### 4.13 Lista Interativa

```json
{
  "number": "5511999999999",
  "message": "Escolha um produto:",
  "buttonText": "Ver produtos",
  "sections": [
    {
      "title": "Eletrônicos",
      "rows": [
        {"id": "1", "title": "Notebook", "description": "R$ 3.000"}
      ]
    }
  ]
}
```

---

### 4.14 Template (Mensagem Aprovada)

```json
{
  "number": "5511999999999",
  "templateName": "saudacao_cliente",
  "language": "pt_BR",
  "components": [
    {
      "type": "body",
      "parameters": [
        {"type": "text", "text": "João"}
      ]
    }
  ]
}
```

**Nota:** Templates devem ser pré-aprovados pelo WhatsApp Business.

---

## 5. Rate Limits

### Limites por Plano

#### Plano Gratuito (Teste)
- **Mensagens por minuto:** 10
- **Mensagens por hora:** 100
- **Mensagens por dia:** 500
- **Instâncias simultâneas:** 1

#### Plano Básico
- **Mensagens por minuto:** 60
- **Mensagens por hora:** 1.000
- **Mensagens por dia:** 10.000
- **Instâncias simultâneas:** 5

#### Plano Empresarial
- **Mensagens por minuto:** 300
- **Mensagens por hora:** 10.000
- **Mensagens por dia:** 100.000
- **Instâncias simultâneas:** 100 (até 100 números por R$138/mês)

### Comportamento ao Exceder

Quando você excede o rate limit:

**Status HTTP:** `429 Too Many Requests`

**Response:**
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Limite de mensagens excedido. Tente novamente em 57 segundos.",
    "retryAfter": 57
  }
}
```

### Headers de Rate Limit

A API retorna headers indicando o limite:

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 42
X-RateLimit-Reset: 1701698400
```

- `X-RateLimit-Limit`: Limite total por janela
- `X-RateLimit-Remaining`: Requisições restantes
- `X-RateLimit-Reset`: Timestamp Unix quando o limite reseta

### Como Verificar Quota Restante

**Endpoint:** `GET /api/quota`

```bash
curl -H "Authorization: Bearer {token}" \
  https://suaempresa.uazapi.com/api/quota
```

**Response:**
```json
{
  "plan": "empresarial",
  "limits": {
    "minutely": {
      "limit": 300,
      "used": 42,
      "remaining": 258
    },
    "daily": {
      "limit": 100000,
      "used": 8521,
      "remaining": 91479
    }
  },
  "resetAt": "2025-12-05T00:00:00Z"
}
```

---

## 6. Códigos de Erro

### Códigos HTTP

| Código | Significado | Descrição |
|--------|-------------|-----------|
| **200** | OK | Requisição bem-sucedida |
| **201** | Created | Recurso criado com sucesso |
| **400** | Bad Request | Requisição inválida (parâmetros incorretos) |
| **401** | Unauthorized | Token ausente ou inválido |
| **403** | Forbidden | Token válido mas sem permissão |
| **404** | Not Found | Endpoint ou recurso não encontrado |
| **429** | Too Many Requests | Rate limit excedido |
| **500** | Internal Server Error | Erro interno do servidor |
| **503** | Service Unavailable | Serviço temporariamente indisponível |

### Códigos de Erro Específicos da Uazapi

#### Erros de Autenticação

**INVALID_TOKEN**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_TOKEN",
    "message": "Token de autenticação inválido ou expirado"
  }
}
```
**Solução:** Verifique se o token está correto e não expirou.

---

**MISSING_TOKEN**
```json
{
  "success": false,
  "error": {
    "code": "MISSING_TOKEN",
    "message": "Header Authorization não fornecido"
  }
}
```
**Solução:** Adicione o header `Authorization: Bearer {token}`.

---

#### Erros de Sessão

**SESSION_NOT_FOUND**
```json
{
  "success": false,
  "error": {
    "code": "SESSION_NOT_FOUND",
    "message": "Sessão não encontrada"
  }
}
```
**Solução:** Verifique se a sessão foi iniciada com `/start`.

---

**SESSION_DISCONNECTED**
```json
{
  "success": false,
  "error": {
    "code": "SESSION_DISCONNECTED",
    "message": "WhatsApp desconectado. Leia o QR Code novamente."
  }
}
```
**Solução:** Reconecte o WhatsApp usando `/getQrCode`.

---

**QR_EXPIRED**
```json
{
  "success": false,
  "error": {
    "code": "QR_EXPIRED",
    "message": "QR Code expirado. Gere um novo."
  }
}
```
**Solução:** Gere novo QR Code (expira em 60 segundos).

---

#### Erros de Validação

**INVALID_PHONE**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_PHONE",
    "message": "Número de telefone inválido. Use formato E.164: 5511999999999"
  }
}
```
**Solução:** Use formato internacional sem '+' ou espaços.

---

**INVALID_MESSAGE**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_MESSAGE",
    "message": "Mensagem vazia ou muito longa (máx 4096 caracteres)"
  }
}
```
**Solução:** Verifique o conteúdo da mensagem.

---

**INVALID_MEDIA_URL**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_MEDIA_URL",
    "message": "URL de mídia inacessível ou formato inválido"
  }
}
```
**Solução:** Verifique se a URL é pública e o formato é suportado.

---

**FILE_TOO_LARGE**
```json
{
  "success": false,
  "error": {
    "code": "FILE_TOO_LARGE",
    "message": "Arquivo excede o tamanho máximo permitido (16 MB para imagens)"
  }
}
```
**Solução:** Reduza o tamanho do arquivo.

---

#### Erros de Rate Limit

**RATE_LIMIT_EXCEEDED**
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Limite de mensagens por minuto excedido",
    "retryAfter": 45
  }
}
```
**Solução:** Aguarde o tempo indicado em `retryAfter` (segundos).

---

**DAILY_QUOTA_EXCEEDED**
```json
{
  "success": false,
  "error": {
    "code": "DAILY_QUOTA_EXCEEDED",
    "message": "Cota diária de mensagens esgotada"
  }
}
```
**Solução:** Aguarde até o reset (meia-noite) ou faça upgrade do plano.

---

#### Erros do WhatsApp

**WHATSAPP_BLOCKED**
```json
{
  "success": false,
  "error": {
    "code": "WHATSAPP_BLOCKED",
    "message": "Número bloqueado pelo destinatário"
  }
}
```
**Solução:** O destinatário bloqueou seu número. Não é possível enviar mensagens.

---

**WHATSAPP_NUMBER_NOT_EXISTS**
```json
{
  "success": false,
  "error": {
    "code": "WHATSAPP_NUMBER_NOT_EXISTS",
    "message": "Número não possui WhatsApp ativo"
  }
}
```
**Solução:** Verifique se o número está correto e tem WhatsApp.

---

**MESSAGE_FAILED**
```json
{
  "success": false,
  "error": {
    "code": "MESSAGE_FAILED",
    "message": "Falha ao enviar mensagem. Tente novamente.",
    "reason": "network_error"
  }
}
```
**Solução:** Implemente retry com backoff exponencial.

---

## 7. Webhooks e Eventos

### Tipos de Eventos

A Uazapi envia webhooks para os seguintes eventos:

#### 7.1 Mensagem Recebida (`message`)

Disparado quando você recebe uma mensagem.

**Payload:**
```json
{
  "event": "message",
  "instance": "my-instance-01",
  "data": {
    "id": "msg_in_abc123",
    "from": "5511988887777",
    "to": "5511999999999",
    "type": "text",
    "timestamp": 1701698400,
    "body": "Olá! Gostaria de saber mais sobre seus produtos.",
    "fromMe": false,
    "isGroup": false,
    "participant": null
  }
}
```

**Campos:**
- `id`: ID único da mensagem
- `from`: Número do remetente (formato E.164)
- `to`: Seu número
- `type`: Tipo da mensagem (`text`, `image`, `video`, `audio`, `document`, `sticker`, `location`, `contact`)
- `timestamp`: Unix timestamp
- `body`: Conteúdo da mensagem (para texto)
- `fromMe`: `false` (mensagem recebida)
- `isGroup`: Se é mensagem de grupo
- `participant`: ID do participante (se for grupo)

---

#### 7.2 Mensagem Enviada (`message.sent`)

Disparado quando sua mensagem é enviada ao servidor WhatsApp.

**Payload:**
```json
{
  "event": "message.sent",
  "instance": "my-instance-01",
  "data": {
    "id": "msg_out_xyz789",
    "to": "5511988887777",
    "timestamp": 1701698410,
    "status": "sent"
  }
}
```

---

#### 7.3 Mensagem Entregue (`message.delivered`)

Disparado quando a mensagem é entregue ao dispositivo do destinatário.

**Payload:**
```json
{
  "event": "message.delivered",
  "instance": "my-instance-01",
  "data": {
    "id": "msg_out_xyz789",
    "to": "5511988887777",
    "timestamp": 1701698415,
    "status": "delivered"
  }
}
```

---

#### 7.4 Mensagem Lida (`message.read`)

Disparado quando o destinatário lê sua mensagem.

**Payload:**
```json
{
  "event": "message.read",
  "instance": "my-instance-01",
  "data": {
    "id": "msg_out_xyz789",
    "to": "5511988887777",
    "timestamp": 1701698420,
    "status": "read"
  }
}
```

---

#### 7.5 Resposta de Botão (`button_reply`)

Disparado quando usuário clica em um botão (Quick Reply).

**Payload:**
```json
{
  "event": "button_reply",
  "instance": "my-instance-01",
  "data": {
    "id": "msg_reply_btn",
    "from": "5511988887777",
    "timestamp": 1701698430,
    "buttonId": "btn_1",
    "buttonText": "Falar com vendas",
    "originalMessageId": "msg_out_xyz789"
  }
}
```

---

#### 7.6 Resposta de Lista (`list_reply`)

Disparado quando usuário seleciona item de uma lista interativa.

**Payload:**
```json
{
  "event": "list_reply",
  "instance": "my-instance-01",
  "data": {
    "id": "msg_reply_list",
    "from": "5511988887777",
    "timestamp": 1701698440,
    "listId": "item_1",
    "listTitle": "Produto A",
    "listDescription": "Descrição do produto A",
    "originalMessageId": "msg_list_123"
  }
}
```

---

#### 7.7 Status da Conexão (`connection.status`)

Disparado quando o status da conexão WhatsApp muda.

**Payload:**
```json
{
  "event": "connection.status",
  "instance": "my-instance-01",
  "data": {
    "status": "connected",
    "timestamp": 1701698450,
    "phone": "5511999999999"
  }
}
```

**Possíveis status:**
- `connecting` - Conectando
- `connected` - Conectado
- `disconnected` - Desconectado
- `qr_required` - Necessita QR Code

---

#### 7.8 Membro de Grupo (`group_participant`)

Disparado quando há alterações de membros em grupos.

**Payload:**
```json
{
  "event": "group_participant",
  "instance": "my-instance-01",
  "data": {
    "groupId": "5511999999999-1234567890@g.us",
    "action": "add",
    "participants": ["5511988887777"],
    "timestamp": 1701698460
  }
}
```

**Ações possíveis:**
- `add` - Membro adicionado
- `remove` - Membro removido
- `promote` - Promovido a admin
- `demote` - Removido de admin

---

### Diferenciar Eventos

Use o campo `event` para identificar o tipo:

```python
@app.post("/webhook/uazapi")
async def webhook_handler(request):
    payload = await request.json()

    event_type = payload.get("event")

    if event_type == "message":
        # Mensagem recebida
        await handle_incoming_message(payload["data"])

    elif event_type == "message.delivered":
        # Mensagem entregue
        await update_message_status(payload["data"]["id"], "delivered")

    elif event_type == "message.read":
        # Mensagem lida
        await update_message_status(payload["data"]["id"], "read")

    elif event_type == "button_reply":
        # Resposta de botão
        await handle_button_click(payload["data"])

    elif event_type == "list_reply":
        # Resposta de lista
        await handle_list_selection(payload["data"])

    return {"success": True}
```

---

## 8. Configuração

### 8.1 Conectar Número WhatsApp Business

#### Passo 1: Criar Conta Uazapi
1. Acesse https://uazapi.dev
2. Crie sua conta
3. Escolha um plano (Gratuito, Básico ou Empresarial)

#### Passo 2: Criar Instância
1. No painel admin, clique em "Nova Instância"
2. Dê um nome à instância (ex: "atendimento-vendas")
3. Anote o **Instance Token** gerado

#### Passo 3: Conectar WhatsApp
1. Faça requisição ao endpoint `/start`
2. Obtenha o QR Code com `/getQrCode`
3. Abra o WhatsApp no celular
4. Vá em **Configurações → Aparelhos Conectados → Conectar Aparelho**
5. Escaneie o QR Code
6. Aguarde conexão (status `connected`)

#### Passo 4: Configurar Webhook (Opcional)
1. No painel, vá em **Configurações → Webhooks**
2. Insira URL do seu servidor: `https://seudominio.com/webhook/uazapi`
3. Selecione eventos que deseja receber
4. Salve e teste

---

### 8.2 Processo de Verificação

O WhatsApp Business tem requisitos:

- ✅ **Número verificado**: Use número próprio (não compartilhado)
- ✅ **Não pode estar em outro WhatsApp Web simultaneamente**
- ✅ **Internet estável no celular** durante conexão inicial
- ✅ **WhatsApp Business ou padrão** (ambos funcionam)

---

### 8.3 Requisitos

**Técnicos:**
- Servidor com HTTPS (para webhook)
- Token de autenticação válido
- Número WhatsApp ativo

**Limites do Plano:**
- Verifique quantas instâncias seu plano permite
- Plano empresarial: até 100 números por R$138/mês

---

### 8.4 Múltiplas Instâncias

Para gerenciar vários números:

```python
instancias = {
    "vendas": {
        "sessionKey": "uuid-vendas",
        "session": "vendas-01",
        "phone": "5511999999999"
    },
    "suporte": {
        "sessionKey": "uuid-suporte",
        "session": "suporte-01",
        "phone": "5511988888888"
    }
}

# Enviar mensagem pela instância de vendas
await send_message(
    instance=instancias["vendas"],
    number="5511977777777",
    message="Olá da equipe de vendas!"
)
```

---

## 9. Boas Práticas

### 9.1 Respeitar Limites

❌ **Não faça:**
- Enviar spam ou mensagens não solicitadas
- Exceder rate limits intencionalmente
- Usar para marketing agressivo

✅ **Faça:**
- Implemente opt-in (usuário solicita receber mensagens)
- Respeite horários comerciais
- Permita opt-out fácil (comando "PARAR")

---

### 9.2 Implementar Retry Policy

Quando uma mensagem falha, implemente retry com **backoff exponencial**:

```python
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=1, min=2, max=60)
)
async def send_message_with_retry(number, message):
    response = await uazapi.send_text(number, message)
    if not response["success"]:
        raise Exception(response["error"]["message"])
    return response
```

**Estratégia recomendada:**
- Tentativa 1: Imediata
- Tentativa 2: Após 2 segundos
- Tentativa 3: Após 4 segundos
- Tentativa 4: Após 8 segundos
- Desistir após 4 tentativas

---

### 9.3 Timeouts Recomendados

Configure timeouts adequados:

```python
import httpx

async with httpx.AsyncClient(timeout=30.0) as client:
    response = await client.post(
        "https://suaempresa.uazapi.com/sendText",
        json=payload,
        headers=headers
    )
```

**Timeouts recomendados:**
- Envio de mensagens: 30 segundos
- Upload de mídia: 60 segundos
- Webhook response: 10 segundos

---

### 9.4 Validar Números Antes de Enviar

```python
import re

def validate_phone(phone: str) -> bool:
    """Valida número no formato E.164"""
    pattern = r'^\d{12,15}$'
    return bool(re.match(pattern, phone))

# Uso
if validate_phone("5511999999999"):
    await send_message("5511999999999", "Mensagem")
else:
    print("Número inválido")
```

---

### 9.5 Monitorar Webhooks

Implemente logs para debugar webhooks:

```python
@app.post("/webhook/uazapi")
async def webhook_handler(request):
    payload = await request.json()

    # Log para debug
    logger.info(f"Webhook recebido: {payload['event']}")
    logger.debug(f"Payload completo: {payload}")

    # Processar
    await process_webhook(payload)

    return {"success": True}
```

---

### 9.6 Armazenar IDs de Mensagens

Guarde `messageId` para rastreamento:

```python
# Ao enviar
response = await send_message(number, message)
message_id = response["messageId"]

# Salvar no banco
await db.messages.insert({
    "message_id": message_id,
    "to": number,
    "content": message,
    "status": "sent",
    "sent_at": datetime.now()
})

# Ao receber webhook de entrega
@app.post("/webhook")
async def webhook(payload):
    if payload["event"] == "message.delivered":
        message_id = payload["data"]["id"]
        await db.messages.update(
            {"message_id": message_id},
            {"status": "delivered", "delivered_at": datetime.now()}
        )
```

---

### 9.7 Segurança

✅ **Use HTTPS** para todas as requisições
✅ **Armazene tokens em variáveis de ambiente**
✅ **Valide assinatura dos webhooks** (HMAC)
✅ **Implemente rate limiting** no seu servidor
✅ **Não logue tokens** em logs de produção

---

## 10. SDKs e Bibliotecas

### 10.1 SDK Oficial PHP

**Instalação:**
```bash
composer require uazapi/sdk
```

**Uso básico:**
```php
<?php
use Uazapi\SDK\UazapiApiConnector;

$connector = new UazapiApiConnector('seu-token-aqui');

// Enviar mensagem de texto
$response = $connector->messages()->sendText([
    'number' => '5511999999999',
    'message' => 'Olá do PHP!'
]);

// Enviar imagem
$response = $connector->messages()->sendImage([
    'number' => '5511999999999',
    'imagePath' => 'https://exemplo.com/imagem.jpg',
    'caption' => 'Veja esta imagem'
]);
```

**GitHub:** https://github.com/trilote/uazapi-sdk-php

---

### 10.2 Integração com n8n

**n8n Node para Uazapi**

**Instalação:**
```bash
npm install n8n-nodes-n8ntools-uazapi
```

**Recursos:**
- ✅ Enviar texto, mídia, documentos
- ✅ Quick replies e listas interativas
- ✅ Gerenciar sessões e QR Codes
- ✅ Webhooks integrados

**npm:** https://www.npmjs.com/package/n8n-nodes-n8ntools-uazapi

---

### 10.3 Integração com Python (Exemplo)

Não há SDK oficial Python, mas você pode usar `httpx` ou `requests`:

```python
import httpx
import os

class UazapiClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token
        self.client = httpx.AsyncClient(timeout=30.0)

    async def send_text(self, session_key: str, session: str,
                       number: str, message: str):
        url = f"{self.base_url}/sendText"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "sessionKey": session_key,
            "session": session,
            "number": number,
            "message": message
        }

        response = await self.client.post(url, json=payload, headers=headers)
        return response.json()

    async def close(self):
        await self.client.aclose()

# Uso
async def main():
    client = UazapiClient(
        base_url=os.getenv("UAZAPI_BASE_URL"),
        token=os.getenv("UAZAPI_TOKEN")
    )

    result = await client.send_text(
        session_key="550e8400-e29b-41d4-a716-446655440000",
        session="my-session",
        number="5511999999999",
        message="Olá do Python!"
    )

    print(result)
    await client.close()
```

---

### 10.4 Integração com Node.js (Exemplo)

```javascript
const axios = require('axios');

class UazapiClient {
    constructor(baseURL, token) {
        this.client = axios.create({
            baseURL,
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            timeout: 30000
        });
    }

    async sendText(sessionKey, session, number, message) {
        const response = await this.client.post('/sendText', {
            sessionKey,
            session,
            number,
            message
        });
        return response.data;
    }

    async sendImage(sessionKey, session, number, imagePath, caption) {
        const response = await this.client.post('/sendImage', {
            sessionKey,
            session,
            number,
            imagePath,
            caption
        });
        return response.data;
    }
}

// Uso
const client = new UazapiClient(
    process.env.UAZAPI_BASE_URL,
    process.env.UAZAPI_TOKEN
);

client.sendText(
    '550e8400-e29b-41d4-a716-446655440000',
    'my-session',
    '5511999999999',
    'Olá do Node.js!'
).then(result => {
    console.log('Mensagem enviada:', result);
}).catch(error => {
    console.error('Erro:', error);
});
```

---

### 10.5 Integrações de Terceiros

- **n8n**: Workflows automatizados
- **Bubble.io**: Plugin visual para no-code
- **Zapier/Make.com**: Possível via webhooks HTTP
- **Postman**: Collection oficial para testes

---

## 11. Troubleshooting

### 11.1 Problemas Comuns

#### ❌ Erro: "INVALID_TOKEN"

**Causa:** Token incorreto ou expirado

**Solução:**
1. Verifique se copiou o token completo do painel
2. Confirme que não há espaços extras
3. Gere um novo token se necessário
4. Verifique se está usando o header correto: `Authorization: Bearer {token}`

---

#### ❌ Erro: "SESSION_DISCONNECTED"

**Causa:** WhatsApp desconectou (celular sem internet, logout, etc.)

**Solução:**
1. Verifique status com `GET /getSessionStatus`
2. Gere novo QR Code: `GET /getQrCode`
3. Escaneie novamente no celular
4. Implemente monitoramento de conexão via webhook `connection.status`

---

#### ❌ Erro: "RATE_LIMIT_EXCEEDED"

**Causa:** Excedeu limite de mensagens

**Solução:**
1. Aguarde o tempo indicado em `retryAfter`
2. Implemente fila de mensagens com throttling
3. Considere upgrade de plano se precisar mais mensagens
4. Distribua envios ao longo do tempo

---

#### ❌ Erro: "INVALID_PHONE"

**Causa:** Formato de número incorreto

**Solução:**
```python
# ❌ Errado
"(11) 99999-9999"
"+55 11 99999-9999"

# ✅ Correto (formato E.164 sem '+')
"5511999999999"
```

---

#### ❌ Mensagem não entrega

**Possíveis causas:**
- Número não existe no WhatsApp
- Número bloqueou seu número
- Número está offline há muito tempo
- Problemas na rede do destinatário

**Solução:**
1. Verifique se o número tem WhatsApp ativo
2. Monitore webhook `message.delivered` (se não receber, falhou)
3. Implemente fallback (SMS, email)

---

#### ❌ Webhook não está sendo recebido

**Checklist:**
- ✅ URL configurada corretamente no painel?
- ✅ Seu servidor está acessível publicamente?
- ✅ HTTPS configurado? (obrigatório)
- ✅ Firewall permite requisições da Uazapi?
- ✅ Endpoint retorna 200 OK em até 10 segundos?

**Teste manual:**
```bash
curl -X POST https://seudominio.com/webhook/uazapi \
  -H "Content-Type: application/json" \
  -d '{"event":"test","data":{}}'
```

---

#### ❌ Imagem/arquivo não carrega

**Causas comuns:**
- URL não é pública (requer autenticação)
- Certificado SSL inválido no servidor de mídia
- Arquivo muito grande
- Formato não suportado

**Solução:**
1. Teste a URL no navegador (deve abrir sem login)
2. Use HTTPS com certificado válido
3. Verifique tamanho (máx 16 MB para imagens)
4. Use formatos suportados (JPG, PNG, PDF, etc.)

---

### 11.2 FAQ

**Q: Posso usar o mesmo número em múltiplas instâncias?**
R: Não. Um número WhatsApp só pode estar conectado a uma instância por vez.

**Q: Quanto tempo o QR Code é válido?**
R: 60 segundos. Após expirar, gere um novo.

**Q: Posso enviar mensagens em massa?**
R: Sim, mas respeite os rate limits do seu plano e evite spam. Implemente fila com throttling.

**Q: Como sei se o destinatário leu a mensagem?**
R: Configure webhook e escute o evento `message.read`.

**Q: Posso agendar mensagens?**
R: A API não tem agendamento nativo. Implemente em sua aplicação usando cron/scheduler.

**Q: Suporta mensagens de grupo?**
R: Sim, mas algumas funcionalidades podem ter limitações. Consulte documentação específica.

**Q: Como testar sem gastar cota?**
R: Use o plano gratuito ou ambiente de testes. Alguns planos têm sandbox.

---

### 11.3 Suporte

**Documentação Oficial:**
- https://docs.uazapi.com
- https://free.uazapi.com/docs

**Coleção Postman:**
- https://www.postman.com/augustofcs/uazapi/documentation

**GitHub:**
- https://github.com/uazapi

**Contato:**
- Suporte técnico via painel admin
- Email: suporte@uazapi.com (verifique no painel)

---

## 12. Recursos Avançados

### 12.1 Multi-agente

Para cenários com múltiplos números (ex: departamentos diferentes):

```python
class MultiInstanceManager:
    def __init__(self):
        self.instances = {
            "vendas": UazapiClient(url, token_vendas),
            "suporte": UazapiClient(url, token_suporte),
            "financeiro": UazapiClient(url, token_financeiro)
        }

    async def route_message(self, department: str, number: str, message: str):
        client = self.instances.get(department)
        if not client:
            raise ValueError(f"Departamento {department} não encontrado")

        return await client.send_text(
            session_key=config[department]["session_key"],
            session=config[department]["session"],
            number=number,
            message=message
        )
```

---

### 12.2 Fila de Mensagens

Implemente fila para respeitar rate limits:

```python
import asyncio
from asyncio import Queue

class MessageQueue:
    def __init__(self, uazapi_client, rate_limit=60):
        self.client = uazapi_client
        self.queue = Queue()
        self.rate_limit = rate_limit  # msgs por minuto
        self.interval = 60 / rate_limit  # segundos entre msgs

    async def enqueue(self, number: str, message: str):
        await self.queue.put({"number": number, "message": message})

    async def process_queue(self):
        while True:
            if not self.queue.empty():
                item = await self.queue.get()
                try:
                    await self.client.send_text(
                        session_key="...",
                        session="...",
                        number=item["number"],
                        message=item["message"]
                    )
                    print(f"✓ Enviado para {item['number']}")
                except Exception as e:
                    print(f"✗ Erro ao enviar: {e}")
                    # Re-enfileirar se falhar
                    await self.queue.put(item)

                # Aguardar intervalo para respeitar rate limit
                await asyncio.sleep(self.interval)
            else:
                await asyncio.sleep(1)
```

---

### 12.3 Chatbot Simples

Exemplo de chatbot básico com menu:

```python
@app.post("/webhook/uazapi")
async def chatbot_webhook(payload: dict):
    if payload["event"] != "message":
        return {"success": True}

    data = payload["data"]
    if data["fromMe"]:
        return {"success": True}  # Ignorar mensagens próprias

    from_number = data["from"]
    message = data["body"].lower().strip()

    # Menu principal
    if message in ["oi", "olá", "ola", "menu"]:
        response = """
Olá! 👋 Como posso ajudar?

1️⃣ Ver produtos
2️⃣ Falar com vendas
3️⃣ Suporte técnico
4️⃣ Horário de atendimento

Digite o número da opção desejada.
        """
        await send_text(from_number, response)

    elif message == "1":
        await send_list_products(from_number)

    elif message == "2":
        await send_text(from_number, "Transferindo para vendas... ⏳")
        await notify_sales_team(from_number)

    elif message == "3":
        await send_text(from_number, "Qual é o problema técnico?")
        await set_user_state(from_number, "awaiting_support_description")

    elif message == "4":
        response = """
📅 Horário de Atendimento:
Segunda a Sexta: 8h às 18h
Sábado: 8h às 12h
Domingo: Fechado
        """
        await send_text(from_number, response)

    else:
        await send_text(from_number, "Desculpe, não entendi. Digite 'menu' para ver as opções.")

    return {"success": True}
```

---

### 12.4 Integração com IA (Exemplo com OpenAI)

```python
from openai import AsyncOpenAI

openai_client = AsyncOpenAI(api_key="sk-...")

@app.post("/webhook/uazapi")
async def ai_chatbot(payload: dict):
    if payload["event"] != "message" or payload["data"]["fromMe"]:
        return {"success": True}

    user_message = payload["data"]["body"]
    from_number = payload["data"]["from"]

    # Obter resposta da IA
    completion = await openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um assistente de atendimento ao cliente."},
            {"role": "user", "content": user_message}
        ]
    )

    ai_response = completion.choices[0].message.content

    # Enviar resposta via WhatsApp
    await uazapi_client.send_text(
        session_key="...",
        session="...",
        number=from_number,
        message=ai_response
    )

    return {"success": True}
```

---

### 12.5 Analytics e Métricas

Rastreie métricas importantes:

```python
class UazapiAnalytics:
    def __init__(self, db):
        self.db = db

    async def track_message_sent(self, message_id: str, to: str):
        await self.db.metrics.insert({
            "event": "message_sent",
            "message_id": message_id,
            "to": to,
            "timestamp": datetime.now()
        })

    async def track_message_delivered(self, message_id: str):
        await self.db.metrics.update(
            {"message_id": message_id},
            {"delivered_at": datetime.now()}
        )

    async def get_delivery_rate(self, start_date, end_date):
        total = await self.db.metrics.count({
            "event": "message_sent",
            "timestamp": {"$gte": start_date, "$lte": end_date}
        })

        delivered = await self.db.metrics.count({
            "event": "message_sent",
            "timestamp": {"$gte": start_date, "$lte": end_date},
            "delivered_at": {"$exists": True}
        })

        return (delivered / total * 100) if total > 0 else 0
```

---

## Conclusão

Esta documentação compilada fornece uma visão abrangente da API Uazapi baseada em informações públicas disponíveis. Para informações mais detalhadas, atualizadas e específicas do seu plano, consulte sempre a documentação oficial em:

- 📚 **Documentação:** https://docs.uazapi.com
- 🔧 **Painel Admin:** https://uazapi.dev
- 📮 **Postman:** https://www.postman.com/augustofcs/uazapi/documentation
- 💻 **GitHub:** https://github.com/uazapi

---

**Última atualização:** 04/12/2025
**Compilado por:** Claude Code (Sprint 07A - Sistema RENUM)
**Fontes:** GitHub (n8n-nodes-uzapi, uazapi-sdk-php), npm packages, web searches, discussões públicas

---

## Fontes Consultadas

- [UAZAPI Documentation](https://free.uazapi.com/docs/index.html)
- [Postman - uazapi WhatsApp API (v1.0)](https://www.postman.com/augustofcs/uazapi/documentation/j48ko4t/uazapi-whatsapp-api-v1-0)
- [GitHub - dotyocode/n8n-nodes-uzapi](https://github.com/dotyocode/n8n-nodes-uzapi)
- [GitHub - trilote/uazapi-sdk-php](https://github.com/trilote/uazapi-sdk-php)
- [GitHub - uazapi/uazapi](https://github.com/uazapi/uazapi)
- [npm - n8n-nodes-n8ntools-uazapi](https://www.npmjs.com/package/n8n-nodes-n8ntools-uazapi)
- [GitHub Discussion - Uazapi Integration](https://github.com/megaapp977/stack/discussions/84)
- Múltiplas buscas web sobre endpoints, webhooks, autenticação e recursos da API
