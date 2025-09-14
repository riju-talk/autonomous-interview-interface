# Autonomous Interview API

This is the backend API for the Autonomous Interview Interface, a comprehensive platform for conducting AI-powered mock interviews. The API provides endpoints for managing interview sessions, evaluating responses, and generating feedback using advanced language models.

## 🚀 Features

- **Interview Management**
  - Create and manage interview sessions
  - Support for different interview types and templates
  - Real-time progress tracking

- **AI-Powered Evaluation**
  - Response evaluation using Groq's LLM services
  - Detailed feedback and scoring
  - Support for coding challenges and technical questions

- **Media Handling**
  - File uploads (PDF, DOCX, images)
  - Video recording and storage
  - Document processing and text extraction

- **Analytics & Reporting**
  - Performance metrics and insights
  - Interview history and comparisons
  - Exportable reports

## 🛠 Tech Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching & Message Broker**: Redis
- **Vector Database**: ChromaDB
- **AI/ML**: LangChain, Groq
- **Containerization**: Docker & Docker Compose
- **Monitoring**: Sentry, Prometheus
- **Documentation**: OpenAPI/Swagger

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+ (for development)
- Docker and Docker Compose
- PostgreSQL 14+
- Redis 7+
- ChromaDB 0.4+

## 🚀 Quick Start

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/autonomous-interview-interface.git
   cd autonomous-interview-interface
   ```

2. Set up environment variables:
   ```bash
   cp apps/api/.env.example apps/api/.env
   # Edit the .env file with your configuration
   ```

3. Start the development environment:
   ```bash
   # Using Docker Compose (recommended)
   docker-compose up -d
   
   # Or run locally
   cd apps/api
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

4. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Production Deployment

1. Build and start the production stack:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

2. Run database migrations:
   ```bash
   docker-compose -f docker-compose.prod.yml exec api alembic upgrade head
   ```

## 🔧 Configuration

Copy the example environment file and update the values:

```bash
cp apps/api/.env.example apps/api/.env
```

Key configuration options:

```env
# Application
APP_NAME="Autonomous Interview API"
DEBUG=false
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/interviewdb

# Redis
REDIS_URL=redis://redis:6379/0

# CORS (comma-separated list of origins)
CORS_ORIGINS=["https://your-frontend.com"]

# LLM Providers (at least one required)
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GROQ_API_KEY=your-groq-key

# Optional: Email Configuration
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASSWORD=your-password
EMAIL_FROM=noreply@example.com
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_endpoints.py -v
```

## 📚 API Documentation

Interactive API documentation is available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- LangChain for LLM integration
- The open-source community for invaluable tools and libraries
   
   # JWT
   JWT_SECRET=your-jwt-secret
   ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours
   
   # OAuth
   GITHUB_CLIENT_ID=your-github-client-id
   GITHUB_CLIENT_SECRET=your-github-client-secret
   
   # LLM
   GROQ_API_KEY=your-groq-api-key
   
   # ChromaDB
   CHROMA_DIR=./chroma_data
   ```

3. Build and start the services:
   ```bash
   docker-compose up --build
   ```

4. Run database migrations:
   ```bash
   docker-compose exec api alembic upgrade head
   ```

## API Documentation

Once the API is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Available Endpoints

### Interview Endpoints
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Logout

### Interview Sessions
- `GET /sessions/` - List interview sessions
- `POST /sessions/` - Create a new interview session
- `GET /sessions/{session_id}` - Get interview session details
- `PUT /sessions/{session_id}` - Update interview session
- `POST /sessions/{session_id}/start` - Start an interview session
- `POST /sessions/{session_id}/submit-answer` - Submit an answer
- `POST /sessions/{session_id}/evaluate` - Evaluate an answer

### Questions
- `GET /questions/` - List questions
- `POST /questions/` - Create a new question
- `GET /questions/{question_id}` - Get question details
- `PUT /questions/{question_id}` - Update a question
- `DELETE /questions/{question_id}` - Delete a question

### Users
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update current user profile
- `GET /users/` - List users (admin only)
- `GET /users/{user_id}` - Get user details (admin only)

## Development

### Running Tests

```bash
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

### Code Style

This project uses:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

Run code style checks:

```bash
# Format code
black .

# Sort imports
isort .

# Lint
flake8

# Type check
mypy .
```

## Deployment

### Production

For production deployment, make sure to:
1. Set `DEBUG=false`
2. Configure proper CORS settings
3. Set up HTTPS
4. Configure proper logging and monitoring
5. Set up database backups

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `false` |
| `SECRET_KEY` | Secret key for the application | - |
| `DATABASE_URL` | Database connection URL | - |
| `REDIS_URL` | Redis connection URL | - |
| `JWT_SECRET` | Secret key for JWT tokens | - |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration time in minutes | `1440` |
| `GITHUB_CLIENT_ID` | GitHub OAuth client ID | - |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth client secret | - |
| `GROQ_API_KEY` | Groq API key for LLM | - |
| `CHROMA_DIR` | Directory for ChromaDB storage | `./chroma_data` |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
