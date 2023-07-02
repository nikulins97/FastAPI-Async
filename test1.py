from fastapi import FastAPI, Depends
from sqlalchemy import select
from db import *
from models import Question, QuestionCreate


app = FastAPI()


# Создание таблицы при первом запуске приложения
@app.on_event("startup")
async def on_startup():
    await init_db()


# Проверка работы приложение
@app.get("/")
async def root():
    return {"Проверка": "Приложение работает"}


# GET-метод, возвращает список вопросов из БД
@app.get("/question_list", response_model=list[Question])
async def get_question_list(sess: AsyncSession = Depends(get_session)):
    result = await sess.execute(select(Question))
    questions = result.scalars().all()
    return [Question(id=q.id, answer=q.answer, question=q.question, created_at=q.created_at) for q in questions]


# POST-метод, добавляет новую запись в БД
@app.post("/add_question")
async def add_question(q: QuestionCreate, sess: AsyncSession = Depends(get_session)):
    q = Question(answer=q.answer, question=q.question, created_at=q.created_at)
    sess.add(q)
    await sess.commit()
    await sess.refresh(q)
    return q


# DELETE-метод, удаляет из БД запись с соответствующим id
@app.delete("/delete/{id}", response_model=list[Question])
async def delete_question(id: int, sess: AsyncSession = Depends(get_session)):
    row = await sess.execute(select(Question).where(Question.id == id))
    row = row.scalar()
    await sess.delete(row)
    await sess.commit()


# PUT-метод, обновляет запись из БД с соответствующим id
@app.put("/update/{id}", response_model=list[Question])
async def update(id: int, q: Question, sess: AsyncSession = Depends(get_session)):
    res = await sess.execute(select(Question).filter_by(id=id))
    res = res.scalar_one()
    res.answer = q.answer
    res.question = q.question
    res.created_at = q.created_at
    updated = await sess.execute(
        select(Question.answer, Question.question, Question.created_at).where(Question.id == id)
    )
    updated = updated.scalar_one()
    await sess.commit()
