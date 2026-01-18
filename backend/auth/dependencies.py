from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth.jwt import verify_token
from database import get_db
from models.user import User

# OAuth2PasswordBearer - mówi FastAPI:
# "Token będzie w headerze Authorization: Bearer <token>"
# tokenUrl - endpoint do logowania (dla dokumentacji Swagger)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),  # FastAPI wyciąga token z headera
    db: Session = Depends(get_db)          # FastAPI daje sesję bazy
) -> User:

    # Błąd do zwrócenia gdy autoryzacja się nie powiedzie
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},  # Standard OAuth2
    )
    
    # 1. Weryfikuj token
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    # 2. Wyciągnij user_id z payloadu
    # "sub" (subject) - standardowa nazwa dla ID użytkownika w JWT
    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # 3. Pobierz usera z bazy
    user = db.get(User, int(user_id))
    if user is None:
        raise credentials_exception
    
    return user