
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class OpenAIClient():

    def __init__(self, model: str = "gpt-4o-mini", embedding_model: str= "text-embedding-3-small"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found. Put it in your .env file or export it.")

        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.embedding_model = embedding_model

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
    
    def embed(self, texts: list[str]) -> list[list[float]]:
        """
        Returns embeddings for a batch of texts.
        Uses OpenAI Embeddings API. :contentReference[oaicite:1]{index=1}
        """
        resp = self.client.embeddings.create(
            model=self.embedding_model,  # e.g. text-embedding-3-small :contentReference[oaicite:2]{index=2}
            input=texts,
        )
        return [d.embedding for d in resp.data]