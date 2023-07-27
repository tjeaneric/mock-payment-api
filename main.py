from fastapi import FastAPI
from database import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from endpoints import user, transaction

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(user.router, prefix="/api/v1")
app.include_router(transaction.router, prefix="/api/v1")



