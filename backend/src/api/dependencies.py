from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.models import models

def get_team_or_404(team_id, db = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.team_id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found"
        )
    
    return team

def get_player_or_404(player_id: int, db: Session = Depends(get_db)) -> models.Player:
    player = db.query(models.Player).filter(models.Player.player_id == player_id).first()
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )
    return player


def get_match_or_404(match_id: int, db: Session = Depends(get_db)) -> models.Match:
    match = db.query(models.Match).filter(models.Match.match_id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with ID {match_id} not found"
        )
    return match