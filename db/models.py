import os
import uuid
from typing import Generator, List, Optional, Dict

from sqlalchemy import create_engine, Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Session

from config import database_url

# Create the SQLAlchemy engine with SQLite-specific settings
engine = create_engine(database_url, echo=False, connect_args={"check_same_thread": False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    grade_level = Column(Integer, nullable=False)

    questions = relationship("Question", back_populates="lesson")


class Question(Base):
    __tablename__ = "questions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lesson_id = Column(String(36), ForeignKey("lessons.id"), nullable=False)
    question_type = Column(String(20), nullable=False)
    question_text = Column(Text, nullable=False)
    options = Column(Text)  # JSON stored as text for SQLite
    correct_answer = Column(Text)

    lesson = relationship("Lesson", back_populates="questions")


def get_db() -> Generator[Session, None, None]:
    """Generator function to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_lesson(
    db: Session, lesson_id: str = None, title: str = None
) -> Optional[Lesson]:
    """
    Get a single lesson by its ID or title.
    """
    if lesson_id:
        return db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if title:
        return db.query(Lesson).filter(Lesson.title == title).first()
    return None


def get_lessons_by_grade(db: Session, grade_level: int) -> List[Lesson]:
    """
    Get a list of lessons for a specific grade level.
    """
    return db.query(Lesson).filter(Lesson.grade_level == grade_level).all()


def get_questions(db: Session, lesson_id: str) -> List[Question]:
    """
    Get all questions for a specific lesson.
    """
    return db.query(Question).filter(Question.lesson_id == lesson_id).all()


def get_questions_by_type(
    db: Session, lesson_id: str, question_type: str
) -> List[Question]:
    """
    Get questions of a specific type for a specific lesson.
    """
    return (
        db.query(Question)
        .filter(
            Question.lesson_id == lesson_id, Question.question_type == question_type
        )
        .all()
    )


def add_questions_from_dict(db: Session, qna_dict: Dict[str, str], lesson_title: str):
    """
    Parses a dictionary of questions and answers and adds them to the Question table.

    Args:
        db: The database session.
        qna_dict: A dictionary where keys are questions and values are answers.
        lesson_title: The title of the lesson to associate these questions with.
    """
    lesson = get_lesson(db, title=lesson_title)
    if not lesson:
        print(f"Error: Lesson with title '{lesson_title}' not found.")
        return

    for question_text, correct_answer in qna_dict.items():
        new_question = Question(
            lesson_id=lesson.id,
            question_type="short_answer",
            question_text=question_text,
            correct_answer=correct_answer,
            options=None,  # No options for short_answer questions
        )
        db.add(new_question)
        print(f"Staging question for addition: {question_text}")

    db.commit()
    print(
        f"\nSuccessfully added {len(qna_dict)} questions for lesson '{lesson_title}' to the database."
    )
