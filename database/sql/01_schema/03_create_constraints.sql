-- Simple Seed Data for Demo

-- LEAGUES
INSERT INTO LEAGUES (name, country, tier, logo_url) VALUES
('Premier League', 'England', 1, 'https://example.com/epl.png'),
('La Liga', 'Spain', 1, 'https://example.com/laliga.png'),
('Serie A', 'Italy', 1, 'https://example.com/seriea.png'),
('Bundesliga', 'Germany', 1, 'https://example.com/bundesliga.png');

-- SEASONS
INSERT INTO SEASONS (year, start_date, end_date, league_id) VALUES
('2024-25', '2024-08-16', '2025-05-25', 1),
('2024-25', '2024-08-18', '2025-05-31', 2);

-- TEAMS
INSERT INTO TEAMS (name, founded_year, stadium_name, city, logo_url) VALUES
('Manchester United', 1878, 'Old Trafford', 'Manchester', 'https://example.com/manutd.png'),
('Liverpool FC', 1892, 'Anfield', 'Liverpool', 'https://example.com/liverpool.png'),
('Manchester City', 1880, 'Etihad Stadium', 'Manchester', 'https://example.com/mancity.png'),
('Arsenal FC', 1886, 'Emirates Stadium', 'London', 'https://example.com/arsenal.png'),
('Real Madrid', 1902, 'Santiago Bernabéu', 'Madrid', 'https://example.com/realmadrid.png'),
('FC Barcelona', 1899, 'Camp Nou', 'Barcelona', 'https://example.com/barca.png');

-- TEAM_SEASONS
INSERT INTO TEAM_SEASONS (team_id, season_id) VALUES
(1, 1), (2, 1), (3, 1), (4, 1),
(5, 2), (6, 2);

-- PLAYERS
INSERT INTO PLAYERS (full_name, dob, nationality, position, height_cm, weight_kg, team_id) VALUES
('Marcus Rashford', '1997-10-31', 'England', 'Forward', 180, 70, 1),
('Bruno Fernandes', '1994-09-08', 'Portugal', 'Midfielder', 179, 69, 1),
('Casemiro', '1992-02-23', 'Brazil', 'Midfielder', 185, 84, 1),
('Mohamed Salah', '1992-06-15', 'Egypt', 'Forward', 175, 71, 2),
('Virgil van Dijk', '1991-07-08', 'Netherlands', 'Defender', 193, 92, 2),
('Alisson Becker', '1992-10-02', 'Brazil', 'Goalkeeper', 191, 91, 2),
('Erling Haaland', '2000-07-21', 'Norway', 'Forward', 195, 88, 3),
('Kevin De Bruyne', '1991-06-28', 'Belgium', 'Midfielder', 181, 70, 3),
('Ederson', '1993-08-17', 'Brazil', 'Goalkeeper', 188, 89, 3),
('Bukayo Saka', '2001-09-05', 'England', 'Forward', 178, 72, 4),
('Martin Ødegaard', '1998-12-17', 'Norway', 'Midfielder', 178, 68, 4),
('Vinícius Júnior', '2000-07-12', 'Brazil', 'Forward', 176, 73, 5),
('Jude Bellingham', '2003-06-29', 'England', 'Midfielder', 186, 75, 5),
('Robert Lewandowski', '1988-08-21', 'Poland', 'Forward', 185, 81, 6),
('Pedri', '2002-11-25', 'Spain', 'Midfielder', 174, 60, 6);

-- PLAYER_NICKNAMES
INSERT INTO PLAYER_NICKNAMES (player_id, nickname) VALUES
(1, 'Rashford'),
(4, 'Mo Salah'),
(4, 'Egyptian King'),
(7, 'The Terminator'),
(12, 'Vini Jr'),
(14, 'Lewy');

-- STAFF
INSERT INTO STAFF (full_name, dob, nationality, role, team_id) VALUES
('Erik ten Hag', '1970-02-02', 'Netherlands', 'Manager', 1),
('Jürgen Klopp', '1967-06-16', 'Germany', 'Manager', 2),
('Pep Guardiola', '1971-01-18', 'Spain', 'Manager', 3),
('Mikel Arteta', '1982-03-26', 'Spain', 'Manager', 4),
('Carlo Ancelotti', '1959-06-10', 'Italy', 'Manager', 5),
('Xavi Hernández', '1980-01-25', 'Spain', 'Manager', 6);

-- MATCHES
INSERT INTO MATCHES (match_date, venue, home_score_final, away_score_final, season_id, home_team_id, away_team_id) VALUES
('2024-08-16 20:00:00', 'Old Trafford', 1, 0, 1, 1, 2),
('2024-08-17 17:30:00', 'Emirates Stadium', 2, 2, 1, 4, 3),
('2024-08-24 15:00:00', 'Anfield', 3, 1, 1, 2, 4),
('2024-08-25 16:30:00', 'Etihad Stadium', 2, 1, 1, 3, 1),
('2024-08-18 21:00:00', 'Santiago Bernabéu', 3, 0, 2, 5, 6),
('2024-08-25 19:00:00', 'Camp Nou', 1, 2, 2, 6, 5);

-- MATCH_LINEUPS (just starters for simplicity)
INSERT INTO MATCH_LINEUPS (is_starter, position_in_match, match_id, player_id, team_id) VALUES
(TRUE, 'Forward', 1, 1, 1),
(TRUE, 'Midfielder', 1, 2, 1),
(TRUE, 'Forward', 1, 4, 2),
(TRUE, 'Defender', 1, 5, 2),
(TRUE, 'Goalkeeper', 1, 6, 2),
(TRUE, 'Forward', 2, 10, 4),
(TRUE, 'Midfielder', 2, 11, 4),
(TRUE, 'Forward', 2, 7, 3),
(TRUE, 'Midfielder', 2, 8, 3);

-- MATCH_EVENT
INSERT INTO MATCH_EVENT (match_id, minute, event_type, xG, xA, player_id, team_id) VALUES
(1, 23, 'Goal', 0.85, NULL, 1, 1),
(1, 22, 'Assist', NULL, 0.75, 2, 1),
(2, 15, 'Goal', 0.65, NULL, 10, 4),
(2, 34, 'Goal', 0.72, NULL, 7, 3),
(2, 56, 'Goal', 0.58, NULL, 10, 4),
(2, 78, 'Goal', 0.81, NULL, 7, 3),
(3, 12, 'Goal', 0.92, NULL, 4, 2),
(3, 45, 'Goal', 0.67, NULL, 4, 2),
(3, 68, 'Goal', 0.73, NULL, 4, 2);

-- MATCH_PREDICTIONS
INSERT INTO MATCH_PREDICTIONS (prediction_date, predicted_score_home, predicted_score_away, win_probability_home, draw_probability, win_probability_away, match_id) VALUES
('2024-08-15 10:00:00', 2, 1, 0.5200, 0.2800, 0.2000, 1),
('2024-08-16 10:00:00', 1, 1, 0.3500, 0.3800, 0.2700, 2),
('2024-08-23 10:00:00', 2, 0, 0.6800, 0.2100, 0.1100, 3);