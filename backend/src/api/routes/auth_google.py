
from fastapi import APIRouter, Request, HTTPException, Depends
from typing import Optional
from google_auth_oauthlib.flow import Flow
import os
from src.services.integration_service import IntegrationService
from src.middleware.auth import get_current_user

router = APIRouter(prefix="/auth/google", tags=["auth"])

# Environment Variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
# This redirect URI must match exactly what is in GCP Console
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/auth/google/callback") 

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/forms.body', 
    'https://www.googleapis.com/auth/meetings.space.created',
    'openid', 'email', 'profile'
]

@router.get("/login")
async def login_google(agent_id: Optional[str] = None):
    """
    Generate Google OAuth Login URL.
    pass agent_id in state if we want to bind to a specific agent.
    """
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Google Credentials not configured in Server")

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    
    # State can carry client identification if needed. 
    # For now ensuring loose coupling.
    authorization_url, state = flow.authorization_url(
        access_type='offline', # Important for Refresh Token
        include_granted_scopes='true'
    )
    
    return {"url": authorization_url}

@router.get("/callback")
async def callback_google(
    code: str, 
    state: Optional[str] = None,
    # In a real production app, we would secure this endpoint better (state validation)
    # and link it to the user session. 
    # For now, we assume this is called with a client's JWT in headers or we store temporary state?
    # OAuth callbacks are tricky with stateless JWTs. 
    # Common pattern: Front-end handles the redirect code, sends code to Backend authenticated endpoint.
):
    """
    Handle Google Callback. 
    EXCHANGE CODE FOR TOKEN.
    NOTE: Browsers hit this directly. So we can't easily expect 'Authorization: Bearer' header here 
    unless we use a popup and message passing, OR we set a cookie.
    
    STRATEGY: Return the credentials to the Frontend (via URL param or HTML)
    And let Frontend POST them to /api/integrations/google to save.
    This avoids complex session cookie logic for this MVP.
    """
    
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Configuration Error")

    try:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=SCOPES,
            state=state
        )
        flow.redirect_uri = REDIRECT_URI
        
        # Fetch token
        flow.fetch_token(code=code)
        
        credentials = flow.credentials
        
        # Serialize
        creds_data = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        # WARNING: Sending token back to frontend via URL is risky in prod. 
        # But for this MVP to close the loop without session DB:
        # Redirect to Frontend Success Page with data encoded?
        # Better: Render a "Success... Closing" HTML that `window.opener.postMessage` the data to the React App.
        
        html_content = f"""
        <html>
            <body>
                <h1>Conexão com Google Realizada!</h1>
                <p>Você pode fechar esta janela.</p>
                <script>
                    // Send data to parent window (React App)
                    if (window.opener) {{
                        window.opener.postMessage({{ type: 'GOOGLE_AUTH_SUCCESS', payload: {creds_data} }}, "*");
                        window.close();
                    }} else {{
                        document.write("Erro: Janela pai não encontrada. Copie o token manual se necessário.");
                    }}
                </script>
            </body>
        </html>
        """
        
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        return {"error": str(e)}
