# Overview

This is an AI-powered Excel interview platform that simulates real technical interviews using artificial intelligence. The system conducts interactive interviews, evaluates responses in real-time, and provides comprehensive feedback to candidates. It's built as a full-stack application designed to help companies assess Excel proficiency during hiring processes.

**Recent Conversion (September 14, 2025)**: Successfully converted from TypeScript + Yarn monorepo to JavaScript + npm setup. All traces of TypeScript and Yarn have been completely removed from the codebase.

# User Preferences

Preferred communication style: Simple, everyday language.
Build system preference: npm + JavaScript (no TypeScript, no Yarn)

# System Architecture

## Frontend Architecture
The frontend is built with React 18 and TypeScript using Vite as the build tool. It features a modern component architecture using shadcn/ui components built on Radix UI primitives. The application uses TanStack Query for server state management and implements session-based persistence to allow users to resume interviews. The UI follows a responsive design pattern with Tailwind CSS for styling.

## Backend Architecture  
The backend uses FastAPI as the web framework with SQLAlchemy for database operations. The system implements a monorepo structure using Turbo for build orchestration. The API follows RESTful conventions with automatic OpenAPI documentation generation. Authentication is simplified for development with optional user creation.

## Database Design
The system uses SQLite for development with async support through SQLAlchemy. The data model includes core entities for users, interview sessions, questions, and responses. The database supports different question types (objective, multi-turn, assignment) and tracks interview progress with session state management.

## AI Integration
The platform integrates with Groq's API for LLM-powered evaluation using the LLaMA3-70b model. It includes fallback mechanisms with mock responses when API keys are unavailable. The system uses ChromaDB for vector storage and similarity search of questions, enabling intelligent question selection and duplicate detection.

## Question Management
Questions are categorized by difficulty (easy, medium, hard) and type (objective, multi-turn, assignment). The system supports dynamic question generation and evaluation with context-aware scoring. Each question includes metadata for proper categorization and evaluation criteria.

## Session Management
Interview sessions maintain state across multiple interactions with automatic persistence. The system tracks timing per question, maintains conversation history, and supports session resumption. Progress is saved incrementally to prevent data loss.

## Evaluation System
The AI evaluation engine provides detailed scoring with breakdown by criteria (accuracy, completeness, clarity). It generates constructive feedback and suggests follow-up questions based on response quality. The system includes confidence scoring and supports multiple evaluation methods based on question type.

# External Dependencies

## AI Services
- **Groq API**: Primary LLM service using LLaMA3-70b for response evaluation and feedback generation
- **ChromaDB**: Vector database for question similarity search and intelligent question selection
- **OpenAI API**: Alternative LLM service with fallback support

## Database & Storage
- **SQLite**: Development database with async support through aiosqlite
- **ChromaDB Local Storage**: Local vector storage in development environment
- **Session Storage**: Browser-based persistence for interview state

## Development Tools
- **Turbo**: Monorepo build system for coordinating frontend and backend builds
- **FastAPI**: Python web framework with automatic API documentation
- **Vite**: Frontend build tool and development server
- **Docker Compose**: Container orchestration for development environment

## UI Framework
- **Radix UI**: Headless UI primitives for accessible components
- **shadcn/ui**: Pre-built component library based on Radix UI
- **Tailwind CSS**: Utility-first CSS framework for styling
- **TanStack Query**: Data fetching and server state management

## Production Dependencies
- **PostgreSQL**: Production database (configurable via environment)
- **Redis**: Caching and session storage for production deployment
- **Uvicorn**: ASGI server for running the FastAPI application