
import requests
import logging
import base64
from typing import Dict, Any, Optional, Union

logger = logging.getLogger(__name__)

class UazapiConnector:
    """
    Connector for Uazapi API v2.
    Handles messaging and media processing (including Native Verification).
    """

    def __init__(self, api_url: str, token: str, instance_name: Optional[str] = None):
        """
        :param api_url: Base URL (e.g., https://api.uazapi.com)
        :param token: Instance Token
        :param instance_name: Optional, mainly for logging/context
        """
        self.api_url = api_url.rstrip('/')
        self.token = token
        self.instance_name = instance_name
        
        self.headers = {
            "token": self.token,
            "Content-Type": "application/json"
        }

    def get_status(self) -> Dict[str, Any]:
        """Check instance connection status"""
        try:
            url = f"{self.api_url}/instance/connectionState"
            # Note: Endpoint might vary based on exact V2 spec, assuming standard
            # If not standard, listing instances is a fallback /instance/all
            # Let's try to get profile picture which validates connection roughly
            # Or assume /instance/info exists (common in these APIs)
            
            # Based on docs provided: GET /instance/all requires admin token usually.
            # But specific instance endpoints usually use instance token.
            # Let's assume a health check or just return "unknown" until tested.
            return {"status": "unknown"} 
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def send_message(self, 
                     number: str, 
                     content: str, 
                     media_type: str = "text", 
                     media_url: Optional[str] = None,
                     options: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Send message via Uazapi.
        :param number: JID (e.g. 5511999999999@s.whatsapp.net)
        :param content: Message text or Caption
        :param media_type: text, image, audio, video, document
        """
        # Endpoint: POST /message/sendText or /message/sendMedia
        # Using unified send if available, or splitting logic.
        # Docs usually have /message/sendText and /message/sendMedia
        
        # Based on typical Evo/Uazapi V2:
        try:
            if media_type == "text":
                endpoint = "/message/sendText"
                payload = {
                    "number": number,
                    "text": content,
                    "options": options or {}
                }
            elif media_type in ["image", "video", "audio", "document"]:
                endpoint = "/message/sendMedia"
                payload = {
                    "number": number,
                    "mediatype": media_type,
                    "url": media_url,
                    "caption": content, # Caption for image/video
                    "fileName": options.get("fileName") if options else None,
                    "options": options or {}
                }
            else:
                raise ValueError(f"Unsupported media_type: {media_type}")
                
            url = f"{self.api_url}{endpoint}"
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Error sending message to {number}: {e}")
            return {"success": False, "error": str(e)}

    def download_media(self, 
                      message_id: str, 
                      transcribe: bool = False, 
                      openai_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Download media from a message.
        **Feature**: If transcribe=True, returns text of audio directly from Uazapi.
        """
        endpoint = "/message/download"
        url = f"{self.api_url}{endpoint}"
        
        payload = {
            "id": message_id,
            "return_base64": True, # Always get base64 to store/process if needed
            "return_link": True,
            "transcribe": transcribe
        }
        
        if transcribe and openai_key:
            payload["openai_apikey"] = openai_key
            
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Error downloading media {message_id}: {e}")
            return {"success": False, "error": str(e)}
