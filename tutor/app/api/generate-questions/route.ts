import { type NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const { lessonText, lessonTitle } = await request.json();

    // Call the backend API
    const response = await fetch("http://localhost:8000/generate-questions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        lesson_title: lessonTitle,
      }),
    });

    if (!response.ok) {
      throw new Error(`Backend API error: ${response.status}`);
    }

    const data = await response.json();

    // Transform backend response to match frontend format
    const questions = Object.entries(data).map(([key, value], index) => ({
      id: index + 1,
      question: value as string,
      type: index % 2 === 0 ? "short" : "essay",
    }));

    return NextResponse.json({ questions });
  } catch (error) {
    console.error("Error generating questions:", error);

    // Fallback questions
    const fallbackQuestions = [
      {
        id: 1,
        question: "What are the main themes discussed in this lesson?",
        type: "essay",
      },
      {
        id: 2,
        question: "Explain one key concept from the text in your own words.",
        type: "short",
      },
      {
        id: 3,
        question: "How does this topic relate to modern English usage?",
        type: "essay",
      },
      {
        id: 4,
        question: "What did you find most interesting about this lesson?",
        type: "short",
      },
    ];

    return NextResponse.json({ questions: fallbackQuestions });
  }
}
