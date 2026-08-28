from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserResponse,UserLogin,UserCreate,TokenResponse
from app.services.auth_service import register_new_user,authenticate_user
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user_model import User

router = APIRouter()

@router.post('/signup',response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def signup(user_in:UserCreate,db:Session=Depends(get_db)):
    return register_new_user(user_in=user_in,db=db)

@router.post('/login',response_model=TokenResponse)
def login(login_in:UserLogin,db:Session = Depends(get_db)):
    return authenticate_user(login_in=login_in,db=db)

@router.get('/me',response_model=UserResponse)
def get_current_user_profile(currentUser:User = Depends(get_current_user)):
    return currentUser