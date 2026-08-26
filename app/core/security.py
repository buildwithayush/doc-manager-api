from pwdlib import PasswordHash
from app.core.config import settings
from datetime import datetime,timedelta,timezone
import jwt

password_hasher =PasswordHash.recommended()

def hash_password(password:str) -> str:
    return password_hasher.hash(password=password)


def verify_password(plain_password:str,hashed_password:str) -> bool:
    return password_hasher.verify(password=plain_password,hash=hashed_password)  

def create_access_token(data:dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    return jwt.encode(payload=to_encode,key=settings.SECRET_KEY,algorithm=settings.ALGORITHM)

