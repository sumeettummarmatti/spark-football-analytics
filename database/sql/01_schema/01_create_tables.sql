-- SPARK Database Schema - FBref Compatible Version
DROP TABLE IF EXISTS MATCH_PREDICTIONS CASCADE;
DROP TABLE IF EXISTS MATCH_EVENT CASCADE;
DROP TABLE IF EXISTS MATCH_LINEUPS CASCADE;
DROP TABLE IF EXISTS MATCHES CASCADE;
DROP TABLE IF EXISTS TEAM_SEASONS CASCADE;
DROP TABLE IF EXISTS PLAYER_NICKNAMES CASCADE;
DROP TABLE IF EXISTS STAFF CASCADE;
DROP TABLE IF EXISTS PLAYERS CASCADE;
DROP TABLE IF EXISTS TEAMS CASCADE;
DROP TABLE IF EXISTS SEASONS CASCADE;
DROP TABLE IF EXISTS LEAGUES CASCADE;

-- LEAGUES
CREATE TABLE LEAGUES (
    league_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50),
    tier INT,
    logo_url VARCHAR(255),
    fbref_id VARCHAR(20) UNIQUE  -- FBref league ID
);

-- SEASONS
CREATE TABLE SEASONS (
    season_id SERIAL PRIMARY KEY,
    year VARCHAR(10) NOT NULL,
    start_date DATE,
    end_date DATE,
    league_id INT,
    FOREIGN KEY (league_id) REFERENCES LEAGUES(league_id) ON DELETE CASCADE
);

-- TEAMS
CREATE TABLE TEAMS (
    team_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    founded_year INT,
    stadium_name VARCHAR(100),
    city VARCHAR(100),
    logo_url VARCHAR(255),
    fbref_id VARCHAR(20) UNIQUE  -- FBref team ID
);

-- PLAYERS
CREATE TABLE PLAYERS (
    player_id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    dob DATE,
    nationality VARCHAR(50),
    position VARCHAR(20) CHECK (position IN ('Goalkeeper', 'Defender', 'Midfielder', 'Forward')),
    height_cm INT,
    weight_kg INT,
    team_id INT,
    fbref_id VARCHAR(20) UNIQUE,  -- FBref player ID
    shirt_number INT,
    FOREIGN KEY (team_id) REFERENCES TEAMS(team_id) ON DELETE SET NULL
);

-- PLAYER_NICKNAMES
CREATE TABLE PLAYER_NICKNAMES (
    player_id INT,
    nickname VARCHAR(50),
    PRIMARY KEY (player_id, nickname),
    FOREIGN KEY (player_id) REFERENCES PLAYERS(player_id) ON DELETE CASCADE
);

-- STAFF
CREATE TABLE STAFF (
    staff_id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    dob DATE,
    nationality VARCHAR(50),
    role VARCHAR(50),
    team_id INT,
    FOREIGN KEY (team_id) REFERENCES TEAMS(team_id) ON DELETE SET NULL
);

-- TEAM_SEASONS
CREATE TABLE TEAM_SEASONS (
    team_season_id SERIAL PRIMARY KEY,
    team_id INT NOT NULL,
    season_id INT NOT NULL,
    points INT DEFAULT 0,
    wins INT DEFAULT 0,
    draws INT DEFAULT 0,
    losses INT DEFAULT 0,
    goals_for INT DEFAULT 0,
    goals_against INT DEFAULT 0,
    goal_diff INT DEFAULT 0,
    position INT,
    FOREIGN KEY (team_id) REFERENCES TEAMS(team_id) ON DELETE CASCADE,
    FOREIGN KEY (season_id) REFERENCES SEASONS(season_id) ON DELETE CASCADE,
    UNIQUE(team_id, season_id)
);

-- MATCHES
CREATE TABLE MATCHES (
    match_id SERIAL PRIMARY KEY,
    match_date TIMESTAMP NOT NULL,
    venue VARCHAR(100),
    home_score_final INT,
    away_score_final INT,
    home_xg DECIMAL(4, 2),  -- Team xG
    away_xg DECIMAL(4, 2),  -- Team xG
    attendance INT,
    referee VARCHAR(100),
    season_id INT NOT NULL,
    home_team_id INT NOT NULL,
    away_team_id INT NOT NULL,
    fbref_id VARCHAR(20) UNIQUE,  -- FBref match ID
    FOREIGN KEY (season_id) REFERENCES SEASONS(season_id) ON DELETE CASCADE,
    FOREIGN KEY (home_team_id) REFERENCES TEAMS(team_id) ON DELETE CASCADE,
    FOREIGN KEY (away_team_id) REFERENCES TEAMS(team_id) ON DELETE CASCADE
);

-- MATCH_LINEUPS
CREATE TABLE MATCH_LINEUPS (
    lineup_id SERIAL PRIMARY KEY,
    is_starter BOOLEAN,
    position_in_match VARCHAR(20),
    minutes_played INT DEFAULT 0,
    match_id INT NOT NULL,
    player_id INT NOT NULL,
    team_id INT NOT NULL,
    FOREIGN KEY (match_id) REFERENCES MATCHES(match_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES PLAYERS(player_id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES TEAMS(team_id) ON DELETE CASCADE
);

-- MATCH_EVENT
CREATE TABLE MATCH_EVENT (
    match_id INT,
    event_id SERIAL,
    minute INT,
    event_type VARCHAR(50),
    xG DECIMAL(4, 3),
    xA DECIMAL(4, 3),
    player_id INT,
    team_id INT,
    PRIMARY KEY (match_id, event_id),
    FOREIGN KEY (match_id) REFERENCES MATCHES(match_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES PLAYERS(player_id) ON DELETE SET NULL,
    FOREIGN KEY (team_id) REFERENCES TEAMS(team_id) ON DELETE CASCADE
);

-- MATCH_PREDICTIONS
CREATE TABLE MATCH_PREDICTIONS (
    prediction_id SERIAL PRIMARY KEY,
    prediction_date TIMESTAMP,
    predicted_score_home INT,
    predicted_score_away INT,
    win_probability_home DECIMAL(5, 4),
    draw_probability DECIMAL(5, 4),
    win_probability_away DECIMAL(5, 4),
    match_id INT UNIQUE,
    FOREIGN KEY (match_id) REFERENCES MATCHES(match_id) ON DELETE CASCADE
);