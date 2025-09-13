# AI-Powered Interview System

A multi-modal AI agent that conducts interviews and evaluates responses with support for text, audio, and image inputs.

## 🚀 Features

- **Interviewer Agent**: Adaptive questioning based on user responses
- **Evaluator Agent**: Comprehensive evaluation based on custom rubrics
- **Multi-modal Support**: Text, audio, and image inputs
- **Modern Tech Stack**: Next.js, FastAPI, LangChain, and more
- **Scalable Architecture**: Containerized with Docker and Kubernetes-ready

## 🏗️ Project Structure

```
interview-ai-agent/
├── frontend/             # Next.js + shadcn/ui
├── backend/              # FastAPI + LangChain
├── database/            # Postgres + Supabase
├── mlops/               # MLflow + pipelines
├── .github/             # CI/CD workflows
└── docs/                # Documentation
```

## 🛠️ Development Setup

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ and npm/yarn
- Python 3.11+

### Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/interview-ai-agent.git
   cd interview-ai-agent
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Update the .env file with your configuration
   ```

3. Start the services:
   ```bash
   docker-compose up -d
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - MLflow UI: http://localhost:5000

## 📚 Documentation

For detailed documentation, please refer to:
- [Architecture](./docs/ARCHITECTURE.md)
- [API Documentation](./docs/API.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](./CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
