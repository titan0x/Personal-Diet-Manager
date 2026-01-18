from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.jwt import create_access_token
from database import get_db
from schemas.auth import Token
from cruds import user as user_crud
from utils import verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    # OAuth2PasswordRequestForm - standardowy formularz logowania
    # Wymaga pól: username, password (wysyłane jako form-data, nie JSON!)
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Logowanie użytkownika.
    
    Flow:
        1. Przyjmij email (jako username) i password
        2. Znajdź usera w bazie po emailu
        3. Sprawdź czy hasło się zgadza
        4. Stwórz token JWT
        5. Zwróć token
    
    Request (form-data, NIE json!):
        username: jan@example.com
        password: Haslo123
    
    Response:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIs...",
            "token_type": "bearer"
        }
    """
    
    # 1. Znajdź usera po emailu
    # (OAuth2 używa "username", ale my logujemy po emailu)
    user = user_crud.get_user_by_email(db, form_data.username)
    
    # 2. Sprawdź czy user istnieje
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Sprawdź hasło
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 4. Stwórz token
    # "sub" (subject) - standardowa nazwa dla ID użytkownika w JWT
    access_token = create_access_token(data={"sub": str(user.id)})
    
    # 5. Zwróć token
    return Token(access_token=access_token, token_type="bearer")