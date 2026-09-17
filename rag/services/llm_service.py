import httpx2

from app.core.config import settings
from fastapi import status,HTTPException

SYSTEM_PROMPT = """You are a precise document question-answering assistant.
Answer the question based ONLY on the provided context.

Guidelines:
1. Extract facts accurately from the context.
2. You may resolve direct synonyms and natural phrasing differences (e.g., "preserves and protects" matches "saved by", "fall" matches "decrease").
3. Do not infer or extrapolate facts that are not grounded in the text.
4. If the requested information is genuinely absent from the context, respond strictly with:
"I don't have enough information in the provided document."
"""

class LLMService:
    @staticmethod

    def generate_answer(query: str, context_chunks:list[str]) -> str:
  
     if not context_chunks:
        return "I don't have enough information in the provided document."

     formatted_context = "\n\n".join(
         [f"[Chunk {idx + 1}]:\n{chunk}" for idx, chunk in enumerate(context_chunks)]
      )

     user_content = f"CONTEXT:\n{formatted_context}\n\nUSER QUESTION:\n{query}"

     payload = {
      'model' : settings.CHAT_MODEL_NAME,
        'messages':[
           {'role' : 'system','content': SYSTEM_PROMPT},
           {'role' : 'user' ,'content' : user_content}
        ],
        'stream':False,
        'options':{
           'temperature':0.1
        }
     }

     try:
       with httpx2.Client(timeout=120.0) as client:
          response = client.post(settings.OLLAMA_CHAT_URL,json=payload)

          if response.status_code != 200:
             raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Ollama generation failed: {response.text}'
             )

          result = response.json()
          return result["message"]["content"].strip()

     except httpx2.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Unable to reach Ollama container: {exc}"
            )   