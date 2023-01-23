import hashlib
import os

from dotenv import load_dotenv

load_dotenv('.')


def get_hashed_password(raw_password: str) -> str:
    pass_with_salt = raw_password + os.getenv('HASH_SALT')
    hash_password = hashlib.sha256(pass_with_salt.encode()).hexdigest()
    return hash_password
