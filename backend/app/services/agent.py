# backend/app/services/agent.py

import os
import logging
import openai
from openai import OpenAIError

class MockAgent:
    """
    Agente de prueba que responde siempre "hello".
    """
    def get_response(self, messages: list[dict]) -> str:
        return "hello"


class OpenAIAgent:
    """
    Agente real que llama a la API de OpenAI usando la nueva interfaz v1.
    """
    def __init__(self, api_key: str | None = None, model: str = "gpt-3.5-turbo"):
        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY is required for OpenAIAgent")
        openai.api_key = key
        self.model = model

    def get_response(self, messages: list[dict]) -> str:
        try:
            # Nueva llamada v1: openai.chat.completions.create(...)
            resp = openai.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return resp.choices[0].message.content
        except OpenAIError as e:
            logging.error(f"OpenAI API error: {e}")
            # Puedes mapear esto a un HTTPException en dependencias si quieres
            raise