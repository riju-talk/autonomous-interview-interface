import axios from 'axios';

const API_BASE_URL = process.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Handle specific status codes
      if (error.response.status === 401) {
        // Handle unauthorized
        console.error('Unauthorized access - please login again');
      } else if (error.response.status === 404) {
        console.error('The requested resource was not found');
      }
    } else if (error.request) {
      console.error('No response received from server');
    } else {
      console.error('Error setting up request:', error.message);
    }
    return Promise.reject(error);
  }
);

export const interviewApi = {
  // Session management
  createSession: (candidateData) => 
    api.post('/sessions/', candidateData),
    
  getSession: (sessionId) => 
    api.get(`/sessions/${sessionId}`),
    
  // Question handling
  submitAnswer: (sessionId, answerData) => 
    api.post(`/sessions/${sessionId}/messages`, answerData),
    
  // Evaluation
  getEvaluation: (sessionId) => 
    api.get(`/sessions/${sessionId}/evaluation`),
    
  // Questions
  getQuestionPool: () => 
    api.get('/questions/pool'),
};

export default api;
