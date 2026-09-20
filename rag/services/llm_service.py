import os
import httpx2
from app.core.config import settings
from fastapi import status,HTTPException
from langchain_core.prompts import load_prompt

PROMPT_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "prompts", "rag_prompt.yaml"
)

RAG_PROMPT_TEMPLATE = load_prompt(PROMPT_FILE_PATH)

class LLMService:
    @staticmethod
    def generate_answer(query: str, context_chunks: list[str]) -> str:
        if not context_chunks:
            return "I don't have enough information in the provided document."

        formatted_context = "\n\n".join(
            [f"[Chunk {idx + 1}]:\n{chunk}" for idx, chunk in enumerate(context_chunks)]
        )

        prompt_value = RAG_PROMPT_TEMPLATE.invoke({
            "context": formatted_context,
            "question": query,
        })
        formatted_messages = [
            {
                "role": msg.type if msg.type != "human" else "user",
                "content": msg.content,
            }
            for msg in prompt_value.to_messages()
        ]

        payload = {
            "model": settings.CHAT_MODEL_NAME,
            "messages": formatted_messages,
            "stream": False,
            "options": {"temperature": 0.1},
        }

        try:
            with httpx2.Client(timeout=120.0) as client:
                response = client.post(settings.OLLAMA_CHAT_URL, json=payload)

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Ollama generation failed: {response.text}",
                    )

                result = response.json()
                return result["message"]["content"].strip()

        except httpx2.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Unable to reach Ollama container: {exc}",
            )   