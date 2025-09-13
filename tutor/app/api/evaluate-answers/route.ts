import { type NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  // Parse request body once at the top
  const { lessonText, lessonTitle, questions, answers } = await request.json();

  try {
    // Transform answers to match backend format
    const qnaObject: Record<string, string> = {};
    questions.forEach((q: any) => {
      const answerKey = `q${q.id}`;
      qnaObject[q.question] = answers[q.id] || "No answer provided";
    });

    // Call the backend API for feedback
    const response = await fetch("http://localhost:8000/feedback", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        lesson_title: lessonTitle,
        qna: qnaObject,
      }),
    });

    if (!response.ok) {
      throw new Error(`Backend API error: ${response.status}`);
    }

    const data = await response.json();

    // The backend already returns properly formatted feedback
    // Just return it as is since the format matches what the frontend expects
    return NextResponse.json({
      feedback: data.feedback,
      score: data.score,
    });
  } catch (error) {
    console.error("Error evaluating answers:", error);

    // Fallback evaluation
    const fallbackFeedback = questions.map((q: any) => ({
      questionId: q.id,
      question: q.question,
      answer: answers[q.id] || "No answer provided",
      feedback:
        "Thank you for your response. Please try to provide more detailed answers that directly address the question and demonstrate your understanding of the lesson content.",
      score: 70,
    }));

    return NextResponse.json({
      feedback: fallbackFeedback,
      score: 70,
    });
  }
}
