from pydantic import BaseModel,EmailStr,ConfigDict

class UserCreate(BaseModel):
    email:EmailStr
    passwprd:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    is_active:bool

    model_config = ConfigDict(from_attributes=True)

        