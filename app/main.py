import os

import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI

from app.core.config import get_settings

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

connection = psycopg2.connect(DATABASE_URL)

settings = get_settings()
app = FastAPI(title=settings.app_name)


@app.get("/health")
def read_root():
    return {"Status": "Api Workinkg!"}
