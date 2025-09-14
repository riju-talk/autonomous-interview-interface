import { useState, useCallback } from 'react';
import { interviewApi } from '../lib/api';

export function useApi(apiFunction) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const execute = useCallback(async (...args) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiFunction(...args);
      setData(response.data);
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'An unexpected error occurred';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [apiFunction]);

  return { data, error, loading, execute };
}

export function useInterviewApi() {
  const createSession = useApi(interviewApi.createSession);
  const getSession = useApi(interviewApi.getSession);
  const submitAnswer = useApi(interviewApi.submitAnswer);
  const getEvaluation = useApi(interviewApi.getEvaluation);
  const getQuestionPool = useApi(interviewApi.getQuestionPool);

  return {
    createSession: {
      ...createSession,
      execute: (candidateData) => createSession.execute(candidateData)
    },
    getSession: {
      ...getSession,
      execute: (sessionId) => getSession.execute(sessionId)
    },
    submitAnswer: {
      ...submitAnswer,
      execute: (sessionId, answerData) => submitAnswer.execute(sessionId, answerData)
    },
    getEvaluation: {
      ...getEvaluation,
      execute: (sessionId) => getEvaluation.execute(sessionId)
    },
    getQuestionPool: {
      ...getQuestionPool,
      execute: () => getQuestionPool.execute()
    }
  };
}
