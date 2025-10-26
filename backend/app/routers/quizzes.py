from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timezone
from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/quizzes", tags=["quizzes"])
FAKE_USER_ID = 1

@router.post("/", response_model=schemas.QuizOut)
def create_quiz(payload: schemas.QuizCreate, db: Session = Depends(get_db)):
    q = models.QuizCard(
        user_id=FAKE_USER_ID,
        question=payload.question,
        answer=payload.answer,
        due_morning=payload.due_morning
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return q

@router.get("/due", response_model=list[schemas.QuizOut])
def due_quizzes(now: datetime | None = None, db: Session = Depends(get_db)):
    now = now or datetime.now(timezone.utc)
    stmt = (
        select(models.QuizCard)
        .where(models.QuizCard.user_id == FAKE_USER_ID)
        .where(models.QuizCard.due_morning <= now)
        .order_by(models.QuizCard.id.asc())
    )
    return db.execute(stmt).scalars().all()

@router.post("/answer")
def answer_quiz(payload: schemas.AnswerIn, db: Session = Depends(get_db)):
    q = db.get(models.QuizCard, payload.quiz_id)
    if not q:
        return {"ok": False, "reason": "not_found"}

    # シンプルな正解判定（前後空白/大小のみ）
    def norm(s: str) -> str:
        return (s or "").strip().lower()

    ok = norm(payload.answer) == norm(q.answer)
    if ok:
        # 正解: 当日分を削除（または次回スケジュール更新など）
        db.delete(q)
        db.commit()
    return {"ok": ok}
