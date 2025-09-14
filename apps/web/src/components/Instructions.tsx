import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { CheckCircle, Clock, FileSpreadsheet, AlertTriangle, Upload } from "lucide-react";

const Instructions = () => {
  const navigate = useNavigate();

  const questionTypes = [
    {
      icon: <FileSpreadsheet className="w-6 h-6 text-primary" />,
      title: "Excel Questions (20)",
      items: [
        "Formula creation and modification",
        "Data analysis and pivot tables",
        "Chart creation and formatting",
        "Function usage (VLOOKUP, INDEX/MATCH, etc.)",
        "Data validation and conditional formatting"
      ]
    },
    {
      icon: <CheckCircle className="w-6 h-6 text-accent" />,
      title: "Aptitude & Behavioral (15)",
      items: [
        "Problem-solving scenarios",
        "Communication and teamwork",
        "Time management situations",
        "Technical reasoning",
        "Professional judgment calls"
      ]
    },
    {
      icon: <Upload className="w-6 h-6 text-success" />,
      title: "Practical Assignments (5)",
      items: [
        "Excel file manipulation tasks",
        "Data cleaning and preparation",
        "Report generation from raw data",
        "Dashboard creation",
        "Advanced formula implementation"
      ]
    }
  ];

  const importantNotes = [
    "Each question has a time limit - manage your time wisely",
    "You can upload CSV or XLSX files for assignment questions",
    "Questions are presented in random order",
    "Some questions may have follow-up prompts",
    "Your session will auto-save progress",
    "Final results include detailed scoring breakdown"
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-secondary/30 border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <FileSpreadsheet className="w-8 h-8 text-primary" />
              <div>
                <h1 className="text-2xl font-bold text-foreground">Excel Interview Assessment</h1>
                <p className="text-sm text-muted-foreground">Instructions and Guidelines</p>
              </div>
            </div>
            <div className="flex items-center space-x-2 bg-card px-4 py-2 rounded-lg shadow-soft">
              <Clock className="w-4 h-4 text-primary" />
              <span className="font-medium">Total Duration: 45-60 minutes</span>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Overview Alert */}
        <Alert className="mb-8 border-primary/20 bg-primary/5">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription className="text-base">
            <strong>Important:</strong> This assessment consists of 40 questions total. Please read these instructions carefully before beginning.
            Once started, you cannot pause the assessment.
          </AlertDescription>
        </Alert>

        {/* Question Types */}
        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          {questionTypes.map((type, index) => (
            <Card key={index} className="shadow-soft hover:shadow-medium transition-all duration-300">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center space-x-3">
                  {type.icon}
                  <span>{type.title}</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {type.items.map((item, idx) => (
                    <li key={idx} className="flex items-start space-x-2 text-sm">
                      <CheckCircle className="w-4 h-4 text-success mt-0.5 flex-shrink-0" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Assessment Rules */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <Card className="shadow-soft">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Clock className="w-5 h-5 text-warning" />
                <span>Timing & Navigation</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between py-2 border-b border-border">
                <span className="text-sm">Per Question Timer</span>
                <span className="font-medium">2-5 minutes</span>
              </div>
              <div className="flex justify-between py-2 border-b border-border">
                <span className="text-sm">Assignment Questions</span>
                <span className="font-medium">10-15 minutes</span>
              </div>
              <div className="flex justify-between py-2">
                <span className="text-sm">Total Time Limit</span>
                <span className="font-medium text-warning">60 minutes max</span>
              </div>
              <Alert className="mt-4">
                <AlertDescription className="text-xs">
                  Questions auto-submit when time expires. Manage your time carefully.
                </AlertDescription>
              </Alert>
            </CardContent>
          </Card>

          <Card className="shadow-soft">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Upload className="w-5 h-5 text-success" />
                <span>File Upload Guidelines</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-success" />
                  <span className="text-sm">Supported: .csv, .xlsx, .xls</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-success" />
                  <span className="text-sm">Maximum file size: 10MB</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-success" />
                  <span className="text-sm">Multiple files allowed per question</span>
                </div>
              </div>
              <Alert className="mt-4">
                <AlertDescription className="text-xs">
                  Ensure your files are properly formatted before uploading.
                </AlertDescription>
              </Alert>
            </CardContent>
          </Card>
        </div>

        {/* Important Notes */}
        <Card className="mb-8 shadow-soft">
          <CardHeader>
            <CardTitle>Important Notes & Tips</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-4">
              {importantNotes.map((note, index) => (
                <div key={index} className="flex items-start space-x-2">
                  <AlertTriangle className="w-4 h-4 text-warning mt-1 flex-shrink-0" />
                  <span className="text-sm">{note}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Technical Requirements */}
        <Card className="mb-8 bg-muted/30">
          <CardHeader>
            <CardTitle>Technical Requirements</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-4 text-sm">
              <div>
                <h4 className="font-medium mb-2">Browser</h4>
                <p className="text-muted-foreground">Chrome, Firefox, Safari, or Edge (latest versions)</p>
              </div>
              <div>
                <h4 className="font-medium mb-2">Connection</h4>
                <p className="text-muted-foreground">Stable internet connection required</p>
              </div>
              <div>
                <h4 className="font-medium mb-2">Files</h4>
                <p className="text-muted-foreground">JavaScript enabled, file upload permissions</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Action Buttons */}
        <div className="text-center space-y-4">
          <div className="space-x-4">
            <Button 
              variant="outline" 
              onClick={() => navigate("/")}
              className="px-8"
            >
              Back to Home
            </Button>
            <Button 
              variant="hero" 
              size="lg"
              onClick={() => navigate("/interview")}
              className="px-12 py-6 h-auto text-lg"
            >
              Begin Assessment
            </Button>
          </div>
          <p className="text-xs text-muted-foreground max-w-md mx-auto">
            By clicking "Begin Assessment", you acknowledge that you have read and understood 
            these instructions and are ready to start your Excel interview assessment.
          </p>
        </div>
      </main>
    </div>
  );
};

export default Instructions;