import uuid
from db.models import (
    get_db,
    get_lesson,
    get_lessons_by_grade,
    get_questions,
    get_questions_by_type,
    Lesson,
    Question,
)


def main():
    """
    This function demonstrates how to use the CRUD functions in db/models.py.
    """
    db_session = next(get_db())

    # Note: For this example to run, you would need to have data in your database.
    # You can create some sample data like this:
    #
    # lesson1 = Lesson(title="The Solar System", content="...", grade_level=4)
    # question1 = Question(lesson_id=lesson1.id, question_type="multiple_choice", question_text="Which is the largest planet?", options={"A": "Earth", "B": "Jupiter"}, correct_answer="B")
    # db_session.add(lesson1)
    # db_session.add(question1)
    # db_session.commit()

    # --- Get a lesson by title ---
    print("--- Getting a lesson by title ---")
    lesson_title = "The Solar System"  # Replace with a title from your DB
    lesson = get_lesson(db=db_session, title=lesson_title)
    if lesson:
        print(f"Found lesson: {lesson.title}")
        lesson_id_for_later = lesson.id
    else:
        print(f"Lesson with title '{lesson_title}' not found.")
        # In a real app, you might exit or use a default
        lesson_id_for_later = uuid.uuid4()  # dummy uuid

    # --- Get a lesson by ID ---
    print("\n--- Getting a lesson by ID ---")
    lesson = get_lesson(db=db_session, lesson_id=lesson_id_for_later)
    if lesson:
        print(f"Found lesson with ID {lesson.id}: {lesson.title}")
    else:
        print(f"Lesson with ID {lesson_id_for_later} not found.")

    # --- Get lessons by grade level ---
    print("\n--- Getting lessons for grade 4 ---")
    grade_4_lessons = get_lessons_by_grade(db=db_session, grade_level=4)
    if grade_4_lessons:
        for l in grade_4_lessons:
            print(f"- {l.title}")
    else:
        print("No lessons found for grade 4.")

    # --- Get all questions for a lesson ---
    print(f"\n--- Getting all questions for lesson ID {lesson_id_for_later} ---")
    all_questions = get_questions(db=db_session, lesson_id=lesson_id_for_later)
    if all_questions:
        for q in all_questions:
            print(f"- Type: {q.question_type}, Text: {q.question_text}")
    else:
        print("No questions found for this lesson.")

    # --- Get multiple choice questions for a lesson ---
    print(
        f"\n--- Getting 'multiple_choice' questions for lesson ID {lesson_id_for_later} ---"
    )
    mc_questions = get_questions_by_type(
        db=db_session, lesson_id=lesson_id_for_later, question_type="multiple_choice"
    )
    if mc_questions:
        for q in mc_questions:
            print(f"- {q.question_text}")
    else:
        print("No multiple choice questions found for this lesson.")


if __name__ == "__main__":
    main()
