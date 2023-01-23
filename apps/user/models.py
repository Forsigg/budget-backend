from sqlalchemy import Column, Integer, String

from core.database import Base


class User(Base):
    __tablename__ = 'budget_user'

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(40))
    email = Column(String(50))
    password = Column(String(100))

    def __repr__(self):
        return f'User {self.login}, ID: {self.id}, email: {self.email}'
