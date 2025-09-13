"use client";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { BookOpen, Clock, Users } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

interface Lesson {
  id: string;
  title: string;
  grade_level: number;
}

export default function HomePage() {
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchLessons = async () => {
      try {
        const response = await fetch("http://localhost:8000/lessons");
        if (!response.ok) {
          throw new Error("Failed to fetch lessons");
        }
        const data = await response.json();
        setLessons(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchLessons();
  }, []);

  const getDifficultyFromGrade = (grade: number) => {
    if (grade <= 3) return "Beginner";
    if (grade <= 6) return "Intermediate";
    return "Advanced";
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "Beginner":
        return "bg-green-100 text-green-800";
      case "Intermediate":
        return "bg-yellow-100 text-yellow-800";
      case "Advanced":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            AI English Tutor
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Choose a lesson to begin your personalized English learning
            experience. Our AI tutor will generate questions and provide
            detailed feedback on your answers.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {loading ? (
            <div className="col-span-full text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-2 text-gray-600">Loading lessons...</p>
            </div>
          ) : error ? (
            <div className="col-span-full text-center py-8">
              <p className="text-red-600">Error: {error}</p>
              <Button onClick={() => window.location.reload()} className="mt-4">
                Try Again
              </Button>
            </div>
          ) : lessons.length === 0 ? (
            <div className="col-span-full text-center py-8">
              <p className="text-gray-600">No lessons available yet.</p>
            </div>
          ) : (
            lessons.map((lesson) => {
              const difficulty = getDifficultyFromGrade(lesson.grade_level);
              return (
                <Card
                  key={lesson.id}
                  className="hover:shadow-lg transition-shadow duration-300"
                >
                  <CardHeader>
                    <div className="flex items-center justify-between mb-2">
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(
                          difficulty
                        )}`}
                      >
                        {difficulty}
                      </span>
                      <BookOpen className="h-5 w-5 text-blue-600" />
                    </div>
                    <CardTitle className="text-xl">{lesson.title}</CardTitle>
                    <CardDescription className="text-sm">
                      Grade {lesson.grade_level} • {difficulty} Level
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex items-center text-sm text-gray-600">
                        <Clock className="h-4 w-4 mr-2" />
                        15-20 minutes
                      </div>

                      <div className="flex flex-wrap gap-1">
                        <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-md text-xs">
                          Reading Comprehension
                        </span>
                        <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-md text-xs">
                          Literature
                        </span>
                      </div>

                      <Link href={`/lesson/${lesson.id}`} className="block">
                        <Button className="w-full mt-4">Start Lesson</Button>
                      </Link>
                    </div>
                  </CardContent>
                </Card>
              );
            })
          )}
        </div>

        <div className="mt-16 text-center">
          <div className="bg-white rounded-lg shadow-md p-8 max-w-2xl mx-auto">
            <Users className="h-12 w-12 text-blue-600 mx-auto mb-4" />
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              How It Works
            </h2>
            <div className="grid md:grid-cols-3 gap-6 text-sm">
              <div>
                <div className="bg-blue-100 rounded-full w-8 h-8 flex items-center justify-center mx-auto mb-2">
                  <span className="text-blue-600 font-semibold">1</span>
                </div>
                <p className="text-gray-600">
                  Select a lesson that matches your level
                </p>
              </div>
              <div>
                <div className="bg-blue-100 rounded-full w-8 h-8 flex items-center justify-center mx-auto mb-2">
                  <span className="text-blue-600 font-semibold">2</span>
                </div>
                <p className="text-gray-600">Answer AI-generated questions</p>
              </div>
              <div>
                <div className="bg-blue-100 rounded-full w-8 h-8 flex items-center justify-center mx-auto mb-2">
                  <span className="text-blue-600 font-semibold">3</span>
                </div>
                <p className="text-gray-600">Receive personalized feedback</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
