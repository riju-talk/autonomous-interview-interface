import React, { useState, useEffect } from 'react';
import { InterviewWindow } from './components/InterviewWindow';
import { Completion } from './components/Completion';
import { useInterviewApi } from './hooks/useApi';
import { Button } from './components/ui/button';
import { Loader2 } from 'lucide-react';

// Mock questions - in a real app, these would come from an API
const MOCK_QUESTIONS = [
  {
    id: 'q1',
    text: 'Tell me about yourself and your experience.',
    type: 'behavioral',
    category: 'Introduction',
    timeLimit: 180, // seconds
  },
  {
    id: 'q2',
    text: 'Describe a challenging project you worked on and how you handled it.',
    type: 'behavioral',
    category: 'Experience',
    timeLimit: 240,
  },
  {
    id: 'q3',
    text: 'How would you approach debugging a complex issue in production?',
    type: 'technical',
    category: 'Problem Solving',
    timeLimit: 300,
  },
  {
    id: 'q4',
    text: 'Explain a time when you had to work with a difficult team member.',
    type: 'behavioral',
    category: 'Teamwork',
    timeLimit: 180,
  },
  {
    id: 'q5',
    text: 'What are your salary expectations?',
    type: 'general',
    category: 'Compensation',
    timeLimit: 120,
  },
];

function App() {
  const [questions, setQuestions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [interviewComplete, setInterviewComplete] = useState(false);
  const [results, setResults] = useState(null);
  
  const { getQuestionPool } = useInterviewApi();
  
  // Load questions on mount
  useEffect(() => {
    const loadQuestions = async () => {
      try {
        // In a real app, we would fetch questions from the API
        // const response = await getQuestionPool.execute();
        // setQuestions(response.questions);
        
        // For now, use mock questions
        setQuestions(MOCK_QUESTIONS);
      } catch (err) {
        console.error('Failed to load questions:', err);
        setError('Failed to load interview questions. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };
    
    loadQuestions();
  }, []);
  
  const handleInterviewComplete = (results) => {
    setResults(results);
    setInterviewComplete(true);
    
    // Clear any saved interview state
    sessionStorage.removeItem('interview_session');
  };
  
  const handleRestart = () => {
    setInterviewComplete(false);
    setResults(null);
    // The InterviewWindow will initialize a new session
  };
  
  const handleDownloadReport = () => {
    if (!results) return;
    
    // Create a blob with the results
    const blob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    // Create a temporary anchor element
    const a = document.createElement('a');
    a.href = url;
    a.download = `interview-results-${results.sessionId || new Date().toISOString()}.json`;
    
    // Trigger the download
    document.body.appendChild(a);
    a.click();
    
    // Cleanup
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };
  
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto text-primary" />
          <p className="mt-4 text-lg font-medium">Loading interview questions...</p>
          <p className="text-sm text-muted-foreground mt-2">Please wait while we prepare your interview.</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center max-w-md p-6 bg-card rounded-lg shadow-md">
          <h2 className="text-xl font-bold text-destructive mb-2">Error Loading Interview</h2>
          <p className="text-muted-foreground mb-4">{error}</p>
          <Button onClick={() => window.location.reload()}>
            Try Again
          </Button>
        </div>
      </div>
    );
  }
  
  if (interviewComplete && results) {
    return (
      <div className="container py-8 px-4">
        <Completion 
          results={results} 
          onRestart={handleRestart}
          onDownload={handleDownloadReport}
        />
      </div>
    );
  }
  
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container flex h-16 items-center justify-between px-4">
          <div className="flex items-center space-x-2">
            <h1 className="text-xl font-bold">Autonomous Interview</h1>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-muted-foreground">
              Powered by AI
            </span>
          </div>
        </div>
      </header>
      
      <main className="container py-8 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight mb-6">Technical Interview</h2>
          
          <div className="bg-card rounded-lg border p-6">
            <InterviewWindow 
              questions={questions} 
              onComplete={handleInterviewComplete}
            />
          </div>
          
          <div className="mt-6 text-center text-sm text-muted-foreground">
            <p>Your progress is automatically saved. You can close the browser and come back later.</p>
          </div>
        </div>
      </main>
      
      <footer className="border-t py-6">
        <div className="container px-4">
          <p className="text-center text-sm text-muted-foreground">
            © {new Date().getFullYear()} Autonomous Interview Interface. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
