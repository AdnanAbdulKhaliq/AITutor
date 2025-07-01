import os
from sqlalchemy import create_engine, Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

# Database connection
from config import database_url

engine = create_engine(database_url)
Base = declarative_base()


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    grade_level = Column(Integer, nullable=False)
    questions = relationship("Question", back_populates="lesson")


class Question(Base):
    __tablename__ = "questions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False)
    question_type = Column(String(20), nullable=False)
    question_text = Column(Text, nullable=False)
    options = Column(JSONB)
    correct_answer = Column(Text)
    lesson = relationship("Lesson", back_populates="questions")


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
