import React, { useState, useEffect, useCallback } from 'react';
import { useInterviewState } from '../hooks/useInterviewState';
import { useQuestionTimer } from '../hooks/useTimer';
import { useInterviewApi } from '../hooks/useApi';
import { Button } from './ui/button';
import { Progress } from './ui/progress';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from './ui/card';
import { Textarea } from './ui/textarea';
import { Loader2, Clock, CheckCircle, AlertCircle } from 'lucide-react';

const QUESTION_TIME_LIMIT = 300; // 5 minutes per question

export function InterviewWindow({ questions = [], onComplete }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [apiError, setApiError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  
  // Initialize interview state and timer
  const {
    currentQuestion,
    currentQuestionIndex,
    answers,
    currentAnswer,
    progress,
    isComplete,
    updateAnswer,
    submitAnswer: submitLocalAnswer,
    goToQuestion,
    resetInterview
  } = useInterviewState(questions);
  
  const {
    startQuestionTimer,
    getFormattedTime,
    getTimeSpent,
    isTimeUp,
    pauseTimer,
    resumeTimer
  } = useQuestionTimer(QUESTION_TIME_LIMIT);
  
  // API hooks
  const {
    createSession,
    submitAnswer: submitAnswerApi,
    getEvaluation
  } = useInterviewApi();
  
  // Start timer when question changes
  useEffect(() => {
    if (currentQuestion?.id) {
      startQuestionTimer(currentQuestion.id);
    }
  }, [currentQuestion?.id, startQuestionTimer]);
  
  // Handle time up
  useEffect(() => {
    if (isTimeUp) {
      handleSubmit();
    }
  }, [isTimeUp]);

  // Create a new session when the interview starts
  useEffect(() => {
    const initSession = async () => {
      try {
        const response = await createSession.execute({
          start_time: new Date().toISOString(),
          question_count: questions.length,
          // Add any other session metadata
        });
        setSessionId(response.id);
      } catch (error) {
        console.error('Failed to create session:', error);
        setApiError('Failed to initialize interview session. Please refresh to try again.');
      }
    };
    
    if (questions.length > 0 && !sessionId) {
      initSession();
    }
  }, [questions, sessionId]);

  const handleAnswerChange = (e) => {
    updateAnswer(e.target.value);
  };

  const handleSubmit = async () => {
    if (!currentAnswer.trim() || isSubmitting) return;
    
    setIsSubmitting(true);
    setApiError(null);
    
    try {
      // Pause timer
      pauseTimer();
      
      // Submit answer to backend
      if (sessionId) {
        await submitAnswerApi.execute(sessionId, {
          question_id: currentQuestion.id,
          answer: currentAnswer,
          time_spent: getTimeSpent(currentQuestion.id),
          is_complete: currentQuestionIndex === questions.length - 1
        });
      }
      
      // Update local state
      submitLocalAnswer();
      
      // If last question, get evaluation
      if (currentQuestionIndex === questions.length - 1) {
        const evaluation = await getEvaluation.execute(sessionId);
        onComplete?.({
          sessionId,
          answers,
          evaluation,
          timePerQuestion: answers.reduce((acc, ans) => ({
            ...acc,
            [ans.questionId]: ans.timeSpent
          }), {})
        });
      }
    } catch (error) {
      console.error('Error submitting answer:', error);
      setApiError('Failed to submit your answer. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!currentQuestion) {
    return (
      <div className="flex flex-col items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <p className="mt-4 text-muted-foreground">Preparing your interview...</p>
      </div>
    );
  }

  if (isComplete) {
    return (
      <div className="text-center p-8">
        <CheckCircle className="h-12 w-12 text-green-500 mx-auto mb-4" />
        <h2 className="text-2xl font-bold mb-2">Interview Complete!</h2>
        <p className="text-muted-foreground mb-6">
          Thank you for completing the interview. Your responses have been recorded.
        </p>
        <Button onClick={() => resetInterview()}>
          Start New Interview
        </Button>
      </div>
    );
  }

  return (
    <Card className="w-full max-w-3xl mx-auto">
      <CardHeader>
        <div className="flex justify-between items-center mb-4">
          <CardTitle className="text-xl">
            Question {currentQuestionIndex + 1} of {questions.length}
          </CardTitle>
          <div className="flex items-center text-muted-foreground">
            <Clock className="h-4 w-4 mr-2" />
            <span>{getFormattedTime(currentQuestion.id)}</span>
          </div>
        </div>
        <Progress value={progress.percentage} className="h-2" />
      </CardHeader>
      
      <CardContent>
        <div className="space-y-6">
          <div className="p-4 bg-muted/50 rounded-lg">
            <p className="font-medium">{currentQuestion.text}</p>
            {currentQuestion.details && (
              <p className="mt-2 text-sm text-muted-foreground">
                {currentQuestion.details}
              </p>
            )}
          </div>
          
          <div className="space-y-2">
            <label htmlFor="answer" className="text-sm font-medium">
              Your Answer
            </label>
            <Textarea
              id="answer"
              value={currentAnswer}
              onChange={handleAnswerChange}
              placeholder="Type your answer here..."
              className="min-h-[120px]"
              disabled={isSubmitting}
            />
          </div>
          
          {apiError && (
            <div className="flex items-center text-destructive text-sm">
              <AlertCircle className="h-4 w-4 mr-2" />
              {apiError}
            </div>
          )}
        </div>
      </CardContent>
      
      <CardFooter className="flex justify-between">
        <Button
          variant="outline"
          onClick={() => goToQuestion(currentQuestionIndex - 1)}
          disabled={currentQuestionIndex === 0 || isSubmitting}
        >
          Previous
        </Button>
        
        <div className="space-x-2">
          <Button
            variant="outline"
            onClick={() => {
              updateAnswer('');
              resumeTimer();
            }}
            disabled={isSubmitting}
          >
            Clear
          </Button>
          
          <Button
            onClick={handleSubmit}
            disabled={!currentAnswer.trim() || isSubmitting}
          >
            {isSubmitting ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Submitting...
              </>
            ) : (
              currentQuestionIndex === questions.length - 1 ? 'Finish' : 'Next'
            )}
          </Button>
        </div>
      </CardFooter>
    </Card>
  );
}
