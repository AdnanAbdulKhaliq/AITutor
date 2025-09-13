#!/usr/bin/env python3
"""
Initialize SQLite database with the same schema as PostgreSQL.
This script creates all the tables and ensures the database is ready to use.
"""

from db.models import Base, engine, SessionLocal, Lesson, Question
import json

def create_tables():
    """Create all tables in the database."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

def add_sample_lesson():
    """Add a sample lesson with questions to test the database."""
    db = SessionLocal()
    try:
        # Check if lesson already exists
        existing_lesson = db.query(Lesson).filter(Lesson.title == "The Best Christmas Present in the World").first()
        if existing_lesson:
            print("Sample lesson already exists, skipping...")
            return

        # Create sample lesson
        lesson = Lesson(
            title="The Best Christmas Present in the World",
            content="This is a story about the power of love and letters during wartime...",
            grade_level=8
        )
        db.add(lesson)
        db.flush()  # Get the ID
        
        # Add sample questions
        questions_data = [
            {
                "question_text": "What is the main theme of the story?",
                "question_type": "short_answer",
                "correct_answer": "The main theme is about love, hope, and the power of human connection during difficult times."
            },
            {
                "question_text": "How does the author convey the importance of letters in the story?",
                "question_type": "essay",
                "correct_answer": "The author shows how letters serve as a bridge between people separated by war, carrying love and hope across time and distance."
            },
            {
                "question_text": "What lesson does the story teach us about Christmas?",
                "question_type": "short_answer",
                "correct_answer": "Christmas is not about material gifts but about love, togetherness, and the precious moments we share with loved ones."
            }
        ]
        
        for q_data in questions_data:
            question = Question(
                lesson_id=lesson.id,
                question_type=q_data["question_type"],
                question_text=q_data["question_text"],
                correct_answer=q_data["correct_answer"],
                options=None
            )
            db.add(question)
        
        db.commit()
        print("✅ Sample lesson and questions added successfully!")
        
    except Exception as e:
        print(f"❌ Error adding sample lesson: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main function to initialize the database."""
    print("🔧 Initializing SQLite database...")
    
    # Create tables
    create_tables()
    
    # Add sample data
    add_sample_lesson()
    
    print("\n🎉 Database initialization complete!")
    print("📍 Database file location: ./tutor.db")
    print("💡 You can now start your FastAPI server with: python -m uvicorn api:app --reload")

if __name__ == "__main__":
    main()
