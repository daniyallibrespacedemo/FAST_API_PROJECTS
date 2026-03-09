from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.user_schema import UserCreate, UserLogin
from app.models.user import User
from app.services.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix='/auth')

@router.post('/register')
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(user.email == User.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists!"
        )
    
    hashed_password = hash_password(user.password)

    new_user = User(
        email = user.email,
        password = hashed_password
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message":"User Created"}

@router.post('/login')
def login(user:UserLogin, db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect Password detected"
        )
    
    token = create_access_token({"user_id":db_user.id})
    return token