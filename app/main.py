import os

import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

connection = psycopg2.connect(DATABASE_URL)

app = FastAPI()


@app.get("/health")
def read_root():
    return {"Status": "Api Workinkg!"}
