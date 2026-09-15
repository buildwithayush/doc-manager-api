
from fastapi import HTTPException,status

from app.core.config import settings
import httpx2


class EmbeddingService:

    @staticmethod
    def get_embedding(text: str) -> list[float]:

        try:
            with httpx2.Client(timeout=60.0) as client:
                response = client.post(
                    settings.OLLAMA_EMBED_URL,
                    json={"model": settings.MODEL_NAME, "prompt": text}
                )
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Ollama API error: {response.text}"
                    )
                return response.json()["embedding"]
            
        except httpx2.RequestError as exc:
            raise RuntimeError(f"Ollama container connection failed: {exc}")         