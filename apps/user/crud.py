from sqlalchemy.orm import Session

from . import models, schemas
from .utils import get_hashed_password


def get_user_by_id(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, user_email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == user_email).first()


def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.login == username).first()


def get_all_users(db: Session) -> list[models.User]:
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_hashed_password(user.password)
    db_user = models.User(email=user.email, password=hashed_password, login=user.login)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.commit()
    return db_user


def delete_user_by_id(db: Session, user_id: int) -> bool:
    db_user = db.get(models.User, {'id': user_id})
    if db_user is None:
        return False
    db.delete(db_user)
    db.commit()
    return True
