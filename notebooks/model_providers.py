"""
Model-Agnostic LLM Provider Support
Supports OpenAI, Anthropic (Claude), and Ollama
"""

import os
from typing import Optional, Dict, List, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """Standardized LLM response format"""
    content: str
    model: str
    provider: str
    tokens_used: Optional[int] = None
    latency_ms: Optional[float] = None
    error: Optional[str] = None


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate a response from the LLM"""
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package not installed. Install with: pip install openai")
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment or provided")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.provider_name = "openai"
    
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate response using OpenAI API"""
        import time
        
        model = kwargs.get("model", self.model)
        max_tokens = kwargs.get("max_tokens", 1000)
        temperature = kwargs.get("temperature", 0.7)
        
        try:
            start_time = time.time()
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            latency_ms = (time.time() - start_time) * 1000
            
            return LLMResponse(
                content=response.choices[0].message.content,
                model=model,
                provider=self.provider_name,
                tokens_used=response.usage.total_tokens if hasattr(response, 'usage') else None,
                latency_ms=latency_ms
            )
        except Exception as e:
            return LLMResponse(
                content="",
                model=model,
                provider=self.provider_name,
                error=str(e)
            )
    
    def get_available_models(self) -> List[str]:
        """Get list of available OpenAI models"""
        return [
            "gpt-4",
            "gpt-4-turbo-preview",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k"
        ]


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError("anthropic package not installed. Install with: pip install anthropic")
        
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment or provided")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.provider_name = "anthropic"
    
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate response using Anthropic API"""
        import time
        
        model = kwargs.get("model", self.model)
        max_tokens = kwargs.get("max_tokens", 1000)
        temperature = kwargs.get("temperature", 0.7)
        
        try:
            start_time = time.time()
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            latency_ms = (time.time() - start_time) * 1000
            
            content = ""
            if response.content:
                # Anthropic returns a list of content blocks
                content = "".join([block.text for block in response.content if hasattr(block, 'text')])
            
            return LLMResponse(
                content=content,
                model=model,
                provider=self.provider_name,
                tokens_used=response.usage.input_tokens + response.usage.output_tokens if hasattr(response, 'usage') else None,
                latency_ms=latency_ms
            )
        except Exception as e:
            return LLMResponse(
                content="",
                model=model,
                provider=self.provider_name,
                error=str(e)
            )
    
    def get_available_models(self) -> List[str]:
        """Get list of available Anthropic models"""
        return [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ]


class OllamaProvider(LLMProvider):
    """Ollama local model provider"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        try:
            import requests
        except ImportError:
            raise ImportError("requests package not installed. Install with: pip install requests")
        
        self.base_url = base_url
        self.model = model
        self.provider_name = "ollama"
        self._requests = requests
    
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate response using Ollama API"""
        import time
        
        model = kwargs.get("model", self.model)
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        
        # Add optional parameters
        if "max_tokens" in kwargs:
            payload["options"] = {"num_predict": kwargs["max_tokens"]}
        if "temperature" in kwargs:
            if "options" not in payload:
                payload["options"] = {}
            payload["options"]["temperature"] = kwargs["temperature"]
        
        try:
            start_time = time.time()
            response = self._requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            latency_ms = (time.time() - start_time) * 1000
            
            return LLMResponse(
                content=result.get("response", ""),
                model=model,
                provider=self.provider_name,
                tokens_used=result.get("eval_count"),  # Ollama's approximate token count
                latency_ms=latency_ms
            )
        except Exception as e:
            return LLMResponse(
                content="",
                model=model,
                provider=self.provider_name,
                error=str(e)
            )
    
    def get_available_models(self) -> List[str]:
        """Get list of available Ollama models (requires API call)"""
        try:
            url = f"{self.base_url}/api/tags"
            response = self._requests.get(url, timeout=5)
            if response.status_code == 200:
                models_data = response.json()
                return [model["name"] for model in models_data.get("models", [])]
        except:
            pass
        
        # Return common defaults if API unavailable
        return ["llama2", "mistral", "codellama", "neural-chat", "starling-lm"]


class ModelProviderFactory:
    """Factory for creating LLM providers"""
    
    @staticmethod
    def create_provider(provider_type: str, **kwargs) -> LLMProvider:
        """
        Create an LLM provider instance.
        
        Args:
            provider_type: 'openai', 'anthropic', or 'ollama'
            **kwargs: Provider-specific arguments
        
        Returns:
            LLMProvider instance
        """
        provider_type = provider_type.lower()
        
        if provider_type == "openai":
            return OpenAIProvider(**kwargs)
        elif provider_type == "anthropic":
            return AnthropicProvider(**kwargs)
        elif provider_type == "ollama":
            return OllamaProvider(**kwargs)
        else:
            raise ValueError(f"Unknown provider type: {provider_type}. Choose from: openai, anthropic, ollama")
    
    @staticmethod
    def auto_detect_provider() -> Optional[LLMProvider]:
        """
        Automatically detect and create a provider based on available API keys.
        Priority: OpenAI > Anthropic > Ollama
        """
        # Check OpenAI
        if os.getenv("OPENAI_API_KEY"):
            try:
                return OpenAIProvider()
            except:
                pass
        
        # Check Anthropic
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                return AnthropicProvider()
            except:
                pass
        
        # Check Ollama (local, so always try)
        try:
            return OllamaProvider()
        except:
            pass
        
        return None


class UnifiedLLMClient:
    """
    Unified client for working with multiple LLM providers.
    Provides a consistent interface regardless of provider.
    """
    
    def __init__(self, provider: Optional[LLMProvider] = None):
        """
        Initialize with a specific provider or auto-detect.
        
        Args:
            provider: LLMProvider instance, or None to auto-detect
        """
        if provider is None:
            provider = ModelProviderFactory.auto_detect_provider()
            if provider is None:
                raise ValueError("No LLM provider available. Please set API keys or start Ollama.")
        
        self.provider = provider
    
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate a response using the configured provider"""
        return self.provider.generate(prompt, **kwargs)
    
    def get_provider_name(self) -> str:
        """Get the name of the current provider"""
        return self.provider.provider_name
    
    def get_available_models(self) -> List[str]:
        """Get available models for the current provider"""
        return self.provider.get_available_models()
    
    def switch_provider(self, provider_type: str, **kwargs):
        """Switch to a different provider"""
        self.provider = ModelProviderFactory.create_provider(provider_type, **kwargs)


# Example usage
if __name__ == "__main__":
    # Example 1: Auto-detect provider
    try:
        client = UnifiedLLMClient()
        print(f"Using provider: {client.get_provider_name()}")
        print(f"Available models: {client.get_available_models()}")
        
        # Generate a response
        response = client.generate("Write a haiku about AI.")
        if response.error:
            print(f"Error: {response.error}")
        else:
            print(f"\nResponse:\n{response.content}")
            print(f"\nStats: {response.latency_ms:.0f}ms, {response.tokens_used} tokens")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Use specific provider
    # client = UnifiedLLMClient(provider=OpenAIProvider(model="gpt-4"))
    # response = client.generate("Hello!")
