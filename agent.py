from langchain.prompts import PromptTemplate
from llm import llm
from db.models import get_db, get_lesson, get_questions
import json

# q stands for question/questions

q_gen_template = """
You are an expert tutor/ question generator. Given the following lesson text and some sample questions, generate 5 new short_answer questions that are similar to the examples provided. Ensure that their answer can be given in 30-50 words by a 5th grade level student.

Give the output as a JSON object with questions as keys and answers as values.

Lesson content:
{lesson_title}

{lesson_content}

Lesson sample questions:
{sample_questions}

Answers to the sample questions:
{sample_question_answers}
"""


q_gen_prompt = PromptTemplate(
    input_variables=[
        "lesson_title",
        "lesson_content",
        "sample-questions",
        "sample_question_answers",
    ],
    template=q_gen_template,
)

q_gen_chain = q_gen_prompt | llm


def generate_q(lesson_title: str):
    db = next(get_db())

    lesson = get_lesson(db, title=lesson_title)
    if not lesson:
        return {"error": f"Lesson with title '{lesson_title}' not found."}

    questions = get_questions(db, lesson_id=lesson.id)

    sample_questions = "\n".join([q.question_text for q in questions])
    sample_question_answers = "\n".join([q.correct_answer for q in questions])

    response = q_gen_chain.invoke(
        {
            "lesson_title": lesson.title,
            "lesson_content": lesson.content,
            "sample_questions": sample_questions,
            "sample_question_answers": sample_question_answers,
        }
    )

    print("prompt:\n ", q_gen_prompt)  # testing
    # The output from the LLM is in the `content` attribute of the response object
    raw_output = response.content
    try:
        # Clean the output by removing markdown code fences
        cleaned_output = raw_output.strip().lstrip("```json").rstrip("```").strip()
        qna_dict = json.loads(cleaned_output)
        return qna_dict
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse LLM output as JSON.",
            "raw_output": raw_output,
        }


q_eval_template = """
You are an expert evaluator of student answers at the 4th grade level. Given the questions and a student's answers, assess the quality of the answers based on the following criteria:
    1. Relevance: Does the answer directly address the question?
    2. Completeness: Is the answer sufficiently detailed for a 4th grade response (30–50 words)?
    3. Clarity: Is the answer clearly written and easy to understand?
    4. Language Level: Is the language appropriate for a 4th grade student?

You have been provided with the lesson's text as well for context to the answers.
You should provide positive constructive feedback. The feedback should be encouraging and peppy. Explain what is done well, what is incorrect (if there is anything), and what can be improved. You must assess the grammar and syntax along with the correctness of the response. Give your feedback in at most 100 words.

Provide your evaulation in this JSON format:
{
    "score": <marks out of 5>,
    "feedback": "<comment explaining the score (max 100 words)>"
}

Lesson content:
{lesson_title}

{lesson_content}


Questions and Answers:
{qna}
"""

q_eval_prompt = PromptTemplate(
    input_variables=[],
    template=q_eval_template,
)

q_eval_chain = q_eval_prompt | llm


if __name__ == "__main__":
    lesson_title_to_test = "The Tinking Bells"
    generated_qna = generate_q(lesson_title_to_test)
    print(generated_qna)
