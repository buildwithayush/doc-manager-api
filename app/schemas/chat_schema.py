from pydantic import BaseModel ,Field   


class ChatRequest(BaseModel):
    question : str = Field(...,min_length=2,examples=['What is the main topic discussed in the proposal?'])
    document_id: int | None = Field(None, description="Optional: specific document tak search restrict karne ke liye")

class ChatResponse(BaseModel):
    question:str
    answer : str
    retrieved_chunks_count:int
    context_used:list[str]    
