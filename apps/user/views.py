from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status

from core.utils import get_db
from . import schemas
from . import crud
from .utils import is_password_valid, create_jwt_token, get_jwt_payload, reuseable_oauth

users_router = APIRouter(prefix='/users', tags=['users'])


@users_router.get('/', response_model=list[schemas.UserBase], tags=['users'])
def get_users_view(db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return users


@users_router.post('/', response_model=schemas.UserBase, tags=['users'])
def create_user_view(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered'
        )
    return crud.create_user(db, user)


@users_router.delete('/{user_id}', response_model=schemas.UserDeleteResponse, tags=['users'])
def delete_user_view(user_id: int, db: Session = Depends(get_db)):
    is_deleted = crud.delete_user_by_id(db, user_id)
    detail = {} if is_deleted else {'error': f'User with id {user_id} not find'}
    return schemas.UserDeleteResponse(id=user_id, deleted=is_deleted, detail=detail)


@users_router.post('/login', response_model=schemas.TokenSchema)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    hashed_pass = user.password
    if not is_password_valid(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_jwt_token(user.email, token_type='access'),
        "refresh_token": create_jwt_token(user.email, token_type='refresh'),
    }


@users_router.get('/me', summary='Get details of currently logged in user', response_model=schemas.UserBase)
def get_current_user(token: str = Depends(reuseable_oauth),
                     db: Session = Depends(get_db)):
    try:
        jwt_payload = get_jwt_payload(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = crud.get_user_by_email(db, jwt_payload.sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user
