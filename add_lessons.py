import uuid
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.models import Base, engine, SessionLocal, Lesson, Question

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# The Q&A data you provided
qna_data = {
    "What kind of condition was the roll-top desk in when the author found it?  Describe its appearance.": "The desk was in poor condition; the roll-top was broken into pieces, one leg was poorly repaired, and there were scorch marks down one side.  It showed signs of both fire and water damage, indicating it had been neglected or poorly cared for.",
    "Why did the author think it was wrong to open the secret drawer, but do it anyway? Explain his reasoning.": "The author knew it was wrong because the note on the tin box indicated the contents were meant to be buried with the owner. However, his curiosity overcame his scruples, a common human tendency to prioritize immediate satisfaction over ethical considerations.",
    "What did Jim and Hans do together in No Man's Land on Christmas Day? Describe their activities.": "Jim and Hans, along with other soldiers, engaged in an impromptu truce. They shared food and drinks (schnapps, sausage, rum, Christmas cake), talked about their lives and families, and even played a football match, symbolizing a temporary peace amidst the war.",
    "How did the author find Mrs. Macpherson? Describe the steps he took to locate her.": "After discovering Jim's letter, the author went to Bridport and inquired about Mrs. Macpherson's whereabouts.  He learned her house had burned down, and she was residing at Burlington House Nursing Home, where he eventually found her.",
    "What was Mrs. Macpherson's reaction when the author gave her the tin box? Describe her emotional state.": "Initially, Mrs. Macpherson seemed confused and vacant. However, upon recognizing the tin box, her eyes lit up, and her face radiated happiness.  She became emotional, expressing overwhelming joy at seeing the author, whom she believed to be her deceased son, Jim, returned home.",
}

lesson_content = """
"The Best Christmas Present in the World" tells the story of an author who discovers a roll-top desk in poor condition. Despite its damaged state - with a broken roll-top, poorly repaired leg, and scorch marks - he decides to restore it. While working on the desk, he discovers a secret drawer containing a tin box with a letter from Jim Macpherson to his wife Connie.

The letter, dated December 26, 1914, describes an extraordinary Christmas Day during World War I when British and German soldiers in the trenches declared an unofficial truce. Jim writes about how he and a German soldier named Hans met in No Man's Land, where soldiers from both sides shared food, drinks, and even played football together. This magical moment of peace amid the horrors of war deeply moved both sides.

The author, feeling it was wrong but driven by curiosity, decides to find Mrs. Macpherson and return the letter. He tracks her down to Burlington House Nursing Home in Bridport, where he finds her living after her house burned down. When he presents her with the tin box, Mrs. Macpherson's eyes light up with joy, and in her confusion, she mistakes the author for her beloved husband Jim returning home for Christmas.

This touching story explores themes of love, war, hope, and the enduring power of human connection across time and conflict.
"""

db = SessionLocal()

try:
    # Check if lesson already exists
    existing = (
        db.query(Lesson)
        .filter(Lesson.title == "The Best Christmas Present in the World")
        .first()
    )

    if existing:
        print("Lesson already exists! Skipping...")
    else:
        # Create lesson
        lesson = Lesson(
            title="The Best Christmas Present in the World",
            content=lesson_content.strip(),
            grade_level=4,
        )

        db.add(lesson)
        db.flush()  # This ensures lesson.id is available
        print(f"Added lesson: {lesson.title}")

        # Add questions
        for question_text, answer in qna_data.items():
            question = Question(
                lesson_id=lesson.id,
                question_type="short_answer",
                question_text=question_text,
                correct_answer=answer,
            )
            db.add(question)

        db.commit()
        print(f"Added {len(qna_data)} questions")
        print("Done!")

except Exception as e:
    db.rollback()
    print(f"Error: {e}")
finally:
    db.close()
