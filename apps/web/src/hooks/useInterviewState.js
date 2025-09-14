import { useState, useEffect, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';

const SESSION_STORAGE_KEY = 'interview_session';

export function useInterviewState(initialQuestions = []) {
  // Load saved state from session storage if available
  const loadState = () => {
    const savedState = sessionStorage.getItem(SESSION_STORAGE_KEY);
    return savedState ? JSON.parse(savedState) : null;
  };

  // Initial state
  const [state, setState] = useState(() => ({
    sessionId: uuidv4(),
    currentQuestionIndex: 0,
    questions: initialQuestions,
    answers: [],
    currentAnswer: '',
    isComplete: false,
    startTime: new Date().toISOString(),
    endTime: null,
    timePerQuestion: {},
    ...loadState(),
  }));

  // Save state to session storage whenever it changes
  useEffect(() => {
    sessionStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify({
      sessionId: state.sessionId,
      currentQuestionIndex: state.currentQuestionIndex,
      questions: state.questions,
      answers: state.answers,
      isComplete: state.isComplete,
      startTime: state.startTime,
      timePerQuestion: state.timePerQuestion,
    }));
  }, [state]);

  // Get current question
  const currentQuestion = useCallback(() => {
    return state.questions[state.currentQuestionIndex];
  }, [state.questions, state.currentQuestionIndex]);

  // Update answer for current question
  const updateAnswer = useCallback((answer) => {
    setState(prev => ({
      ...prev,
      currentAnswer: answer
    }));
  }, []);

  // Submit answer and move to next question
  const submitAnswer = useCallback(() => {
    const now = new Date().toISOString();
    const questionId = currentQuestion()?.id;
    
    setState(prev => {
      const updatedAnswers = [...prev.answers];
      const answerIndex = updatedAnswers.findIndex(a => a.questionId === questionId);
      
      const answerData = {
        questionId,
        answer: prev.currentAnswer,
        timestamp: now,
        timeSpent: Math.floor((new Date(now) - new Date(prev.answers[answerIndex]?.timestamp || prev.startTime)) / 1000)
      };

      if (answerIndex >= 0) {
        updatedAnswers[answerIndex] = answerData;
      } else {
        updatedAnswers.push(answerData);
      }

      const isLastQuestion = prev.currentQuestionIndex >= prev.questions.length - 1;
      
      return {
        ...prev,
        answers: updatedAnswers,
        currentAnswer: '',
        currentQuestionIndex: isLastQuestion ? prev.currentQuestionIndex : prev.currentQuestionIndex + 1,
        isComplete: isLastQuestion,
        endTime: isLastQuestion ? now : prev.endTime,
        timePerQuestion: {
          ...prev.timePerQuestion,
          [questionId]: answerData.timeSpent
        }
      };
    });
  }, [currentQuestion]);

  // Go to specific question
  const goToQuestion = useCallback((index) => {
    if (index >= 0 && index < state.questions.length) {
      setState(prev => ({
        ...prev,
        currentQuestionIndex: index
      }));
    }
  }, [state.questions.length]);

  // Reset interview
  const resetInterview = useCallback(() => {
    sessionStorage.removeItem(SESSION_STORAGE_KEY);
    setState({
      sessionId: uuidv4(),
      currentQuestionIndex: 0,
      questions: initialQuestions,
      answers: [],
      currentAnswer: '',
      isComplete: false,
      startTime: new Date().toISOString(),
      endTime: null,
      timePerQuestion: {},
    });
  }, [initialQuestions]);

  // Calculate progress
  const progress = {
    current: state.currentQuestionIndex + 1,
    total: state.questions.length,
    percentage: Math.round(((state.currentQuestionIndex) / state.questions.length) * 100)
  };

  return {
    // State
    ...state,
    currentQuestion: currentQuestion(),
    progress,
    
    // Actions
    updateAnswer,
    submitAnswer,
    goToQuestion,
    resetInterview,
  };
}
