import os
import pathlib
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from database import create_db_and_tables
from endpoints import transaction, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
        - Increases the number of threadpool(bigger threadpool)
        - by default the number of threads is 40, here it is increased to 1000
    """
    import anyio
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 1000
    # Create Database tables on Startup
    create_db_and_tables()
    # Create log folder to save log files
    pathlib.Path(f"{os.getcwd()}/logs").mkdir(parents=True, exist_ok=True)
    yield  # Task to be done before shutting down


origins = ["*"]

app = FastAPI(title="Mock Payment API", version="1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(user.router, prefix="/api/v1")
app.include_router(transaction.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
