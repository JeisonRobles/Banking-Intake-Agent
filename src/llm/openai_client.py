
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class OpenAIClient():

    def __init__(self, model: str = "gpt-4o-mini"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found. Put it in your .env file or export it.")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat(self, messages: list[dict], temperature: float = 0.0) -> str:
        """
            messages format:
            [{"role": "system", "content: "..."},
             {"role": "user", "content": "..."}
            ]
        """

        response = self.client.chat.completions.create(
            model=self.model,          # must be a valid model id you have access to
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content