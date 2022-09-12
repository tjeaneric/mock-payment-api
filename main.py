from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from sqlmodel import Session, select
from database import create_db_and_tables, engine
from middlewares.protect import protect
from models import User, UserCreate, ResponseBase, UserUpdate, TokenBase, Transaction
from utils import get_password_hash, verify_password, create_access_token
from decouple import config
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/users/signup", response_model=ResponseBase, status_code=status.HTTP_201_CREATED, tags=['Authentication'])
def create_user(user: UserCreate):
    if not len(user.phone) == 10:
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number must be 10 digits",
                )
    with Session(engine) as session:
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


@app.post("/users/login", status_code=status.HTTP_200_OK, response_model=TokenBase, tags=['Authentication'])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
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


@app.get("/users/", response_model=List[ResponseBase], status_code=status.HTTP_200_OK, tags=['Users'])
def read_users(current_user: User = Depends(protect)):
    # print(current_user)
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users


@app.get("/users/{user_id}", response_model=ResponseBase, status_code=status.HTTP_200_OK, tags=['Users'])
def read_users(user_id: str):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user


@app.patch("/users/{user_id}", response_model=UserUpdate, status_code=status.HTTP_200_OK, tags=['Users'])
def update_hero(user_id: str, user: UserUpdate):
    with Session(engine) as session:
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


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=['Users'])
def delete_hero(user_id: str):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        session.delete(user)
        session.commit()
        return {"ok": True}


@app.post("/transactions", status_code=status.HTTP_201_CREATED, tags=['Transaction'])
def create_user(transaction: Transaction):
    if not transaction.amount > 0:
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Amount should be greater than 0",
                )
    with Session(engine) as session:
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