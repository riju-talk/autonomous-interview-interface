# Debugging Guide

Comprehensive troubleshooting guide for the AI Excel Interview platform.

## 🚨 Quick Diagnostic Commands

Run these first to identify the issue:

```bash
# Check all services status
curl -s http://localhost:8000/api/health || echo "❌ Backend API down"
curl -s http://localhost:5000 >/dev/null && echo "✅ Frontend up" || echo "❌ Frontend down"

# Check workflows in Replit
# Backend logs: Check Replit console for Backend workflow
# Frontend logs: Check Replit console for Frontend workflow

# Test database connection
cd apps/api && python -c "
try:
    from app.core.database import engine
    print('✅ Database connection OK')
except Exception as e:
    print(f'❌ Database error: {e}')
"

# Test AI services
cd apps/api && python -c "
from app.services.llm_service import llm_service
from app.services.chroma_service import chroma_service
print(f'LLM Client: {\"✅ Connected\" if llm_service.client else \"⚠️ Mock mode\"}')
print(f'ChromaDB: ✅ Ready')
"
```

## 🔧 Common Issues & Solutions

### Backend Issues

#### 1. "Module not found" errors
```bash
# Symptoms: ImportError, ModuleNotFoundError
# Solution: Reinstall dependencies
cd apps/api
pip install -r requirements.txt

# Or in Replit: Use the packager tool to install missing packages
```

#### 2. Database connection failed
```bash
# Symptoms: "sqlite3.OperationalError" or database locked
# Solution: Reset database
cd apps/api
rm -f interview.db interview.db-*  # Remove SQLite files
python -c "
import asyncio
from app.core.database import init_db
asyncio.run(init_db())
print('✅ Database reset complete')
"
```

#### 3. ChromaDB initialization errors
```bash
# Symptoms: "chromadb.errors.ChromaError"
# Solution: Reset ChromaDB storage
cd apps/api
rm -rf chroma_data
mkdir chroma_data
python -c "
from app.services.chroma_service import chroma_service
collection = chroma_service.get_or_create_collection('interview_questions')
print('✅ ChromaDB reset complete')
"
```

#### 4. Redis connection errors
```bash
# Symptoms: "redis.exceptions.ConnectionError"
# Current Status: Expected behavior - Redis is optional
# Solution: Install Redis (optional) or ignore warnings

# Install Redis (Ubuntu/Debian):
sudo apt-get install redis-server
redis-server

# Or accept graceful degradation (recommended for development)
# The app will log warnings but continue working
```

#### 5. AI service not working
```bash
# Symptoms: Mock responses, "API key not set"
# Solution: Add API keys to environment

# Edit apps/api/.env
GROQ_API_KEY="your-groq-api-key-here"
# Or
OPENAI_API_KEY="your-openai-api-key-here"

# Restart backend workflow
# Test with:
cd apps/api && python -c "
import asyncio
from app.services.llm_service import llm_service

async def test():
    class MockQ:
        text = 'Test'
        question_type = 'technical'
        def dict(self): return {}
    result = await llm_service.evaluate_response(MockQ(), {'text': 'answer'})
    print(f'AI Status: {\"Real\" if not result.metadata.get(\"is_mock\") else \"Mock\"}')
    
asyncio.run(test())
"
```

### Frontend Issues

#### 1. Frontend won't start
```bash
# Symptoms: Vite errors, dependency issues
# Solution: Clean and reinstall
cd apps/web
rm -rf node_modules .yarn/cache
yarn install
yarn dev
```

#### 2. API connection failed
```bash
# Symptoms: Network errors, CORS issues
# Check backend is running:
curl http://localhost:8000/api/health

# Check frontend environment:
cat apps/web/.env
# Should contain: VITE_API_BASE_URL=http://localhost:8000

# Check CORS configuration in apps/api/.env:
# CORS_ORIGINS should include frontend URL
```

#### 3. TypeScript/React errors
```bash
# Symptoms: Type errors, import issues
# Solution: Clean and rebuild
cd apps/web
yarn build  # Check for build errors
yarn lint   # Check for linting issues

# Fix common issues:
# - Check import paths use '@/' alias
# - Ensure all components export correctly
# - Verify .tsx files don't conflict with .jsx files
```

#### 4. Hot reload not working
```bash
# Symptoms: Changes not reflected in browser
# Solution: Restart Vite dev server
# In Replit: Restart Frontend workflow
# Or manually:
cd apps/web
yarn dev
```

### Environment Issues

#### 1. Port conflicts
```bash
# Symptoms: "Port already in use"
# Check what's using ports:
lsof -i :5000  # Frontend
lsof -i :8000  # Backend

# Solution: Kill conflicting processes or change ports
# In Replit: Stop and restart workflows
```

#### 2. Environment variables not loaded
```bash
# Check environment files exist:
ls -la apps/api/.env apps/web/.env

# Verify content:
cat apps/api/.env
cat apps/web/.env

# Common fixes:
# - No quotes around values (DEBUG=true not DEBUG="true")
# - No spaces around = (PORT=8000 not PORT = 8000)
# - Restart services after changes
```

#### 3. File permissions
```bash
# Symptoms: Permission denied errors
# Solution: Fix permissions
chmod +x scripts/*.sh
chmod 755 apps/api apps/web
```

## 🔍 Advanced Debugging

### Backend Deep Dive

#### Check all services status:
```bash
cd apps/api && python -c "
import asyncio
from app.core.database import get_db
from app.services.chroma_service import chroma_service
from app.services.llm_service import llm_service
from app.core.redis import redis

async def diagnose():
    print('=== Backend Service Diagnosis ===')
    
    # Database
    try:
        async for session in get_db():
            print('✅ Database: Connected')
            break
    except Exception as e:
        print(f'❌ Database: {e}')
    
    # ChromaDB
    try:
        stats = await chroma_service.get_collection_stats('test')
        print('✅ ChromaDB: Connected')
    except Exception as e:
        print(f'❌ ChromaDB: {e}')
    
    # LLM Service
    print(f'{"✅" if llm_service.client else "⚠️"} LLM: {"Connected" if llm_service.client else "Mock mode"}')
    
    # Redis
    try:
        await redis.ping()
        print('✅ Redis: Connected')
    except Exception as e:
        print(f'⚠️ Redis: {e} (Optional)')

asyncio.run(diagnose())
"
```

#### API Endpoint Testing:
```bash
# Test all main endpoints:
echo "Testing API endpoints..."
curl -s http://localhost:8000/ | jq .message || echo "❌ Root endpoint"
curl -s http://localhost:8000/api/health | jq .status || echo "❌ Health endpoint" 
curl -s http://localhost:8000/docs >/dev/null && echo "✅ API docs" || echo "❌ API docs"
curl -s http://localhost:8000/openapi.json >/dev/null && echo "✅ OpenAPI spec" || echo "❌ OpenAPI spec"
```

### Database Debugging

#### SQLite Inspection:
```bash
cd apps/api
sqlite3 interview.db << EOF
.tables
.schema
SELECT name FROM sqlite_master WHERE type='table';
EOF
```

#### Reset Everything:
```bash
cd apps/api
rm -f interview.db interview.db-* chroma_data
mkdir chroma_data
python -c "
import asyncio
from app.core.database import init_db
asyncio.run(init_db())
print('🔄 Full reset complete')
"
```

### Log Analysis

#### View Backend Logs:
```bash
# In Replit: Check Backend workflow logs in console
# Or if running manually:
cd apps/api
python -m uvicorn app.main:app --log-level debug
```

#### View Frontend Logs:
```bash
# In Replit: Check Frontend workflow logs in console  
# Or if running manually:
cd apps/web
yarn dev --debug
```

## 🚨 Emergency Recovery

### Complete Reset (Nuclear Option):
```bash
echo "🚨 COMPLETE RESET - This will delete all data!"
read -p "Are you sure? (y/N): " confirm
if [[ $confirm == [yY] ]]; then
    # Stop all services first
    # Clean databases
    rm -rf apps/api/interview.db* apps/api/chroma_data
    
    # Clean frontend
    cd apps/web && rm -rf node_modules .yarn/cache dist
    
    # Clean backend
    cd ../api && rm -rf __pycache__ .pytest_cache
    
    # Reinstall everything
    cd ../web && yarn install
    cd ../api && pip install -r requirements.txt
    
    # Restart workflows in Replit
    echo "✅ Reset complete - restart workflows in Replit"
fi
```

## 📞 Getting Additional Help

### Log Collection for Support:
```bash
echo "=== System Info ===" > debug_info.txt
date >> debug_info.txt
python --version >> debug_info.txt
node --version >> debug_info.txt

echo -e "\n=== Environment ===" >> debug_info.txt
env | grep -E "(GROQ|OPENAI|DATABASE|REDIS)" >> debug_info.txt

echo -e "\n=== Service Status ===" >> debug_info.txt
curl -s http://localhost:8000/api/health >> debug_info.txt 2>&1
curl -s http://localhost:5000 >/dev/null && echo "Frontend: UP" >> debug_info.txt || echo "Frontend: DOWN" >> debug_info.txt

echo "Debug info saved to debug_info.txt"
```

### Common Error Patterns:

| Error Message | Likely Cause | Quick Fix |
|---------------|--------------|-----------|
| `ModuleNotFoundError` | Missing dependencies | `pip install -r requirements.txt` |
| `sqlite3.OperationalError` | Database locked/corrupt | Delete .db files and reinitialize |
| `chromadb.errors.ChromaError` | ChromaDB state issue | Delete `chroma_data` folder |
| `redis.exceptions.ConnectionError` | Redis not running | Install Redis or ignore (optional) |
| `CORS error` | Frontend can't reach backend | Check CORS_ORIGINS in .env |
| `Port already in use` | Service running elsewhere | Kill process or change port |
| `Permission denied` | File permissions | `chmod +x` on scripts |

**Remember**: Most issues can be resolved by restarting the workflows in Replit and checking the console logs!