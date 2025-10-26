from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timezone
from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/alarms", tags=["alarms"])
FAKE_USER_ID = 1

@router.post("/", response_model=schemas.AlarmOut)
def create_alarm(payload: schemas.AlarmCreate, db: Session = Depends(get_db)):
    a = models.Alarm(user_id=FAKE_USER_ID, fire_at=payload.fire_at, label=payload.label)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

@router.get("/next", response_model=list[schemas.AlarmOut])
def due_alarms(now: datetime | None = None, db: Session = Depends(get_db)):
    now = now or datetime.now(timezone.utc)
    stmt = (
        select(models.Alarm)
        .where(models.Alarm.user_id == FAKE_USER_ID)
        .where(models.Alarm.active.is_(True))
        .where(models.Alarm.fire_at <= now)
        .order_by(models.Alarm.id.asc())
    )
    return db.execute(stmt).scalars().all()
