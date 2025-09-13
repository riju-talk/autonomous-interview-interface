#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "PostgreSQL is up - executing command"

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Load initial data (if any)
if [ -f "/app/scripts/seed_data.py" ]; then
    echo "Loading initial data..."
    python /app/scripts/seed_data.py
fi

echo "Database initialization complete"
