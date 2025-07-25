"""Memory Bridge - Integrates OMI memories with Mem0 for enhanced AI memory capabilities."""

import os
import json
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from mem0 import MemoryClient
from integrations.omi_connector import OMIConnector
import structlog

logger = structlog.get_logger()


class MemoryBridge:
    """Bridges OMI device memories with Mem0 for persistent, searchable memory storage."""
    
    def __init__(self, omi_connector: OMIConnector, mem0_api_key: Optional[str] = None):
        self.omi = omi_connector
        self.mem0 = MemoryClient(api_key=mem0_api_key) if mem0_api_key else None
        
    async def sync_omi_memory_to_mem0(
        self,
        team_id: str,
        omi_memory: Dict[str, Any]
    ) -> Optional[str]:
        """Sync a single OMI memory to Mem0 with enhanced metadata."""
        if not self.mem0:
            logger.warning("Mem0 not configured, skipping sync")
            return None
            
        try:
            # Extract key information from OMI memory
            memory_content = {
                "role": "user",
                "content": f"Memory from OMI device: {omi_memory.get('transcript', '')}"
            }
            
            # Enhanced metadata for workshop context
            metadata = {
                "source": "omi_device",
                "team_id": team_id,
                "memory_id": omi_memory.get("id", str(uuid.uuid4())),
                "timestamp": omi_memory.get("created_at", datetime.utcnow().isoformat()),
                "duration": omi_memory.get("duration", 0),
                "participants": omi_memory.get("participants", []),
                "location": omi_memory.get("location", {}),
                "emotions": omi_memory.get("emotions", []),
                "topics": omi_memory.get("topics", []),
                "action_items": omi_memory.get("action_items", []),
                "app_results": omi_memory.get("app_results", {})
            }
            
            # Store in Mem0 with team-specific user ID
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.mem0.add(
                    [memory_content],
                    user_id=f"neurohub_team_{team_id}",
                    metadata=metadata
                )
            )
            
            logger.info(f"Synced OMI memory to Mem0", team_id=team_id, memory_id=metadata["memory_id"])
            return metadata["memory_id"]
            
        except Exception as e:
            logger.error(f"Failed to sync memory to Mem0", error=str(e))
            return None
    
    async def sync_team_memories(self, team_id: str, omi_api_key: str) -> Dict[str, Any]:
        """Sync all memories for a team from OMI to Mem0."""
        synced_count = 0
        failed_count = 0
        
        try:
            # Create temporary OMI connector with team's API key
            team_omi = OMIConnector(self.omi.api_url, omi_api_key)
            
            # Get team's memories from OMI
            memories = await team_omi.get_user_memories(user_id=team_id, limit=100)
            
            for memory in memories:
                result = await self.sync_omi_memory_to_mem0(team_id, memory)
                if result:
                    synced_count += 1
                else:
                    failed_count += 1
                    
            return {
                "status": "success",
                "synced": synced_count,
                "failed": failed_count,
                "total": len(memories)
            }
            
        except Exception as e:
            logger.error(f"Failed to sync team memories", error=str(e))
            return {
                "status": "error",
                "error": str(e),
                "synced": synced_count,
                "failed": failed_count
            }
    
    async def search_unified_memories(
        self,
        team_id: str,
        query: str,
        include_omi: bool = True,
        include_mem0: bool = True,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search memories across both OMI and Mem0 systems."""
        results = []
        
        # Search Mem0 memories
        if include_mem0 and self.mem0:
            try:
                loop = asyncio.get_event_loop()
                mem0_results = await loop.run_in_executor(
                    None,
                    lambda: self.mem0.search(
                        query,
                        user_id=f"neurohub_team_{team_id}",
                        limit=limit
                    )
                )
                
                # Format Mem0 results
                mem0_memories = mem0_results if isinstance(mem0_results, list) else mem0_results.get("results", [])
                for memory in mem0_memories:
                    results.append({
                        "source": "mem0",
                        "content": memory.get("memory", ""),
                        "metadata": memory.get("metadata", {}),
                        "score": memory.get("score", 0)
                    })
                    
            except Exception as e:
                logger.error(f"Mem0 search failed", error=str(e))
        
        # Search OMI memories (would need team's OMI API key)
        if include_omi:
            # This would require the team's OMI API key
            # For now, we'll skip OMI search in the unified interface
            pass
            
        # Sort by relevance score
        results.sort(key=lambda x: x.get("score", 0), reverse=True)
        return results[:limit]
    
    async def analyze_team_memories(self, team_id: str) -> Dict[str, Any]:
        """Analyze a team's memories to extract insights."""
        if not self.mem0:
            return {"error": "Mem0 not configured"}
            
        try:
            # Get all team memories from Mem0
            loop = asyncio.get_event_loop()
            memories = await loop.run_in_executor(
                None,
                lambda: self.mem0.search(
                    "",  # Empty query to get all
                    user_id=f"neurohub_team_{team_id}",
                    limit=1000
                )
            )
            
            memory_list = memories if isinstance(memories, list) else memories.get("results", [])
            
            # Analyze memories
            total_duration = 0
            all_topics = []
            all_participants = set()
            all_emotions = []
            all_action_items = []
            
            for memory in memory_list:
                metadata = memory.get("metadata", {})
                total_duration += metadata.get("duration", 0)
                all_topics.extend(metadata.get("topics", []))
                all_participants.update(metadata.get("participants", []))
                all_emotions.extend(metadata.get("emotions", []))
                all_action_items.extend(metadata.get("action_items", []))
            
            # Calculate insights
            topic_frequency = {}
            for topic in all_topics:
                topic_frequency[topic] = topic_frequency.get(topic, 0) + 1
                
            emotion_summary = {}
            for emotion in all_emotions:
                emotion_summary[emotion] = emotion_summary.get(emotion, 0) + 1
            
            return {
                "total_memories": len(memory_list),
                "total_duration_minutes": round(total_duration / 60, 2),
                "unique_participants": list(all_participants),
                "top_topics": sorted(topic_frequency.items(), key=lambda x: x[1], reverse=True)[:5],
                "emotion_summary": emotion_summary,
                "action_items_count": len(all_action_items),
                "recent_action_items": all_action_items[-5:] if all_action_items else []
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze team memories", error=str(e))
            return {"error": str(e)}
    
    async def create_memory_from_conversation(
        self,
        team_id: str,
        conversation: Dict[str, Any]
    ) -> Optional[str]:
        """Create a memory from a processed conversation."""
        if not self.mem0:
            return None
            
        try:
            # Create memory content from conversation analysis
            memory_content = {
                "role": "assistant",
                "content": f"Conversation analysis: {conversation.get('summary', '')}"
            }
            
            # Extract metadata from conversation analysis
            metadata = {
                "source": "neurohub_analysis",
                "team_id": team_id,
                "timestamp": datetime.utcnow().isoformat(),
                "analysis": conversation.get("analysis", {}),
                "actions": conversation.get("actions", []),
                "key_points": conversation.get("analysis", {}).get("key_points", [])
            }
            
            # Store in Mem0
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.mem0.add(
                    [memory_content],
                    user_id=f"neurohub_team_{team_id}",
                    metadata=metadata
                )
            )
            
            return metadata.get("timestamp")
            
        except Exception as e:
            logger.error(f"Failed to create memory from conversation", error=str(e))
            return None
    
    async def get_contextual_memories(
        self,
        team_id: str,
        context: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Get memories relevant to a specific context for AI agents."""
        if not self.mem0:
            return []
            
        try:
            # Search for contextually relevant memories
            results = await self.search_unified_memories(
                team_id=team_id,
                query=context,
                include_mem0=True,
                include_omi=False,  # Skip OMI for now
                limit=limit
            )
            
            # Format for AI agent consumption
            formatted_memories = []
            for memory in results:
                formatted_memories.append({
                    "content": memory.get("content", ""),
                    "timestamp": memory.get("metadata", {}).get("timestamp", ""),
                    "relevance_score": memory.get("score", 0),
                    "context": memory.get("metadata", {})
                })
                
            return formatted_memories
            
        except Exception as e:
            logger.error(f"Failed to get contextual memories", error=str(e))
            return []


class MemoryEnhancedAgent:
    """Base class for agents with memory access capabilities."""
    
    def __init__(self, memory_bridge: MemoryBridge):
        self.memory = memory_bridge
        
    async def get_relevant_context(self, team_id: str, query: str) -> List[Dict[str, Any]]:
        """Get relevant memories for the current context."""
        return await self.memory.get_contextual_memories(team_id, query)
        
    async def store_insight(self, team_id: str, insight: Dict[str, Any]) -> bool:
        """Store an insight or decision as a memory."""
        conversation = {
            "summary": insight.get("summary", ""),
            "analysis": insight.get("analysis", {}),
            "actions": insight.get("actions", [])
        }
        result = await self.memory.create_memory_from_conversation(team_id, conversation)
        return result is not None