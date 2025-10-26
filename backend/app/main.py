# app/main.py
from fastapi import FastAPI
from .db import Base, engine  # Base に 全モデルが import 済みであることが重要
from . import models  # ← これでモデルを登録

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)  # 開発用: 無ければ作る

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id" : item_id, "q": q}