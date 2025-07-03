from langchain.prompts import PromptTemplate
from llm import llm
from db.models import get_db, get_lesson, get_questions
from utils import qna_dict_to_string
from schemas import (
    LessonIn,
    QuestionAnswer,
    QnAList,
    StudentAnswers,
    EvalResult,
    EvalResultList,
)
import json

# q stands for question/questions

q_gen_template = """
You are an expert tutor/ question generator. Given the following lesson text and some sample questions, generate 5 new short_answer questions that are similar to the examples provided. Ensure that their answer can be given in 30-50 words by a 4th grade level student. The level of the questions and answers should be such that a 4th grade level student living in rural India can answer it.

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


def generate_q(lesson_title: str) -> QnAList:
    db = next(get_db())

    lesson = get_lesson(db, title=lesson_title)
    if not lesson:
        return QnAList(items=[])

    questions = get_questions(db, lesson_id=lesson.id)
    qna_items = [
        QuestionAnswer(question=q.question_text, answer=q.correct_answer)
        for q in questions
    ]

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

    raw_output = response.content
    try:
        # Clean the output by removing markdown code fences
        cleaned_output = raw_output.strip().lstrip("```json").rstrip("```").strip()
        qna_dict = json.loads(cleaned_output)
        # Convert dict to QnAList
        items = [QuestionAnswer(question=k, answer=v) for k, v in qna_dict.items()]
        return QnAList(items=items)
    except json.JSONDecodeError:
        return QnAList(items=[])


q_eval_template = """
You are an expert evaluator of student answers at the 4th grade level. The students come from rural Indian villages. Keep in mind that English is not their first language. Given the questions and a student's answers, assess the quality of the answers based on the following criteria:
    1. Relevance: Does the answer directly address the question?
    2. Completeness: Is the answer sufficiently detailed for a 4th grade response (30–50 words)?
    3. Clarity: Is the answer clearly written and easy to understand?
    4. Language Level: Is the language appropriate for a 4th grade student?

You have been provided with the sample answers to the questions as well. Evaluate the student's answers by comparing them with the sample answers.

You should provide positive constructive feedback. The feedback should be encouraging and peppy. Explain what is done well, what is incorrect (if there is anything), and what can be improved. You must assess the grammar and syntax along with the correctness of the response. Give your feedback in at most 100 words.

Provide your evaulation in this JSON format:
{
    "score": <marks out of 5>,
    "feedback": "<comment explaining the score (max 100 words)>"
}

Return a JSON array (list) of such objects, one for each student answer, in the same order as the questions.

Questions and sample answers:
{qna}

Student's answers:
{student_answers}
"""

q_eval_prompt = PromptTemplate(
    input_variables=[
        "qna",
        "student_answers",
    ],
    template=q_eval_template,
)

q_eval_chain = q_eval_prompt | llm


def eval_answers(qna: QnAList, student_answers: StudentAnswers) -> EvalResultList:
    qna_string = "\n".join(
        [f"Q: {item.question}\nA: {item.answer}" for item in qna.items]
    )
    student_answers_string = "\n".join(student_answers.answers)

    response = q_eval_chain.invoke(
        {
            "qna": qna_string,
            "student_answers": student_answers_string,
        }
    )

    raw_output = response.content
    try:
        cleaned_output = raw_output.strip().lstrip("```json").rstrip("```").strip()
        eval_list = json.loads(cleaned_output)
        results = [EvalResult(**item) for item in eval_list]
        return EvalResultList(results=results)
    except json.JSONDecodeError:
        return EvalResultList(results=[])


if __name__ == "__main__":
    lesson_title_to_test = "The Tinking Bells"
    generated_qna = generate_q(lesson_title_to_test)
    print(generated_qna)
