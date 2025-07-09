from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Depends
from database import get_db

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def read(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )
    return blog

def destroy(id: int, db: Session = Depends(get_db)):
    if not db.query(models.Blog).filter(models.Blog.id == id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {"message": "Blog deleted successfully"}

def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    if not db.query(models.Blog).filter(models.Blog.id == id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    db.query(models.Blog).filter(models.Blog.id == id).update(
    request.model_dump(),
    synchronize_session=False
)

    db.commit()
    return db.query(models.Blog).filter(models.Blog.id == id).first()
