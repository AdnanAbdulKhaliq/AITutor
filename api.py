from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from db.models import get_db, get_lesson, get_lessons_by_grade, get_questions
from agent import generate_q

app = FastAPI()


class LessonOut(BaseModel):
    id: str
    title: str
    grade_level: int


class GenerateQuestionsRequest(BaseModel):
    lesson_title: str


class SubmitAnswersRequest(BaseModel):
    lesson_title: str
    answers: Dict[str, str]


class FeedbackRequest(BaseModel):
    lesson_title: str
    qna: Dict[str, str]


@app.get("/lessons", response_model=List[LessonOut])
def list_lessons():
    db = next(get_db())
    lessons = db.query(get_lesson.__annotations__["return"]).all()
    return [
        LessonOut(id=str(l.id), title=l.title, grade_level=l.grade_level)
        for l in lessons
    ]


@app.post(
    "/generate-questions"
)  # TODO: lesson title being used right now, update to use lesson id later.
def generate_questions(req: GenerateQuestionsRequest):
    qna = generate_q(req.lesson_title)
    if "error" in qna:
        raise HTTPException(status_code=404, detail=qna["error"])
    return qna


@app.post("/submit-answers")
def submit_answers(req: SubmitAnswersRequest):
    # For now, just echo back the answers. You can expand this to store in DB.
    return {"received": req.answers}


@app.post("/feedback")
def get_feedback(req: FeedbackRequest):
    from agent import q_eval_chain, q_eval_prompt

    db = next(get_db())
    lesson = get_lesson(db, title=req.lesson_title)
    if not lesson:
        raise HTTPException(
            status_code=404, detail=f"Lesson '{req.lesson_title}' not found."
        )
    response = q_eval_chain.invoke(
        {
            "lesson_title": lesson.title,
            "lesson_content": lesson.content,
            "qna": req.qna,
        }
    )
    return {"feedback": response.content}


# To run: uvicorn api:app --reload
