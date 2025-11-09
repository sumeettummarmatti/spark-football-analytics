#!/bin/bash
set -e

echo "🗄️  Initializing database..."

# Wait for PostgreSQL to be ready
until pg_isready -U spark_user -d spark_db; do
  echo "⏳ Waiting for PostgreSQL to be ready..."
  sleep 2
done

echo "✅ PostgreSQL is ready!"

# Run SQL files in order
echo "📝 Running schema files..."

# Run all SQL files in 01_schema directory in order
for file in /docker-entrypoint-initdb.d/sql/01_schema/*.sql; do
    if [ -f "$file" ]; then
        echo "  → Executing $(basename $file)..."
        psql -U spark_user -d spark_db -f "$file" || true
    fi
done

echo "✅ Database initialization complete!"

