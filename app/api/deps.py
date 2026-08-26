from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError

from app.database import get_db
from app.models.user_model import User
from app.core.security import settings

security_scheme = HTTPBearer()

def get_current_user(
        credentials:HTTPAuthorizationCredentials=Depends(security_scheme),
        db:Session=Depends(get_db)
) -> User:
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate' :'Bearer'}
    )

    try:
      payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
      user_id: str | None = payload.get("sub")
      if user_id is None:
         raise credentials_exception
      
    except InvalidTokenError:
       raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.is_active:
       raise credentials_exception

    return user
      
    