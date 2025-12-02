# Requirements Document - Backend Foundation & Authentication

## Introduction

This document specifies the requirements for establishing the foundational backend infrastructure for the RENUM platform using Python/FastAPI and implementing real authentication with Supabase Auth. The system will replace the current mock authentication in the frontend with a production-ready authentication system integrated with a PostgreSQL database via Supabase.

## Glossary

- **Backend System**: The FastAPI-based server application that handles API requests and business logic
- **Supabase**: Backend-as-a-Service platform providing PostgreSQL database and authentication services
- **JWT Token**: JSON Web Token used for stateless authentication
- **RLS**: Row Level Security - PostgreSQL feature for data access control at the database level
- **Profile**: User metadata stored in the public.profiles table
- **Auth User**: User account managed by Supabase Auth in the auth.users table
- **Service Role Key**: Supabase administrative key that bypasses RLS policies
- **Anon Key**: Supabase public key that respects RLS policies
- **CORS**: Cross-Origin Resource Sharing - mechanism for allowing frontend to access backend
- **Health Check**: Endpoint that verifies system operational status

## Requirements

### Requirement 1

**User Story:** As a system administrator, I want a properly structured Python backend project, so that the codebase is maintainable and follows best practices.

#### Acceptance Criteria

1. WHEN the project is initialized THEN the Backend System SHALL create a virtual environment for isolated dependency management
2. WHEN the project structure is created THEN the Backend System SHALL organize code into logical modules (api, services, models, config, utils)
3. WHEN Python packages are defined THEN the Backend System SHALL mark all module directories with __init__.py files
4. WHEN dependencies are specified THEN the Backend System SHALL list all required packages in requirements.txt with pinned versions
5. WHEN the environment is configured THEN the Backend System SHALL load configuration from environment variables using Pydantic Settings

### Requirement 2

**User Story:** As a developer, I want secure configuration management, so that sensitive credentials are protected and never committed to version control.

#### Acceptance Criteria

1. WHEN environment variables are defined THEN the Backend System SHALL provide a .env.example template with placeholder values
2. WHEN credentials are stored locally THEN the Backend System SHALL use a .env file that is excluded from version control
3. WHEN the .gitignore is configured THEN the Backend System SHALL prevent committing .env files, credentials, and sensitive data
4. WHEN configuration is loaded THEN the Backend System SHALL validate that all required environment variables exist
5. WHEN required variables are missing THEN the Backend System SHALL raise a clear error indicating which variables are missing

### Requirement 3

**User Story:** As a developer, I want to connect to Supabase, so that the backend can interact with the PostgreSQL database and authentication services.

#### Acceptance Criteria

1. WHEN Supabase clients are initialized THEN the Backend System SHALL create two client instances (admin and public)
2. WHEN administrative operations are needed THEN the Backend System SHALL use the Service Role Key client to bypass RLS
3. WHEN user operations are performed THEN the Backend System SHALL use the Anon Key client to respect RLS policies
4. WHEN database queries are executed THEN the Backend System SHALL use the Supabase Python client library
5. WHEN connection fails THEN the Backend System SHALL log the error with sufficient detail for debugging

### Requirement 4

**User Story:** As a user, I want to register a new account, so that I can access the system with my credentials.

#### Acceptance Criteria

1. WHEN a user submits registration data THEN the Backend System SHALL validate the email format
2. WHEN registration data is valid THEN the Backend System SHALL create an Auth User in Supabase Auth
3. WHEN an Auth User is created THEN the Backend System SHALL automatically create a corresponding Profile via database trigger
4. WHEN registration succeeds THEN the Backend System SHALL return a JWT Token and user profile data
5. WHEN the email already exists THEN the Backend System SHALL return a validation error with status 400

### Requirement 5

**User Story:** As a user, I want to login with my email and password, so that I can access my account.

#### Acceptance Criteria

1. WHEN a user submits login credentials THEN the Backend System SHALL validate the email format
2. WHEN credentials are submitted THEN the Backend System SHALL authenticate via Supabase Auth
3. WHEN authentication succeeds THEN the Backend System SHALL retrieve the user's Profile from the database
4. WHEN authentication succeeds THEN the Backend System SHALL return a JWT Token with expiration time
5. WHEN credentials are invalid THEN the Backend System SHALL return an authentication error with status 401

### Requirement 6

**User Story:** As an authenticated user, I want my session to be validated on each request, so that only authorized users can access protected resources.

#### Acceptance Criteria

1. WHEN a protected endpoint is accessed THEN the Backend System SHALL extract the JWT Token from the Authorization header
2. WHEN a token is provided THEN the Backend System SHALL validate the token with Supabase Auth
3. WHEN the token is valid THEN the Backend System SHALL retrieve the current user's profile
4. WHEN the token is invalid or expired THEN the Backend System SHALL return a 401 Unauthorized error
5. WHEN no token is provided THEN the Backend System SHALL return a 401 Unauthorized error

### Requirement 7

**User Story:** As a user, I want to logout, so that my session is terminated and my token is invalidated.

#### Acceptance Criteria

1. WHEN a user requests logout THEN the Backend System SHALL invalidate the session in Supabase Auth
2. WHEN logout succeeds THEN the Backend System SHALL return a success message
3. WHEN logout is called with an invalid token THEN the Backend System SHALL still return success
4. WHEN logout completes THEN the Backend System SHALL log the logout event
5. WHEN the frontend receives logout confirmation THEN the Frontend SHALL clear the stored JWT Token

### Requirement 8

**User Story:** As a system administrator, I want role-based access control, so that admin users have elevated privileges.

#### Acceptance Criteria

1. WHEN a user profile is created THEN the Backend System SHALL assign a default role of "guest"
2. WHEN admin endpoints are accessed THEN the Backend System SHALL verify the user's role is "admin"
3. WHEN a non-admin accesses admin endpoints THEN the Backend System SHALL return a 403 Forbidden error
4. WHEN role verification is needed THEN the Backend System SHALL provide a require_admin middleware
5. WHEN an admin user is created THEN the Profile SHALL be manually updated to set role as "admin"

### Requirement 9

**User Story:** As a system operator, I want health check endpoints, so that I can monitor the system's operational status.

#### Acceptance Criteria

1. WHEN the health endpoint is accessed THEN the Backend System SHALL return status "healthy" with timestamp
2. WHEN the database health endpoint is accessed THEN the Backend System SHALL execute a test query to verify connectivity
3. WHEN the database is accessible THEN the Backend System SHALL return status "healthy" with "connected" indicator
4. WHEN the database is not accessible THEN the Backend System SHALL return status "unhealthy" with error details
5. WHEN health checks are performed THEN the Backend System SHALL not require authentication

### Requirement 10

**User Story:** As a developer, I want comprehensive logging, so that I can debug issues and audit system activity.

#### Acceptance Criteria

1. WHEN the logging system is initialized THEN the Backend System SHALL configure console and file output
2. WHEN log messages are written THEN the Backend System SHALL include timestamp, level, and context
3. WHEN log files grow large THEN the Backend System SHALL rotate files at 500 MB
4. WHEN log files are old THEN the Backend System SHALL retain logs for 10 days
5. WHEN critical operations occur THEN the Backend System SHALL log authentication events, errors, and important state changes

### Requirement 11

**User Story:** As a frontend developer, I want CORS properly configured, so that the React application can communicate with the backend API.

#### Acceptance Criteria

1. WHEN CORS is configured THEN the Backend System SHALL allow requests from specified origins
2. WHEN the frontend makes requests THEN the Backend System SHALL include appropriate CORS headers
3. WHEN credentials are sent THEN the Backend System SHALL allow credentials in cross-origin requests
4. WHEN any HTTP method is used THEN the Backend System SHALL allow all standard methods
5. WHEN custom headers are sent THEN the Backend System SHALL allow all headers

### Requirement 12

**User Story:** As a developer, I want automatic API documentation, so that I can understand and test endpoints without reading code.

#### Acceptance Criteria

1. WHEN the backend starts THEN the Backend System SHALL generate OpenAPI specification
2. WHEN the /docs endpoint is accessed THEN the Backend System SHALL serve Swagger UI interface
3. WHEN the /redoc endpoint is accessed THEN the Backend System SHALL serve ReDoc interface
4. WHEN endpoints are defined THEN the Backend System SHALL include request/response schemas in documentation
5. WHEN authentication is required THEN the Backend System SHALL indicate protected endpoints in documentation

### Requirement 13

**User Story:** As a frontend developer, I want to integrate Supabase Auth in the React application, so that users can authenticate from the browser.

#### Acceptance Criteria

1. WHEN the Supabase client is initialized THEN the Frontend SHALL use environment variables for configuration
2. WHEN a user logs in THEN the Frontend SHALL call Supabase Auth signInWithPassword
3. WHEN authentication succeeds THEN the Frontend SHALL store the JWT Token in localStorage
4. WHEN the user profile is needed THEN the Frontend SHALL query the profiles table
5. WHEN the session changes THEN the Frontend SHALL listen to auth state changes and update the UI

### Requirement 14

**User Story:** As a developer, I want data validation, so that invalid data is rejected before reaching the database.

#### Acceptance Criteria

1. WHEN request data is received THEN the Backend System SHALL validate using Pydantic models
2. WHEN email is provided THEN the Backend System SHALL validate email format
3. WHEN required fields are missing THEN the Backend System SHALL return a 400 error with field details
4. WHEN data types are incorrect THEN the Backend System SHALL return a 400 error with type information
5. WHEN validation passes THEN the Backend System SHALL proceed with the request

### Requirement 15

**User Story:** As a system administrator, I want the first admin user created, so that I can access the system with administrative privileges.

#### Acceptance Criteria

1. WHEN the admin user is created THEN the Backend System SHALL create an Auth User with email admin@renum.tech
2. WHEN the Auth User is created THEN the Backend System SHALL automatically create a Profile via trigger
3. WHEN the Profile is created THEN the Profile SHALL be manually updated to set role as "admin"
4. WHEN the admin user logs in THEN the Backend System SHALL return a token with admin role
5. WHEN the admin accesses protected endpoints THEN the Backend System SHALL grant access based on admin role

### Requirement 16

**User Story:** As a DevOps engineer, I want Docker configuration prepared, so that the system can be deployed to production when ready.

#### Acceptance Criteria

1. WHEN Docker is configured THEN the Backend System SHALL provide a Dockerfile with Python 3.11 base image
2. WHEN Docker Compose is configured THEN the Backend System SHALL define services for API and Redis
3. WHEN the Docker image is built THEN the Backend System SHALL include all dependencies from requirements.txt
4. WHEN environment variables are needed THEN the Backend System SHALL pass them from .env to containers
5. WHEN Docker is configured THEN the Backend System SHALL NOT be used for local development yet
