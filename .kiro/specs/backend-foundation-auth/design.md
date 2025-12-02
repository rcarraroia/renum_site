# Design Document - Backend Foundation & Authentication

## Overview

The backend foundation establishes a production-ready FastAPI application with Supabase integration for authentication and data persistence. The system follows a layered architecture with clear separation of concerns: API routes handle HTTP requests, services contain business logic, models define data structures, and configuration manages environment-specific settings.

The authentication flow leverages Supabase Auth for user management while maintaining custom user profiles in PostgreSQL. JWT tokens are issued by Supabase and validated on each request through middleware, enabling stateless authentication across distributed systems.

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                         │
│  - Supabase Auth Client                                      │
│  - JWT Token Storage (localStorage)                          │
│  - AuthContext Provider                                      │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS + JWT Bearer Token
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  BACKEND (FastAPI)                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ API Layer (routes/)                                  │   │
│  │  - /health, /health/db                               │   │
│  │  - /auth/login, /auth/register, /auth/logout        │   │
│  │  - /auth/me, /auth/verify                            │   │
│  └────────────┬─────────────────────────────────────────┘   │
│               │                                              │
│  ┌────────────▼─────────────────────────────────────────┐   │
│  │ Middleware Layer                                     │   │
│  │  - CORS Middleware                                   │   │
│  │  - Auth Middleware (JWT validation)                 │   │
│  └────────────┬─────────────────────────────────────────┘   │
│               │                                              │
│  ┌────────────▼─────────────────────────────────────────┐   │
│  │ Service Layer (services/)                            │   │
│  │  - AuthService (login, register, logout)            │   │
│  └────────────┬─────────────────────────────────────────┘   │
│               │                                              │
│  ┌────────────▼─────────────────────────────────────────┐   │
│  │ Configuration Layer (config/)                        │   │
│  │  - Settings (Pydantic)                               │   │
│  │  - Supabase Clients (admin, public)                 │   │
│  └────────────┬─────────────────────────────────────────┘   │
└───────────────┼──────────────────────────────────────────────┘
                │
┌───────────────▼──────────────────────────────────────────────┐
│               SUPABASE (Postgres + Auth)                     │
│  - auth.users (managed by Supabase Auth)                    │
│  - public.profiles (custom user data)                       │
│  - RLS Policies (row-level security)                        │
│  - Triggers (auto-create profiles)                          │
└─────────────────────────────────────────────────────────────┘
```

### Authentication Flow

**Registration:**
1. User submits email/password to POST /auth/register
2. Backend validates input with Pydantic
3. Backend calls Supabase Auth sign_up
4. Supabase creates auth.users record
5. Database trigger creates public.profiles record
6. Backend retrieves profile data
7. Backend returns JWT token + user profile

**Login:**
1. User submits email/password to POST /auth/login
2. Backend validates input with Pydantic
3. Backend calls Supabase Auth sign_in_with_password
4. Supabase validates credentials and returns session
5. Backend retrieves profile from public.profiles
6. Backend returns JWT token + user profile
7. Frontend stores token in localStorage

**Protected Request:**
1. Frontend sends request with Authorization: Bearer <token>
2. Backend middleware extracts token
3. Backend calls Supabase Auth get_user(token)
4. Supabase validates token and returns user
5. Backend retrieves profile from public.profiles
6. Backend attaches user to request context
7. Route handler processes request with user context

## Components and Interfaces

### API Routes

**Health Routes** (`src/api/routes/health.py`)
- `GET /health` - Basic health check (public)
- `GET /health/db` - Database connectivity check (public)

**Auth Routes** (`src/api/routes/auth.py`)
- `POST /auth/login` - Authenticate user (public)
- `POST /auth/register` - Create new user (public)
- `POST /auth/logout` - Invalidate session (protected)
- `GET /auth/me` - Get current user profile (protected)
- `GET /auth/verify` - Verify token validity (protected)

### Services

**AuthService** (`src/services/auth_service.py`)

```python
class AuthService:
    async def login(credentials: UserLogin) -> Dict[str, Any]
    async def register(user_data: UserRegister) -> Dict[str, Any]
    async def logout(token: str) -> bool
    async def get_current_user(token: str) -> Optional[UserProfile]
```

### Middleware

**Auth Middleware** (`src/api/middleware/auth_middleware.py`)

```python
async def get_current_user(credentials: HTTPAuthorizationCredentials) -> UserProfile
async def require_admin(current_user: UserProfile) -> UserProfile
```

### Configuration

**Settings** (`src/config/settings.py`)

```python
class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str
    
    # FastAPI
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: str
    
    # Logging
    LOG_LEVEL: str = "INFO"
```

**Supabase Clients** (`src/config/supabase.py`)

```python
supabase_admin: Client  # Service Role - bypasses RLS
supabase_client: Client  # Anon Key - respects RLS
```

## Data Models

### Pydantic Models (`src/models/user.py`)

**UserBase**
```python
class UserBase(BaseModel):
    email: EmailStr
```

**UserLogin**
```python
class UserLogin(UserBase):
    password: str
```

**UserRegister**
```python
class UserRegister(UserBase):
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
```

**UserProfile**
```python
class UserProfile(BaseModel):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = "guest"
    avatar_url: Optional[str] = None
    updated_at: Optional[datetime] = None
```

**TokenResponse**
```python
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserProfile
```

### Database Schema

**profiles table** (already exists in Supabase)
```sql
CREATE TABLE profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id),
    email TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    role TEXT DEFAULT 'guest',
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Environment Configuration Validation

*For any* application startup, all required environment variables must be present and valid, otherwise the application shall fail to start with a clear error message.

**Validates: Requirements 2.4, 2.5**

### Property 2: Authentication Token Validity

*For any* valid JWT token issued by the system, when validated through the auth middleware, the system shall successfully retrieve the corresponding user profile.

**Validates: Requirements 6.2, 6.3**

### Property 3: Invalid Token Rejection

*For any* invalid, expired, or missing JWT token, when a protected endpoint is accessed, the system shall return a 401 Unauthorized error.

**Validates: Requirements 6.4, 6.5**

### Property 4: Registration Email Uniqueness

*For any* registration attempt with an email that already exists in auth.users, the system shall reject the registration and return a 400 validation error.

**Validates: Requirements 4.5**

### Property 5: Profile Auto-Creation

*For any* successful user registration in Supabase Auth, a corresponding profile record shall be automatically created in the public.profiles table via database trigger.

**Validates: Requirements 4.3**

### Property 6: Login Credential Validation

*For any* login attempt with invalid credentials (wrong email or password), the system shall return a 401 authentication error without revealing which credential was incorrect.

**Validates: Requirements 5.5**

### Property 7: Role-Based Access Control

*For any* endpoint protected by require_admin middleware, when accessed by a user with role other than "admin", the system shall return a 403 Forbidden error.

**Validates: Requirements 8.3**

### Property 8: Health Check Availability

*For any* health check endpoint access, the system shall respond without requiring authentication and return the current operational status.

**Validates: Requirements 9.5**

### Property 9: Database Connectivity Verification

*For any* database health check, when the database is accessible, the system shall successfully execute a test query and return "connected" status.

**Validates: Requirements 9.3**

### Property 10: CORS Origin Validation

*For any* request from an origin listed in CORS_ORIGINS, the system shall include appropriate CORS headers allowing the request to proceed.

**Validates: Requirements 11.1, 11.2**

### Property 11: Pydantic Validation Enforcement

*For any* API request with invalid data (wrong types, missing required fields, invalid email format), the system shall return a 400 error with detailed validation messages before processing the request.

**Validates: Requirements 14.2, 14.3, 14.4**

### Property 12: Logout Session Invalidation

*For any* logout request with a valid token, the system shall invalidate the session in Supabase Auth and return success.

**Validates: Requirements 7.1, 7.2**

## Error Handling

### Exception Hierarchy

```python
# Custom Exceptions (src/utils/exceptions.py)
class AuthenticationError(Exception)  # 401 errors
class ValidationError(Exception)      # 400 errors
class NotFoundError(Exception)        # 404 errors
class PermissionError(Exception)      # 403 errors
```

### Error Response Format

All errors return consistent JSON structure:

```json
{
    "detail": "Human-readable error message"
}
```

### HTTP Status Codes

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `204 No Content` - Successful deletion
- `400 Bad Request` - Validation error
- `401 Unauthorized` - Authentication required or failed
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Unexpected server error

### Logging Strategy

All errors are logged with context:
- Authentication failures: email attempted, timestamp
- Validation errors: fields that failed, values provided
- Database errors: query attempted, error message
- System errors: stack trace, request context

## Testing Strategy

### Unit Testing

**Framework:** pytest with pytest-asyncio

**Coverage Target:** 70% minimum

**Test Categories:**

1. **Model Validation Tests**
   - Valid data passes validation
   - Invalid email formats rejected
   - Missing required fields rejected
   - Type mismatches rejected

2. **Service Logic Tests**
   - AuthService.login with valid credentials
   - AuthService.login with invalid credentials
   - AuthService.register with new email
   - AuthService.register with existing email
   - AuthService.get_current_user with valid token
   - AuthService.get_current_user with invalid token

3. **Middleware Tests**
   - get_current_user with valid token
   - get_current_user with missing token
   - get_current_user with expired token
   - require_admin with admin user
   - require_admin with non-admin user

### Integration Testing

**Test Categories:**

1. **API Endpoint Tests**
   - POST /auth/register creates user and returns token
   - POST /auth/login authenticates and returns token
   - GET /auth/me returns profile with valid token
   - GET /auth/me returns 401 with invalid token
   - POST /auth/logout invalidates session

2. **Database Integration Tests**
   - Profile auto-created on user registration
   - Profile retrieved correctly after login
   - RLS policies enforced correctly

3. **Health Check Tests**
   - GET /health returns healthy status
   - GET /health/db returns connected when database accessible
   - GET /health/db returns error when database unavailable

### Property-Based Testing

**Framework:** Hypothesis (Python property-based testing library)

**Configuration:** Minimum 100 iterations per property test

**Test Format:**
```python
# Each test tagged with property reference
# Example: Property 11: Pydantic Validation Enforcement

@given(st.emails(), st.text())
def test_property_11_invalid_email_rejected(email, password):
    """
    Feature: backend-foundation-auth, Property 11: Pydantic Validation Enforcement
    Validates: Requirements 14.2
    """
    # Test implementation
```

**Properties to Test:**

1. **Property 2:** Generate random valid tokens, verify all retrieve profiles
2. **Property 3:** Generate random invalid tokens, verify all return 401
3. **Property 4:** Attempt registration with same email twice, verify second fails
4. **Property 11:** Generate random invalid data, verify all return 400 with details

### Manual Testing Checklist

1. Start backend server and verify startup logs
2. Access /docs and verify Swagger UI loads
3. Test /health endpoint returns healthy
4. Test /health/db endpoint returns connected
5. Register new user via Swagger UI
6. Login with registered user
7. Copy token and test /auth/me endpoint
8. Test /auth/verify with valid token
9. Test protected endpoint without token (should fail)
10. Logout and verify token invalidated

## Deployment Considerations

### Local Development (Current Sprint)

- Run backend with `python src/main.py`
- Hot reload enabled with `RELOAD=True`
- Debug mode enabled with `DEBUG=True`
- Logs output to console and file
- **NO Docker** - Direct Python execution

### Production (Future - Docker Configured But Not Used)

⚠️ **IMPORTANT:** Docker configuration files (Dockerfile, docker-compose.yml) will be created in this sprint but **NOT USED** for local development. They are prepared for future production deployment only.

- Docker containers with docker-compose
- Environment variables from secrets management
- Debug mode disabled
- Structured logging to centralized system
- Health checks for load balancer
- Horizontal scaling with multiple instances

**Decision Rationale:**
- Configure Docker now to have it ready
- Use direct Python execution for faster development iteration
- Deploy with Docker later when moving to production VPS

### Environment Variables

**Required:**
- SUPABASE_URL
- SUPABASE_ANON_KEY
- SUPABASE_SERVICE_KEY
- SECRET_KEY
- CORS_ORIGINS

**Optional (with defaults):**
- API_HOST (default: 0.0.0.0)
- API_PORT (default: 8000)
- DEBUG (default: True)
- LOG_LEVEL (default: INFO)

## Security Considerations

### Credential Protection

- All credentials in .env file (never committed)
- .gitignore prevents accidental commits
- Service role key only used server-side
- Anon key safe to expose to frontend

### Token Security

- JWT tokens signed by Supabase
- Tokens include expiration time
- Tokens validated on every protected request
- Logout invalidates tokens server-side

### RLS Policies

- Profiles table has RLS enabled
- Users can only access their own profile
- Admin users can access all profiles
- Service role bypasses RLS for admin operations

### CORS Configuration

- Only specified origins allowed
- Credentials allowed for authenticated requests
- Preflight requests handled correctly

### Input Validation

- All inputs validated with Pydantic
- Email format validated
- SQL injection prevented by Supabase client
- XSS prevented by JSON responses

## Performance Considerations

### Database Queries

- Single query to fetch profile after authentication
- Indexes on profiles.id (primary key)
- Connection pooling handled by Supabase client

### Caching Strategy

- No caching in initial implementation
- Future: Redis cache for user profiles
- Future: Token validation caching

### Response Times

- Health check: < 50ms
- Database health: < 200ms
- Login: < 500ms (includes Supabase Auth call)
- Protected endpoints: < 100ms (token validation)

## Monitoring and Observability

### Logging

- All authentication events logged
- Failed login attempts logged with email
- Errors logged with full context
- Log rotation at 500 MB
- Log retention for 10 days

### Metrics (Future)

- Request count by endpoint
- Response time percentiles
- Error rate by type
- Active user sessions

### Health Checks

- Basic health: API responsiveness
- Database health: Connection and query execution
- Future: Redis health, external service health

## Documentation

### API Documentation

- Automatic OpenAPI spec generation
- Swagger UI at /docs
- ReDoc at /redoc
- Request/response schemas included
- Authentication requirements indicated

### Code Documentation

- Docstrings on all public functions
- Type hints on all function signatures
- Comments explaining complex logic
- README with setup instructions

## Dependencies

### Python Packages

- **fastapi** (0.109.0) - Web framework
- **uvicorn** (0.27.0) - ASGI server
- **supabase** (2.3.4) - Supabase client
- **pydantic** (2.5.3) - Data validation
- **pydantic-settings** (2.1.0) - Settings management
- **pyjwt** (2.8.0) - JWT handling
- **python-jose** (3.3.0) - JWT cryptography
- **loguru** (0.7.2) - Logging
- **httpx** (0.26.0) - HTTP client
- **pytest** (7.4.4) - Testing framework
- **pytest-asyncio** (0.23.3) - Async testing
- **hypothesis** (6.92.0) - Property-based testing

### External Services

- **Supabase** - Database and authentication
- **PostgreSQL** (via Supabase) - Data persistence

## Future Enhancements

1. **Rate Limiting** - Prevent brute force attacks
2. **Refresh Tokens** - Long-lived sessions
3. **Email Verification** - Confirm email ownership
4. **Password Reset** - Self-service password recovery
5. **OAuth Integration** - Social login (Google, GitHub)
6. **2FA Support** - Two-factor authentication
7. **Session Management** - View and revoke active sessions
8. **Audit Logging** - Detailed activity tracking
