CREATE TABLE "lessons" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "title" varchar(200) NOT NULL,
  "content" text NOT NULL,
  "grade_level" integer NOT NULL
);

CREATE TABLE "questions" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "lesson_id" uuid NOT NULL,
  "question_type" varchar(20) NOT NULL,
  "question_text" text NOT NULL,
  "options" jsonb,
  "correct_answer" text
);


CREATE INDEX ON "lessons" ("grade_level");

CREATE INDEX ON "questions" ("lesson_id");

CREATE INDEX ON "questions" ("question_type");

COMMENT ON TABLE "lessons" IS 'Core lesson content - chapters from which questions are generated';

COMMENT ON COLUMN "lessons"."grade_level" IS 'Constraint: BETWEEN 3 AND 5';

COMMENT ON TABLE "questions" IS 'Questions generated from lessons by AI or created by teachers';

COMMENT ON COLUMN "questions"."question_type" IS 'multiple_choice, short_answer, long_answer';

COMMENT ON COLUMN "questions"."options" IS 'For multiple choice: {"A": "option1", "B": "option2", "C": "option3", "D": "option4"}';

COMMENT ON COLUMN "questions"."correct_answer" IS 'Correct answer or answer key';

ALTER TABLE "questions" ADD FOREIGN KEY ("lesson_id") REFERENCES "lessons" ("id");
