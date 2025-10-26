from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .routers import memories, quizzes, alarms
import os

app = FastAPI(title="Memory Alarm API")

# CORS
origins_env = os.getenv("BACKEND_CORS_ORIGINS")
origins = (origins_env.split(",") if origins_env else ["*"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MVP: 起動時にテーブル作成（本番は Alembic 推奨）
Base.metadata.create_all(bind=engine)

# ルーター
app.include_router(memories.router)
app.include_router(quizzes.router)
app.include_router(alarms.router)

@app.get("/api/health")
def health():
    return {"status": "ok"}
