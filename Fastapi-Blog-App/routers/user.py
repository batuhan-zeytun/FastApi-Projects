from fastapi import APIRouter, Depends, status
import schemas
from sqlalchemy.orm import Session
from database import get_db
from repository import user

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post("/", response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create(request: schemas.User, db: Session = Depends(get_db)):
    return user.create_user(request, db)


@router.get("/{id}", response_model=schemas.ShowUser)
def read(id: int, db: Session = Depends(get_db)):
    return user.get_user(id, db)
