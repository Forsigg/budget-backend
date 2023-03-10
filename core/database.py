import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv('.env')
logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = f"postgresql://" \
                          f"{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}" \
                          f"@db/{os.getenv('POSTGRES_DB')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
