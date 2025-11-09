import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { CheckCircle2, XCircle } from 'lucide-react';

interface MiniProblemSetExerciseProps {
  exercise: any;
  onSubmit: (answers: string[]) => Promise<void>;
  isSubmitting: boolean;
}

export function MiniProblemSetExercise({ exercise, onSubmit, isSubmitting }: MiniProblemSetExerciseProps) {
  const payload = exercise.payload;
  const answered = exercise.is_correct !== null;
  const problems = payload.problems || [];

  // Initialize answers array with empty strings
  const [answers, setAnswers] = useState<string[]>(new Array(problems.length).fill(''));

  const updateAnswer = (index: number, value: string) => {
    const newAnswers = [...answers];
    newAnswers[index] = value;
    setAnswers(newAnswers);
  };

  const handleSubmit = async () => {
    // Only submit if all problems have answers
    if (answers.every(a => a.trim() !== '')) {
      await onSubmit(answers);
    }
  };

  const allAnswered = answers.every(a => a.trim() !== '');

  return (
    <Card className={answered ? (exercise.is_correct ? 'border-green-500' : 'border-red-500') : ''}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Badge variant="outline">{payload.topic || exercise.topic}</Badge>
            <Badge variant="secondary">Difficulty: {exercise.difficulty}/5</Badge>
            <Badge variant="secondary">{payload.totalPoints} points</Badge>
          </div>
          {answered && (
            <div className="flex items-center gap-2">
              {exercise.is_correct ? (
                <CheckCircle2 className="h-5 w-5 text-green-500" />
              ) : (
                <XCircle className="h-5 w-5 text-red-500" />
              )}
            </div>
          )}
        </div>
        <CardTitle className="text-lg mt-4">Mini Problem Set</CardTitle>
        <CardDescription>{payload.instructions}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {problems.map((problem: any, index: number) => (
            <div key={index} className="border rounded-lg p-4 bg-muted/30">
              <div className="flex items-start justify-between mb-3">
                <h4 className="font-medium text-sm">Problem {index + 1}</h4>
                <Badge variant="outline" className="text-xs">{problem.points} pts</Badge>
              </div>

              <p className="text-sm mb-4">{problem.question}</p>

              {!answered ? (
                <>
                  {problem.type === 'multiple_choice' && problem.options ? (
                    <RadioGroup
                      value={answers[index]}
                      onValueChange={(value) => updateAnswer(index, value)}
                    >
                      <div className="space-y-2">
                        {problem.options.map((option: string, optIndex: number) => (
                          <div key={optIndex} className="flex items-center space-x-2">
                            <RadioGroupItem
                              value={String.fromCharCode(65 + optIndex)}
                              id={`problem-${index}-option-${optIndex}`}
                            />
                            <Label
                              htmlFor={`problem-${index}-option-${optIndex}`}
                              className="cursor-pointer flex-1 text-sm"
                            >
                              <span className="font-semibold mr-1">
                                {String.fromCharCode(65 + optIndex)}.
                              </span>
                              {option}
                            </Label>
                          </div>
                        ))}
                      </div>
                    </RadioGroup>
                  ) : (
                    <Input
                      type={problem.type === 'numerical' ? 'number' : 'text'}
                      placeholder="Your answer..."
                      value={answers[index]}
                      onChange={(e) => updateAnswer(index, e.target.value)}
                      className="text-sm"
                    />
                  )}
                </>
              ) : (
                <div className="space-y-2 bg-background p-3 rounded-md text-sm">
                  <p>
                    <strong>Your Answer:</strong>{' '}
                    {Array.isArray(exercise.user_answer?.answer)
                      ? (exercise.user_answer.answer[index] || 'No answer')
                      : 'No answer'}
                  </p>
                  <p>
                    <strong>Correct Answer:</strong>{' '}
                    {problem.correctAnswer}
                  </p>
                  {problem.explanation && (
                    <p className="text-muted-foreground mt-2">
                      <strong>Explanation:</strong> {problem.explanation}
                    </p>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>

        {!answered && (
          <Button
            onClick={handleSubmit}
            disabled={!allAnswered || isSubmitting}
            className="w-full mt-6"
          >
            {isSubmitting ? 'Submitting...' : 'Submit All Answers'}
          </Button>
        )}

        {answered && exercise.feedback && (
          <div className="mt-4 p-4 bg-muted rounded-md">
            <p className="text-sm"><strong>Overall Feedback:</strong> {exercise.feedback}</p>
            {exercise.score !== null && (
              <p className="text-sm mt-2">
                <strong>Score:</strong> {exercise.score}/{payload.totalPoints} points
              </p>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
