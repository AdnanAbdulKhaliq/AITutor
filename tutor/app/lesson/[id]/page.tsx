"use client";

import { useState, useEffect, use } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, BookOpen, Send } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

interface Question {
  id: number;
  question: string;
  type: "short" | "essay";
}

interface Lesson {
  id: string;
  title: string;
  grade_level: number;
}

export default function LessonPage({ params }: { params: Promise<{ id: string }> }) {
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const { id: lessonId } = use(params);

  useEffect(() => {
    fetchLessonAndQuestions();
  }, [lessonId]);

  const fetchLessonAndQuestions = async () => {
    setLoading(true);
    setError(null);

    try {
      // Fetch lesson questions
      const response = await fetch(
        `http://localhost:8000/lessons/${lessonId}/questions`
      );

      if (!response.ok) {
        if (response.status === 404) {
          setError("Lesson not found");
        } else {
          setError("Failed to load lesson");
        }
        return;
      }

      const data = await response.json();
      setLesson(data.lesson);
      setQuestions(data.questions);
    } catch (err) {
      setError("Error loading lesson. Please try again.");
      console.error("Error fetching lesson:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (questionId: number, answer: string) => {
    setAnswers((prev) => ({ ...prev, [questionId]: answer }));
  };

  const handleSubmit = async () => {
    if (!lesson) return;

    setSubmitting(true);
    try {
      const response = await fetch("/api/evaluate-answers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          lessonTitle: lesson.title,
          questions,
          answers,
        }),
      });

      const feedback = await response.json();

      // Store results in localStorage for the feedback page
      localStorage.setItem(
        "tutorResults",
        JSON.stringify({
          lessonTitle: lesson.title,
          questions,
          answers,
          feedback: feedback.feedback,
          score: feedback.score,
        })
      );

      router.push("/feedback");
    } catch (error) {
      console.error("Error submitting answers:", error);
      setError("Failed to submit answers. Please try again.");
    }
    setSubmitting(false);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-2 text-gray-600">Loading lesson...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="text-center py-8">
            <p className="text-red-600 mb-4">{error}</p>
            <div className="space-y-2">
              <Link href="/">
                <Button>Back to Lessons</Button>
              </Link>
              <Button
                variant="outline"
                onClick={() => fetchLessonAndQuestions()}
              >
                Try Again
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="text-center py-8">
            <p className="text-gray-600 mb-4">Lesson not found</p>
            <Link href="/">
              <Button>Back to Lessons</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <Link
            href="/"
            className="inline-flex items-center text-blue-600 hover:text-blue-800"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Lessons
          </Link>
        </div>

        <div className="max-w-4xl mx-auto space-y-8">
          {/* Questions */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2 mb-2">
                <BookOpen className="h-5 w-5 text-blue-600" />
                <Badge variant="secondary">Grade {lesson.grade_level}</Badge>
              </div>
              <CardTitle className="text-2xl">{lesson.title}</CardTitle>
              <CardDescription>
                Answer the following questions based on your understanding of
                the lesson.
              </CardDescription>
            </CardHeader>
            <CardContent>
              {questions.length === 0 ? (
                <div className="text-center py-8">
                  <p className="text-gray-600">
                    No questions available for this lesson.
                  </p>
                </div>
              ) : (
                <div className="space-y-6">
                  {questions.map((question, index) => (
                    <div key={question.id} className="space-y-2">
                      <label className="block">
                        <div className="flex items-start gap-2 mb-2">
                          <span className="bg-blue-100 text-blue-800 text-sm font-medium px-2 py-1 rounded">
                            Q{index + 1}
                          </span>
                          <span className="font-medium text-gray-900">
                            {question.question}
                          </span>
                        </div>
                        <Textarea
                          placeholder="Type your answer here..."
                          value={answers[question.id] || ""}
                          onChange={(e) =>
                            handleAnswerChange(question.id, e.target.value)
                          }
                          className="min-h-[100px]"
                        />
                      </label>
                    </div>
                  ))}

                  <div className="pt-6">
                    <Button
                      onClick={handleSubmit}
                      disabled={submitting || Object.keys(answers).length === 0}
                      className="w-full"
                      size="lg"
                    >
                      {submitting ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                          Evaluating Your Answers...
                        </>
                      ) : (
                        <>
                          <Send className="h-4 w-4 mr-2" />
                          Submit Answers for Evaluation
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
