"""LLM Factory Module.

This module handles model configuration and factory creation for different LLM 
providers, supporting multiple model types and deployment configurations.

Classes:
    ModelConfig: Configuration container for specific models
    LLMFactory: Factory for creating LLM provider instances
"""

import os
from typing import Dict, Any
from .provider import LLMProvider
from openai import AsyncOpenAI, AsyncAzureOpenAI
import config.config_loader as config_loader
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_models_info.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ModelConfig:
    """Configuration container for a specific model.
    
    Stores model-specific configuration including provider type,
    API credentials, and deployment details.
    
    Attributes:
        name: Model name identifier
        provider_type: Type of provider ('azure', 'openai', etc.)
        config: Dictionary of additional configuration parameters
        
    Example:
        >>> config = ModelConfig("gpt-4o", "azure", api_key="...", endpoint="...")
    """
    
    def __init__(self, name: str, provider_type: str, **kwargs: Any) -> None:
        """Initialize model configuration.
        
        Args:
            name: Model name identifier
            provider_type: Type of provider ('azure', 'openai', etc.)
            **kwargs: Additional configuration parameters
        """
        self.name: str = name
        self.provider_type: str = provider_type
        self.config: Dict[str, Any] = kwargs


class LLMFactory:
    """Factory for creating LLM providers for different models.
    
    This class manages model configurations and creates appropriate
    LLM provider instances based on the model type and configuration.
    
    Example:
        >>> configs = LLMFactory.get_model_configs()
        >>> provider = await LLMFactory.create_llm_provider(configs["gpt-4o"])
    """
    

    @staticmethod
    def get_model_configs() -> Dict[str, ModelConfig]:
        """Get all available model configurations from environment variables.
        
        Scans environment variables to detect available API keys and endpoints,
        then creates ModelConfig instances for each available model.
        
        Returns:
            Dictionary mapping model names to ModelConfig instances
        """
        configs = {}
        logger.info("Loading model configurations from environment variables.")
        
        ai_gateway_url = os.getenv("AI_GATEWAY_URL")
        ai_gateway_key = os.getenv("AI_GATEWAY_API_KEY")
        ai_gateway_deployment = os.getenv("AI_GATEWAY_DEPLOYMENT")
        
        if ai_gateway_url and ai_gateway_key and ai_gateway_deployment:
            logger.info(f"Model {ai_gateway_deployment} configured for AI Gateway provider.")
            configs["ai-gateway"] = ModelConfig(
                name="ai-gateway",
                provider_type="ai_gateway",
                base_url=ai_gateway_url.rstrip("/"),
                api_key=ai_gateway_key,
                api_version=config_loader.get_ai_gateway_api_version(),
                deployment_name=ai_gateway_deployment
        )

        # Local LLM (LMStudio)
        local_llm_base_url = os.getenv("LOCAL_LLM_BASE_URL")
        local_llm_model_name = os.getenv("LOCAL_LLM_MODEL_NAME")
        
        if local_llm_base_url and local_llm_model_name:
            logger.info(f"Model {local_llm_model_name} configured for local LMStudio provider.")
            configs["Phi-4-mini-instruct"] = ModelConfig(
                name="Phi-4-mini-instruct",
                provider_type="local",
                base_url=local_llm_base_url,
                model_name=local_llm_model_name
            )

        # Databricks models
        databricks_token = os.getenv("DATABRICKS_TOKEN")
        databricks_host = os.getenv("DATABRICKS_HOST")
        databricks_workspace_id = os.getenv("DATABRICKS_WORKSPACE_ID")
        
        if databricks_token and databricks_host:
            databricks_models = [
            "databricks-claude-sonnet-4-5",
            "databricks-claude-sonnet-4"            ]
            
            for model_name in databricks_models:
                logger.info(f"Models {model_name} configured for Databricks provider.")
                configs[model_name] = ModelConfig(
                    name=model_name,
                    provider_type="databricks",
                    token=databricks_token,
                    host=databricks_host,
                    workspace_id=databricks_workspace_id,
                    model_name=model_name
                )
        return configs

    @staticmethod
    async def create_llm_provider(model_config: ModelConfig) -> LLMProvider:
        """Create an LLM provider for the given model configuration.
        
        Creates appropriate client and provider instance based on the
        model configuration's provider type.
        
        Args:
            model_config: Configuration for the model to create
            
        Returns:
            Configured LLMProvider instance
            
        Raises:
            ValueError: If provider type is not supported
        """
        if model_config.provider_type == "ai_gateway":
            # AI Gateway uses Azure OpenAI-compatible API
            client = AsyncAzureOpenAI(
                azure_endpoint=model_config.config["base_url"],
                api_key=model_config.config["api_key"],
                api_version=model_config.config["api_version"]
            )
            return LLMProvider(
                client=client,
                deployment_name=model_config.config["deployment_name"],
                provider_type="ai_gateway"
            )
        if model_config.provider_type == "local":
            # Local LLM (LMStudio) uses OpenAI-compatible API
            client = AsyncOpenAI(
                api_key="not-needed",  # LMStudio doesn't require API key
                base_url=model_config.config["base_url"]
            )
            return LLMProvider(
                client=client,
                deployment_name=model_config.config["model_name"],
                provider_type="local"
            )
        if model_config.provider_type == "databricks":
            # Databricks uses OpenAI-compatible API with Bearer token auth
            # Clean the host URL to remove any browser paths
            
            host = model_config.config["host"]
            if "/browse/" in host:
                # Extract just the workspace URL part
                host = host.split("/browse/")[0]
                
            
            client = AsyncOpenAI(
                api_key=model_config.config["token"],
                base_url=f"{host}/serving-endpoints/{model_config.config['model_name']}"
            )
            return LLMProvider(
                client=client,
                deployment_name=model_config.config["model_name"],
                provider_type="databricks"
            )
        if model_config.provider_type == "azure":
            client = AsyncAzureOpenAI(
                azure_endpoint=model_config.config["endpoint"],
                api_key=model_config.config["api_key"],
                api_version=config_loader.get_azure_api_version()
            )
            return LLMProvider(
                client=client,
                deployment_name=model_config.config["deployment_name"],
                provider_type="azure"
            )
        
        else:
            raise ValueError(f"Supported provider type: {model_config.provider_type}")
