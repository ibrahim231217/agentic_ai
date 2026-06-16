"""
Document Review Agent
Uses Gemini 2.5 Flash as the primary provider with OpenRouter fallback.
"""

import requests
import os
from typing import Optional
from utils.prompts import get_document_agent_prompt


class DocumentAgent:
    """
    Agent for document review and improvement.
    Uses Gemini 2.5 Flash as primary provider and OpenRouter free models as fallback.
    """

    def __init__(self, api_key: Optional[str] = None, gemini_key: Optional[str] = None):
        """
        Initialize the Document Agent.

        Args:
            api_key: OpenRouter API key. If None, reads from environment.
            gemini_key: Gemini API key. If None, reads from environment.
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.gemini_key = gemini_key or os.getenv("GEMINI_API_KEY")
        self.username = os.getenv("OPENROUTER_USERNAME", "agentic-ai-assistant")

        if not self.api_key and not self.gemini_key:
            raise ValueError("Neither OPENROUTER_API_KEY nor GEMINI_API_KEY found in environment variables")

        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

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
            Dictionary containing improved document, changes summary, and the API used.
        """
        try:
            prompts = get_document_agent_prompt(document_text)

            # Try Gemini 2.5 Flash first
            if self.gemini_key:
                try:
                    response = self._call_gemini(
                        system_prompt=prompts["system"],
                        user_message=prompts["task"]
                    )

                    result = self._parse_response(response)
                    return {
                        "status": "success",
                        "improved_document": result.get("improved_document", ""),
                        "changes_summary": result.get("changes_summary", ""),
                        "raw_response": response,
                        "api_used": "gemini"
                    }
                except Exception as gemini_error:
                    if not self.api_key:
                        raise gemini_error

            # Fallback to OpenRouter free models
            if self.api_key:
                response = self._call_openrouter(
                    system_prompt=prompts["system"],
                    user_message=prompts["task"]
                )
                result = self._parse_response(response)
                return {
                    "status": "success",
                    "improved_document": result.get("improved_document", ""),
                    "changes_summary": result.get("changes_summary", ""),
                    "raw_response": response,
                    "api_used": "openrouter"
                }

            raise Exception("No available API key for document review")

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "improved_document": "",
                "changes_summary": "",
                "api_used": None
            }

    def _call_gemini(self, system_prompt: str, user_message: str) -> str:
        """
        Call Gemini 2.5 Flash API.

        Args:
            system_prompt: System prompt for the model
            user_message: User message/task

        Returns:
            API response text
        """
        headers = {
            "Content-Type": "application/json"
        }

        full_prompt = f"{system_prompt}\n\n{user_message}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": full_prompt
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
            "improved_document": "",
            "changes_summary": ""
        }

        sections = response_text.split("---")
        for i, section in enumerate(sections):
            section = section.strip()
            if "IMPROVED DOCUMENT" in section:
                if i + 1 < len(sections):
                    result["improved_document"] = sections[i + 1].split("---")[0].strip()
            elif "CHANGES SUMMARY" in section or "CHANGES" in section:
                if i + 1 < len(sections):
                    result["changes_summary"] = sections[i + 1].split("---")[0].strip()

        if not result["improved_document"]:
            result["improved_document"] = response_text
        if not result["changes_summary"]:
            result["changes_summary"] = "Document has been reviewed and improved."

        return result
