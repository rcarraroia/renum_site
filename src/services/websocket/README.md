# WebSocket Integration - Sprint 09

## 📋 Visão Geral

Este diretório contém a implementação completa do cliente WebSocket para comunicação em tempo real.

## 🗂️ Arquivos

- **`types.ts`**: Definições de tipos TypeScript
- **`WebSocketClient.ts`**: Cliente WebSocket com reconexão automática
- **`README.md`**: Este arquivo

## 🚀 Como Usar

### 1. Usando o Hook `useWebSocket`

```typescript
import { useWebSocket } from '@/hooks/useWebSocket';

function MyComponent() {
  const {
    isConnected,
    connectionStatus,
    sendMessage,
    sendTyping,
    markAsRead,
  } = useWebSocket({
    url: 'ws://localhost:8000/ws',
    token: 'your-jwt-token',
    autoConnect: true,
    
    onMessage: (data) => {
      console.log('New message:', data);
    },
    
    onTyping: (data) => {
      console.log('User typing:', data);
    },
  });

  return (
    <div>
      <p>Status: {connectionStatus}</p>
      <button 
        onClick={() => sendMessage('conv-123', 'Hello!')}
        disabled={!isConnected}
      >
        Send Message
      </button>
    </div>
  );
}
```

### 2. Usando o Cliente Diretamente

```typescript
import { WebSocketClient } from '@/services/websocket/WebSocketClient';

const client = new WebSocketClient(
  {
    url: 'ws://localhost:8000/ws',
    token: 'your-jwt-token',
  },
  {
    onMessage: (data) => {
      console.log('Message received:', data);
    },
    onError: (data) => {
      console.error('Error:', data);
    },
  }
);

// Connect
client.connect();

// Send message
client.sendMessage('conversation-id', 'Hello World!');

// Disconnect
client.disconnect();
```

## 📡 Tipos de Mensagens

### Cliente → Servidor

```typescript
// Enviar mensagem
{
  type: 'message',
  conversation_id: 'uuid',
  content: 'Hello!'
}

// Indicador de digitação
{
  type: 'typing',
  conversation_id: 'uuid',
  is_typing: true
}

// Marcar como lida
{
  type: 'read',
  conversation_id: 'uuid',
  message_id: 'uuid'
}

// Sincronizar mensagens perdidas
{
  type: 'sync',
  conversation_id: 'uuid',
  last_message_id: 'uuid'
}

// Keep-alive
{
  type: 'ping'
}

// Atualizar presença
{
  type: 'presence',
  status: 'online' | 'away' | 'offline'
}

// Entrar em conversa
{
  type: 'join',
  conversation_id: 'uuid'
}

// Sair de conversa
{
  type: 'leave',
  conversation_id: 'uuid'
}
```

### Servidor → Cliente

```typescript
// Conexão estabelecida
{
  type: 'connected',
  user_id: 'uuid',
  timestamp: '2025-12-07T...'
}

// Nova mensagem
{
  type: 'message',
  message: {
    id: 'uuid',
    conversation_id: 'uuid',
    user_id: 'uuid',
    content: 'Hello!',
    role: 'user',
    created_at: '2025-12-07T...'
  }
}

// Mensagem enviada (confirmação)
{
  type: 'message_sent',
  message_id: 'uuid',
  timestamp: '2025-12-07T...'
}

// Indicador de digitação
{
  type: 'typing',
  user_id: 'uuid',
  conversation_id: 'uuid',
  is_typing: true
}

// Mensagem lida
{
  type: 'read',
  user_id: 'uuid',
  conversation_id: 'uuid',
  message_id: 'uuid',
  read_at: '2025-12-07T...'
}

// Atualização de presença
{
  type: 'presence',
  user_id: 'uuid',
  status: 'online',
  timestamp: '2025-12-07T...'
}

// Dados de sincronização
{
  type: 'sync_data',
  conversation_id: 'uuid',
  messages: [...],
  count: 5
}

// Keep-alive response
{
  type: 'pong',
  timestamp: '2025-12-07T...'
}

// Erro
{
  type: 'error',
  error: 'Error message',
  code: 'ERROR_CODE'
}
```

## 🔄 Reconexão Automática

O cliente implementa reconexão automática com backoff exponencial:

- **Tentativa 1**: 1 segundo
- **Tentativa 2**: 2 segundos
- **Tentativa 3**: 4 segundos
- **Tentativa 4**: 8 segundos
- **Tentativa 5**: 16 segundos
- **Tentativa 6+**: 32 segundos (máximo)

Máximo de 10 tentativas por padrão.

## 📦 Fila de Mensagens

Mensagens enviadas durante desconexão são armazenadas em fila e reenviadas automaticamente após reconexão.

Limite: 100 mensagens na fila.

## 🔐 Autenticação

O WebSocket usa JWT token para autenticação:

```typescript
const token = localStorage.getItem('token');

const ws = useWebSocket({
  url: 'ws://localhost:8000/ws',
  token: token,
});
```

O token é enviado como query parameter: `ws://api/ws?token=JWT_TOKEN`

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
VITE_WS_URL=ws://localhost:8000/ws
```

### Opções do Cliente

```typescript
interface WebSocketConfig {
  url: string;                    // URL do WebSocket
  token: string;                  // JWT token
  reconnectInterval?: number;     // Intervalo inicial (padrão: 1000ms)
  maxReconnectAttempts?: number;  // Máximo de tentativas (padrão: 10)
  pingInterval?: number;          // Intervalo de ping (padrão: 30000ms)
}
```

## 🧪 Testando

### Backend

```bash
cd backend
python test_websocket_simple.py
```

### Frontend

1. Inicie o backend:
```bash
cd backend
python -m src.main
```

2. Inicie o frontend:
```bash
npm run dev
```

3. Abra o navegador e acesse a página de conversas

4. Abra o console do navegador para ver logs do WebSocket

## 📊 Status de Conexão

```typescript
type ConnectionStatus = 
  | 'disconnected'   // Desconectado
  | 'connecting'     // Conectando
  | 'connected'      // Conectado
  | 'reconnecting'   // Reconectando
  | 'error';         // Erro
```

## 🎯 Exemplo Completo

Veja o arquivo `src/pages/dashboard/AdminConversationsPageWithWebSocket.tsx` para um exemplo completo de integração.

## ⚠️ Notas Importantes

1. **Token JWT**: Certifique-se de ter um token válido antes de conectar
2. **Backend Rodando**: O backend deve estar rodando na porta 8000
3. **CORS**: Configure CORS no backend para permitir conexões WebSocket
4. **Cleanup**: O hook `useWebSocket` faz cleanup automático ao desmontar

## 🐛 Troubleshooting

### Erro: "Invalid token"

- Verifique se o token JWT é válido
- Verifique se o token não expirou
- Verifique se o token está sendo enviado corretamente

### Erro: "Connection refused"

- Verifique se o backend está rodando
- Verifique se a porta está correta (8000)
- Verifique se não há firewall bloqueando

### Mensagens não aparecem

- Verifique se está conectado (`isConnected === true`)
- Verifique se entrou na conversa (`joinConversation()`)
- Verifique os logs do console

### Reconexão não funciona

- Verifique se `maxReconnectAttempts` não foi atingido
- Verifique se o backend está acessível
- Verifique os logs do console

## 📚 Referências

- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
- [JWT Authentication](https://jwt.io/)
