# Autonomous Interview Interface

A modern, AI-powered interview platform that provides a seamless interview experience with real-time feedback and evaluation. This full-stack application features a React/Next.js frontend and FastAPI backend, with PostgreSQL, Redis, and ChromaDB for data storage and vector search.

## 🚀 Features

- **Interactive Interview Interface**: Clean, responsive UI for conducting interviews
- **Real-time Feedback**: Get instant feedback on your responses
- **Question Timer**: Per-question timing with auto-submission
- **Session Persistence**: Never lose your progress with auto-save functionality
- **Comprehensive Evaluation**: Detailed feedback and scoring
- **Modern Tech Stack**: Built with Next.js, FastAPI, PostgreSQL, Redis, and ChromaDB
- **Containerized Development**: Easy setup with Docker Compose
- **Authentication**: Secure user authentication system

## 🏗️ Project Structure

```
autonomous-interview-interface/
├── apps/
│   ├── web/              # Frontend application (Next.js + TypeScript)
│   └── api/              # Backend API (FastAPI + Python)
│       ├── app/          # FastAPI application code
│       │   ├── api/      # API endpoints
│       │   ├── core/     # Core application logic
│       │   ├── models/   # Database models
│       │   └── services/ # Business logic
│       └── requirements.txt
├── packages/             # Shared packages and configurations
│   ├── eslint-config/    # ESLint configuration
│   ├── typescript-config/# TypeScript configuration
│   └── ui/              # Shared UI components
├── scripts/             # Utility scripts
│   ├── init-chroma.sh   # ChromaDB initialization
│   └── init-db.sh       # Database setup and sample data
├── docker-compose.yml   # Development Docker Compose configuration
├── docker-compose.prod.yml # Production Docker Compose configuration
└── .env.example         # Environment variables example
```

## 🚀 Quick Start

### Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- [Node.js](https://nodejs.org/) 18+ (LTS recommended) - for local development
- [Python](https://www.python.org/) 3.9+ - for local development
- [Git](https://git-scm.com/)

### 🐳 Development with Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/autonomous-interview-interface.git
   cd autonomous-interview-interface
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file and update the necessary values.

3. **Start the services**:
   ```bash
   docker-compose up -d
   ```
   This will start:
   - API server on http://localhost:8000
   - PostgreSQL database on port 5432
   - Redis on port 6379
   - ChromaDB on port 8001
   - PgAdmin on http://localhost:5050

4. **Access the application**:
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs
   - PgAdmin: http://localhost:5050

### 🛠️ Local Development Setup

#### Backend Setup

1. **Set up Python virtual environment**:
   ```bash
   cd apps/api
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   # OR
   source venv/bin/activate  # macOS/Linux
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Install Node.js dependencies**:
   ```bash
   cd ../../apps/web
   yarn install
   ```

2. **Start the development server**:
   ```bash
   yarn dev
   ```

## 🛠️ Services

### Backend API (FastAPI)
- **Port**: 8000
- **Documentation**: Available at `/docs` (Swagger UI) and `/redoc`
- **Features**:
  - RESTful API endpoints
  - JWT Authentication
  - Database models with SQLAlchemy
  - Async support

### Database (PostgreSQL)
- **Port**: 5432
- **Database**: interview_ai
- **Default Credentials**: postgres/postgres

### Redis
- **Port**: 6379
- **Used for**: Caching and session management

### ChromaDB
- **Port**: 8001
- **Used for**: Vector storage and similarity search

### PgAdmin (Optional)
- **URL**: http://localhost:5050
- **Default Email**: admin@example.com
- **Default Password**: admin

## 🔧 Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
# API
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://postgres:postgres@db:5432/interview_ai
REDIS_URL=redis://redis:6379/0
CHROMA_SERVER=http://chroma:8000

# Authentication
JWT_SECRET=your-jwt-secret
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# External Services
GROQ_API_KEY=your-groq-api-key
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md) - High-level architecture and design decisions
- [API Reference](docs/API.md) - Detailed API documentation
- [Development Guide](docs/DEVELOPMENT.md) - Development setup and workflow

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- [Next.js](https://nextjs.org/) - The React Framework for Production
- [PostgreSQL](https://www.postgresql.org/) - The World's Most Advanced Open Source Relational Database
- [Redis](https://redis.io/) - In-memory data structure store
- [ChromaDB](https://www.trychroma.com/) - AI-native open-source embedding database
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
   # - GROQ_API_KEY for LLM services
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
