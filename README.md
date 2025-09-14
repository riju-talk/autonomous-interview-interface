# Autonomous Interview Interface

A modern, AI-powered interview platform that provides a seamless interview experience with real-time feedback and evaluation.

## 🚀 Features

- **Interactive Interview Interface**: Clean, responsive UI for conducting interviews
- **Real-time Feedback**: Get instant feedback on your responses
- **Question Timer**: Per-question timing with auto-submission
- **Session Persistence**: Never lose your progress with auto-save functionality
- **Comprehensive Evaluation**: Detailed feedback and scoring
- **Modern Tech Stack**: Built with React, Vite, FastAPI, and more

## 🏗️ Project Structure

```
autonomous-interview-interface/
├── apps/
│   ├── web/              # Frontend application (React + Vite)
│   └── api/              # Backend API (FastAPI)
├── packages/             # Shared packages and configurations
│   ├── eslint-config/    # ESLint configuration
│   ├── typescript-config/# TypeScript configuration
│   └── ui/               # Shared UI components
├── scripts/              # Utility scripts
├── .env.example          # Environment variables example
├── docker-compose.yml    # Docker Compose configuration
└── Makefile              # Development tasks and utilities
```

## 🚀 Quick Start

### Prerequisites

- [Node.js](https://nodejs.org/) 18+ (LTS recommended)
- [Yarn](https://yarnpkg.com/) 1.22+ or npm 8+
- [Python](https://www.python.org/) 3.9+
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/)

### 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/autonomous-interview-interface.git
   cd autonomous-interview-interface
   ```

2. **Install dependencies**:
   ```bash
   # Install root dependencies
   yarn install
   
   # Install and build all project dependencies
   make install
   ```

3. **Set up environment variables**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Update the .env file with your configuration
   # At minimum, update these values:
   # - SECRET_KEY
   # - DATABASE_URL (if not using default Docker setup)
   # - Any API keys for LLM providers (OpenAI, Anthropic, etc.)
   ```

### 🚦 Running the Application

#### Development Mode

```bash
# Start all services (web, api, database, redis, etc.)
make dev

# Or start services individually
make dev-web    # Frontend only (http://localhost:3000)
make dev-api    # API only (http://localhost:8000)
```

#### Production Mode

```bash
# Build the application
make build

# Start all services in production mode
make start

# Stop all services
make stop
```

### 🔍 Access the Application

- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Base URL**: http://localhost:8000/api/v1

## 🧪 Testing

Run the test suite with:

```bash
# Run all tests
make test

# Run web frontend tests
make test-web

# Run API tests
make test-api

# Generate test coverage report
cd apps/api && yarn test:cov
```

## 🧹 Maintenance

```bash
# Format code
make format

# Lint code
make lint

# Clean build artifacts
make clean
```

## 🐳 Docker

### Development

```bash
# Build and start all services
docker-compose up --build

# Stop all services
docker-compose down
```

### Production

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start production services
docker-compose -f docker-compose.prod.yml up -d
```

## 🚀 Development

### Available Scripts

Use the Makefile to run common development tasks:

```bash
# Install dependencies
make install       # Install all dependencies
make install-web   # Install web dependencies
make install-api   # Install API dependencies

# Development servers
make dev           # Start all services in development mode
make dev-web       # Start web frontend only
make dev-api       # Start API server only

# Testing
make test          # Run all tests
make test-web      # Run web frontend tests
make test-api      # Run API tests

# Linting & Formatting
make lint          # Run all linters
make format        # Format all code

# Build for production
make build         # Build all services
make build-web     # Build web frontend
make build-api     # Build API

# Production
make start         # Start all services in production mode
make stop          # Stop all services

# Cleanup
make clean         # Remove build artifacts and dependencies
```

## 🏗️ Project Structure

### Frontend (apps/web)

- `src/` - Application source code
  - `components/` - Reusable UI components
  - `hooks/` - Custom React hooks
  - `pages/` - Next.js pages
  - `styles/` - Global styles and themes
  - `utils/` - Utility functions

### Backend (apps/api)

- `app/` - Application source code
  - `api/` - API endpoints
  - `core/` - Core application logic
  - `models/` - Database models
  - `services/` - Business logic
  - `utils/` - Utility functions

## 📦 Dependencies

### Frontend

- React 18
- Vite
- Radix UI
- Tailwind CSS
- Axios

### Backend

- FastAPI
- SQLAlchemy
- Alembic (for database migrations)
- Pydantic
- Uvicorn

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Radix UI](https://www.radix-ui.com/) for accessible UI primitives
- [Vite](https://vitejs.dev/) for fast frontend tooling
- [FastAPI](https://fastapi.tiangolo.com/) for the high-performance API framework

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
