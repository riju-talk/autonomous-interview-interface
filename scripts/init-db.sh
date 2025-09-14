#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "PostgreSQL is up - initializing database..."

# Initialize database tables
echo "Initializing database schema..."
python -c "
import asyncio
from app.core.database import init_db
asyncio.run(init_db())
"

# Load sample data
echo "Loading sample data..."
python -c "
import asyncio
from app.data.sample import load_all_sample_data
result = asyncio.run(load_all_sample_data())
print(f'Successfully loaded {result["questions_loaded"]} questions and created {result["sessions_created"]} interview sessions.')
"

echo "Database initialization completed successfully!"

echo "Database initialization complete"
