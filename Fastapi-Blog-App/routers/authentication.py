from fastapi import APIRouter, Depends, status, HTTPException
import database, models, token_1
from sqlalchemy.orm import Session
from hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/login",
    tags=["Authentication"],
)

@router.post("/")
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )
    if not Hash.verify(user.password,request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect Password"
        )
    
    access_token = token_1.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
