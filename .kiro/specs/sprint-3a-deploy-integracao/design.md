# Design Document - Sprint 3A: Deploy e Integração

## Architecture Overview

Este sprint estabelece a arquitetura de integração entre frontend React e backend FastAPI, com foco em desenvolvimento local e preparação para produção futura.

### System Context

```
┌─────────────────────────────────────────────────────────────────┐
│                      DESENVOLVIMENTO LOCAL                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │  Frontend React  │         │  Backend FastAPI │             │
│  │  localhost:5173  │◄───────►│  localhost:8000  │             │
│  │                  │  HTTP   │                  │             │
│  │  - Login/Logout  │  + JWT  │  - Auth Routes   │             │
│  │  - CRUD Pages    │         │  - CRUD Routes   │             │
│  │  - API Client    │         │  - Middleware    │             │
│  └──────────────────┘         └────────┬─────────┘             │
│                                         │                        │
│                                         │ Supabase Client        │
│                                         ▼                        │
│                              ┌──────────────────┐               │
│                              │    Supabase      │               │
│                              │   (PostgreSQL)   │               │
│                              │                  │               │
│                              │  - profiles      │               │
│                              │  - clients       │               │
│                              │  - leads         │               │
│                              │  - projects      │               │
│                              │  - RLS Policies  │               │
│                              └──────────────────┘               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Production Architecture (Preparada, Não Usada)

```
┌─────────────────────────────────────────────────────────────────┐
│                         PRODUÇÃO (VPS)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐                                           │
│  │      Nginx       │  Proxy Reverso + SSL                      │
│  │   Port 80/443    │                                           │
│  └────────┬─────────┘                                           │
│           │                                                      │
│           ├──────────► /api/* ──────┐                          │
│           │                          │                          │
│           └──────────► /* ───────┐  │                          │
│                                   │  │                          │
│  ┌────────────────────────────┐  │  │  ┌──────────────────┐   │
│  │    Frontend (Static)       │◄─┘  └─►│  Backend FastAPI │   │
│  │    Servido pelo Nginx      │         │   Port 8000      │   │
│  └────────────────────────────┘         └────────┬─────────┘   │
│                                                   │              │
│  ┌────────────────┐                              │              │
│  │     Redis      │◄─────────────────────────────┘              │
│  │   Port 6379    │  Cache + Celery Broker                      │
│  └────────────────┘                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Internet
                              ▼
                   ┌──────────────────┐
                   │    Supabase      │
                   │   (PostgreSQL)   │
                   └──────────────────┘
```

## Component Design

### Backend Components

#### 1. Main Application (src/main.py)

**Responsibilities:**
- Initialize FastAPI application
- Configure CORS middleware
- Register API routers
- Configure exception handlers
- Setup logging

**Key Configuration:**
```python
app = FastAPI(
    title="RENUM API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 2. Configuration (src/config/settings.py)

**Responsibilities:**
- Load environment variables
- Validate configuration
- Provide settings singleton

**Key Settings:**
```python
class Settings(BaseSettings):
    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_key: str
    
    # App
    python_env: str = "development"
    port: int = 8000
    
    # CORS
    cors_origins: list[str] = ["http://localhost:5173"]
    
    class Config:
        env_file = ".env"
```


#### 3. API Routes (src/api/routes/)

**Structure:**
```
src/api/routes/
├── __init__.py          # Export all routers
├── auth.py              # Authentication endpoints
├── clients.py           # Client CRUD endpoints
├── leads.py             # Lead CRUD endpoints
└── projects.py          # Project CRUD endpoints
```

**Common Pattern:**
```python
router = APIRouter(prefix="/api/clients", tags=["clients"])

@router.get("/", response_model=list[ClientResponse])
async def list_clients(
    current_user: User = Depends(get_current_user)
):
    # Implementation
    pass

@router.post("/", response_model=ClientResponse, status_code=201)
async def create_client(
    data: ClientCreate,
    current_user: User = Depends(get_current_user)
):
    # Implementation
    pass
```

#### 4. Services (src/services/)

**Responsibilities:**
- Business logic
- Database operations
- Data validation

**Structure:**
```
src/services/
├── __init__.py
├── auth_service.py      # Authentication logic
├── client_service.py    # Client business logic
├── lead_service.py      # Lead business logic
└── project_service.py   # Project business logic
```


#### 5. Models (src/models/)

**Pydantic Models for Validation:**
```
src/models/
├── __init__.py
├── user.py              # User models
├── client.py            # Client models
├── lead.py              # Lead models
└── project.py           # Project models
```

**Example Pattern:**
```python
class ClientBase(BaseModel):
    company_name: str
    cnpj: str
    plan: str
    status: str

class ClientCreate(ClientBase):
    profile_id: UUID

class ClientResponse(ClientBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

### Frontend Components

#### 1. API Client (src/services/api.ts)

**Responsibilities:**
- HTTP client configuration
- Request/response interceptors
- Token management
- Error handling

**Implementation:**
```typescript
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - add JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

#### 2. Auth Context (src/contexts/AuthContext.tsx)

**Responsibilities:**
- Manage authentication state
- Login/logout functions
- Token persistence
- User data management

**Key Functions:**
```typescript
interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  isLoading: boolean;
}
```

#### 3. Service Layer (src/services/)

**Structure:**
```
src/services/
├── api.ts               # Base API client
├── authService.ts       # Authentication API calls
├── clientService.ts     # Client API calls
├── leadService.ts       # Lead API calls
└── projectService.ts    # Project API calls
```

**Example Pattern:**
```typescript
export const clientService = {
  getAll: () => api.get<Client[]>('/api/clients'),
  getById: (id: string) => api.get<Client>(`/api/clients/${id}`),
  create: (data: ClientCreate) => api.post<Client>('/api/clients', data),
  update: (id: string, data: ClientUpdate) => api.put<Client>(`/api/clients/${id}`, data),
  delete: (id: string) => api.delete(`/api/clients/${id}`),
};
```

## Data Flow

### Authentication Flow

```
┌─────────┐                ┌──────────┐                ┌──────────┐
│ User    │                │ Frontend │                │ Backend  │
└────┬────┘                └────┬─────┘                └────┬─────┘
     │                          │                           │
     │ 1. Enter credentials     │                           │
     ├─────────────────────────►│                           │
     │                          │                           │
     │                          │ 2. POST /api/auth/login   │
     │                          ├──────────────────────────►│
     │                          │                           │
     │                          │                           │ 3. Validate
     │                          │                           │    credentials
     │                          │                           │
     │                          │ 4. Return JWT token       │
     │                          │◄──────────────────────────┤
     │                          │                           │
     │                          │ 5. Store token            │
     │                          │    in localStorage        │
     │                          │                           │
     │ 6. Redirect to dashboard │                           │
     │◄─────────────────────────┤                           │
     │                          │                           │
```

### CRUD Operation Flow

```
┌─────────┐                ┌──────────┐                ┌──────────┐                ┌──────────┐
│ User    │                │ Frontend │                │ Backend  │                │ Supabase │
└────┬────┘                └────┬─────┘                └────┬─────┘                └────┬─────┘
     │                          │                           │                           │
     │ 1. Click "Create"        │                           │                           │
     ├─────────────────────────►│                           │                           │
     │                          │                           │                           │
     │                          │ 2. Show loading           │                           │
     │◄─────────────────────────┤                           │                           │
     │                          │                           │                           │
     │                          │ 3. POST /api/clients      │                           │
     │                          │    + JWT token            │                           │
     │                          ├──────────────────────────►│                           │
     │                          │                           │                           │
     │                          │                           │ 4. Validate token         │
     │                          │                           │                           │
     │                          │                           │ 5. Validate data          │
     │                          │                           │                           │
     │                          │                           │ 6. INSERT INTO clients    │
     │                          │                           ├──────────────────────────►│
     │                          │                           │                           │
     │                          │                           │                           │ 7. Check RLS
     │                          │                           │                           │
     │                          │                           │ 8. Return created record  │
     │                          │                           │◄──────────────────────────┤
     │                          │                           │                           │
     │                          │ 9. Return 201 + data      │                           │
     │                          │◄──────────────────────────┤                           │
     │                          │                           │                           │
     │                          │ 10. Update UI             │                           │
     │                          │     Hide loading          │                           │
     │◄─────────────────────────┤                           │                           │
     │                          │                           │                           │
```

## Database Design

### Tables Used in This Sprint

#### profiles
```sql
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'client')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### clients
```sql
CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    profile_id UUID REFERENCES profiles(id),
    company_name TEXT NOT NULL,
    cnpj TEXT UNIQUE NOT NULL,
    plan TEXT NOT NULL CHECK (plan IN ('basic', 'pro', 'enterprise')),
    status TEXT NOT NULL CHECK (status IN ('active', 'inactive', 'suspended')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### leads
```sql
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID REFERENCES clients(id),
    phone TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT,
    metadata JSONB DEFAULT '{}',
    status TEXT NOT NULL CHECK (status IN ('active', 'inactive', 'blocked')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### projects
```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID REFERENCES clients(id),
    name TEXT NOT NULL,
    description TEXT,
    type TEXT NOT NULL CHECK (type IN ('survey', 'campaign', 'support')),
    status TEXT NOT NULL CHECK (status IN ('draft', 'active', 'paused', 'completed')),
    config JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### RLS Policies

**Admin Access (All Tables):**
```sql
CREATE POLICY "Admins have full access"
    ON <table_name>
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );
```

**Client Access (clients table):**
```sql
CREATE POLICY "Clients can view own data"
    ON clients
    FOR SELECT
    TO authenticated
    USING (profile_id = auth.uid());
```

**Client Access (leads table):**
```sql
CREATE POLICY "Clients can view own leads"
    ON leads
    FOR SELECT
    TO authenticated
    USING (
        client_id IN (
            SELECT id FROM clients
            WHERE profile_id = auth.uid()
        )
    );
```

## Infrastructure Design

### Docker Configuration

#### Dockerfile (backend/Dockerfile)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
      - SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}
    depends_on:
      - redis
    volumes:
      - ./backend/logs:/app/logs

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./frontend/dist:/usr/share/nginx/html:ro
    depends_on:
      - backend

volumes:
  redis_data:
```

#### nginx.conf
```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    server {
        listen 80;
        server_name localhost;

        # Frontend
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;
        }

        # Backend API
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Backend Docs
        location /docs {
            proxy_pass http://backend;
        }
    }
}
```

## Security Design

### Authentication Flow
1. User submits credentials
2. Backend validates against Supabase Auth
3. Backend generates JWT token
4. Frontend stores token in localStorage
5. Frontend includes token in all API requests
6. Backend validates token on each request

### Authorization
- RLS policies enforce data access at database level
- Backend validates user role before operations
- Frontend hides UI elements based on user role

### CORS Configuration
- Allow origin: http://localhost:5173 (development)
- Allow credentials: true
- Allow methods: GET, POST, PUT, DELETE, OPTIONS
- Allow headers: Authorization, Content-Type

## Error Handling Design

### Backend Error Responses
```python
{
    "detail": "Error message",
    "status_code": 400,
    "error_type": "ValidationError"
}
```

### Frontend Error Handling
```typescript
try {
    await clientService.create(data);
    toast.success('Client created successfully');
} catch (error) {
    if (axios.isAxiosError(error)) {
        const message = error.response?.data?.detail || 'An error occurred';
        toast.error(message);
    }
}
```

## Correctness Properties

### CP-001: Authentication Token Validity
**Property:** All authenticated requests must include valid JWT token  
**Verification:** Token is validated on backend before processing request  
**Test:** Send request without token → expect 401

### CP-002: CRUD Data Persistence
**Property:** All CRUD operations must persist data to Supabase  
**Verification:** Query database after operation to confirm data  
**Test:** Create client → query Supabase → verify client exists

### CP-003: RLS Enforcement
**Property:** Users can only access data allowed by RLS policies  
**Verification:** Attempt to access unauthorized data → expect 403  
**Test:** Client user tries to access another client's data → expect error

### CP-004: CORS Configuration
**Property:** Frontend can make requests to backend without CORS errors  
**Verification:** Browser allows requests from localhost:5173  
**Test:** Make API call from frontend → no CORS error in console

### CP-005: Error Handling
**Property:** All errors are caught and displayed to user  
**Verification:** Error message appears in UI when operation fails  
**Test:** Submit invalid data → expect error message displayed

### CP-006: Loading States
**Property:** Loading indicator shown during async operations  
**Verification:** UI shows loading state while request is pending  
**Test:** Click create button → loading indicator appears → disappears when done

### CP-007: Token Persistence
**Property:** Token persists across page refreshes  
**Verification:** Token remains in localStorage after refresh  
**Test:** Login → refresh page → still authenticated

### CP-008: Logout Cleanup
**Property:** Logout removes token and redirects to login  
**Verification:** Token removed from localStorage, user redirected  
**Test:** Logout → token gone → redirected to login page

## Performance Considerations

### Backend Optimization
- Use connection pooling for Supabase client
- Implement query result caching where appropriate
- Add database indexes on frequently queried columns
- Use async/await for non-blocking operations

### Frontend Optimization
- Implement debouncing for search inputs
- Use React.memo for expensive components
- Lazy load routes with React.lazy
- Cache API responses where appropriate

### Database Optimization
- Indexes on foreign keys (client_id, profile_id)
- Indexes on frequently filtered columns (status, created_at)
- Optimize RLS policies to avoid full table scans

## Monitoring and Logging

### Backend Logging
```python
import logging

logger = logging.getLogger(__name__)

@router.post("/")
async def create_client(data: ClientCreate):
    logger.info(f"Creating client: {data.company_name}")
    try:
        result = service.create(data)
        logger.info(f"Client created: {result.id}")
        return result
    except Exception as e:
        logger.error(f"Error creating client: {str(e)}")
        raise
```

### Frontend Logging
```typescript
console.log('[API] Creating client:', data);
try {
    const result = await clientService.create(data);
    console.log('[API] Client created:', result);
    return result;
} catch (error) {
    console.error('[API] Error creating client:', error);
    throw error;
}
```

## Testing Strategy

### Backend Tests
- Unit tests for services
- Integration tests for API endpoints
- Test RLS policies
- Test authentication flow

### Frontend Tests
- Unit tests for components
- Integration tests for API calls
- E2E tests for critical flows
- Test error handling

### Manual Testing Checklist
- [ ] Login with valid credentials
- [ ] Login with invalid credentials
- [ ] Create client
- [ ] Edit client
- [ ] Delete client
- [ ] Repeat for leads and projects
- [ ] Logout
- [ ] Verify data in Supabase

## Deployment Strategy (Future)

### Development (Current Sprint)
- Backend runs locally with uvicorn
- Frontend runs locally with vite
- Direct connection to Supabase

### Production (Future Sprint)
- Backend in Docker container
- Frontend served by Nginx
- Redis for caching and Celery
- Nginx as reverse proxy
- SSL/TLS certificates
- Environment-specific configurations

## Migration Path

### From Mock to Real API
1. Keep mock data as fallback
2. Implement API client
3. Update one component at a time
4. Test each component thoroughly
5. Remove mock data after validation

### From Local to Docker
1. Test Docker build locally
2. Verify all services start
3. Test connectivity between services
4. Deploy to VPS
5. Configure domain and SSL
6. Monitor and optimize

## Conclusion

This design establishes a solid foundation for integrating frontend and backend, with clear separation of concerns, proper error handling, and security measures. The Docker infrastructure is prepared for future production deployment while maintaining simplicity for local development.
