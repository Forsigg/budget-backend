from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.utils import get_db
from . import schemas
from . import crud


users_router = APIRouter(prefix='/users', tags=['users'])


@users_router.get('/', response_model=list[schemas.UserBase], tags=['users'])
def get_users_view(db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return users


@users_router.post('/', response_model=schemas.UserBase, tags=['users'])
def create_user_view(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return crud.create_user(db, user)


@users_router.delete('/{user_id}', response_model=schemas.UserDeleteResponse, tags=['users'])
def delete_user_view(user_id: int, db: Session = Depends(get_db)):
    is_deleted = crud.delete_user_by_id(db, user_id)
    detail = {} if is_deleted else {'error': f'User with id {user_id} not find'}
    return schemas.UserDeleteResponse(id=user_id, deleted=is_deleted, detail=detail)
