from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.database_echo #Logi SQL w trybie debug
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    """Bazowa klasa dla wszystkich modeli."""
    pass

def get_db():
    """Dependency dla FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
