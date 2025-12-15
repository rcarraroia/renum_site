
import logging
from typing import Dict, Any, List, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

class GoogleConnector:
    """
    Connector for Google Workspace Services (Gmail, Calendar, Drive, Sheets).
    Uses 'credentials' dict containing OAuth2 tokens.
    """
    
    def __init__(self, credentials_config: Dict[str, Any]):
        """
        :param credentials_config: Dict stored in DB (access_token, refresh_token, etc.)
        """
        self.config = credentials_config
        self.creds = self._get_credentials()
        self._services = {}

    def _get_credentials(self) -> Credentials:
        """Hydrate google.oauth2.credentials.Credentials from config dict."""
        return Credentials(
            token=self.config.get('access_token'),
            refresh_token=self.config.get('refresh_token'),
            token_uri=self.config.get('token_uri', "https://oauth2.googleapis.com/token"),
            client_id=self.config.get('client_id'),
            client_secret=self.config.get('client_secret'),
            scopes=self.config.get('scopes')
        )

    def _get_service(self, service_name: str, version: str):
        """Lazy load service clients."""
        key = f"{service_name}_{version}"
        if key not in self._services:
            self._services[key] = build(service_name, version, credentials=self.creds)
        return self._services[key]

    # --- Gmail ---
    def send_email(self, to: str, subject: str, message_text: str) -> Dict[str, Any]:
        """Send an email via Gmail API."""
        try:
            service = self._get_service('gmail', 'v1')
            
            message = MIMEText(message_text)
            message['to'] = to
            message['subject'] = subject
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            res = service.users().messages().send(userId='me', body={'raw': raw}).execute()
            return {"success": True, "id": res.get("id")}
        except Exception as e:
            logger.error(f"Gmail Send Error: {e}")
            return {"success": False, "error": str(e)}

    # --- Calendar ---
    def list_events(self, max_results: int = 10) -> Dict[str, Any]:
        """List upcoming calendar events."""
        try:
            service = self._get_service('calendar', 'v3')
            events_result = service.events().list(calendarId='primary', maxResults=max_results,
                                                singleEvents=True, orderBy='startTime').execute()
            events = events_result.get('items', [])
            return {"success": True, "events": events}
        except Exception as e:
            logger.error(f"Calendar List Error: {e}")
            return {"success": False, "error": str(e)}

    # --- Drive ---
    def list_files(self, page_size: int = 10) -> Dict[str, Any]:
        """List files in Drive."""
        try:
            service = self._get_service('drive', 'v3')
            results = service.files().list(
                pageSize=page_size, fields="nextPageToken, files(id, name, mimeType)").execute()
            items = results.get('files', [])
            return {"success": True, "files": items}
        except Exception as e:
            # Handle Auth Error specifically?
            logger.error(f"Drive List Error: {e}")
            return {"success": False, "error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """Check connection by listing profile."""
        try:
            # We can use Oauth2 v2 to check user info, or just try list messages
            # Let's try Gmail profile
            service = self._get_service('gmail', 'v1')
            profile = service.users().getProfile(userId='me').execute()
            return {"connected": True, "email": profile.get("emailAddress")}
        except Exception as e:
            return {"connected": False, "error": str(e)}
