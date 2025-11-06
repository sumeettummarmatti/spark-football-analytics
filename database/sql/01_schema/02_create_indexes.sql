-- Essential Indexes for Performance

-- Foreign key indexes
CREATE INDEX idx_seasons_league ON SEASONS(league_id);
CREATE INDEX idx_players_team ON PLAYERS(team_id);
CREATE INDEX idx_staff_team ON STAFF(team_id);
CREATE INDEX idx_teamseasons_team ON TEAM_SEASONS(team_id);
CREATE INDEX idx_teamseasons_season ON TEAM_SEASONS(season_id);
CREATE INDEX idx_matches_season ON MATCHES(season_id);
CREATE INDEX idx_matches_home ON MATCHES(home_team_id);
CREATE INDEX idx_matches_away ON MATCHES(away_team_id);
CREATE INDEX idx_lineups_match ON MATCH_LINEUPS(match_id);
CREATE INDEX idx_lineups_player ON MATCH_LINEUPS(player_id);
CREATE INDEX idx_events_match ON MATCH_EVENT(match_id);
CREATE INDEX idx_predictions_match ON MATCH_PREDICTIONS(match_id);

-- Common query indexes
CREATE INDEX idx_matches_date ON MATCHES(match_date);
CREATE INDEX idx_players_position ON PLAYERS(position);