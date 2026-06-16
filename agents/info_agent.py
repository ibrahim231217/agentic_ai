"""
Information Collection and Distribution Agent
Uses DeepSeek or other models via OpenRouter.
"""

import requests
import os
from typing import Optional
from utils.prompts import get_info_agent_prompt


class InfoAgent:
    """
    Agent for information extraction and organization.
    Uses OpenRouter API with DeepSeek or alternative models.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Information Agent.
        
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
        Extract and organize information from document.
        
        Args:
            document_text: The document text to process
            
        Returns:
            Dictionary containing extracted entities, action items, data points, etc.
        """
        try:
            prompts = get_info_agent_prompt(document_text)
            
            # Call OpenRouter API
            response = self._call_api(
                system_prompt=prompts["system"],
                user_message=prompts["task"]
            )
            
            # Parse the response
            result = self._parse_response(response)
            
            return {
                "status": "success",
                "entities": result.get("entities", ""),
                "action_items": result.get("action_items", ""),
                "data_points": result.get("data_points", ""),
                "categorized_info": result.get("categorized_info", ""),
                "distribution_report": result.get("distribution_report", ""),
                "raw_response": response
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "entities": "",
                "action_items": "",
                "data_points": "",
                "categorized_info": "",
                "distribution_report": ""
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
            "max_tokens": 2500
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
            "entities": "",
            "action_items": "",
            "data_points": "",
            "categorized_info": "",
            "distribution_report": ""
        }
        
        # Split by section markers
        sections = response_text.split("---")
        
        for i, section in enumerate(sections):
            section = section.strip()
            
            if "IMPORTANT ENTITIES" in section:
                if i + 1 < len(sections):
                    result["entities"] = sections[i + 1].split("---")[0].strip()
            
            elif "ACTION ITEM" in section:
                if i + 1 < len(sections):
                    result["action_items"] = sections[i + 1].split("---")[0].strip()
            
            elif "KEY DATA" in section:
                if i + 1 < len(sections):
                    result["data_points"] = sections[i + 1].split("---")[0].strip()
            
            elif "CATEGORIZED" in section and "INFORMATION" in section:
                if i + 1 < len(sections):
                    result["categorized_info"] = sections[i + 1].split("---")[0].strip()
            
            elif "DISTRIBUTION" in section and "REPORT" in section:
                if i + 1 < len(sections):
                    result["distribution_report"] = sections[i + 1].split("---")[0].strip()
        
        # If parsing failed, return the full response
        if not result["entities"]:
            result["entities"] = response_text[:400]
        
        if not result["action_items"]:
            result["action_items"] = "No specific action items identified."
        
        if not result["data_points"]:
            result["data_points"] = "No numeric data points found."
        
        if not result["categorized_info"]:
            result["categorized_info"] = "Information has been extracted from the document."
        
        if not result["distribution_report"]:
            result["distribution_report"] = "Distribution-ready format of extracted information."
        
        return result
