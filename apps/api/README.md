# Excel Mock Interviewer API

This is the backend API for the AI-Powered Excel Mock Interviewer application. It provides endpoints for managing interview sessions, evaluating responses, and generating feedback using AI.

## Features

- **User Authentication**: JWT-based authentication with email/password and GitHub OAuth
- **Interview Management**: Create, update, and manage interview sessions
- **Question Bank**: Store and retrieve interview questions with different difficulty levels
- **AI-Powered Evaluation**: Evaluate candidate responses using LLM (ChatGroq)
- **Multi-turn Conversations**: Support for follow-up questions and contextual interviews
- **File Uploads**: Handle Excel/CSV file submissions for assignments
- **Real-time Feedback**: Get instant feedback on responses

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis for session management
- **Vector Store**: ChromaDB for embeddings and semantic search
- **LLM Integration**: ChatGroq for response evaluation
- **Authentication**: JWT with OAuth2
- **Containerization**: Docker

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Groq API key (for LLM functionality)
- GitHub OAuth credentials (for GitHub login)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/autonomous-interview-interface.git
   cd autonomous-interview-interface
   ```

2. Create a `.env` file in the `apps/api` directory with the following variables:
   ```env
   # App
   DEBUG=true
   SECRET_KEY=your-secret-key
   
   # Database
   DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/interviewdb
   
   # Redis
   REDIS_URL=redis://redis:6379/0
   
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

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login with email/password
- `GET /auth/github` - Start GitHub OAuth flow
- `GET /auth/github/callback` - GitHub OAuth callback
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
