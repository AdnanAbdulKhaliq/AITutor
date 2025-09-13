"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, Trophy, BookOpen, CheckCircle, AlertCircle, Home } from "lucide-react"
import Link from "next/link"

interface FeedbackItem {
  questionId: number
  question: string
  answer: string
  feedback: string
  score: number
}

interface Results {
  lessonTitle: string
  questions: Array<{ id: number; question: string }>
  answers: Record<number, string>
  feedback: FeedbackItem[]
  score: number
}

export default function FeedbackPage() {
  const [results, setResults] = useState<Results | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const storedResults = localStorage.getItem("tutorResults")
    if (storedResults) {
      setResults(JSON.parse(storedResults))
    }
    setLoading(false)
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!results) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="text-center py-8">
            <AlertCircle className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
            <h2 className="text-xl font-semibold mb-2">No Results Found</h2>
            <p className="text-gray-600 mb-4">Please complete a lesson first to view your feedback.</p>
            <Link href="/">
              <Button>
                <Home className="h-4 w-4 mr-2" />
                Go to Lessons
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    )
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-green-600"
    if (score >= 60) return "text-yellow-600"
    return "text-red-600"
  }

  const getScoreBadge = (score: number) => {
    if (score >= 80) return { text: "Excellent", color: "bg-green-100 text-green-800" }
    if (score >= 60) return { text: "Good", color: "bg-yellow-100 text-yellow-800" }
    return { text: "Needs Improvement", color: "bg-red-100 text-red-800" }
  }

  const scoreBadge = getScoreBadge(results.score)

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <Link href="/" className="inline-flex items-center text-blue-600 hover:text-blue-800">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Lessons
          </Link>
        </div>

        <div className="max-w-4xl mx-auto space-y-8">
          {/* Score Overview */}
          <Card className="border-2 border-blue-200">
            <CardHeader className="text-center">
              <div className="flex items-center justify-center gap-2 mb-2">
                <Trophy className="h-6 w-6 text-yellow-500" />
                <CardTitle className="text-2xl">Lesson Complete!</CardTitle>
              </div>
              <CardDescription className="text-lg">{results.lessonTitle}</CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <div className="mb-6">
                <div className={`text-6xl font-bold mb-2 ${getScoreColor(results.score)}`}>{results.score}%</div>
                <Badge className={scoreBadge.color}>{scoreBadge.text}</Badge>
              </div>

              <div className="grid md:grid-cols-3 gap-4 text-sm">
                <div className="bg-blue-50 rounded-lg p-4">
                  <BookOpen className="h-6 w-6 text-blue-600 mx-auto mb-2" />
                  <div className="font-semibold">Questions Answered</div>
                  <div className="text-2xl font-bold text-blue-600">{results.feedback.length}</div>
                </div>
                <div className="bg-green-50 rounded-lg p-4">
                  <CheckCircle className="h-6 w-6 text-green-600 mx-auto mb-2" />
                  <div className="font-semibold">Strong Answers</div>
                  <div className="text-2xl font-bold text-green-600">
                    {results.feedback.filter((f) => f.score >= 80).length}
                  </div>
                </div>
                <div className="bg-yellow-50 rounded-lg p-4">
                  <AlertCircle className="h-6 w-6 text-yellow-600 mx-auto mb-2" />
                  <div className="font-semibold">Areas to Improve</div>
                  <div className="text-2xl font-bold text-yellow-600">
                    {results.feedback.filter((f) => f.score < 60).length}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Detailed Feedback */}
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900">Detailed Feedback</h2>

            {results.feedback.map((item, index) => (
              <Card key={item.questionId} className="overflow-hidden">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="bg-blue-100 text-blue-800 text-sm font-medium px-2 py-1 rounded">
                          Question {index + 1}
                        </span>
                        <Badge
                          className={
                            item.score >= 80
                              ? "bg-green-100 text-green-800"
                              : item.score >= 60
                                ? "bg-yellow-100 text-yellow-800"
                                : "bg-red-100 text-red-800"
                          }
                        >
                          {item.score}%
                        </Badge>
                      </div>
                      <CardTitle className="text-lg">{item.question}</CardTitle>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Your Answer:</h4>
                    <div className="bg-gray-50 rounded-lg p-4 text-gray-700">{item.answer}</div>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">AI Tutor Feedback:</h4>
                    <div className="bg-blue-50 rounded-lg p-4 text-gray-700">{item.feedback}</div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-8">
            <Link href="/">
              <Button variant="outline" className="w-full sm:w-auto bg-transparent">
                <BookOpen className="h-4 w-4 mr-2" />
                Try Another Lesson
              </Button>
            </Link>
            <Button onClick={() => window.print()} variant="secondary" className="w-full sm:w-auto">
              Print Results
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
