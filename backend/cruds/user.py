from sqlalchemy.orm import Session
from sqlalchemy import select

from models.user import User
from schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: int) -> User | None:
    """Pobierz usera po ID."""
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> User | None:
    """Pobierz usera po email."""
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_username(db: Session, username: str) -> User | None:
    """Pobierz usera po username."""
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalar_one_or_none()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Pobierz listę userów."""
    stmt = select(User).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def create_user(db: Session, user: UserCreate, hashed_password: str) -> User:
    """Stwórz nowego usera."""
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        date_of_birth=user.date_of_birth,
        gender=user.gender,
        height=user.height,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: User, user_update: UserUpdate) -> User:
    """Aktualizuj usera."""
    update_data = user_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: User) -> None:
    """Usuń usera."""
    db.delete(db_user)
    db.commit()