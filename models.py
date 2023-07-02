from sqlmodel import SQLModel, Field


# Базовая модель
class QuestionBase(SQLModel):
    answer: str
    question: str
    created_at: str


# Табличная модель
class Question(QuestionBase, table=True):
    id: int = Field(default=None, primary_key=True)


# Модель pydantic
class QuestionCreate(QuestionBase):
    pass
