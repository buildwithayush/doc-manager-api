from langchain_text_splitters import RecursiveCharacterTextSplitter
class LangChainChunkService:
    @staticmethod

    def chunk__by_characters(
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> list[str]:

        if not text or not text.strip():
            return[]

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
            keep_separator=True 
        )

        return splitter.split_text(text)

    @staticmethod
    def chunk_by_tokens(
        text: str,
        max_tokens: int = 300,
        token_overlap: int = 50
    ) -> list[str]:
      
        if not text or not text.strip():
            return []

        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            encoding_name="cl100k_base",
            chunk_size=max_tokens,
            chunk_overlap=token_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

        return splitter.split_text(text)