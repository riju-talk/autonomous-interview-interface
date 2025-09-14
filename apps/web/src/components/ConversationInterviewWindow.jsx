import React, { Component } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { 
  Clock, 
  Upload, 
  AlertTriangle, 
  CheckCircle, 
  FileText, 
  Send, 
  MessageSquare,
  Brain,
  Calculator,
  ClipboardList,
  User,
  Bot
} from "lucide-react";

// Section configurations
const SECTIONS = {
  APTITUDE: {
    name: 'Aptitude',
    icon: Brain,
    color: 'text-accent',
    questions: 10,
    description: 'Logical reasoning and problem-solving questions',
    timePerQuestion: 90
  },
  EXCEL: {
    name: 'Excel Skills',
    icon: Calculator,
    color: 'text-primary',
    questions: 10,
    description: 'Excel formulas, functions, and data analysis',
    timePerQuestion: 120
  },
  SITUATIONAL: {
    name: 'Situational/Assignment',
    icon: ClipboardList,
    color: 'text-success',
    questions: 5,
    description: 'Real-world scenarios and file assignments',
    timePerQuestion: 300
  }
};

const QUESTION_POOLS = {
  APTITUDE: [
    {
      id: 'apt_1',
      question: 'If all Bloops are Razzles and all Razzles are Lazzles, then all Bloops are definitely Lazzles. Is this statement true or false?',
      type: 'objective',
      options: ['True', 'False'],
      followUpProbability: 0.3
    },
    {
      id: 'apt_2', 
      question: 'A train travels 240 miles in 3 hours. If it maintains the same speed, how long will it take to travel 400 miles?',
      type: 'objective',
      followUpProbability: 0.2
    },
    {
      id: 'apt_3',
      question: 'Complete the sequence: 2, 6, 12, 20, 30, ?',
      type: 'objective',
      followUpProbability: 0.4
    }
  ],
  EXCEL: [
    {
      id: 'excel_1',
      question: 'What Excel formula would you use to count the number of cells in range A1:A100 that contain values greater than 50?',
      type: 'text',
      followUpProbability: 0.5
    },
    {
      id: 'excel_2',
      question: 'How would you create a pivot table to analyze sales data by region and product category?',
      type: 'text',
      followUpProbability: 0.6
    },
    {
      id: 'excel_3',
      question: 'Explain the difference between VLOOKUP and INDEX-MATCH functions. When would you use each?',
      type: 'text',
      followUpProbability: 0.7
    }
  ],
  SITUATIONAL: [
    {
      id: 'sit_1',
      question: 'You receive a large dataset with inconsistent formatting and missing values. Walk me through your approach to clean and analyze this data.',
      type: 'multi-turn',
      followUpProbability: 0.8
    },
    {
      id: 'sit_2',
      question: 'Create a financial dashboard for monthly sales analysis. Upload your Excel file when complete.',
      type: 'assignment',
      requiresFile: true,
      followUpProbability: 0.9
    }
  ]
};

class ConversationInterviewWindow extends Component {
  constructor(props) {
    super(props);
    this.fileInputRef = React.createRef();
    this.chatEndRef = React.createRef();
    this.timerInterval = null;
    
    this.state = {
      // Session management
      sessionId: null,
      currentSection: 'APTITUDE',
      sectionProgress: { APTITUDE: 0, EXCEL: 0, SITUATIONAL: 0 },
      
      // Conversation state
      conversation: [],
      currentQuestion: null,
      awaitingResponse: false,
      
      // Timer and progress
      timeRemaining: 0,
      totalTimeElapsed: 0,
      
      // Answer state
      currentAnswer: '',
      uploadedFiles: [],
      
      // UI state
      isLoading: true,
      error: null,
      isSubmitting: false,
      isCompleted: false,
      
      // Session transcript for internal review
      sessionTranscript: {
        startTime: new Date(),
        sections: {},
        responses: [],
        evaluations: []
      }
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

  componentDidUpdate() {
    // Auto-scroll to bottom of conversation
    if (this.chatEndRef.current) {
      this.chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }

  initializeSession = async () => {
    try {
      // Real API call would be: const response = await axios.post('/api/sessions/');
      const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      
      this.setState({ 
        sessionId, 
        isLoading: false,
        sessionTranscript: {
          ...this.state.sessionTranscript,
          sessionId
        }
      });
      
      await this.startSection('APTITUDE');
    } catch (error) {
      this.setState({ 
        error: "Failed to initialize interview session. Please try again.", 
        isLoading: false 
      });
    }
  };

  startSection = async (sectionKey) => {
    const section = SECTIONS[sectionKey];
    
    // Add section introduction to conversation
    const introMessage = {
      id: `intro_${sectionKey}`,
      type: 'system',
      content: `Welcome to the ${section.name} section. ${section.description}. You'll have ${section.questions} questions with ${section.timePerQuestion} seconds each. Let's begin!`,
      timestamp: new Date(),
      section: sectionKey
    };

    this.setState(prevState => ({
      currentSection: sectionKey,
      conversation: [...prevState.conversation, introMessage],
      sessionTranscript: {
        ...prevState.sessionTranscript,
        sections: {
          ...prevState.sessionTranscript.sections,
          [sectionKey]: { startTime: new Date(), questions: [] }
        }
      }
    }));

    // Small delay for better UX
    setTimeout(() => {
      this.fetchNextQuestion();
    }, 1500);
  };

  fetchNextQuestion = async () => {
    const { sessionId, currentSection, sectionProgress } = this.state;
    
    if (!sessionId) return;

    try {
      this.setState({ isLoading: true });
      
      // Check if current section is complete
      const currentSectionInfo = SECTIONS[currentSection];
      if (sectionProgress[currentSection] >= currentSectionInfo.questions) {
        return this.proceedToNextSection();
      }

      // Real API call would be: 
      // const response = await axios.get(`/api/sessions/${sessionId}/messages`);
      
      // Simulate randomized question selection
      const questionPool = QUESTION_POOLS[currentSection];
      const randomQuestion = questionPool[Math.floor(Math.random() * questionPool.length)];
      
      const questionMessage = {
        id: `q_${Date.now()}`,
        type: 'question',
        content: randomQuestion.question,
        questionData: randomQuestion,
        timestamp: new Date(),
        section: currentSection
      };

      this.setState(prevState => ({
        conversation: [...prevState.conversation, questionMessage],
        currentQuestion: randomQuestion,
        awaitingResponse: true,
        timeRemaining: SECTIONS[currentSection].timePerQuestion,
        isLoading: false
      }));

      this.startTimer();
    } catch (error) {
      this.setState({ 
        error: "Failed to fetch next question. Please try again.", 
        isLoading: false 
      });
    }
  };

  proceedToNextSection = () => {
    const { currentSection } = this.state;
    
    if (currentSection === 'APTITUDE') {
      this.startSection('EXCEL');
    } else if (currentSection === 'EXCEL') {
      this.startSection('SITUATIONAL');
    } else {
      this.completeInterview();
    }
  };

  completeInterview = async () => {
    const { sessionId } = this.state;
    
    try {
      // Real API call would be:
      // const response = await axios.get(`/api/sessions/${sessionId}/evaluation`);
      
      this.setState({ isCompleted: true });
      // Navigate to completion page in real app
      window.location.href = "/completion";
    } catch (error) {
      this.setState({ error: "Failed to complete interview. Please try again." });
    }
  };

  startTimer = () => {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
    }

    this.timerInterval = setInterval(() => {
      this.setState(prevState => {
        const newTimeRemaining = prevState.timeRemaining - 1;
        const newTotalTimeElapsed = prevState.totalTimeElapsed + 1;
        
        if (newTimeRemaining <= 0) {
          this.handleAutoSubmit();
          return { 
            timeRemaining: 0, 
            totalTimeElapsed: newTotalTimeElapsed 
          };
        }
        
        return { 
          timeRemaining: newTimeRemaining,
          totalTimeElapsed: newTotalTimeElapsed
        };
      });
    }, 1000);
  };

  handleAutoSubmit = () => {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
    }
    this.submitResponse(true);
  };

  submitResponse = async (isAutoSubmit = false) => {
    const { 
      sessionId, 
      currentQuestion, 
      currentAnswer, 
      uploadedFiles, 
      currentSection,
      sectionProgress 
    } = this.state;
    
    if (!sessionId || !currentQuestion) return;

    try {
      this.setState({ isSubmitting: true });

      // Create response message
      const responseMessage = {
        id: `resp_${Date.now()}`,
        type: 'response',
        content: currentAnswer || (isAutoSubmit ? '[Time expired - no response]' : ''),
        files: uploadedFiles.map(f => ({ name: f.name, size: f.size })),
        timestamp: new Date(),
        section: currentSection,
        isAutoSubmit
      };

      // Real API call would be:
      // const formData = new FormData();
      // formData.append('message', JSON.stringify(responseMessage));
      // uploadedFiles.forEach(file => formData.append('files', file));
      // const response = await axios.post(`/api/sessions/${sessionId}/messages`, formData);

      // Update conversation and progress
      this.setState(prevState => ({
        conversation: [...prevState.conversation, responseMessage],
        sectionProgress: {
          ...prevState.sectionProgress,
          [currentSection]: prevState.sectionProgress[currentSection] + 1
        },
        currentAnswer: '',
        uploadedFiles: [],
        awaitingResponse: false,
        isSubmitting: false,
        sessionTranscript: {
          ...prevState.sessionTranscript,
          responses: [...prevState.sessionTranscript.responses, responseMessage]
        }
      }));

      // Check for follow-up questions
      if (currentQuestion.followUpProbability && Math.random() < currentQuestion.followUpProbability) {
        setTimeout(() => this.generateFollowUp(), 1000);
      } else {
        setTimeout(() => this.fetchNextQuestion(), 1000);
      }
    } catch (error) {
      this.setState({ 
        error: "Failed to submit response. Please try again.",
        isSubmitting: false
      });
    }
  };

  generateFollowUp = () => {
    const { currentSection } = this.state;
    
    const followUpQuestions = {
      APTITUDE: [
        "Can you explain your reasoning for that answer?",
        "What alternative approach could you have taken?",
        "How confident are you in your response on a scale of 1-10?"
      ],
      EXCEL: [
        "What would happen if the data range was dynamic?",
        "How would you handle errors in this formula?",
        "Can you suggest a more efficient alternative?"
      ],
      SITUATIONAL: [
        "What challenges might you encounter with this approach?",
        "How would you communicate this to stakeholders?",
        "What would be your backup plan if this doesn't work?"
      ]
    };

    const followUps = followUpQuestions[currentSection];
    const randomFollowUp = followUps[Math.floor(Math.random() * followUps.length)];

    const followUpMessage = {
      id: `followup_${Date.now()}`,
      type: 'followup',
      content: randomFollowUp,
      timestamp: new Date(),
      section: currentSection
    };

    this.setState(prevState => ({
      conversation: [...prevState.conversation, followUpMessage],
      currentQuestion: { ...prevState.currentQuestion, isFollowUp: true },
      awaitingResponse: true,
      timeRemaining: 60 // Shorter time for follow-ups
    }));

    this.startTimer();
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

  getTotalProgress = () => {
    const { sectionProgress } = this.state;
    const totalQuestions = Object.values(SECTIONS).reduce((sum, section) => sum + section.questions, 0);
    const completedQuestions = Object.values(sectionProgress).reduce((sum, count) => sum + count, 0);
    return (completedQuestions / totalQuestions) * 100;
  };

  renderConversationMessage = (message) => {
    const isBot = message.type === 'system' || message.type === 'question' || message.type === 'followup';
    const section = SECTIONS[message.section];
    const SectionIcon = section?.icon || MessageSquare;

    return (
      <div key={message.id} className={`flex gap-3 mb-4 ${isBot ? 'justify-start' : 'justify-end'}`}>
        {isBot && (
          <div className="flex-shrink-0">
            <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
              <Bot className="w-4 h-4 text-primary" />
            </div>
          </div>
        )}
        
        <div className={`max-w-[80%] ${isBot ? 'order-2' : 'order-1'}`}>
          <div className={`rounded-lg p-3 ${
            isBot 
              ? 'bg-muted text-muted-foreground' 
              : 'bg-primary text-primary-foreground'
          }`}>
            {message.type === 'system' && (
              <div className="flex items-center gap-2 mb-2">
                <SectionIcon className={`w-4 h-4 ${section?.color}`} />
                <Badge variant="secondary" className="text-xs">
                  {section?.name}
                </Badge>
              </div>
            )}
            
            <p className="text-sm leading-relaxed">{message.content}</p>
            
            {message.files && message.files.length > 0 && (
              <div className="mt-2 pt-2 border-t border-current/20">
                <p className="text-xs opacity-75">Attached files:</p>
                {message.files.map((file, index) => (
                  <div key={index} className="text-xs opacity-75">
                    📎 {file.name} ({(file.size / 1024).toFixed(1)} KB)
                  </div>
                ))}
              </div>
            )}
          </div>
          
          <div className="text-xs text-muted-foreground mt-1">
            {message.timestamp.toLocaleTimeString()}
          </div>
        </div>
        
        {!isBot && (
          <div className="flex-shrink-0 order-2">
            <div className="w-8 h-8 rounded-full bg-accent/10 flex items-center justify-center">
              <User className="w-4 h-4 text-accent" />
            </div>
          </div>
        )}
      </div>
    );
  };

  render() {
    const { 
      conversation,
      currentSection,
      sectionProgress,
      timeRemaining, 
      currentAnswer, 
      uploadedFiles, 
      isLoading, 
      error, 
      isSubmitting,
      awaitingResponse,
      currentQuestion
    } = this.state;

    const currentSectionInfo = SECTIONS[currentSection];
    const isTimeWarning = timeRemaining <= 30;
    const isTimeCritical = timeRemaining <= 10;

    if (isLoading && conversation.length === 0) {
      return (
        <div className="min-h-screen bg-background flex items-center justify-center">
          <Card className="w-96 shadow-medium">
            <CardContent className="p-8 text-center">
              <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4"></div>
              <p>Initializing your interview session...</p>
            </CardContent>
          </Card>
        </div>
      );
    }

    return (
      <div className="min-h-screen bg-background">
        {/* Header */}
        <header className="bg-secondary/30 border-b sticky top-0 z-10">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <MessageSquare className="w-6 h-6 text-primary" />
                  <span className="font-semibold">AI Mock Interview</span>
                </div>
                
                {/* Section indicators */}
                <div className="flex space-x-2">
                  {Object.entries(SECTIONS).map(([key, section]) => {
                    const SectionIcon = section.icon;
                    const isActive = key === currentSection;
                    const isCompleted = sectionProgress[key] >= section.questions;
                    
                    return (
                      <div 
                        key={key}
                        className={`flex items-center space-x-1 px-2 py-1 rounded text-xs ${
                          isActive ? 'bg-primary text-primary-foreground' :
                          isCompleted ? 'bg-success text-success-foreground' :
                          'bg-muted text-muted-foreground'
                        }`}
                      >
                        <SectionIcon className="w-3 h-3" />
                        <span>{section.name}</span>
                        <span>({sectionProgress[key]}/{section.questions})</span>
                      </div>
                    );
                  })}
                </div>
              </div>
              
              {awaitingResponse && (
                <div className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-mono text-lg ${
                  isTimeCritical ? 'bg-destructive text-destructive-foreground' :
                  isTimeWarning ? 'bg-warning text-warning-foreground' :
                  'bg-card text-foreground'
                }`}>
                  <Clock className="w-5 h-5" />
                  <span>{this.formatTime(timeRemaining)}</span>
                </div>
              )}
            </div>
            
            <div className="mt-4">
              <Progress value={this.getTotalProgress()} className="h-2" />
              <div className="flex justify-between text-xs text-muted-foreground mt-1">
                <span>Overall Progress</span>
                <span>{Math.round(this.getTotalProgress())}% Complete</span>
              </div>
            </div>
          </div>
        </header>

        <main className="container mx-auto px-4 py-4 max-w-4xl">
          {error && (
            <Alert className="mb-4 border-destructive bg-destructive/10">
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {/* Conversation Area */}
          <Card className="h-[60vh] flex flex-col shadow-soft">
            <CardHeader className="pb-4">
              <CardTitle className="text-lg flex items-center gap-2">
                <MessageSquare className="w-5 h-5" />
                Interview Conversation
              </CardTitle>
            </CardHeader>
            
            <CardContent className="flex-1 overflow-y-auto p-4">
              {conversation.map(message => this.renderConversationMessage(message))}
              
              {isLoading && (
                <div className="flex gap-3 mb-4">
                  <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                    <Bot className="w-4 h-4 text-primary" />
                  </div>
                  <div className="bg-muted rounded-lg p-3">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={this.chatEndRef} />
            </CardContent>
          </Card>

          {/* Response Area */}
          {awaitingResponse && currentQuestion && (
            <Card className="mt-4 shadow-soft">
              <CardContent className="p-6">
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="answer" className="text-base font-medium">Your Response</Label>
                    <Textarea
                      id="answer"
                      value={currentAnswer}
                      onChange={(e) => this.setState({ currentAnswer: e.target.value })}
                      placeholder="Type your response here..."
                      className="mt-2 min-h-[100px] resize-y"
                      disabled={isSubmitting}
                    />
                  </div>

                  {/* File Upload for Assignment Questions */}
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
                  <div className="flex justify-end">
                    <Button
                      variant="interview"
                      size="lg"
                      onClick={() => this.submitResponse()}
                      disabled={
                        isSubmitting || 
                        (!currentAnswer.trim() && (!currentQuestion.requiresFile || uploadedFiles.length === 0))
                      }
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
                          Send Response
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Time Warning */}
          {awaitingResponse && isTimeWarning && (
            <Alert className={`mt-4 ${isTimeCritical ? 'border-destructive bg-destructive/10' : 'border-warning bg-warning/10'}`}>
              <Clock className="h-4 w-4" />
              <AlertDescription>
                {isTimeCritical 
                  ? "⚠️ Less than 10 seconds remaining! Your response will be auto-submitted."
                  : "⏰ Less than 30 seconds remaining. Please finalize your response."
                }
              </AlertDescription>
            </Alert>
          )}
        </main>
      </div>
    );
  }
}

export default ConversationInterviewWindow;