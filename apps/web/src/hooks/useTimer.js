import { useState, useEffect, useRef, useCallback } from 'react';

export function useTimer(initialTime = 0, { onComplete } = {}) {
  const [time, setTime] = useState(initialTime);
  const [isRunning, setIsRunning] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const timerRef = useRef(null);

  // Format time as MM:SS
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  // Start the timer
  const start = useCallback(() => {
    if (!isRunning && !isComplete) {
      setIsRunning(true);
    }
  }, [isRunning, isComplete]);

  // Pause the timer
  const pause = useCallback(() => {
    setIsRunning(false);
  }, []);

  // Reset the timer
  const reset = useCallback((newTime = initialTime) => {
    setTime(newTime);
    setIsRunning(false);
    setIsComplete(false);
  }, [initialTime]);

  // Timer effect
  useEffect(() => {
    if (isRunning && time > 0) {
      timerRef.current = setInterval(() => {
        setTime(prevTime => {
          if (prevTime <= 1) {
            setIsRunning(false);
            setIsComplete(true);
            if (onComplete) onComplete();
            return 0;
          }
          return prevTime - 1;
        });
      }, 1000);
    } else if (time === 0) {
      setIsRunning(false);
      setIsComplete(true);
      if (onComplete) onComplete();
    }

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [isRunning, time, onComplete]);

  return {
    time,
    formattedTime: formatTime(time),
    isRunning,
    isComplete,
    start,
    pause,
    reset,
    setTime,
  };
}

export function useQuestionTimer(questionTimeLimit = 300) { // 5 minutes default
  const [activeQuestionId, setActiveQuestionId] = useState(null);
  const [timers, setTimers] = useState({});
  const timer = useTimer(questionTimeLimit, {
    onComplete: () => {
      // Auto-submit or handle time out
      console.log(`Time's up for question ${activeQuestionId}`);
    }
  });

  // Start timer for a specific question
  const startQuestionTimer = useCallback((questionId) => {
    // Pause current timer if any
    if (activeQuestionId && activeQuestionId !== questionId) {
      timer.pause();
      // Save the remaining time for the current question
      setTimers(prev => ({
        ...prev,
        [activeQuestionId]: timer.time
      }));
    }

    // Set new active question
    setActiveQuestionId(questionId);
    
    // Get remaining time for the new question or use default
    const remainingTime = timers[questionId] !== undefined 
      ? timers[questionId] 
      : questionTimeLimit;
    
    // Reset timer with the remaining time
    timer.reset(remainingTime);
    timer.start();
    
  }, [activeQuestionId, timer, timers, questionTimeLimit]);

  // Get time spent on a question
  const getTimeSpent = useCallback((questionId) => {
    if (questionId === activeQuestionId) {
      return questionTimeLimit - timer.time;
    }
    return timers[questionId] !== undefined 
      ? questionTimeLimit - timers[questionId]
      : 0;
  }, [activeQuestionId, timer.time, timers, questionTimeLimit]);

  // Get formatted time for display
  const getFormattedTime = useCallback((questionId) => {
    if (questionId === activeQuestionId) {
      return timer.formattedTime;
    }
    return timers[questionId] !== undefined 
      ? `${Math.floor((questionTimeLimit - timers[questionId]) / 60).toString().padStart(2, '0')}:${((questionTimeLimit - timers[questionId]) % 60).toString().padStart(2, '0')}`
      : '--:--';
  }, [activeQuestionId, timer.formattedTime, timers, questionTimeLimit]);

  return {
    startQuestionTimer,
    getTimeSpent,
    getFormattedTime,
    activeQuestionId,
    isTimeUp: timer.isComplete,
    pauseTimer: timer.pause,
    resumeTimer: timer.start,
  };
}
