from langchain_text_splitters import MarkdownHeaderTextSplitter

class MarkdownChunkService:
    
    HEADERS_TO_SPLIT_ON = [
        ("#", "Header_1"),
        ("##", "Header_2"),
        ("###", "Header_3"),
    ]

    @classmethod
    def split_by_headers(cls, markdown_text: str):
        if not markdown_text or not markdown_text.strip():
            return []

        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=cls.HEADERS_TO_SPLIT_ON,
            strip_headers=False  
        )

        return splitter.split_text(markdown_text)