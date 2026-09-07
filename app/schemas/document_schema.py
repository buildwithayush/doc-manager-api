from pydantic import BaseModel,Field,ConfigDict
from datetime import datetime

# Base Schema
class DocumentBase(BaseModel):
    title: str = Field(min_length=1, max_length=255, examples=["Project Proposal"])
    description: str|None = Field(None,examples=['Annual architecture proposal'])

# Create Document
class DocumentUpdate(BaseModel):
    title :str|None = Field(None,min_length=1,max_length=255)
    description:str|None = None

class DocumentResponse(DocumentBase):
    id: int
    user_id: int
    file_name:str
    file_type:str
    file_size:int
    file_path:str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

