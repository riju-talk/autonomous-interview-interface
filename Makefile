.PHONY: help install test lint format clean build up down restart logs db-shell redis-cli chroma-shell

# Default target
help:
	@echo "Available commands:"
	@echo "  make install       Install dependencies"
	@echo "  make test          Run tests"
	@echo "  make lint          Run linters"
	@echo "  make format        Format code"
	@echo "  make build         Build containers"
	@echo "  make up            Start all services"
	@echo "  make down          Stop all services"
	@echo "  make restart       Restart all services"
	@echo "  make logs          Show container logs"
	@echo "  make db-shell      Open database shell"
	@echo "  make redis-cli     Open Redis CLI"
	@echo "  make chroma-shell  Open ChromaDB shell"

# Install dependencies
install:
	pip install --upgrade pip
	pip install -r apps/api/requirements.txt

# Run tests
test:
	docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

# Run linters
lint:
	docker-compose run --rm api flake8 .
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
