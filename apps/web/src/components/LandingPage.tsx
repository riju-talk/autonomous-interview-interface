import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { CheckCircle, Clock, FileSpreadsheet, Brain, Award } from "lucide-react";

const LandingPage = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <FileSpreadsheet className="w-8 h-8" />,
      title: "Excel Mastery",
      description: "Test your Excel skills with 20 comprehensive questions covering formulas, functions, and data analysis."
    },
    {
      icon: <Brain className="w-8 h-8" />,
      title: "Behavioral Assessment",
      description: "15 aptitude and behavioral questions to evaluate your problem-solving and communication skills."
    },
    {
      icon: <Award className="w-8 h-8" />,
      title: "Practical Assignment",
      description: "5 hands-on assignments with real Excel files to demonstrate your practical expertise."
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-secondary">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <FileSpreadsheet className="w-8 h-8 text-primary" />
            <h1 className="text-2xl font-bold text-foreground">Excel Interview AI</h1>
          </div>
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <Clock className="w-4 h-4" />
            <span>45-60 minutes</span>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="container mx-auto px-4 py-12">
        <div className="text-center max-w-4xl mx-auto mb-16">
          <h2 className="text-5xl font-bold text-foreground mb-6">
            Master Your Excel Interview
          </h2>
          <p className="text-xl text-muted-foreground mb-8 leading-relaxed">
            Prepare for your next job interview with our AI-powered Excel assessment platform. 
            Get real-time evaluation and personalized feedback on your Excel skills.
          </p>
          <Button 
            variant="hero" 
            size="lg" 
            onClick={() => navigate("/instructions")}
            className="text-lg px-12 py-6 h-auto"
          >
            Start Interview Assessment
          </Button>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {features.map((feature, index) => (
            <Card key={index} className="bg-card border-0 shadow-soft hover:shadow-medium transition-all duration-300">
              <CardContent className="p-8 text-center">
                <div className="text-primary mb-4 flex justify-center">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Assessment Overview */}
        <Card className="bg-gradient-to-r from-accent/10 to-primary/10 border-primary/20 shadow-medium">
          <CardContent className="p-8">
            <h3 className="text-2xl font-bold text-center mb-8">Assessment Overview</h3>
            <div className="grid md:grid-cols-3 gap-8 text-center">
              <div>
                <div className="text-3xl font-bold text-primary mb-2">40</div>
                <div className="text-sm text-muted-foreground">Total Questions</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-accent mb-2">60</div>
                <div className="text-sm text-muted-foreground">Minutes Duration</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-success mb-2">AI</div>
                <div className="text-sm text-muted-foreground">Powered Evaluation</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Process Steps */}
        <div className="mt-16">
          <h3 className="text-2xl font-bold text-center mb-8">How It Works</h3>
          <div className="grid md:grid-cols-4 gap-6">
            {[
              { step: "1", title: "Read Instructions", desc: "Review the assessment process" },
              { step: "2", title: "Answer Questions", desc: "Complete Excel and behavioral questions" },
              { step: "3", title: "Upload Files", desc: "Submit your assignment work" },
              { step: "4", title: "Get Results", desc: "Receive your comprehensive score" }
            ].map((item, index) => (
              <div key={index} className="text-center">
                <div className="w-12 h-12 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-lg font-bold mx-auto mb-4">
                  {item.step}
                </div>
                <h4 className="font-semibold mb-2">{item.title}</h4>
                <p className="text-sm text-muted-foreground">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-secondary/50 mt-20 py-8">
        <div className="container mx-auto px-4 text-center text-muted-foreground">
          <p>&copy; 2024 Excel Interview AI. Powered by artificial intelligence.</p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;