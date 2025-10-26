from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

# 共通: ORMからの変換を有効化
class OrmBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

# Memories
class MemoryCreate(BaseModel):
    content: str
    due_morning: datetime  # UTC想定（クライアントでローカル→ISO->UTC変換）

class MemoryOut(OrmBase):
    id: int
    content: str
    due_morning: datetime

# Quizzes
class QuizCreate(BaseModel):
    question: str
    answer: str
    due_morning: datetime

class QuizOut(OrmBase):
    id: int
    question: str
    due_morning: datetime

class AnswerIn(BaseModel):
    quiz_id: int
    answer: str

# Alarms
class AlarmCreate(BaseModel):
    fire_at: datetime
    label: str = Field(default="morning")

class AlarmOut(OrmBase):
    id: int
    fire_at: datetime
    label: str
    active: bool
