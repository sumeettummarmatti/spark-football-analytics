-- ============================================
-- MOCK LEADERBOARD DATA
-- ============================================

BEGIN;

-- 1. Insert Mock Users
INSERT INTO USERS (username, email, password_hash, full_name, profile_picture_url) VALUES
('football_fan_99', 'fan99@example.com', 'hashed_password_1', 'John Doe', 'https://ui-avatars.com/api/?name=John+Doe&background=random'),
('premier_pro', 'pro@example.com', 'hashed_password_2', 'Sarah Smith', 'https://ui-avatars.com/api/?name=Sarah+Smith&background=random'),
('goal_machine', 'goal@example.com', 'hashed_password_3', 'Mike Johnson', 'https://ui-avatars.com/api/?name=Mike+Johnson&background=random'),
('tactical_genius', 'tactic@example.com', 'hashed_password_4', 'Emma Wilson', 'https://ui-avatars.com/api/?name=Emma+Wilson&background=random'),
('var_official', 'var@example.com', 'hashed_password_5', 'Tom Brown', 'https://ui-avatars.com/api/?name=Tom+Brown&background=random'),
('stat_master', 'stat@example.com', 'hashed_password_6', 'Lisa Davis', 'https://ui-avatars.com/api/?name=Lisa+Davis&background=random'),
('red_devil', 'mufc@example.com', 'hashed_password_7', 'James Miller', 'https://ui-avatars.com/api/?name=James+Miller&background=random'),
('gunner_4_life', 'afc@example.com', 'hashed_password_8', 'Robert Taylor', 'https://ui-avatars.com/api/?name=Robert+Taylor&background=random'),
('kopite_king', 'lfc@example.com', 'hashed_password_9', 'William Anderson', 'https://ui-avatars.com/api/?name=William+Anderson&background=random'),
('city_zen', 'mcfc@example.com', 'hashed_password_10', 'David Thomas', 'https://ui-avatars.com/api/?name=David+Thomas&background=random')
ON CONFLICT (username) DO NOTHING;

-- 2. Insert Leaderboard Entries (linked to users by username)
INSERT INTO USER_LEADERBOARD (user_id, username, total_predictions, correct_predictions, total_points, accuracy_percentage, rank)
SELECT 
    u.user_id,
    u.username,
    FLOOR(RANDOM() * 50 + 10)::INT as total_predictions,
    FLOOR(RANDOM() * 30 + 5)::INT as correct_predictions,
    FLOOR(RANDOM() * 500 + 100)::INT as total_points,
    ROUND((RANDOM() * 40 + 40)::numeric, 2) as accuracy_percentage,
    ROW_NUMBER() OVER (ORDER BY RANDOM()) as rank
FROM USERS u
WHERE u.username IN (
    'football_fan_99', 'premier_pro', 'goal_machine', 'tactical_genius', 'var_official',
    'stat_master', 'red_devil', 'gunner_4_life', 'kopite_king', 'city_zen'
)
ON CONFLICT (user_id) DO UPDATE 
SET 
    total_predictions = EXCLUDED.total_predictions,
    correct_predictions = EXCLUDED.correct_predictions,
    total_points = EXCLUDED.total_points,
    accuracy_percentage = EXCLUDED.accuracy_percentage;

-- 3. Recalculate Ranks based on points
WITH RankedUsers AS (
    SELECT user_id, RANK() OVER (ORDER BY total_points DESC) as new_rank
    FROM USER_LEADERBOARD
)
UPDATE USER_LEADERBOARD ul
SET rank = ru.new_rank
FROM RankedUsers ru
WHERE ul.user_id = ru.user_id;

COMMIT;

DO $$ 
BEGIN 
    RAISE NOTICE '✅ Mock leaderboard data inserted successfully!';
END $$;
