import re

class ChunkService:
    @staticmethod

    def clean_and_normalize_text(text:str) ->str:
        if not text:
            return ''

        text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)

        text = text.replace('\r', ' ').replace('\t', ' ')

        text =re.sub(r'\s+', ' ', text)

        return text.strip()

    @classmethod
    def chunk_text(cls,text:str,chunk_size:int = 1000, chunk_overlap:int = 200) -> list[str]:
       cleaned_text = cls.clean_and_normalize_text(text)

       if not cleaned_text:
           return []

       if len(cleaned_text) <= chunk_size:
           return [cleaned_text]

       step = chunk_size - chunk_overlap
       if step <= 0:
           raise ValueError("The Chunk size must be greater than the chunk overlap.")

       chunks: list[str] = []
       total_length = len(cleaned_text)

       start = 0
       while start < total_length:
           end = min(start + chunk_size, total_length)
           chunk = cleaned_text[start:end]
           chunks.append(chunk)
           start += step

       return chunks