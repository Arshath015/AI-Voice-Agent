from abc import ABC, abstractmethod
from typing import List, Dict
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()


class LLMEngine(ABC):
    @abstractmethod
    async def generate_response(self, messages: List[Dict[str, str]]) -> str:
        pass


class GroqLLM(LLMEngine):
    """
    Groq LLM Engine using Llama3.
    Replaces Gemini API with Groq inference.
    """

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")

        self.client = Groq(api_key=api_key)

    async def generate_response(self, messages: List[Dict[str, str]]) -> str:

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7
        )

        return response.choices[0].message.content