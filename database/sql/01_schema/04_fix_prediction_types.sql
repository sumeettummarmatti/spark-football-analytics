-- Migration script to update prediction_type constraint
-- This adds support for 'match_outcome' and 'season_performance' prediction types

-- Drop the existing constraint
ALTER TABLE user_predictions DROP CONSTRAINT IF EXISTS user_predictions_prediction_type_check;

-- Add the new constraint with all prediction types
ALTER TABLE user_predictions 
ADD CONSTRAINT user_predictions_prediction_type_check 
CHECK (prediction_type IN ('season_winner', 'top_scorer', 'top_assists', 'golden_boot', 'match_outcome', 'season_performance'));

