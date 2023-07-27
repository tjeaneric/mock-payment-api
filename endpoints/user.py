from datetime import timedelta

from fastapi import  APIRouter, Depends, status, HTTPException
from sqlmodel import select

from fastapi.security import OAuth2PasswordRequestForm

from config import settings
from database import sessionDep
from middlewares.protect import protect
from models import ResponseBase, UserCreate, User, UserUpdate, TokenBase
from utils import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["Authentication"], dependencies=[Depends(protect)])


ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


@router.post("/users/signup", status_code=status.HTTP_201_CREATED)
def create_user(session:sessionDep,user: UserCreate)->ResponseBase:
    if not len(user.phone) == 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number must be 10 digits",
        )
    statement = select(User).where(User.phone == user.phone)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already used",
        )
    user.password = get_password_hash(user.password)
    user_created = User.from_orm(user)
    session.add(user_created)
    session.commit()
    session.refresh(user_created)
    return user_created



@router.post("/users/login", status_code=status.HTTP_200_OK)
def login(session:sessionDep,form_data: OAuth2PasswordRequestForm = Depends())->TokenBase:
    statement = select(User).where(User.phone == form_data.username)
    results = session.exec(statement).first()
    if not results:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect phone or password"
        )
    hashed_pass = results.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(results.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "data": results}


@router.get("/users/", status_code=status.HTTP_200_OK)
def read_users(session: sessionDep,current_user: User = Depends(protect))->list[ResponseBase]:
        users = session.exec(select(User)).all()
        return users


@router.get("/users/{user_id}", response_model=ResponseBase, status_code=status.HTTP_200_OK)
def read_users(session: sessionDep,user_id: str):
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user


@router.patch("/users/{user_id}", status_code=status.HTTP_200_OK)
def update_hero(session:sessionDep,user_id: str, user: UserUpdate)->UserUpdate:
        db_user = session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hero(session: sessionDep,user_id: str):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
