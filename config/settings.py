"""Application Settings

Centralized configuration management with environment variable support.
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from dotenv import load_dotenv

# Load environment variables
env_file = Path(__file__).parent.parent / ".env.local"
if env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv()  # Load default .env


@dataclass
class AgentDBConfig:
    """AgentDB configuration settings."""
    api_key: str
    api_url: str = "https://api.agentdb.dev"
    
    @classmethod
    def from_env(cls) -> "AgentDBConfig":
        api_key = os.getenv("AGENTDB_API_KEY")
        if not api_key:
            raise ValueError(
                "AGENTDB_API_KEY not found in environment. "
                "Please set it in .env.local or as an environment variable."
            )
        
        return cls(
            api_key=api_key,
            api_url=os.getenv("AGENTDB_API_URL", "https://api.agentdb.dev")
        )


@dataclass
class OMIConfig:
    """OMI backend configuration."""
    api_url: str
    api_key: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> "OMIConfig":
        # Support both OMI_API_URL and OMI_API_BASE_URL for compatibility
        api_url = os.getenv("OMI_API_URL") or os.getenv("OMI_API_BASE_URL", "http://localhost:8000")
        return cls(
            api_url=api_url,
            api_key=os.getenv("OMI_API_KEY")
        )


@dataclass
class OpenAIConfig:
    """OpenAI configuration for agents."""
    api_key: Optional[str] = None
    model: str = "gpt-4-turbo-preview"
    
    @classmethod
    def from_env(cls) -> "OpenAIConfig":
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        )


@dataclass
class AgentConfig:
    """Individual agent configuration."""
    agent_id: str
    name: str
    port: int
    
    @classmethod
    def from_env(cls, agent_id: str, default_port: int) -> "AgentConfig":
        port_key = f"{agent_id.upper().replace('-', '_')}_PORT"
        return cls(
            agent_id=agent_id,
            name=agent_id.replace("-", " ").title(),
            port=int(os.getenv(port_key, default_port))
        )


class Settings:
    """Global application settings."""
    
    def __init__(self):
        # Load configurations
        self.agentdb = AgentDBConfig.from_env()
        self.omi = OMIConfig.from_env()
        self.openai = OpenAIConfig.from_env()
        
        # Agent configurations
        self.agents = {
            "gateway": AgentConfig.from_env("gateway-agent", 8001),
            "context": AgentConfig.from_env("context-agent", 8002),
            "action": AgentConfig.from_env("action-agent", 8003),
            "knowledge": AgentConfig.from_env("knowledge-agent", 8004),
            "communication": AgentConfig.from_env("communication-agent", 8005),
        }
        
        # General settings
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    def get_agent_db_manager(self):
        """Create AgentDB manager with current settings."""
        from integrations.agentdb_manager import AgentDBManager
        return AgentDBManager(
            api_key=self.agentdb.api_key,
            api_url=self.agentdb.api_url
        )
    
    def validate(self):
        """Validate required settings are present."""
        errors = []
        
        # Check required API keys
        if not self.agentdb.api_key:
            errors.append("AGENTDB_API_KEY is required")
        
        if not self.omi.api_url:
            errors.append("OMI_API_URL is required")
        
        # Warn about optional keys
        warnings = []
        if not self.openai.api_key:
            warnings.append("OPENAI_API_KEY not set - some agents may not function")
        
        if errors:
            raise ValueError(f"Configuration errors: {'; '.join(errors)}")
        
        if warnings:
            for warning in warnings:
                print(f"Warning: {warning}")
        
        return True


# Global settings instance
settings = Settings()

# Validate on import
try:
    settings.validate()
except ValueError as e:
    print(f"\n⚠️  Configuration Error: {e}")
    print("\nPlease ensure you have:")
    print("1. Created .env.local file")
    print("2. Added required API keys")
    print("3. See .env.example for all required variables\n")
    raise