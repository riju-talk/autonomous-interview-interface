.PHONY: help install install-web install-api dev dev-web dev-api test test-web test-api lint lint-web lint-api format format-web format-api build build-web build-api start stop clean

# Default target
help:
	@echo "Autonomous Interview Interface - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install all dependencies (web + api)"
	@echo "  make install-web   Install web dependencies"
	@echo "  make install-api   Install API dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make dev           Start all services in development mode"
	@echo "  make dev-web       Start web frontend in development mode"
	@echo "  make dev-api       Start API server in development mode"
	@echo ""
	@echo "Testing:"
	@echo "  make test          Run all tests (web + api)"
	@echo "  make test-web      Run web frontend tests"
	@echo "  make test-api      Run API tests"
	@echo ""
	@echo "Linting & Formatting:"
	@echo "  make lint          Run all linters (web + api)"
	@echo "  make lint-web      Lint web frontend code"
	@echo "  make lint-api      Lint API code"
	@echo "  make format        Format all code (web + api)"
	@echo "  make format-web    Format web frontend code"
	@echo "  make format-api    Format API code"
	@echo ""
	@echo "Build & Deployment:"
	@echo "  make build         Build all services for production"
	@echo "  make build-web     Build web frontend for production"
	@echo "  make build-api     Build API for production"
	@echo "  make start         Start all services in production mode"
	@echo "  make stop          Stop all services"
	@echo "  make clean         Remove build artifacts and dependencies"

# Install dependencies
install: install-web install-api

install-web:
	@echo "\nInstalling web dependencies..."
	cd apps/web && yarn install

install-api:
	@echo "\nInstalling API dependencies..."
	cd apps/api && pip install --upgrade pip && pip install -r requirements.txt

# Development
.PHONY: dev dev-web dev-api
dev:
	@echo "Starting development environment..."
	yarn dev

dev-web:
	@echo "Starting web frontend in development mode..."
	cd apps/web && yarn dev

dev-api:
	@echo "Starting API server in development mode..."
	cd apps/api && yarn dev

# Testing
.PHONY: test test-web test-api
test: test-web test-api

test-web:
	@echo "Running web frontend tests..."
	cd apps/web && yarn test

test-api:
	@echo "Running API tests..."
	cd apps/api && yarn test

# Linting & Formatting
.PHONY: lint lint-web lint-api
lint: lint-web lint-api

lint-web:
	@echo "Linting web frontend code..."
	cd apps/web && yarn lint

lint-api:
	@echo "Linting API code..."
	cd apps/api && yarn lint

.PHONY: format format-web format-api
format: format-web format-api

format-web:
	@echo "Formatting web frontend code..."
	cd apps/web && yarn format

format-api:
	@echo "Formatting API code..."
	cd apps/api && yarn format

# Build & Deployment
.PHONY: build build-web build-api
build: build-web build-api

build-web:
	@echo "Building web frontend for production..."
	cd apps/web && yarn build

build-api:
	@echo "Building API for production..."
	cd apps/api && yarn build

# Service Management
.PHONY: start stop
start:
	@echo "Starting all services in production mode..."
	docker-compose up -d

stop:
	@echo "Stopping all services..."
	docker-compose down

# Cleanup
.PHONY: clean
clean:
	@echo "Cleaning up..."
	cd apps/web && rm -rf node_modules .next
	cd apps/api && find . -type d -name "__pycache__" -exec rm -r {} +
	docker-compose run --rm api black --check .
	docker-compose run --rm api isort --check-only .
	docker-compose run --rm api mypy .

# Format code
format:
	docker-compose run --rm api black .
	docker-compose run --rm api isort .

# Clean up
clean:
	docker-compose down -v --remove-orphans
	rm -rf __pycache__ .pytest_cache

# Build containers
build:
	docker-compose build

# Start services
up:
	docker-compose up -d

# Stop services
down:
	docker-compose down

# Restart services
restart: down up

# Show logs
logs:
	docker-compose logs -f

# Database shell
db-shell:
	docker-compose exec db psql -U postgres -d interview_ai

# Redis CLI
redis-cli:
	docker-compose exec redis redis-cli -a "${REDIS_PASSWORD}"

# ChromaDB shell
chroma-shell:
	docker-compose exec chroma python -m chromadb shell --host chroma --port 8000
