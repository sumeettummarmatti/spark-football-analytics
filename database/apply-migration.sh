#!/bin/bash
# Script to apply the prediction type migration to existing database

echo "🔄 Applying prediction type migration..."

docker exec -i spark_postgres psql -U spark_user -d spark_db <<EOF
-- Drop the existing constraint
ALTER TABLE user_predictions DROP CONSTRAINT IF EXISTS user_predictions_prediction_type_check;

-- Add the new constraint with all prediction types
ALTER TABLE user_predictions 
ADD CONSTRAINT user_predictions_prediction_type_check 
CHECK (prediction_type IN ('season_winner', 'top_scorer', 'top_assists', 'golden_boot', 'match_outcome', 'season_performance'));

SELECT '✅ Migration applied successfully!' AS status;
EOF

