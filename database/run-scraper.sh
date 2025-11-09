#!/bin/bash
set -e

echo "🕷️  Starting data scraper..."

# Wait for PostgreSQL to be ready
until pg_isready -U spark_user -d spark_db -h spark_postgres; do
  echo "⏳ Waiting for PostgreSQL to be ready..."
  sleep 2
done

echo "✅ PostgreSQL is ready!"

# Set environment variables for scraper
export POSTGRES_HOST=spark_postgres
export POSTGRES_PORT=5432
export POSTGRES_DB=spark_db
export POSTGRES_USER=spark_user
export POSTGRES_PASSWORD=spark_password_2024

# Run the scraper
cd /app/backend
python -c "from src.scraper.fbref_scraper import main; main()"

echo "✅ Data scraping complete!"

