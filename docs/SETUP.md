# Complete Setup & Installation Guide

Comprehensive guide for setting up the AI Excel Interview platform in any environment.

## 🏗️ Architecture Overview

```mermaid
graph TD
    A[React Frontend :5000] --> B[FastAPI Backend :8000]
    B --> C[SQLite Database]
    B --> D[ChromaDB Vector Store]
    B --> E[AI Services]
    E --> F[Groq API]
    E --> G[OpenAI API]
    B --> H[Redis Cache]
```

## 📋 System Requirements

### Development Environment
- **Python**: 3.11+ 
- **Node.js**: 18+ with Yarn 4.x
- **Memory**: 2GB+ RAM
- **Storage**: 1GB+ free space

### Production (Optional)
- **Database**: PostgreSQL 13+ (or SQLite for simple deployments)
- **Cache**: Redis 6+ (optional, graceful degradation)
- **Compute**: 1 CPU core, 1GB RAM minimum

## 🛠️ Manual Installation

### 1. Backend Setup

```bash
# Navigate to backend
cd apps/api

# Create virtual environment (if not using Replit)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python -c "
import asyncio
from app.core.database import init_db
asyncio.run(init_db())
"

# Start backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend Setup

```bash
# Navigate to frontend
cd apps/web

# Install dependencies
yarn install

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Start frontend
yarn dev
```

### 3. Initialize AI Services

```bash
cd apps/api

# Test ChromaDB
python -c "
import asyncio
from app.services.chroma_service import chroma_service

async def setup():
    collection = chroma_service.get_or_create_collection('interview_questions')
    print('✅ ChromaDB initialized')
    
asyncio.run(setup())
"

# Test LLM Services (with mock fallback)
python -c "
from app.services.llm_service import llm_service
print('✅ LLM services ready')
print(f'   Model: {llm_service.model}')
print(f'   API Key Set: {bool(llm_service.client)}')
"
```

## 🔧 Configuration

### Environment Variables

#### Backend Configuration (`apps/api/.env`)

```bash
# Application
APP_NAME="AI Excel Interview API"
DEBUG=true
SECRET_KEY="your-secret-key-here"

# Database
DATABASE_URL="sqlite+aiosqlite:///./interview.db"
# For PostgreSQL: "postgresql+asyncpg://user:pass@localhost:5432/interview"

# AI Services
GROQ_API_KEY="your-groq-api-key"      # For fast inference
OPENAI_API_KEY="your-openai-api-key"  # Fallback option

# Vector Storage
CHROMA_DIR="./chroma_data"

# Cache (Optional)
REDIS_URL="redis://localhost:6379/0"

# Server
HOST="0.0.0.0"
PORT=8000
CORS_ORIGINS=["http://localhost:5000","http://localhost:3000"]
```

#### Frontend Configuration (`apps/web/.env`)

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000

# Application
VITE_APP_SECRET=dev-shared-secret-key-2024
VITE_ENVIRONMENT=development
```

### Database Migration

```bash
cd apps/api

# Generate migration (if using Alembic)
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head

# Or use simple init for development
python -c "
import asyncio
from app.core.database import init_db
asyncio.run(init_db())
"
```

## 🧪 Verification Tests

### Backend Health Check
```bash
curl http://localhost:8000/api/health
# Expected: {"status":"ok"}

curl http://localhost:8000/
# Expected: {"message":"Welcome to the Autonomous Interview API",...}
```

### Database Connection
```bash
cd apps/api && python -c "
import asyncio
from app.core.database import get_db

async def test():
    async for session in get_db():
        print('✅ Database connection successful')
        break
        
asyncio.run(test())
"
```

### ChromaDB Vector Storage
```bash
cd apps/api && python -c "
import asyncio
from app.services.chroma_service import chroma_service

async def test():
    # Create test collection
    collection = chroma_service.get_or_create_collection('test')
    
    # Add sample document
    await chroma_service.add_documents('test', [{'text': 'Hello world'}])
    
    # Query
    results = await chroma_service.query('test', 'Hello', n_results=1)
    print(f'✅ ChromaDB working: {len(results[\"documents\"][0])} results')
    
asyncio.run(test())
"
```

### AI Services
```bash
cd apps/api && python -c "
import asyncio
from app.services.llm_service import llm_service

async def test():
    class MockQ:
        text = 'Test question'
        question_type = 'technical'
        def dict(self): return {'text': self.text}
    
    result = await llm_service.evaluate_response(
        MockQ(), 
        {'text': 'Test answer'}
    )
    print(f'✅ LLM evaluation: Score {result.score}')
    
asyncio.run(test())
"
```

### Frontend Build
```bash
cd apps/web

# Development server
yarn dev
# Should start on http://localhost:5000

# Production build
yarn build
# Should create dist/ directory
```

## 🔍 Development Tools

### API Documentation
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Database Tools
```bash
# SQLite browser (if using SQLite)
sqlite3 apps/api/interview.db

# View tables
.tables

# Query data
SELECT * FROM interview_sessions LIMIT 5;
```

### ChromaDB Admin
```bash
cd apps/api && python -c "
from app.services.chroma_service import chroma_service

# List all collections
client = chroma_service._client
collections = client.list_collections()
print('Collections:', [c.name for c in collections])

# Collection stats
for collection in collections:
    print(f'{collection.name}: {collection.count()} documents')
"
```

## 🚀 Production Considerations

### Database
- Switch to PostgreSQL for production
- Set up connection pooling
- Configure automated backups

### Security
- Change all default secrets
- Set up proper CORS origins
- Enable HTTPS
- Add rate limiting

### Monitoring
- Set up logging aggregation
- Configure health checks
- Monitor API response times
- Track AI service usage

### Scaling
- Use Redis for session management
- Consider AI service load balancing
- Set up horizontal scaling for FastAPI

## 🆘 Common Issues

See [Debugging Guide](./DEBUGGING.md) for detailed troubleshooting steps.