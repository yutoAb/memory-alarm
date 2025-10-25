# app/main.py
from fastapi import FastAPI
from .db import Base, engine  # Base に 全モデルが import 済みであることが重要
from . import models  # ← これでモデルを登録

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)  # 開発用: 無ければ作る
