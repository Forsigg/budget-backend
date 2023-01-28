import hashlib
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Union, Literal

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from apps.user.schemas import TokenPayload
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY, ALGORITHM, \
    REFRESH_TOKEN_EXPIRE_MINUTES, JWT_REFRESH_SECRET_KEY

load_dotenv('.')

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/users/login",
    scheme_name="JWT"
)


def get_hashed_password(raw_password: str) -> str:
    logging.getLogger().warning(f'HASH SALT: {os.getenv("HASH_SALT")}')
    pass_with_salt = raw_password + os.getenv('HASH_SALT')
    hash_password = hashlib.sha256(pass_with_salt.encode()).hexdigest()
    return hash_password


def is_password_valid(password: str, hashed_password: str) -> bool:
    return get_hashed_password(password) == hashed_password


def create_jwt_token(subject: Union[str, Any],
                     token_type: Union[Literal['access'], Literal['refresh']],
                     expires_delta: int = None) -> str:
    if token_type == 'access':
        expire_constance = ACCESS_TOKEN_EXPIRE_MINUTES
        secret_key_constance = JWT_SECRET_KEY
    elif token_type == 'refresh':
        expire_constance = REFRESH_TOKEN_EXPIRE_MINUTES
        secret_key_constance = JWT_REFRESH_SECRET_KEY
    else:
        raise ValueError(f'token_type must be \'access\' or \'refresh\', not {token_type}')

    exp_minutes = expire_constance if expires_delta is None else expires_delta
    expires_delta = datetime.utcnow() + timedelta(minutes=exp_minutes)
    to_encode = {'exp': expires_delta, 'sub': str(subject)}
    encoded_jwt = jwt.encode(to_encode, secret_key_constance, ALGORITHM)
    return encoded_jwt


def get_jwt_payload(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise ValueError

    except (jwt.JWTError, ValidationError):
        raise
    return token_data
