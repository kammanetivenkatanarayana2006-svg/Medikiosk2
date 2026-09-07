"""
Ollama provider for local Qwen3 1.7B integration.
"""
import json
import re
from typing import Optional, Dict, Any
import aiohttp
from app.core.config import settings
from app.ai.prompts import SYSTEM_PROMPT, build_interview_prompt
import logging

logger = logging.getLogger(__name__)

class OllamaProvider:
    """Ollama LLM provider."""
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL or "http://localhost:11434"
        self.model = settings.OLLAMA_MODEL or "qwen3:1.7b"
        self.timeout = settings.OLLAMA_TIMEOUT_SECONDS or 60
    
    async def check_health(self) -> Dict[str, Any]:
        """Check Ollama availability and model."""
        result = {
            "available": False,
            "model_available": False,
            "model_name": self.model,
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Check Ollama reachable
                async with session.get(
                    f"{self.base_url}/api/tags",
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as response:
                    if response.status != 200:
                        return result
                    
                    data = await response.json()
                    models = data.get("models", [])
                    
                    # Check if configured model exists
                    model_names = [m.get("name", "") for m in models]
                    result["available"] = True
                    
                    for name in model_names:
                        if self.model in name or name in self.model:
                            result["model_available"] = True
                            break
                    
                    if not result["model_available"]:
                        result["error"] = f"Model '{self.model}' not found. Available: {model_names}"
        
        except Exception as e:
            result["error"] = f"Ollama unreachable: {str(e)}"
        
        return result
    
    async def generate_structured_response(
        self,
        prompt: str,
    ) -> Dict[str, Any]:
        """
        Generate structured response from Ollama.
        Returns dict with success status and parsed JSON.
        """
        if not settings.OLLAMA_ENABLED:
            return {"success": False, "error": "Ollama disabled"}
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "system": SYSTEM_PROMPT,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 300,
                        "top_p": 0.9,
                    },
                    "format": "json",
                }
                
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as response:
                    if response.status != 200:
                        return {
                            "success": False,
                            "error": f"Ollama error: {response.status}",
                        }
                    
                    data = await response.json()
                    raw_output = data.get("response", "")
                    
                    # Try to parse JSON
                    parsed = self._extract_json(raw_output)
                    if not parsed:
                        return {
                            "success": False,
                            "error": "Malformed JSON from model",
                        }
                    
                    return {
                        "success": True,
                        "data": parsed,
                    }
        
        except aiohttp.ClientTimeout:
            return {"success": False, "error": "Ollama timeout"}
        except Exception as e:
            return {"success": False, "error": f"Ollama error: {str(e)}"}
    
    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from model output."""
        if not text:
            return None
        
        # Try direct parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON in text
        json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        
        return None

ollama_provider = OllamaProvider()