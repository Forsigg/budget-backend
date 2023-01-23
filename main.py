from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from apps.user import schemas, crud
from core.database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/users/', response_model=list[schemas.UserBase])
def get_users_view(db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return users


@app.post('/users/', response_model=schemas.UserBase)
def create_user_view(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return crud.create_user(db, user)
