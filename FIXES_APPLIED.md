# Fixes Applied

## 1. Database Constraint Fix

**Problem:** The `user_predictions` table had a CHECK constraint that only allowed:
- 'season_winner'
- 'top_scorer'  
- 'top_assists'
- 'golden_boot'

But the code was trying to insert 'match_outcome' and 'season_performance'.

**Solution:**
- Updated `database/sql/01_schema/03_user_tables.sql` to include all prediction types
- Created migration script `database/sql/01_schema/04_fix_prediction_types.sql`
- Created `database/apply-migration.sh` to apply the fix to existing databases

**To apply the migration to your existing database:**
```bash
bash database/apply-migration.sh
```

Or manually:
```bash
docker exec -i spark_postgres psql -U spark_user -d spark_db -f database/sql/01_schema/04_fix_prediction_types.sql
```

## 2. Leaderboard Rank Fix

**Problem:** The leaderboard endpoint was returning `rank: None` causing validation errors.

**Solution:**
- Updated `backend/src/api/routes/profile.py` to calculate ranks dynamically when they're None
- Both `/leaderboard` and `/leaderboard/top` endpoints now ensure ranks are always integers

## 3. Docker Setup for SQL Initialization

**Problem:** SQL files weren't running automatically when Docker starts.

**Solution:**
- Updated `docker-compose.yml` to mount `./database/sql/01_schema` to `/docker-entrypoint-initdb.d`
- PostgreSQL automatically runs all `.sql` files in that directory on first initialization
- Files are executed in alphabetical order (01, 02, 03, 04)

**Note:** SQL files only run on **first initialization** (when the volume is empty). To re-run them:
```bash
docker-compose down -v  # Removes volumes
docker-compose up -d    # Recreates and runs SQL files
```

## 4. Docker Setup for Data Scraping

**Problem:** Data scraping wasn't automated on startup.

**Solution:**
- Created `backend/Dockerfile.scraper` for the scraper service
- Created `database/run-scraper.sh` to run the scraper
- Added `scraper` service to `docker-compose.yml` that:
  - Waits for PostgreSQL to be healthy
  - Runs the scraper automatically
  - Exits after completion (restart: "no")

**To run with scraping:**
```bash
docker-compose up -d
```

The scraper will run automatically after the database is ready.

**To skip scraping:**
```bash
docker-compose up -d postgres adminer
```

