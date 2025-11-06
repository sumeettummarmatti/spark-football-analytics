"""
SQLAlchemy ORM Models
Maps to database tables
"""
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Boolean, 
    DECIMAL, ForeignKey, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.core.database import Base


class League(Base):
    __tablename__ = "leagues"
    
    league_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    country = Column(String(50))
    tier = Column(Integer)
    logo_url = Column(String(255))
    fbref_id = Column(String(20), unique=True)
    
    # Relationships
    seasons = relationship("Season", back_populates="league")


class Season(Base):
    __tablename__ = "seasons"
    
    season_id = Column(Integer, primary_key=True, index=True)
    year = Column(String(10), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    league_id = Column(Integer, ForeignKey("leagues.league_id", ondelete="CASCADE"))
    
    # Relationships
    league = relationship("League", back_populates="seasons")
    matches = relationship("Match", back_populates="season")
    team_seasons = relationship("TeamSeason", back_populates="season")


class Team(Base):
    __tablename__ = "teams"
    
    team_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    founded_year = Column(Integer)
    stadium_name = Column(String(100))
    city = Column(String(100))
    logo_url = Column(String(255))
    fbref_id = Column(String(20), unique=True)
    
    # Relationships
    players = relationship("Player", back_populates="team")
    staff = relationship("Staff", back_populates="team")
    home_matches = relationship("Match", foreign_keys="Match.home_team_id", back_populates="home_team")
    away_matches = relationship("Match", foreign_keys="Match.away_team_id", back_populates="away_team")
    team_seasons = relationship("TeamSeason", back_populates="team")


class Player(Base):
    __tablename__ = "players"
    
    player_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    dob = Column(Date)
    nationality = Column(String(50))
    position = Column(String(20))
    height_cm = Column(Integer)
    weight_kg = Column(Integer)
    team_id = Column(Integer, ForeignKey("teams.team_id", ondelete="SET NULL"))
    fbref_id = Column(String(20), unique=True)
    shirt_number = Column(Integer)
    
    # Relationships
    team = relationship("Team", back_populates="players")
    nicknames = relationship("PlayerNickname", back_populates="player")
    match_lineups = relationship("MatchLineup", back_populates="player")
    match_events = relationship("MatchEvent", back_populates="player")


class PlayerNickname(Base):
    __tablename__ = "player_nicknames"
    
    player_id = Column(Integer, ForeignKey("players.player_id", ondelete="CASCADE"), primary_key=True)
    nickname = Column(String(50), primary_key=True)
    
    # Relationships
    player = relationship("Player", back_populates="nicknames")


class Staff(Base):
    __tablename__ = "staff"
    
    staff_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    dob = Column(Date)
    nationality = Column(String(50))
    role = Column(String(50))
    team_id = Column(Integer, ForeignKey("teams.team_id", ondelete="SET NULL"))
    
    # Relationships
    team = relationship("Team", back_populates="staff")


class TeamSeason(Base):
    __tablename__ = "team_seasons"
    
    team_season_id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.team_id", ondelete="CASCADE"), nullable=False)
    season_id = Column(Integer, ForeignKey("seasons.season_id", ondelete="CASCADE"), nullable=False)
    points = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    draws = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    goals_for = Column(Integer, default=0)
    goals_against = Column(Integer, default=0)
    goal_diff = Column(Integer, default=0)
    position = Column(Integer)
    
    # Relationships
    team = relationship("Team", back_populates="team_seasons")
    season = relationship("Season", back_populates="team_seasons")
    
    __table_args__ = (
        UniqueConstraint('team_id', 'season_id', name='uk_team_season'),
    )


class Match(Base):
    __tablename__ = "matches"
    
    match_id = Column(Integer, primary_key=True, index=True)
    match_date = Column(DateTime, nullable=False)
    venue = Column(String(100))
    home_score_final = Column(Integer)
    away_score_final = Column(Integer)
    home_xg = Column(DECIMAL(4, 2))
    away_xg = Column(DECIMAL(4, 2))
    attendance = Column(Integer)
    referee = Column(String(100))
    season_id = Column(Integer, ForeignKey("seasons.season_id", ondelete="CASCADE"), nullable=False)
    home_team_id = Column(Integer, ForeignKey("teams.team_id", ondelete="CASCADE"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.team_id", ondelete="CASCADE"), nullable=False)
    fbref_id = Column(String(20), unique=True)
    
    # Relationships
    season = relationship("Season", back_populates="matches")
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    lineups = relationship("MatchLineup", back_populates="match")
    events = relationship("MatchEvent", back_populates="match")
    prediction = relationship("MatchPrediction", uselist=False, back_populates="match")


class MatchLineup(Base):
    __tablename__ = "match_lineups"
    
    lineup_id = Column(Integer, primary_key=True, index=True)
    is_starter = Column(Boolean)
    position_in_match = Column(String(20))
    minutes_played = Column(Integer, default=0)
    match_id = Column(Integer, ForeignKey("matches.match_id", ondelete="CASCADE"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.player_id", ondelete="CASCADE"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.team_id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    match = relationship("Match", back_populates="lineups")
    player = relationship("Player", back_populates="match_lineups")


class MatchEvent(Base):
    __tablename__ = "match_event"
    
    match_id = Column(Integer, ForeignKey("matches.match_id", ondelete="CASCADE"), primary_key=True)
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    minute = Column(Integer)
    event_type = Column(String(50))
    xg = Column(DECIMAL(4, 3))
    xa = Column(DECIMAL(4, 3))
    player_id = Column(Integer, ForeignKey("players.player_id", ondelete="SET NULL"))
    team_id = Column(Integer, ForeignKey("teams.team_id", ondelete="CASCADE"))
    
    # Relationships
    match = relationship("Match", back_populates="events")
    player = relationship("Player", back_populates="match_events")


class MatchPrediction(Base):
    __tablename__ = "match_predictions"
    
    prediction_id = Column(Integer, primary_key=True, index=True)
    prediction_date = Column(DateTime)
    predicted_score_home = Column(Integer)
    predicted_score_away = Column(Integer)
    win_probability_home = Column(DECIMAL(5, 4))
    draw_probability = Column(DECIMAL(5, 4))
    win_probability_away = Column(DECIMAL(5, 4))
    match_id = Column(Integer, ForeignKey("matches.match_id", ondelete="CASCADE"), unique=True)
    
    # Relationships
    match = relationship("Match", back_populates="prediction")