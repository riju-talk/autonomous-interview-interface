import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { 
  CheckCircle, 
  Award, 
  TrendingUp, 
  FileSpreadsheet, 
  Brain, 
  Upload,
  Star,
  Download,
  Home
} from "lucide-react";

const Completion = () => {
  const navigate = useNavigate();
  const [scoreData, setScoreData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate fetching final results
    const fetchResults = async () => {
      try {
        // In real app: const response = await axios.get(`/api/sessions/${sessionId}/finish`);
        
        // Mock score data
        const mockResults = {
          totalScore: 342,
          maxScore: 400,
          excelScore: 168,
          behavioralScore: 94,
          assignmentScore: 80,
          completionTime: 45,
          strengths: [
            "Strong Excel formula knowledge",
            "Excellent problem-solving approach",
            "Clear communication skills",
            "Efficient pivot table creation"
          ],
          improvements: [
            "Advanced charting techniques",
            "VBA/Macro understanding",
            "Complex data modeling",
            "Time management under pressure"
          ],
          grade: "B+"
        };

        // Simulate API delay
        setTimeout(() => {
          setScoreData(mockResults);
          setIsLoading(false);
        }, 1500);
      } catch (error) {
        setIsLoading(false);
      }
    };

    fetchResults();
  }, []);

  const getGradeColor = (grade) => {
    switch (grade) {
      case 'A+':
      case 'A': return 'text-success';
      case 'A-':
      case 'B+': return 'text-primary';
      case 'B':
      case 'B-': return 'text-accent';
      case 'C+':
      case 'C': return 'text-warning';
      default: return 'text-destructive';
    }
  };

  const getPerformanceLevel = (percentage) => {
    if (percentage >= 90) return { label: "Excellent", color: "bg-success" };
    if (percentage >= 80) return { label: "Very Good", color: "bg-primary" };
    if (percentage >= 70) return { label: "Good", color: "bg-accent" };
    if (percentage >= 60) return { label: "Fair", color: "bg-warning" };
    return { label: "Needs Improvement", color: "bg-destructive" };
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Card className="w-96 shadow-medium">
          <CardContent className="p-8 text-center">
            <div className="animate-spin w-12 h-12 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4"></div>
            <h3 className="text-lg font-semibold mb-2">Calculating Your Results</h3>
            <p className="text-muted-foreground">Our AI is analyzing your responses...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!scoreData) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Card className="w-96 shadow-medium">
          <CardContent className="p-8 text-center">
            <h3 className="text-lg font-semibold mb-2">Unable to Load Results</h3>
            <p className="text-muted-foreground mb-4">There was an error retrieving your assessment results.</p>
            <Button onClick={() => navigate("/")}>Return to Home</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const overallPercentage = (scoreData.totalScore / scoreData.maxScore) * 100;
  const excelPercentage = (scoreData.excelScore / 200) * 100; // 20 questions * 10 points
  const behavioralPercentage = (scoreData.behavioralScore / 150) * 100; // 15 questions * 10 points
  const assignmentPercentage = (scoreData.assignmentScore / 50) * 100; // 5 questions * 10 points

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-secondary">
      {/* Header */}
      <header className="bg-card/80 backdrop-blur-sm border-b sticky top-0 z-10">
        <div className="container mx-auto px-4 py-6">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 mb-2">
              <Award className="w-8 h-8 text-primary" />
              <h1 className="text-3xl font-bold">Assessment Complete!</h1>
            </div>
            <p className="text-muted-foreground">Your Excel interview assessment results</p>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Overall Score Card */}
        <Card className="mb-8 bg-gradient-to-r from-primary/10 to-accent/10 border-primary/20 shadow-medium">
          <CardContent className="p-8">
            <div className="text-center mb-6">
              <div className="flex items-center justify-center space-x-4 mb-4">
                <div className={`text-6xl font-bold ${getGradeColor(scoreData.grade)}`}>
                  {scoreData.grade}
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-foreground">
                    {scoreData.totalScore}/{scoreData.maxScore}
                  </div>
                  <div className="text-sm text-muted-foreground">Total Points</div>
                </div>
              </div>
              
              <div className="mb-4">
                <Progress value={overallPercentage} className="h-3 mb-2" />
                <div className="flex justify-between text-sm">
                  <span>Overall Performance</span>
                  <span className="font-medium">{overallPercentage.toFixed(1)}%</span>
                </div>
              </div>

              <Badge variant="secondary" className="px-4 py-2 text-base">
                {getPerformanceLevel(overallPercentage).label}
              </Badge>
            </div>

            <div className="grid md:grid-cols-3 gap-6 text-center">
              <div>
                <TrendingUp className="w-8 h-8 text-success mx-auto mb-2" />
                <div className="font-semibold text-lg">{scoreData.completionTime} min</div>
                <div className="text-sm text-muted-foreground">Completion Time</div>
              </div>
              <div>
                <Star className="w-8 h-8 text-primary mx-auto mb-2" />
                <div className="font-semibold text-lg">{scoreData.strengths.length}</div>
                <div className="text-sm text-muted-foreground">Key Strengths</div>
              </div>
              <div>
                <CheckCircle className="w-8 h-8 text-accent mx-auto mb-2" />
                <div className="font-semibold text-lg">40/40</div>
                <div className="text-sm text-muted-foreground">Questions Answered</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Detailed Scores */}
        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          <Card className="shadow-soft">
            <CardHeader className="pb-4">
              <CardTitle className="flex items-center space-x-2">
                <FileSpreadsheet className="w-5 h-5 text-primary" />
                <span>Excel Technical</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm">Score</span>
                    <span className="font-medium">{scoreData.excelScore}/200</span>
                  </div>
                  <Progress value={excelPercentage} className="h-2" />
                  <div className="text-right text-xs text-muted-foreground mt-1">
                    {excelPercentage.toFixed(1)}%
                  </div>
                </div>
                <Badge variant="outline" className={getPerformanceLevel(excelPercentage).color + " text-white"}>
                  {getPerformanceLevel(excelPercentage).label}
                </Badge>
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-soft">
            <CardHeader className="pb-4">
              <CardTitle className="flex items-center space-x-2">
                <Brain className="w-5 h-5 text-accent" />
                <span>Behavioral</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm">Score</span>
                    <span className="font-medium">{scoreData.behavioralScore}/150</span>
                  </div>
                  <Progress value={behavioralPercentage} className="h-2" />
                  <div className="text-right text-xs text-muted-foreground mt-1">
                    {behavioralPercentage.toFixed(1)}%
                  </div>
                </div>
                <Badge variant="outline" className={getPerformanceLevel(behavioralPercentage).color + " text-white"}>
                  {getPerformanceLevel(behavioralPercentage).label}
                </Badge>
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-soft">
            <CardHeader className="pb-4">
              <CardTitle className="flex items-center space-x-2">
                <Upload className="w-5 h-5 text-success" />
                <span>Assignments</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm">Score</span>
                    <span className="font-medium">{scoreData.assignmentScore}/50</span>
                  </div>
                  <Progress value={assignmentPercentage} className="h-2" />
                  <div className="text-right text-xs text-muted-foreground mt-1">
                    {assignmentPercentage.toFixed(1)}%
                  </div>
                </div>
                <Badge variant="outline" className={getPerformanceLevel(assignmentPercentage).color + " text-white"}>
                  {getPerformanceLevel(assignmentPercentage).label}
                </Badge>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Strengths and Improvements */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <Card className="shadow-soft">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Star className="w-5 h-5 text-success" />
                <span>Key Strengths</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {scoreData.strengths.map((strength, index) => (
                  <li key={index} className="flex items-start space-x-2">
                    <CheckCircle className="w-4 h-4 text-success mt-1 flex-shrink-0" />
                    <span className="text-sm">{strength}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          <Card className="shadow-soft">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <TrendingUp className="w-5 h-5 text-primary" />
                <span>Areas for Improvement</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {scoreData.improvements.map((improvement, index) => (
                  <li key={index} className="flex items-start space-x-2">
                    <TrendingUp className="w-4 h-4 text-primary mt-1 flex-shrink-0" />
                    <span className="text-sm">{improvement}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </div>

        {/* Action Buttons */}
        <div className="text-center space-y-4">
          <div className="space-x-4">
            <Button variant="outline" size="lg" className="px-8">
              <Download className="w-4 h-4 mr-2" />
              Download Report
            </Button>
            <Button variant="hero" size="lg" onClick={() => navigate("/")} className="px-8">
              <Home className="w-4 h-4 mr-2" />
              Return to Home
            </Button>
          </div>
          <p className="text-xs text-muted-foreground max-w-md mx-auto">
            Thank you for completing the Excel Interview Assessment. Use these results to identify your strengths and areas for professional development.
          </p>
        </div>
      </main>
    </div>
  );
};

export default Completion;