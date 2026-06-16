"""
Summarization Agent
Uses Gemini API for generating summaries (with OpenRouter fallback).
"""

import requests
import os
from typing import Optional
from utils.prompts import get_summary_agent_prompt


class SummaryAgent:
    """
    Agent for document summarization.
    Uses Gemini API as primary, with OpenRouter as fallback.
    """
    
    def __init__(self, gemini_key: Optional[str] = None, openrouter_key: Optional[str] = None):
        """
        Initialize the Summary Agent.
        
        Args:
            gemini_key: Gemini API key. If None, reads from environment.
            openrouter_key: OpenRouter API key for fallback.
        """
        self.gemini_key = gemini_key or os.getenv("GEMINI_API_KEY")
        self.openrouter_key = openrouter_key or os.getenv("OPENROUTER_API_KEY")
        self.openrouter_username = os.getenv("OPENROUTER_USERNAME", "agentic-ai-assistant")
        
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.openrouter_models = [
            "deepseek/deepseek-chat-v3-0324:free",
            "meta-llama/llama-3.3-8b-instruct:free",
            "qwen/qwen3-8b:free"
        ]
        
        if not self.gemini_key and not self.openrouter_key:
            raise ValueError("Neither GEMINI_API_KEY nor OPENROUTER_API_KEY found in environment")
    
    def process_document(self, document_text: str) -> dict:
        """
        Generate summary of document.
        
        Args:
            document_text: The document text to summarize
            
        Returns:
            Dictionary containing executive summary, bullet points, and key takeaways
        """
        try:
            prompts = get_summary_agent_prompt(document_text)
            
            # Try Gemini first
            if self.gemini_key:
                try:
                    response = self._call_gemini(prompts["task"])
                    result = self._parse_response(response)
                    
                    return {
                        "status": "success",
                        "executive_summary": result.get("executive_summary", ""),
                        "bullet_summary": result.get("bullet_summary", ""),
                        "key_takeaways": result.get("key_takeaways", ""),
                        "raw_response": response,
                        "api_used": "gemini"
                    }
                except Exception as e:
                    print(f"Gemini API error: {str(e)}")
                    if self.openrouter_key:
                        print("Falling back to OpenRouter...")
            
            # Fallback to OpenRouter
            if self.openrouter_key:
                response = self._call_openrouter(
                    system_prompt=prompts["system"],
                    user_message=prompts["task"]
                )
                result = self._parse_response(response)
                
                return {
                    "status": "success",
                    "executive_summary": result.get("executive_summary", ""),
                    "bullet_summary": result.get("bullet_summary", ""),
                    "key_takeaways": result.get("key_takeaways", ""),
                    "raw_response": response,
                    "api_used": "openrouter"
                }
            
            raise Exception("No available API key for summarization")
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "executive_summary": "",
                "bullet_summary": "",
                "key_takeaways": "",
                "api_used": None
            }
    
    def _call_gemini(self, prompt: str) -> str:
        """
        Call Gemini API.
        
        Args:
            prompt: The prompt for Gemini
            
        Returns:
            API response text
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2000
            }
        }
        
        url = f"{self.gemini_url}?key={self.gemini_key}"
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code != 200:
            raise Exception(f"Gemini API error: {response.status_code} - {response.text}")
        
        response_data = response.json()
        
        if "candidates" not in response_data or len(response_data["candidates"]) == 0:
            raise Exception("Invalid Gemini API response")
        
        return response_data["candidates"][0]["content"]["parts"][0]["text"]
    
    def _call_openrouter(self, system_prompt: str, user_message: str) -> str:
        """
        Call OpenRouter API as fallback.
        
        Args:
            system_prompt: System prompt for the model
            user_message: User message/task
            
        Returns:
            API response text
        """
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
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
            response = requests.post(self.openrouter_url, json=payload, headers=headers, timeout=30)

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
            "executive_summary": "",
            "bullet_summary": "",
            "key_takeaways": ""
        }
        
        # Split by section markers
        sections = response_text.split("---")
        
        for i, section in enumerate(sections):
            section = section.strip()
            
            if "EXECUTIVE SUMMARY" in section:
                if i + 1 < len(sections):
                    result["executive_summary"] = sections[i + 1].split("---")[0].strip()
            
            elif "BULLET" in section and "SUMMARY" in section:
                if i + 1 < len(sections):
                    result["bullet_summary"] = sections[i + 1].split("---")[0].strip()
            
            elif "KEY TAKEAWAY" in section:
                if i + 1 < len(sections):
                    result["key_takeaways"] = sections[i + 1].split("---")[0].strip()
        
        # If parsing failed, return the full response
        if not result["executive_summary"]:
            result["executive_summary"] = response_text[:500]
        
        if not result["bullet_summary"]:
            result["bullet_summary"] = "• Document has been analyzed and summarized."
        
        if not result["key_takeaways"]:
            result["key_takeaways"] = "Key points have been extracted from the document."
        
        return result
