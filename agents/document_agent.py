"""
Document Checking and Writing Agent
Uses deepseek / geminbi model  to review and improve documents.
"""

import requests
import os
from typing import Optional
from utils.prompts import get_document_agent_prompt


class DocumentAgent:
    """
    Agent for document review and improvement.
    Uses OpenRouter API with free models.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Document Agent.
        
        Args:
            api_key: OpenRouter API key. If None, reads from environment.
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.username = os.getenv("OPENROUTER_USERNAME", "agentic-ai-assistant")
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

        # Try a prioritized list of OpenRouter free models (fallback order)
        self.openrouter_models = [
            "deepseek/deepseek-chat-v3-0324:free",
            "meta-llama/llama-3.3-8b-instruct:free",
            "qwen/qwen3-8b:free"
        ]
    
    def process_document(self, document_text: str) -> dict:
        """
        Process document for review and improvement.
        
        Args:
            document_text: The document text to process
            
        Returns:
            Dictionary containing improved document and changes summary
        """
        try:
            prompts = get_document_agent_prompt(document_text)
            
            # Call OpenRouter API
            response = self._call_api(
                system_prompt=prompts["system"],
                user_message=prompts["task"]
            )
            
            # Parse the response
            result = self._parse_response(response)
            
            return {
                "status": "success",
                "improved_document": result.get("improved_document", ""),
                "changes_summary": result.get("changes_summary", ""),
                "raw_response": response
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "improved_document": "",
                "changes_summary": ""
            }
    
    def _call_api(self, system_prompt: str, user_message: str) -> str:
        """
        Call OpenRouter API.
        
        Args:
            system_prompt: System prompt for the model
            user_message: User message/task
            
        Returns:
            API response text
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://agentic-ai-assistant.local",
            "X-Title": "Agentic AI Document Assistant",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.openrouter_models[0],
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        last_error = None
        for model in self.openrouter_models:
            payload["model"] = model
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)

            if response.status_code == 200:
                response_data = response.json()
                if "choices" not in response_data or len(response_data["choices"]) == 0:
                    raise Exception("Invalid API response format")
                return response_data["choices"][0]["message"]["content"]

            last_error = Exception(f"OpenRouter API error: {response.status_code} - {response.text}")
            text_lower = response.text.lower()

            if model != self.openrouter_models[-1] and (
                response.status_code == 404 or
                (response.status_code == 400 and "not a valid model id" in text_lower) or
                (response.status_code == 400 and "no endpoints found" in text_lower)
            ):
                continue
            break

        raise last_error
    
    def _parse_response(self, response_text: str) -> dict:
        """
        Parse the agent's response.
        
        Args:
            response_text: Raw response from the model
            
        Returns:
            Parsed response dictionary
        """
        result = {
            "improved_document": "",
            "changes_summary": ""
        }
        
        # Split by section markers
        sections = response_text.split("---")
        
        for i, section in enumerate(sections):
            section = section.strip()
            
            if "IMPROVED DOCUMENT" in section:
                # Extract improved document
                if i + 1 < len(sections):
                    result["improved_document"] = sections[i + 1].split("---")[0].strip()
            
            elif "CHANGES SUMMARY" in section or "CHANGES" in section:
                # Extract changes summary
                if i + 1 < len(sections):
                    changes = sections[i + 1].split("---")[0].strip()
                    result["changes_summary"] = changes
        
        # If parsing failed, return the full response
        if not result["improved_document"]:
            result["improved_document"] = response_text
        
        if not result["changes_summary"]:
            result["changes_summary"] = "Document has been reviewed and improved."
        
        return result
