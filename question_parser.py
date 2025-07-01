from db.models import get_db, add_questions_from_dict

if __name__ == "__main__":
    # --- Example Usage ---
    # This is an example of how to use the function.
    # Make sure you have a lesson with the title specified in `lesson_title_to_test`
    # in your database before running this script.

    chinna_qa = {
        "Why was Chinna upset?": "Chinna was upset because he lost the money his Dadaji had given him to buy the tinkling bells.",
        "How did Kamala help Chinna feel better?": "Kamala consoled Chinna gently, wiped his tears, and promised to give him money to buy the bells.",
        "What did the fruit seller do by mistake?": "The fruit seller gave Chinna ten rupees extra by mistake, while returning the change.",
        "How did Chinna manage to buy the bells from Chacha in the end?": "After honestly returning the extra money to the fruit seller, Chinna’s mother was pleased and took him to Chacha’s shop to buy the bells.",
        "Why do you think Chinna decided to return the money instead of keeping it?": "Chinna remembered how sad he felt when he lost his own money. He realized that keeping the extra money would be like stealing and would make the fruit seller feel the same way. His mother also reminded him to be honest.",
        "Think of a time when you found something that didn’t belong to you. What did you do? How did it make you feel?": "Once, I found a pencil box at school. I gave it to my teacher so she could return it to the right person. It made me feel happy and proud that I did the right thing.",
    }

    lesson_title = "The Tinking Bells"  # Replace with a valid lesson title from your DB

    db_session = next(get_db())
    try:
        add_questions_from_dict(db_session, chinna_qa, lesson_title)
    finally:
        db_session.close()
