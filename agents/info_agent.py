"""
Information Extraction Agent
Uses DeepSeek R1 free as primary provider, DeepSeek Chat V3 free as fallback, and Gemini 2.5 Flash as final fallback.
"""

import requests
import os
from typing import Optional
from utils.prompts import get_info_agent_prompt


class InfoAgent:
    """
    Agent for information extraction and organization.
    Uses OpenRouter free models with DeepSeek priority and Gemini fallback.
    """

    def __init__(self, api_key: Optional[str] = None, gemini_key: Optional[str] = None):
        """
        Initialize the Information Agent.

        Args:
            api_key: OpenRouter API key. If None, reads from environment.
            gemini_key: Gemini API key. If None, reads from environment.
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.gemini_key = gemini_key or os.getenv("GEMINI_API_KEY")
        self.username = os.getenv("OPENROUTER_USERNAME", "agentic-ai-assistant")

        if not self.api_key and not self.gemini_key:
            raise ValueError("Neither OPENROUTER_API_KEY nor GEMINI_API_KEY found in environment variables")

        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

        self.openrouter_models = [
            "deepseek/deepseek-r1:free",
            "deepseek/deepseek-chat-v3:free",
            "meta-llama/llama-3.3-8b-instruct:free"
        ]

    def process_document(self, document_text: str) -> dict:
        """
        Extract and organize information from document.

        Args:
            document_text: The document text to process

        Returns:
            Dictionary containing extracted entities, deadlines, action items, facts, and distribution report
        """
        try:
            prompts = get_info_agent_prompt(document_text)

            response = None
            if self.api_key:
                try:
                    response = self._call_openrouter(
                        system_prompt=prompts["system"],
                        user_message=prompts["task"]
                    )
                    api_used = "openrouter"
                except Exception as openrouter_error:
                    response = None
                    if not self.gemini_key:
                        raise openrouter_error

            if response is None and self.gemini_key:
                response = self._call_gemini(
                    system_prompt=prompts["system"],
                    user_message=prompts["task"]
                )
                api_used = "gemini"

            if response is None:
                raise Exception("No available API key for information extraction")

            result = self._parse_response(response)
            result["raw_response"] = response
            result["api_used"] = api_used
            result["status"] = "success"
            return result

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "entities": "",
                "dates_deadlines": "",
                "action_items": "",
                "key_facts": "",
                "categorized_info": "",
                "distribution_report": "",
                "api_used": None
            }

    def _call_openrouter(self, system_prompt: str, user_message: str) -> str:
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

    def _call_gemini(self, system_prompt: str, user_message: str) -> str:
        """
        Call Gemini 2.5 Flash API as a final fallback.

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
                "maxOutputTokens": 2500
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
            "dates_deadlines": "",
            "action_items": "",
            "key_facts": "",
            "categorized_info": "",
            "distribution_report": ""
        }

        sections = response_text.split("---")
        for i, section in enumerate(sections):
            section = section.strip()
            if "IMPORTANT ENTITIES" in section:
                if i + 1 < len(sections):
                    result["entities"] = sections[i + 1].split("---")[0].strip()
            elif "DATES AND DEADLINES" in section:
                if i + 1 < len(sections):
                    result["dates_deadlines"] = sections[i + 1].split("---")[0].strip()
            elif "ACTION ITEMS" in section:
                if i + 1 < len(sections):
                    result["action_items"] = sections[i + 1].split("---")[0].strip()
            elif "KEY FACTS" in section:
                if i + 1 < len(sections):
                    result["key_facts"] = sections[i + 1].split("---")[0].strip()
            elif "CATEGORIZED INFORMATION" in section:
                if i + 1 < len(sections):
                    result["categorized_info"] = sections[i + 1].split("---")[0].strip()
            elif "DISTRIBUTION REPORT" in section:
                if i + 1 < len(sections):
                    result["distribution_report"] = sections[i + 1].split("---")[0].strip()

        if not result["entities"]:
            result["entities"] = response_text[:400]
        if not result["dates_deadlines"]:
            result["dates_deadlines"] = "No dates or deadlines identified."
        if not result["action_items"]:
            result["action_items"] = "No action items identified."
        if not result["key_facts"]:
            result["key_facts"] = "No key facts identified."
        if not result["categorized_info"]:
            result["categorized_info"] = "Information has been extracted and organized."
        if not result["distribution_report"]:
            result["distribution_report"] = "Distribution-ready report information is available."

        return result
