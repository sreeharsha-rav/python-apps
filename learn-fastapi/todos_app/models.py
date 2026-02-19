from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from passlib.context import CryptContext
from todos_app.database import Base


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    _password_hash = Column(String)
    is_active = Column(Boolean, default=True)

    @hybrid_property
    def password(self):
        raise ValueError("Password is hashed; use verify_password() instead.")

    @password.setter
    def password(self, password: str) -> None:
        if password:
            self._password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self._password_hash)

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer, default=1)
    completed = Column(Boolean, default=False)
    owner = Column(Integer, ForeignKey("users.id"))
