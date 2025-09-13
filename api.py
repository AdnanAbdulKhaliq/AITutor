from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import asyncio
from concurrent.futures import ThreadPoolExecutor
from db.models import get_db, get_lesson, get_lessons_by_grade, get_questions, Lesson
from agent import generate_q

app = FastAPI()

# Create thread pool for CPU-bound tasks
executor = ThreadPoolExecutor(max_workers=4)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
async def list_lessons():
    db = next(get_db())
    lessons = db.query(Lesson).all()
    return [
        LessonOut(id=str(l.id), title=l.title, grade_level=l.grade_level)
        for l in lessons
    ]


@app.post(
    "/generate-questions"
)  # TODO: lesson title being used right now, update to use lesson id later.
async def generate_questions(req: GenerateQuestionsRequest):
    # Run the AI operation in a thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    qna_list = await loop.run_in_executor(executor, generate_q, req.lesson_title)

    if not qna_list.items:
        raise HTTPException(
            status_code=404, detail="No questions could be generated for this lesson"
        )

    # Convert QnAList to dictionary format
    qna_dict = {item.question: item.answer for item in qna_list.items}
    return qna_dict


@app.post("/submit-answers")
async def submit_answers(req: SubmitAnswersRequest):
    # For now, just echo back the answers. You can expand this to store in DB.
    return {"received": req.answers}


@app.post("/feedback")
async def get_feedback(req: FeedbackRequest):
    from agent import q_eval_chain
    import json

    db = next(get_db())
    lesson = get_lesson(db, title=req.lesson_title)
    if not lesson:
        raise HTTPException(
            status_code=404, detail=f"Lesson '{req.lesson_title}' not found."
        )

    # Format QnA for the prompt
    qna_string = "\n".join([f"Q: {q}\nA: {a}" for q, a in req.qna.items()])
    student_answers_string = "\n".join(
        [f"Q: {q}\nStudent Answer: {a}" for q, a in req.qna.items()]
    )

    # Run the AI evaluation in a thread pool to avoid blocking
    loop = asyncio.get_event_loop()

    def run_evaluation():
        return q_eval_chain.invoke(
            {
                "qna": qna_string,
                "student_answers": student_answers_string,
            }
        )

    response = await loop.run_in_executor(executor, run_evaluation)

    try:
        # Try to parse the JSON response from the LLM
        cleaned_output = (
            response.content.strip().lstrip("```json").rstrip("```").strip()
        )
        feedback_data = json.loads(cleaned_output)

        # Transform the feedback to match frontend format
        if isinstance(feedback_data, list):
            # If it's already a list of feedback items
            questions_list = list(req.qna.keys())
            formatted_feedback = []

            for i, item in enumerate(feedback_data):
                formatted_feedback.append(
                    {
                        "questionId": i + 1,
                        "question": (
                            questions_list[i]
                            if i < len(questions_list)
                            else f"Question {i + 1}"
                        ),
                        "answer": (
                            list(req.qna.values())[i]
                            if i < len(req.qna)
                            else "No answer provided"
                        ),
                        "feedback": item.get("feedback", "No feedback available"),
                        "score": item.get("score", 0)
                        * 20,  # Convert 0-5 scale to 0-100
                    }
                )

            # Calculate overall score
            total_score = sum(item.get("score", 0) for item in feedback_data)
            overall_score = (
                (total_score / len(feedback_data)) * 20 if feedback_data else 0
            )

            return {"feedback": formatted_feedback, "score": round(overall_score)}
        else:
            # Fallback if not a list
            raise ValueError("Expected list format")

    except (json.JSONDecodeError, ValueError) as e:
        # Fallback to simple feedback if JSON parsing fails
        questions_list = list(req.qna.keys())
        fallback_feedback = []

        for i, (question, answer) in enumerate(req.qna.items()):
            fallback_feedback.append(
                {
                    "questionId": i + 1,
                    "question": question,
                    "answer": answer,
                    "feedback": "Thank you for your response. Your tutor will review this and provide detailed feedback.",
                    "score": 70,
                }
            )

        return {"feedback": fallback_feedback, "score": 70}


@app.get("/lessons/{lesson_id}/questions")
async def get_lesson_questions(lesson_id: str):
    """Get all questions for a specific lesson"""
    db = next(get_db())
    try:
        # First check if lesson exists
        lesson = get_lesson(db, lesson_id=lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        
        # Get questions for this lesson
        questions = get_questions(db, lesson_id=lesson_id)
        
        # Format questions for frontend
        formatted_questions = []
        for i, q in enumerate(questions):
            formatted_questions.append({
                "id": i + 1,  # Sequential ID for frontend
                "question": q.question_text,
                "type": "short" if q.question_type == "short_answer" else "essay"
            })
        
        return {
            "lesson": {
                "id": str(lesson.id),
                "title": lesson.title,
                "grade_level": lesson.grade_level
            },
            "questions": formatted_questions
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching questions: {str(e)}")
    finally:
        db.close()


@app.get("/lessons/{lesson_id}")
async def get_lesson_details(lesson_id: str):
    """Get lesson details by ID"""
    db = next(get_db())
    try:
        lesson = get_lesson(db, lesson_id=lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        
        return {
            "id": str(lesson.id),
            "title": lesson.title,
            "content": lesson.content,
            "grade_level": lesson.grade_level
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching lesson: {str(e)}")
    finally:
        db.close()


# To run: uvicorn api:app --reload


@app.post("/create-test-lesson")
async def create_test_lesson():
    """Create a test lesson for development purposes"""
    from db.models import Lesson, Question, SessionLocal
    import uuid

    db = SessionLocal()
    try:
        # Create a test lesson
        lesson_id = str(uuid.uuid4())
        lesson = Lesson(
            id=lesson_id,
            title="Introduction to Shakespeare",
            content="""William Shakespeare (1564-1616) was an English playwright, poet, and actor widely regarded as the greatest writer in the English language. Born in Stratford-upon-Avon, Shakespeare wrote approximately 37 plays and 154 sonnets during his career.

His works are divided into three main categories: comedies (such as "A Midsummer Night's Dream" and "Much Ado About Nothing"), tragedies (including "Hamlet," "Macbeth," and "Romeo and Juliet"), and histories (like "Henry V" and "Richard III").

Shakespeare's writing is renowned for its complex characters, intricate plots, and beautiful language. He invented many words and phrases that are still used today, such as "break the ice," "heart of gold," and "wild goose chase." His influence on literature, theater, and the English language continues to this day.""",
            grade_level=4,
        )

        # Check if lesson already exists
        existing = (
            db.query(Lesson)
            .filter(Lesson.title == "Introduction to Shakespeare")
            .first()
        )
        if not existing:
            db.add(lesson)
            db.commit()

            # Add some sample questions
            questions = [
                Question(
                    id=str(uuid.uuid4()),
                    lesson_id=lesson.id,
                    question_type="short_answer",
                    question_text="When was William Shakespeare born?",
                    correct_answer="William Shakespeare was born in 1564 in Stratford-upon-Avon, England.",
                ),
                Question(
                    id=str(uuid.uuid4()),
                    lesson_id=lesson.id,
                    question_type="short_answer",
                    question_text="What are the three main categories of Shakespeare's works?",
                    correct_answer="Shakespeare's works are divided into comedies, tragedies, and histories.",
                ),
            ]

            for q in questions:
                db.add(q)

            db.commit()
            return {
                "message": "Test lesson created successfully",
                "lesson_id": lesson.id,
            }
        else:
            return {"message": "Test lesson already exists", "lesson_id": existing.id}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error creating test lesson: {str(e)}"
        )
    finally:
        db.close()
