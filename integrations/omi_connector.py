"""OMI Backend Connector

Handles integration with OMI backend services.
"""

import asyncio
import json
from typing import Dict, Any, Optional, List
from datetime import datetime

import aiohttp
import websockets
import structlog

logger = structlog.get_logger()


class OMIConnector:
    """Connector for OMI backend services."""
    
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.session = None
        
    async def __aenter__(self):
        # Create session with connection pooling
        connector = aiohttp.TCPConnector(
            limit=100,  # Total connection pool size
            limit_per_host=30,  # Per-host connection limit
            ttl_dns_cache=300,  # DNS cache timeout
        )
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        self.session = aiohttp.ClientSession(
            headers=self.headers,
            connector=connector,
            timeout=timeout
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def process_audio(self, audio_data: bytes, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Process audio through OMI's transcription service."""
        # In a real implementation, this would send audio to OMI's backend
        # For now, we'll simulate the response
        logger.info("Processing audio", size=len(audio_data))
        
        # Simulated transcription result
        return {
            "transcript": metadata.get("simulated_transcript", "This is a simulated transcript."),
            "segments": [],
            "audio_url": f"{self.api_url}/audio/{metadata.get('session_id', 'test')}",
            "duration": 10.5,
            "language": "en"
        }
    
    async def get_user_memories(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve user memories from OMI backend."""
        try:
            if not self.session:
                # Create session if not in context manager
                connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
                timeout = aiohttp.ClientTimeout(total=30, connect=10)
                self.session = aiohttp.ClientSession(
                    headers=self.headers,
                    connector=connector,
                    timeout=timeout
                )
            
            async with self.session.get(
                f"{self.api_url}/v3/memories",
                params={"user_id": user_id, "limit": limit}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("memories", [])
                else:
                    logger.error(f"Failed to get memories", status=response.status)
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting memories", error=str(e))
            return []
    
    async def search_memories(
        self,
        user_id: str,
        query: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Search user memories using vector similarity."""
        try:
            if not self.session:
                # Create session if not in context manager
                connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
                timeout = aiohttp.ClientTimeout(total=30, connect=10)
                self.session = aiohttp.ClientSession(
                    headers=self.headers,
                    connector=connector,
                    timeout=timeout
                )
            
            async with self.session.post(
                f"{self.api_url}/v3/memories/search",
                json={
                    "user_id": user_id,
                    "query": query,
                    "limit": limit
                }
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("results", [])
                else:
                    logger.error(f"Failed to search memories", status=response.status)
                    return []
                    
        except Exception as e:
            logger.error(f"Error searching memories", error=str(e))
            return []
    
    async def get_user_context(self, user_id: str) -> Dict[str, Any]:
        """Get user context including preferences and recent activities."""
        try:
            if not self.session:
                # Create session if not in context manager
                connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
                timeout = aiohttp.ClientTimeout(total=30, connect=10)
                self.session = aiohttp.ClientSession(
                    headers=self.headers,
                    connector=connector,
                    timeout=timeout
                )
            
            # Get user profile
            async with self.session.get(
                f"{self.api_url}/v3/users/{user_id}/context"
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get user context", status=response.status)
                    return {}
                    
        except Exception as e:
            logger.error(f"Error getting user context", error=str(e))
            return {}
    
    async def create_memory(
        self,
        user_id: str,
        memory_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create a new memory in OMI backend."""
        try:
            if not self.session:
                # Create session if not in context manager
                connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
                timeout = aiohttp.ClientTimeout(total=30, connect=10)
                self.session = aiohttp.ClientSession(
                    headers=self.headers,
                    connector=connector,
                    timeout=timeout
                )
            
            async with self.session.post(
                f"{self.api_url}/v3/memories",
                json={
                    "user_id": user_id,
                    **memory_data
                }
            ) as response:
                if response.status == 201:
                    return await response.json()
                else:
                    logger.error(f"Failed to create memory", status=response.status)
                    return None
                    
        except Exception as e:
            logger.error(f"Error creating memory", error=str(e))
            return None
    
    async def stream_transcription(
        self,
        websocket_url: str,
        audio_stream,
        on_transcript
    ):
        """Stream audio to OMI's transcription WebSocket."""
        try:
            async with websockets.connect(
                websocket_url,
                extra_headers={"Authorization": f"Bearer {self.api_key}"}
            ) as websocket:
                
                # Start receiving transcripts
                async def receive_transcripts():
                    while True:
                        try:
                            message = await websocket.recv()
                            data = json.loads(message)
                            
                            if data.get("type") == "transcript":
                                await on_transcript(data)
                                
                        except websockets.exceptions.ConnectionClosed:
                            break
                        except Exception as e:
                            logger.error("Error receiving transcript", error=str(e))
                
                # Start sending audio
                async def send_audio():
                    async for audio_chunk in audio_stream:
                        await websocket.send(audio_chunk)
                
                # Run both tasks concurrently
                await asyncio.gather(
                    receive_transcripts(),
                    send_audio()
                )
                
        except Exception as e:
            logger.error("WebSocket error", error=str(e))
    
    async def get_apps(self, enabled_only: bool = True) -> List[Dict[str, Any]]:
        """Get available OMI apps."""
        try:
            if not self.session:
                # Create session if not in context manager
                connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
                timeout = aiohttp.ClientTimeout(total=30, connect=10)
                self.session = aiohttp.ClientSession(
                    headers=self.headers,
                    connector=connector,
                    timeout=timeout
                )
            
            params = {"enabled": enabled_only} if enabled_only else {}
            
            async with self.session.get(
                f"{self.api_url}/v1/apps",
                params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("apps", [])
                else:
                    logger.error(f"Failed to get apps", status=response.status)
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting apps", error=str(e))
            return []
    
    async def trigger_app_webhook(
        self,
        app_id: str,
        webhook_type: str,
        data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Trigger an app webhook."""
        try:
            if not self.session:
                # Create session if not in context manager
                connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
                timeout = aiohttp.ClientTimeout(total=30, connect=10)
                self.session = aiohttp.ClientSession(
                    headers=self.headers,
                    connector=connector,
                    timeout=timeout
                )
            
            async with self.session.post(
                f"{self.api_url}/v1/apps/{app_id}/webhook/{webhook_type}",
                json=data
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(
                        f"Failed to trigger webhook",
                        app_id=app_id,
                        webhook_type=webhook_type,
                        status=response.status
                    )
                    return None
                    
        except Exception as e:
            logger.error(f"Error triggering webhook", error=str(e))
            return None