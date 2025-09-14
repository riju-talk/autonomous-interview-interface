import React from 'react';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from './ui/card';
import { CheckCircle, Clock, AlertCircle, BarChart2, Download } from 'lucide-react';

export function Completion({ results, onRestart, onDownload }) {
  const { sessionId, answers = [], evaluation = {}, timePerQuestion = {} } = results || {};
  
  // Calculate summary statistics
  const totalQuestions = answers.length;
  const totalTime = Object.values(timePerQuestion).reduce((sum, time) => sum + (time || 0), 0);
  const avgTimePerQuestion = totalQuestions > 0 ? Math.round(totalTime / totalQuestions) : 0;
  
  const formatTime = (seconds) => {
    if (seconds === 0) return '0s';
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return mins > 0 ? `${mins}m ${secs}s` : `${secs}s`;
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="text-center">
        <CheckCircle className="h-12 w-12 text-green-500 mx-auto mb-4" />
        <h1 className="text-3xl font-bold tracking-tight">Interview Complete!</h1>
        <p className="text-muted-foreground mt-2">
          Thank you for completing the interview. Here's your performance summary.
        </p>
      </div>
      
      <div className="grid gap-4 md:grid-cols-3">
        {/* Summary Card */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Questions Answered
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalQuestions}</div>
            <p className="text-xs text-muted-foreground">
              All questions completed
            </p>
          </CardContent>
        </Card>
        
        {/* Time Spent */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Total Time
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatTime(totalTime)}</div>
            <p className="text-xs text-muted-foreground">
              ~{formatTime(avgTimePerQuestion)} per question
            </p>
          </CardContent>
        </Card>
        
        {/* Performance */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Session ID
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-sm font-mono text-muted-foreground truncate">
              {sessionId || 'N/A'}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Keep this for reference
            </p>
          </CardContent>
        </Card>
      </div>
      
      {/* Detailed Results */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <BarChart2 className="h-5 w-5 mr-2" />
            Detailed Results
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {evaluation.scores && (
              <div>
                <h3 className="font-medium mb-2">Scores by Category</h3>
                <div className="space-y-2">
                  {Object.entries(evaluation.scores).map(([category, score]) => (
                    <div key={category} className="flex items-center">
                      <span className="w-32 text-sm font-medium">
                        {category.charAt(0).toUpperCase() + category.slice(1)}
                      </span>
                      <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-primary" 
                          style={{ width: `${(score / 10) * 100}%` }}
                        />
                      </div>
                      <span className="w-10 text-right text-sm font-medium ml-2">
                        {score}/10
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            <div>
              <h3 className="font-medium mb-2">Question Breakdown</h3>
              <div className="border rounded-lg divide-y">
                {answers.map((answer, index) => (
                  <div key={index} className="p-4">
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-medium">Question {index + 1}</p>
                        <p className="text-sm text-muted-foreground">
                          {answer.questionText || 'Question details not available'}
                        </p>
                      </div>
                      <span className="text-xs text-muted-foreground flex items-center">
                        <Clock className="h-3 w-3 mr-1" />
                        {formatTime(answer.timeSpent || 0)}
                      </span>
                    </div>
                    {evaluation.feedback && evaluation.feedback[index] && (
                      <div className="mt-2 p-3 bg-muted/30 rounded text-sm">
                        <p className="font-medium text-sm mb-1">Feedback:</p>
                        <p>{evaluation.feedback[index]}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
            
            {evaluation.overallFeedback && (
              <div className="p-4 bg-muted/20 rounded-lg">
                <h3 className="font-medium mb-2">Overall Feedback</h3>
                <p className="whitespace-pre-line">{evaluation.overallFeedback}</p>
              </div>
            )}
          </div>
        </CardContent>
        <CardFooter className="flex justify-between border-t">
          <Button variant="outline" onClick={onRestart}>
            Start New Interview
          </Button>
          <Button onClick={onDownload}>
            <Download className="h-4 w-4 mr-2" />
            Download Report
          </Button>
        </CardFooter>
      </Card>
      
      <div className="text-center text-sm text-muted-foreground">
        <p>Thank you for participating in this interview process.</p>
        <p>Your results have been recorded and will be reviewed by our team.</p>
      </div>
    </div>
  );
}
