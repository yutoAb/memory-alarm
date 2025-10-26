from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/memories", tags=["memories"])
FAKE_USER_ID = 1  # MVP: ユーザー固定

@router.post("/", response_model=schemas.MemoryOut)
def create_memory(payload: schemas.MemoryCreate, db: Session = Depends(get_db)):
    m = models.MemoryItem(user_id=FAKE_USER_ID, content=payload.content, due_morning=payload.due_morning)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.get("/", response_model=list[schemas.MemoryOut])
def list_memories(db: Session = Depends(get_db)):
    q = db.query(models.MemoryItem).filter(models.MemoryItem.user_id == FAKE_USER_ID).order_by(models.MemoryItem.id.desc())
    return q.all()
