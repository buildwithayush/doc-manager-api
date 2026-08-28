from fastapi import status,HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password,verify_password,create_access_token
from app.models.user_model import User
from app.schemas.user_schema import UserCreate,UserLogin,TokenResponse

def register_new_user(
        user_in: UserCreate,
        db: Session
) -> User:
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email is already registered.'
        )

    new_user = User(
        email = user_in.email,
        hashed_password = hash_password(password=user_in.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
   
def authenticate_user(db:Session,login_in:UserLogin) -> TokenResponse:
    user = db.query(User).filter(User.email == login_in.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password'
        )

    if not verify_password(login_in.password,user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password'
        )
    access_token = create_access_token(data={'sub' : str(user.id)})
    return TokenResponse(access_token=access_token)

