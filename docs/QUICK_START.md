# Quick Start Guide

Get the AI Excel Interview platform running in 5 minutes.

## Prerequisites

✅ **Already Set Up in Replit:**
- Python 3.11 with all dependencies installed
- Node.js with Yarn package manager
- Both frontend and backend workflows running

## 🚀 Immediate Access

The application is **already running** with these endpoints:

| Service | URL | Status |
|---------|-----|--------|
| **Frontend** | http://localhost:5000 | ✅ Running |
| **Backend API** | http://localhost:8000 | ✅ Running |
| **API Documentation** | http://localhost:8000/docs | ✅ Available |
| **Health Check** | http://localhost:8000/api/health | ✅ Active |

## 🧪 Quick Tests

### 1. Test Backend API
```bash
curl http://localhost:8000/api/health
# Expected: {"status":"ok"}
```

### 2. Test Database Connection
```bash
cd apps/api && python -c "
from app.core.database import engine
print('✅ Database connection successful!')
"
```

### 3. Test ChromaDB Vector Storage
```bash
cd apps/api && python -c "
from app.services.chroma_service import chroma_service
stats = chroma_service.get_collection_stats('interview_questions')
print(f'✅ ChromaDB working! Collection: {stats}')
"
```

### 4. Test AI Services
```bash
cd apps/api && python -c "
from app.services.llm_service import llm_service
print('✅ LLM Service initialized with mock fallbacks')
"
```

## 📁 Project Structure

```
├── apps/
│   ├── web/          # React frontend (port 5000)
│   └── api/          # FastAPI backend (port 8000)
├── docs/             # This documentation
└── packages/         # Shared utilities
```

## 🔧 Environment Configuration

### Frontend (.env)
```bash
# apps/web/.env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_SECRET=dev-shared-secret-key-2024
VITE_ENVIRONMENT=development
```

### Backend (.env)  
```bash
# apps/api/.env
DATABASE_URL=sqlite+aiosqlite:///./interview.db
GROQ_API_KEY=""  # Optional - enables real AI evaluation
OPENAI_API_KEY=""  # Optional - fallback for LLM services
```

## 🎯 Next Steps

1. **Browse the Frontend**: Visit http://localhost:5000
2. **Explore API Docs**: Visit http://localhost:8000/docs
3. **Set up AI Keys**: Add `GROQ_API_KEY` or `OPENAI_API_KEY` for real AI features
4. **Start Development**: See [Development Workflow](./DEVELOPMENT.md)

## 🆘 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Frontend not loading | Check port 5000 is available, restart Frontend workflow |
| Backend API errors | Check logs in Replit console, verify database path |
| AI services not working | Expected behavior - add API keys for real AI features |
| Import errors | Run `yarn install` in apps/web or `pip install -r requirements.txt` in apps/api |

**Need more help?** See [Debugging Guide](./DEBUGGING.md)