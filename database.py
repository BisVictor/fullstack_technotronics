from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./batteries.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

#Создаём фабрику сессий
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

#Родитель для всех моделей
Base = declarative_base()