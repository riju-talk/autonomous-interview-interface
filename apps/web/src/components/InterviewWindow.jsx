import React, { Component } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Clock, Upload, AlertTriangle, CheckCircle, FileText, Send } from "lucide-react";


class InterviewWindow extends Component {
  timerInterval = null;
  fileInputRef;

  constructor(props) {
    super(props);
    this.fileInputRef = React.createRef();
    this.state = {
      sessionId: null,
      currentQuestion: null,
      questionNumber: 0,
      totalQuestions: 40,
      timeRemaining: 0,
      answer: "",
      uploadedFiles: [],
      isLoading: true,
      error: null,
      isSubmitting: false,
      isCompleted: false,
    };
  }

  async componentDidMount() {
    await this.initializeSession();
  }

  componentWillUnmount() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
    }
  }

  initializeSession = async () => {
    try {
      // In a real app, this would call your backend API
      // For now, we'll simulate the session creation
      const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      
      this.setState({ sessionId, isLoading: false });
      await this.fetchNextQuestion();
    } catch (error) {
      this.setState({ 
        error: "Failed to initialize interview session. Please try again.", 
        isLoading: false 
      });
    }
  };

  fetchNextQuestion = async () => {
    const { sessionId, questionNumber } = this.state;
    
    if (!sessionId) return;

    try {
      this.setState({ isLoading: true });
      
      // Simulate API call to get next question
      // In real app: const response = await axios.get(`/api/sessions/${sessionId}/next`);
      
      // Mock question data
      const mockQuestions = [
        {
          id: "q1",
          type: "excel",
          question: "Create a formula to calculate the sum of values in column A where corresponding values in column B are greater than 100. What formula would you use?",
          timeLimit: 180,
          requiresFile: false
        },
        {
          id: "q2", 
          type: "behavioral",
          question: "Describe a time when you had to work with a large dataset in Excel. What challenges did you face and how did you overcome them?",
          timeLimit: 240,
          requiresFile: false
        },
        {
          id: "q3",
          type: "assignment",
          question: "Using the provided sales data, create a pivot table that shows total sales by region and product category. Upload your completed Excel file.",
          timeLimit: 600,
          requiresFile: true
        }
      ];

      const currentQ = mockQuestions[questionNumber % 3];
      
      this.setState({
        currentQuestion: currentQ,
        questionNumber: questionNumber + 1,
        timeRemaining: currentQ.timeLimit,
        answer: "",
        uploadedFiles: [],
        isLoading: false
      });

      this.startTimer();
    } catch (error) {
      this.setState({ 
        error: "Failed to fetch next question. Please try again.", 
        isLoading: false 
      });
    }
  };

  startTimer = () => {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
    }

    this.timerInterval = setInterval(() => {
      this.setState(prevState => {
        const newTimeRemaining = prevState.timeRemaining - 1;
        
        if (newTimeRemaining <= 0) {
          this.handleAutoSubmit();
          return { timeRemaining: 0 };
        }
        
        return { timeRemaining: newTimeRemaining };
      });
    }, 1000);
  };

  handleAutoSubmit = () => {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
    }
    this.submitAnswer(true);
  };

  submitAnswer = async (isAutoSubmit = false) => {
    const { sessionId, currentQuestion, answer, uploadedFiles } = this.state;
    
    if (!sessionId || !currentQuestion) return;

    try {
      this.setState({ isSubmitting: true });

      // Simulate API call to submit answer
      // In real app: 
      // const formData = new FormData();
      // formData.append('answer', answer);
      // uploadedFiles.forEach(file => formData.append('files', file));
      // await axios.post(`/api/sessions/${sessionId}/answer`, formData);

      // Check if interview is complete
      if (this.state.questionNumber >= this.state.totalQuestions) {
        this.setState({ isCompleted: true });
        // Navigate to completion page
        window.location.href = "/completion";
        return;
      }

      // Fetch next question
      await this.fetchNextQuestion();
    } catch (error) {
      this.setState({ 
        error: "Failed to submit answer. Please try again.",
        isSubmitting: false
      });
    }
  };

  handleFileUpload = (event) => {
    const files = Array.from(event.target.files || []);
    const validFiles = files.filter(file => {
      const validTypes = ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/csv'];
      const validExtensions = ['.csv', '.xlsx', '.xls'];
      return validTypes.includes(file.type) || validExtensions.some(ext => file.name.toLowerCase().endsWith(ext));
    });

    if (validFiles.length !== files.length) {
      this.setState({ error: "Some files were not uploaded. Please use only CSV or Excel files." });
    }

    this.setState({ uploadedFiles: validFiles, error: null });
  };

  removeFile = (index) => {
    this.setState(prevState => ({
      uploadedFiles: prevState.uploadedFiles.filter((_, i) => i !== index)
    }));
  };

  formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  getProgressPercentage = () => {
    return (this.state.questionNumber / this.state.totalQuestions) * 100;
  };

  getQuestionTypeColor = (type) => {
    switch (type) {
      case 'excel': return 'text-primary';
      case 'behavioral': return 'text-accent';
      case 'assignment': return 'text-success';
      default: return 'text-foreground';
    }
  };

  getQuestionTypeLabel = (type) => {
    switch (type) {
      case 'excel': return 'Excel Technical';
      case 'behavioral': return 'Behavioral';
      case 'assignment': return 'Practical Assignment';
      default: return 'Question';
    }
  };

  render() {
    const { 
      currentQuestion, 
      questionNumber, 
      totalQuestions, 
      timeRemaining, 
      answer, 
      uploadedFiles, 
      isLoading, 
      error, 
      isSubmitting 
    } = this.state;

    if (isLoading) {
      return (
        <div className="min-h-screen bg-background flex items-center justify-center">
          <Card className="w-96 shadow-medium">
            <CardContent className="p-8 text-center">
              <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4"></div>
              <p>Loading your interview...</p>
            </CardContent>
          </Card>
        </div>
      );
    }

    if (error && !currentQuestion) {
      return (
        <div className="min-h-screen bg-background flex items-center justify-center">
          <Card className="w-96 shadow-medium">
            <CardContent className="p-8 text-center">
              <AlertTriangle className="w-12 h-12 text-destructive mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">Connection Error</h3>
              <p className="text-muted-foreground mb-4">{error}</p>
              <Button onClick={() => window.location.reload()}>Try Again</Button>
            </CardContent>
          </Card>
        </div>
      );
    }

    if (!currentQuestion) return null;

    const isTimeWarning = timeRemaining <= 60;
    const isTimeCritical = timeRemaining <= 30;

    return (
      <div className="min-h-screen bg-background">
        {/* Header */}
        <header className="bg-secondary/30 border-b sticky top-0 z-10">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <FileText className="w-6 h-6 text-primary" />
                  <span className="font-semibold">Question {questionNumber} of {totalQuestions}</span>
                </div>
                <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm font-medium ${this.getQuestionTypeColor(currentQuestion.type)} bg-card`}>
                  <span>{this.getQuestionTypeLabel(currentQuestion.type)}</span>
                </div>
              </div>
              
              <div className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-mono text-lg ${
                isTimeCritical ? 'bg-destructive text-destructive-foreground' :
                isTimeWarning ? 'bg-warning text-warning-foreground' :
                'bg-card text-foreground'
              }`}>
                <Clock className="w-5 h-5" />
                <span>{this.formatTime(timeRemaining)}</span>
              </div>
            </div>
            
            <div className="mt-4">
              <Progress value={this.getProgressPercentage()} className="h-2" />
              <div className="flex justify-between text-xs text-muted-foreground mt-1">
                <span>Progress</span>
                <span>{Math.round(this.getProgressPercentage())}% Complete</span>
              </div>
            </div>
          </div>
        </header>

        <main className="container mx-auto px-4 py-8 max-w-4xl">
          {error && (
            <Alert className="mb-6 border-destructive bg-destructive/10">
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {/* Question Card */}
          <Card className="mb-6 shadow-soft">
            <CardHeader>
              <CardTitle className="text-xl leading-relaxed">
                {currentQuestion.question}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Answer Input */}
              <div>
                <Label htmlFor="answer" className="text-base font-medium">Your Answer</Label>
                <Textarea
                  id="answer"
                  value={answer}
                  onChange={(e) => this.setState({ answer: e.target.value })}
                  placeholder="Enter your detailed answer here..."
                  className="mt-2 min-h-[120px] resize-y"
                  disabled={isSubmitting}
                />
              </div>

              {/* File Upload Section */}
              {currentQuestion.requiresFile && (
                <div>
                  <Label className="text-base font-medium flex items-center space-x-2">
                    <Upload className="w-4 h-4" />
                    <span>File Upload Required</span>
                  </Label>
                  <div className="mt-2 space-y-4">
                    <div className="border-2 border-dashed border-border rounded-lg p-6 text-center hover:border-primary/50 transition-colors">
                      <Input
                        ref={this.fileInputRef}
                        type="file"
                        accept=".csv,.xlsx,.xls"
                        multiple
                        onChange={this.handleFileUpload}
                        className="hidden"
                        disabled={isSubmitting}
                      />
                      <Upload className="w-8 h-8 text-muted-foreground mx-auto mb-2" />
                      <p className="text-sm text-muted-foreground mb-2">
                        Upload your Excel or CSV files
                      </p>
                      <Button 
                        variant="outline" 
                        onClick={() => this.fileInputRef.current?.click()}
                        disabled={isSubmitting}
                      >
                        Choose Files
                      </Button>
                    </div>

                    {/* Uploaded Files */}
                    {uploadedFiles.length > 0 && (
                      <div className="space-y-2">
                        <Label className="text-sm font-medium">Uploaded Files:</Label>
                        {uploadedFiles.map((file, index) => (
                          <div key={index} className="flex items-center justify-between bg-muted p-3 rounded-lg">
                            <div className="flex items-center space-x-2">
                              <CheckCircle className="w-4 h-4 text-success" />
                              <span className="text-sm font-medium">{file.name}</span>
                              <span className="text-xs text-muted-foreground">
                                ({(file.size / 1024).toFixed(1)} KB)
                              </span>
                            </div>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => this.removeFile(index)}
                              disabled={isSubmitting}
                            >
                              Remove
                            </Button>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Submit Button */}
              <div className="flex justify-end space-x-4">
                <Button
                  variant="interview"
                  size="lg"
                  onClick={() => this.submitAnswer()}
                  disabled={isSubmitting || (!answer.trim() && (!currentQuestion.requiresFile || uploadedFiles.length === 0))}
                  className="px-8"
                >
                  {isSubmitting ? (
                    <>
                      <div className="animate-spin w-4 h-4 border-2 border-current border-t-transparent rounded-full mr-2"></div>
                      Submitting...
                    </>
                  ) : (
                    <>
                      <Send className="w-4 h-4 mr-2" />
                      Submit Answer
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Time Warning */}
          {isTimeWarning && (
            <Alert className={`${isTimeCritical ? 'border-destructive bg-destructive/10' : 'border-warning bg-warning/10'}`}>
              <Clock className="h-4 w-4" />
              <AlertDescription>
                {isTimeCritical 
                  ? "⚠️ Less than 30 seconds remaining! Your answer will be auto-submitted."
                  : "⏰ Less than 1 minute remaining. Please finalize your answer."
                }
              </AlertDescription>
            </Alert>
          )}
        </main>
      </div>
    );
  }
}

export default InterviewWindow;