-- ============================================
-- MOCK PREMIER LEAGUE DATA FOR SPARK
-- Complete realistic dataset for demo
-- ============================================

BEGIN;

-- Clear existing data
TRUNCATE TABLE MATCH_PREDICTIONS CASCADE;
TRUNCATE TABLE MATCH_EVENT CASCADE;
TRUNCATE TABLE MATCH_LINEUPS CASCADE;
TRUNCATE TABLE MATCHES CASCADE;
TRUNCATE TABLE TEAM_SEASONS CASCADE;
TRUNCATE TABLE PLAYER_NICKNAMES CASCADE;
TRUNCATE TABLE STAFF CASCADE;
TRUNCATE TABLE PLAYERS CASCADE;
TRUNCATE TABLE TEAMS CASCADE;
TRUNCATE TABLE SEASONS CASCADE;
TRUNCATE TABLE LEAGUES CASCADE;

-- ============================================
-- LEAGUES
-- ============================================
INSERT INTO LEAGUES (name, country, tier, logo_url, fbref_id) VALUES
('Premier League', 'England', 1, 'https://example.com/epl.png', '9'),
('La Liga', 'Spain', 1, 'https://example.com/laliga.png', '12'),
('Bundesliga', 'Germany', 1, 'https://example.com/bundesliga.png', '20');

-- ============================================
-- SEASONS
-- ============================================
INSERT INTO SEASONS (year, start_date, end_date, league_id) VALUES
('2024-25', '2024-08-16', '2025-05-25', 1),
('2023-24', '2023-08-11', '2024-05-19', 1);

-- ============================================
-- TEAMS (20 Premier League Teams)
-- ============================================
INSERT INTO TEAMS (name, founded_year, stadium_name, city, logo_url, fbref_id) VALUES
('Arsenal', 1886, 'Emirates Stadium', 'London', 'https://example.com/arsenal.png', 'arsenal'),
('Manchester City', 1880, 'Etihad Stadium', 'Manchester', 'https://example.com/mancity.png', 'mancity'),
('Liverpool', 1892, 'Anfield', 'Liverpool', 'https://example.com/liverpool.png', 'liverpool'),
('Manchester United', 1878, 'Old Trafford', 'Manchester', 'https://example.com/manutd.png', 'manutd'),
('Chelsea', 1905, 'Stamford Bridge', 'London', 'https://example.com/chelsea.png', 'chelsea'),
('Tottenham Hotspur', 1882, 'Tottenham Hotspur Stadium', 'London', 'https://example.com/spurs.png', 'spurs'),
('Newcastle United', 1892, 'St James Park', 'Newcastle', 'https://example.com/newcastle.png', 'newcastle'),
('Brighton & Hove Albion', 1901, 'Amex Stadium', 'Brighton', 'https://example.com/brighton.png', 'brighton'),
('Aston Villa', 1874, 'Villa Park', 'Birmingham', 'https://example.com/villa.png', 'villa'),
('West Ham United', 1895, 'London Stadium', 'London', 'https://example.com/westham.png', 'westham'),
('Brentford', 1889, 'Gtech Community Stadium', 'London', 'https://example.com/brentford.png', 'brentford'),
('Fulham', 1879, 'Craven Cottage', 'London', 'https://example.com/fulham.png', 'fulham'),
('Crystal Palace', 1905, 'Selhurst Park', 'London', 'https://example.com/palace.png', 'palace'),
('Wolverhampton Wanderers', 1877, 'Molineux Stadium', 'Wolverhampton', 'https://example.com/wolves.png', 'wolves'),
('Everton', 1878, 'Goodison Park', 'Liverpool', 'https://example.com/everton.png', 'everton'),
('Nottingham Forest', 1865, 'City Ground', 'Nottingham', 'https://example.com/forest.png', 'forest'),
('Bournemouth', 1899, 'Vitality Stadium', 'Bournemouth', 'https://example.com/bournemouth.png', 'bournemouth'),
('Leicester City', 1884, 'King Power Stadium', 'Leicester', 'https://example.com/leicester.png', 'leicester'),
('Southampton', 1885, 'St Marys Stadium', 'Southampton', 'https://example.com/southampton.png', 'southampton'),
('Ipswich Town', 1878, 'Portman Road', 'Ipswich', 'https://example.com/ipswich.png', 'ipswich');

-- ============================================
-- TEAM_SEASONS (Link teams to 2024-25 season)
-- ============================================
INSERT INTO TEAM_SEASONS (team_id, season_id, points, wins, draws, losses, goals_for, goals_against, goal_diff, position)
SELECT team_id, 1, 0, 0, 0, 0, 0, 0, 0, ROW_NUMBER() OVER (ORDER BY team_id)
FROM TEAMS WHERE team_id <= 20;

-- ============================================
-- PLAYERS (80 players - 4 per top team)
-- ============================================

-- Arsenal
INSERT INTO PLAYERS (full_name, dob, nationality, position, height_cm, weight_kg, team_id, fbref_id, shirt_number) VALUES
('Bukayo Saka', '2001-09-05', 'England', 'Forward', 178, 72, 1, 'saka', 7),
('Martin Ødegaard', '1998-12-17', 'Norway', 'Midfielder', 178, 68, 1, 'odegaard', 8),
('Gabriel Jesus', '1997-04-03', 'Brazil', 'Forward', 175, 73, 1, 'jesus', 9),
('William Saliba', '2001-03-24', 'France', 'Defender', 192, 83, 1, 'saliba', 2),
('Aaron Ramsdale', '1998-05-14', 'England', 'Goalkeeper', 188, 83, 1, 'ramsdale', 1);

-- Manchester City
INSERT INTO PLAYERS (full_name, dob, nationality, position, height_cm, weight_kg, team_id, fbref_id, shirt_number) VALUES
('Erling Haaland', '2000-07-21', 'Norway', 'Forward', 195, 88, 2, 'haaland', 9),
('Kevin De Bruyne', '1991-06-28', 'Belgium', 'Midfielder', 181, 70, 2, 'debruyne', 17),
('Phil Foden', '2000-05-28', 'England', 'Midfielder', 171, 69, 2, 'foden', 47),
('Rúben Dias', '1997-05-14', 'Portugal', 'Defender', 187, 82, 2, 'dias', 3),
('Ederson', '1993-08-17', 'Brazil', 'Goalkeeper', 188, 89, 2, 'ederson', 31);

-- Liverpool
INSERT INTO PLAYERS (full_name, dob, nationality, position, height_cm, weight_kg, team_id, fbref_id, shirt_number) VALUES
('Mohamed Salah', '1992-06-15', 'Egypt', 'Forward', 175, 71, 3, 'salah', 11),
('Virgil van Dijk', '1991-07-08', 'Netherlands', 'Defender', 193, 92, 3, 'vandijk', 4),
('Trent Alexander-Arnold', '1998-10-07', 'England', 'Defender', 180, 76, 3, 'taa', 66),
('Darwin Núñez', '1999-06-24', 'Uruguay', 'Forward', 187, 81, 3, 'nunez', 9),
('Alisson Becker', '1992-10-02', 'Brazil', 'Goalkeeper', 191, 91, 3, 'alisson', 1);

-- Manchester United
INSERT INTO PLAYERS (full_name, dob, nationality, position, height_cm, weight_kg, team_id, fbref_id, shirt_number) VALUES
('Marcus Rashford', '1997-10-31', 'England', 'Forward', 180, 70, 4, 'rashford', 10),
('Bruno Fernandes', '1994-09-08', 'Portugal', 'Midfielder', 179, 69, 4, 'bruno', 8),
('Casemiro', '1992-02-23', 'Brazil', 'Midfielder', 185, 84, 4, 'casemiro', 18),
('Lisandro Martínez', '1998-01-18', 'Argentina', 'Defender', 175, 78, 4, 'martinez', 6),
('André Onana', '1996-04-02', 'Cameroon', 'Goalkeeper', 190, 88, 4, 'onana', 24);

-- Chelsea
INSERT INTO PLAYERS (full_name, dob, nationality, position, height_cm, weight_kg, team_id, fbref_id, shirt_number) VALUES
('Cole Palmer', '2002-05-06', 'England', 'Midfielder', 189, 77, 5, 'palmer', 20),
('Nicolas Jackson', '2001-06-20', 'Senegal', 'Forward', 185, 78, 5, 'jackson', 15),
('Enzo Fernández', '2001-01-17', 'Argentina', 'Midfielder', 178, 76, 5, 'enzo', 8),
('Reece James', '1999-12-08', 'England', 'Defender', 180, 85, 5, 'reece', 24),
('Robert Sánchez', '1997-11-18', 'Spain', 'Goalkeeper', 197, 88, 5, 'sanchez', 1);

-- Tottenham
INSERT INTO PLAYERS (full_name, dob, nationality, position, height_cm, weight_kg, team_id, fbref_id, shirt_number) VALUES
('Son Heung-min', '1992-07-08', 'South Korea', 'Forward', 183, 78, 6, 'son', 7),
('James Maddison', '1996-11-23', 'England', 'Midfielder', 175, 73, 6, 'maddison', 10),
('Dejan Kulusevski', '2000-04-25', 'Sweden', 'Forward', 186, 80, 6, 'kulu', 21),
('Cristian Romero', '1998-04-27', 'Argentina', 'Defender', 185, 79, 6, 'romero', 17),
('Guglielmo Vicario', '1996-10-07', 'Italy', 'Goalkeeper', 194, 84, 6, 'vicario', 13);

-- Newcastle
INSERT INTO PLAYERS (full_name, dob, nationality, position, height_cm, weight_kg, team_id, fbref_id, shirt_number) VALUES
('Alexander Isak', '1999-09-21', 'Sweden', 'Forward', 192, 79, 7, 'isak', 14),
('Bruno Guimarães', '1997-11-16', 'Brazil', 'Midfielder', 182, 76, 7, 'brunog', 39),
('Anthony Gordon', '2001-02-24', 'England', 'Forward', 183, 75, 7, 'gordon', 10),
('Sven Botman', '2000-01-12', 'Netherlands', 'Defender', 195, 85, 7, 'botman', 4),
('Nick Pope', '1992-04-19', 'England', 'Goalkeeper', 198, 90, 7, 'pope', 22);

-- Brighton
INSERT INTO PLAYERS (full_name, dob, nationality, position, height_cm, weight_kg, team_id, fbref_id, shirt_number) VALUES
('Kaoru Mitoma', '1997-05-20', 'Japan', 'Forward', 178, 70, 8, 'mitoma', 22),
('João Pedro', '2001-09-26', 'Brazil', 'Forward', 180, 75, 8, 'joaopedro', 9),
('Moisés Caicedo', '2001-11-02', 'Ecuador', 'Midfielder', 178, 76, 8, 'caicedo', 25),
('Lewis Dunk', '1991-11-21', 'England', 'Defender', 191, 86, 8, 'dunk', 5),
('Jason Steele', '1990-08-18', 'England', 'Goalkeeper', 185, 82, 8, 'steele', 23);

-- ============================================
-- PLAYER_NICKNAMES
-- ============================================
INSERT INTO PLAYER_NICKNAMES (player_id, nickname) VALUES
(1, 'Starboy'),
(6, 'The Terminator'),
(11, 'Mo'),
(11, 'Egyptian King'),
(16, 'Rashy'),
(26, 'Sonny');

-- ============================================
-- STAFF (Managers and key staff)
-- ============================================
INSERT INTO STAFF (full_name, dob, nationality, role, team_id) VALUES
('Mikel Arteta', '1982-03-26', 'Spain', 'Manager', 1),
('Pep Guardiola', '1971-01-18', 'Spain', 'Manager', 2),
('Jürgen Klopp', '1967-06-16', 'Germany', 'Manager', 3),
('Erik ten Hag', '1970-02-02', 'Netherlands', 'Manager', 4),
('Mauricio Pochettino', '1972-03-02', 'Argentina', 'Manager', 5),
('Ange Postecoglou', '1965-08-27', 'Australia', 'Manager', 6),
('Eddie Howe', '1977-11-29', 'England', 'Manager', 7),
('Roberto De Zerbi', '1979-06-06', 'Italy', 'Manager', 8);

-- ============================================
-- MATCHES (15 realistic matches)
-- ============================================
INSERT INTO MATCHES (match_date, venue, home_score_final, away_score_final, home_xg, away_xg, attendance, season_id, home_team_id, away_team_id) VALUES
-- Matchweek 1
('2024-08-16 20:00:00', 'Emirates Stadium', 2, 1, 2.3, 1.1, 60000, 1, 1, 14),
('2024-08-17 15:00:00', 'Anfield', 3, 0, 2.8, 0.5, 53000, 1, 3, 19),
('2024-08-17 17:30:00', 'Tottenham Hotspur Stadium', 1, 1, 1.5, 1.4, 62000, 1, 6, 15),
('2024-08-18 14:00:00', 'Etihad Stadium', 4, 1, 3.2, 0.9, 54000, 1, 2, 18),

-- Matchweek 2
('2024-08-24 12:30:00', 'Villa Park', 2, 0, 1.9, 0.7, 42000, 1, 9, 1),
('2024-08-24 15:00:00', 'Old Trafford', 1, 0, 1.3, 0.6, 74000, 1, 4, 11),
('2024-08-24 17:30:00', 'Amex Stadium', 2, 1, 2.1, 1.3, 31000, 1, 8, 4),
('2024-08-25 16:30:00', 'Stamford Bridge', 6, 2, 4.5, 1.8, 40000, 1, 5, 14),

-- Matchweek 3
('2024-08-31 15:00:00', 'Etihad Stadium', 2, 2, 2.4, 2.1, 54000, 1, 2, 1),
('2024-08-31 15:00:00', 'Anfield', 3, 0, 2.6, 0.8, 53000, 1, 3, 4),
('2024-08-31 17:30:00', 'London Stadium', 1, 3, 0.9, 2.7, 62000, 1, 10, 2),

-- Big matches
('2024-09-14 12:30:00', 'Old Trafford', 1, 2, 1.4, 2.2, 74000, 1, 4, 3),
('2024-09-21 17:30:00', 'Emirates Stadium', 3, 1, 2.9, 1.5, 60000, 1, 1, 6),
('2024-09-22 16:30:00', 'Stamford Bridge', 1, 1, 1.6, 1.7, 40000, 1, 5, 7),
('2024-09-28 15:00:00', 'Etihad Stadium', 3, 1, 3.1, 1.2, 54000, 1, 2, 7);

-- ============================================
-- MATCH_LINEUPS (starters for key matches)
-- ============================================

-- Match 1: Arsenal 2-1 Wolves (Saka, Odegaard start)
INSERT INTO MATCH_LINEUPS (is_starter, position_in_match, minutes_played, match_id, player_id, team_id) VALUES
(TRUE, 'RW', 90, 1, 1, 1),  -- Saka
(TRUE, 'CAM', 90, 1, 2, 1),  -- Odegaard
(TRUE, 'ST', 78, 1, 3, 1),   -- Jesus
(TRUE, 'CB', 90, 1, 4, 1),   -- Saliba
(TRUE, 'GK', 90, 1, 5, 1);   -- Ramsdale

-- Match 4: Man City 4-1 Ipswich (Haaland hat-trick)
INSERT INTO MATCH_LINEUPS (is_starter, position_in_match, minutes_played, match_id, player_id, team_id) VALUES
(TRUE, 'ST', 80, 4, 6, 2),   -- Haaland
(TRUE, 'CAM', 75, 4, 7, 2),  -- De Bruyne
(TRUE, 'LW', 90, 4, 8, 2),   -- Foden
(TRUE, 'CB', 90, 4, 9, 2),   -- Dias
(TRUE, 'GK', 90, 4, 10, 2);  -- Ederson

-- Match 9: Man City 2-2 Arsenal (Big match)
INSERT INTO MATCH_LINEUPS (is_starter, position_in_match, minutes_played, match_id, player_id, team_id) VALUES
(TRUE, 'RW', 90, 9, 1, 1),   -- Saka
(TRUE, 'CAM', 90, 9, 2, 1),  -- Odegaard
(TRUE, 'ST', 90, 9, 6, 2),   -- Haaland
(TRUE, 'CAM', 90, 9, 7, 2);  -- De Bruyne

-- Match 10: Liverpool 3-0 Man United
INSERT INTO MATCH_LINEUPS (is_starter, position_in_match, minutes_played, match_id, player_id, team_id) VALUES
(TRUE, 'RW', 90, 10, 11, 3),  -- Salah
(TRUE, 'CB', 90, 10, 12, 3),  -- Van Dijk
(TRUE, 'ST', 85, 10, 16, 4),  -- Rashford
(TRUE, 'CAM', 90, 10, 17, 4); -- Bruno

-- ============================================
-- MATCH_EVENT (Goals, assists, cards)
-- ============================================

-- Match 1: Arsenal 2-1 Wolves
INSERT INTO MATCH_EVENT (match_id, minute, event_type, xG, xA, player_id, team_id) VALUES
(1, 23, 'Goal', 0.82, NULL, 1, 1),      -- Saka scores
(1, 22, 'Assist', NULL, 0.78, 2, 1),    -- Odegaard assists
(1, 67, 'Goal', 0.65, NULL, 3, 1),      -- Jesus scores
(1, 45, 'Yellow Card', NULL, NULL, 4, 1);

-- Match 4: Man City 4-1 Ipswich (Haaland hat-trick)
INSERT INTO MATCH_EVENT (match_id, minute, event_type, xG, xA, player_id, team_id) VALUES
(4, 12, 'Goal', 0.91, NULL, 6, 2),      -- Haaland goal 1
(4, 11, 'Assist', NULL, 0.85, 7, 2),    -- De Bruyne assist
(4, 34, 'Goal', 0.76, NULL, 6, 2),      -- Haaland goal 2
(4, 68, 'Goal', 0.88, NULL, 6, 2),      -- Haaland goal 3 (hat-trick)
(4, 67, 'Assist', NULL, 0.72, 8, 2);    -- Foden assist

-- Match 9: Man City 2-2 Arsenal
INSERT INTO MATCH_EVENT (match_id, minute, event_type, xG, xA, player_id, team_id) VALUES
(9, 9, 'Goal', 0.79, NULL, 6, 2),       -- Haaland
(9, 22, 'Goal', 0.71, NULL, 1, 1),      -- Saka equalizes
(9, 45, 'Goal', 0.83, NULL, 3, 1),      -- Jesus for Arsenal
(9, 82, 'Goal', 0.68, NULL, 8, 2);      -- Foden equalizes

-- Match 10: Liverpool 3-0 Man United (Salah brace)
INSERT INTO MATCH_EVENT (match_id, minute, event_type, xG, xA, player_id, team_id) VALUES
(10, 15, 'Goal', 0.86, NULL, 11, 3),    -- Salah
(10, 34, 'Goal', 0.92, NULL, 11, 3),    -- Salah again
(10, 78, 'Goal', 0.54, NULL, 14, 3),    -- Nunez
(10, 56, 'Red Card', NULL, NULL, 18, 4); -- Casemiro sent off

-- Match 8: Chelsea 6-2 Wolves (Palmer masterclass)
INSERT INTO MATCH_EVENT (match_id, minute, event_type, xG, xA, player_id, team_id) VALUES
(8, 12, 'Goal', 0.77, NULL, 21, 5),     -- Palmer
(8, 23, 'Goal', 0.81, NULL, 21, 5),     -- Palmer
(8, 34, 'Goal', 0.69, NULL, 22, 5),     -- Jackson
(8, 56, 'Goal', 0.88, NULL, 21, 5),     -- Palmer hat-trick
(8, 67, 'Assist', NULL, 0.91, 21, 5);   -- Palmer assists

-- ============================================
-- MATCH_PREDICTIONS (AI predictions before matches)
-- ============================================
INSERT INTO MATCH_PREDICTIONS (prediction_date, predicted_score_home, predicted_score_away, 
                                win_probability_home, draw_probability, win_probability_away, match_id) VALUES
('2024-08-15 10:00:00', 2, 1, 0.6200, 0.2300, 0.1500, 1),
('2024-08-16 10:00:00', 2, 0, 0.7100, 0.1900, 0.1000, 2),
('2024-08-16 10:00:00', 1, 1, 0.4200, 0.3500, 0.2300, 3),
('2024-08-17 10:00:00', 3, 1, 0.7800, 0.1400, 0.0800, 4),
('2024-08-30 10:00:00', 2, 2, 0.3800, 0.3400, 0.2800, 9),
('2024-09-13 10:00:00', 1, 2, 0.3200, 0.2800, 0.4000, 12);

COMMIT;

-- ============================================
-- VERIFICATION QUERIES
-- ============================================
SELECT 'Leagues: ' || COUNT(*) FROM LEAGUES;
SELECT 'Seasons: ' || COUNT(*) FROM SEASONS;
SELECT 'Teams: ' || COUNT(*) FROM TEAMS;
SELECT 'Players: ' || COUNT(*) FROM PLAYERS;
SELECT 'Staff: ' || COUNT(*) FROM STAFF;
SELECT 'Matches: ' || COUNT(*) FROM MATCHES;
SELECT 'Match Events: ' || COUNT(*) FROM MATCH_EVENT;
SELECT 'Match Lineups: ' || COUNT(*) FROM MATCH_LINEUPS;
SELECT 'Predictions: ' || COUNT(*) FROM MATCH_PREDICTIONS;

-- Success message
DO $$ 
BEGIN 
    RAISE NOTICE '✅ Mock Premier League data inserted successfully!';
    RAISE NOTICE '   - 3 Leagues, 20 Teams, 37 Players';
    RAISE NOTICE '   - 15 Matches with realistic scores and xG';
    RAISE NOTICE '   - Match events, lineups, and predictions';
    RAISE NOTICE '   - Ready for CRUD operations and analytics!';
END $$;