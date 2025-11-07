"""
View-only API endpoints for teams, players, and matches
Public access - no authentication required for viewing
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from src.core.database import get_db
from src.models import models
from src.schemas import schemas
from src.api.dependencies import get_team_or_404, get_player_or_404, get_match_or_404

router = APIRouter(prefix="/view", tags=["View"])


@router.get("/teams", response_model=List[schemas.Team])
def get_all_teams(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all teams (view-only)"""
    teams = db.query(models.Team).offset(skip).limit(limit).all()
    return teams


@router.get("/teams/{team_id}", response_model=schemas.Team)
def get_team(team_id: int, db: Session = Depends(get_db)):
    """Get a specific team by ID"""
    return get_team_or_404(team_id, db)


@router.get("/teams/{team_id}/players", response_model=List[schemas.Player])
def get_team_players(team_id: int, db: Session = Depends(get_db)):
    """Get all players for a specific team"""
    get_team_or_404(team_id, db)  # Verify team exists
    players = db.query(models.Player).filter(models.Player.team_id == team_id).all()
    return players


@router.get("/players", response_model=List[schemas.Player])
def get_all_players(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    team_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all players (optionally filtered by team)"""
    query = db.query(models.Player)
    if team_id:
        query = query.filter(models.Player.team_id == team_id)
    players = query.offset(skip).limit(limit).all()
    return players


@router.get("/players/{player_id}", response_model=schemas.Player)
def get_player(player_id: int, db: Session = Depends(get_db)):
    """Get a specific player by ID"""
    return get_player_or_404(player_id, db)


@router.get("/matches", response_model=List[schemas.MatchWithTeams])
def get_all_matches(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    team_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all matches (optionally filtered by team)"""
    query = db.query(models.Match)
    if team_id:
        query = query.filter(
            (models.Match.home_team_id == team_id) | 
            (models.Match.away_team_id == team_id)
        )
    matches = query.order_by(models.Match.match_date.desc()).offset(skip).limit(limit).all()
    return matches


@router.get("/matches/{match_id}", response_model=schemas.MatchWithTeams)
def get_match(match_id: int, db: Session = Depends(get_db)):
    """Get a specific match by ID"""
    return get_match_or_404(match_id, db)


@router.get("/teams/{team_id}/matches", response_model=List[schemas.MatchWithTeams])
def get_team_matches(
    team_id: int,
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get recent matches for a team"""
    get_team_or_404(team_id, db)
    
    matches = (
        db.query(models.Match)
        .filter(
            (models.Match.home_team_id == team_id) | 
            (models.Match.away_team_id == team_id)
        )
        .order_by(models.Match.match_date.desc())
        .limit(limit)
        .all()
    )
    
    return matches

