"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""

# import os
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import (
    relationship,
    declarative_base,
    sessionmaker,
)


# PG_CONN_URI = os.environ.get("SQLALCHEMY_PG_CONN_URI")

PG_CONN_URI = "postgresql+asyncpg://postgres:password@localhost/postgres"  #  "postgresql+asyncpg://postgres:secretpassword@localhost:5432/postgres"

engine = create_async_engine(PG_CONN_URI, echo=True)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False )


# ---- Для теста на локальном PG ----------
# conn = psycopg2.connect("dbname = db user=postgres password=16c808 port=5432 host=localhost")
# PG_CONN_URI = "postgresql+asyncpg://postgres:16c808@localhost/db"
# engine = create_async_engine(PG_CONN_URI, echo=True)
# Base = declarative_base()
# async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
# ------------------------------------------

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    city = Column(String(100))
    phone = Column(String(100), unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.now())

    __mapper_args__ = {"eager_defaults": True}

    post = relationship("Post", back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__} (id={self.id}, username={self.username}, name={self.name}," \
               f" email={self.email}, city={self.city}, phone={self.phone})"

    def __repr__(self):
        return str(self)


class Post(Base):
    __tablename__ = "posts"
    userId = Column(Integer, ForeignKey(User.id), nullable=False)
    id = Column(Integer, primary_key=True)
    title = Column(String(1000), nullable=False, default="", server_default="")
    body = Column(String(5000), nullable=False, default="", server_default="")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.now())

    __mapper_args__ = {"eager_defaults": True}

    user = relationship(User, back_populates="post")

    def __str__(self):
        return f"{self.__class__.__name__} (id={self.id}, user_id={self.user_id}, title={self.title}, body={self.body}"

    def __repr__(self):
        return str(self)
