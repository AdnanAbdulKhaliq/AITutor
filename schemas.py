from pydantic import BaseModel, Field
from typing import List, Dict


class LessonIn(BaseModel):
    title: str
    content: str
    grade_level: int


class QuestionAnswer(BaseModel):
    question: str
    answer: str


class QnAList(BaseModel):
    items: List[QuestionAnswer]


class StudentAnswers(BaseModel):
    answers: List[str]  # Should match order of questions


class EvalResult(BaseModel):
    score: int = Field(..., ge=0, le=5)
    feedback: str


class EvalResultList(BaseModel):
    results: List[EvalResult]
