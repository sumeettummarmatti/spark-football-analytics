"""
Teams API endpoints - CRUD operations
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.models import models
from src.schemas import schemas
from src.api.dependencies import get_team_or_404

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.get("/", response_model=List[schemas.Team])
def get_all_teams(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all teams with pagination
    
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    teams = db.query(models.Team).offset(skip).limit(limit).all()
    return teams


@router.get("/{team_id}", response_model=schemas.Team)
def get_team(team_id: int, db: Session = Depends(get_db)):
    """Get a specific team by ID"""
    team = get_team_or_404(team_id, db)
    return team


@router.post("/", response_model=schemas.Team, status_code=status.HTTP_201_CREATED)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    """
    Create a new team
    
    - **name**: Team name (required, unique)
    - **founded_year**: Year team was founded
    - **stadium_name**: Home stadium name
    - **city**: City where team is based
    """
    # Check if team name already exists
    existing_team = db.query(models.Team).filter(models.Team.name == team.name).first()
    if existing_team:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team with name '{team.name}' already exists"
        )
    
    # Create new team
    db_team = models.Team(**team.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


@router.put("/{team_id}", response_model=schemas.Team)
def update_team(
    team_id: int,
    team_update: schemas.TeamUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing team"""
    db_team = get_team_or_404(team_id, db)
    
    # Update only provided fields
    update_data = team_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_team, key, value)
    
    db.commit()
    db.refresh(db_team)
    return db_team


@router.delete("/{team_id}", response_model=schemas.MessageResponse)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    """Delete a team"""
    db_team = get_team_or_404(team_id, db)
    
    db.delete(db_team)
    db.commit()
    
    return schemas.MessageResponse(
        message="Team deleted successfully",
        detail=f"Team '{db_team.name}' has been removed"
    )


@router.get("/{team_id}/players", response_model=List[schemas.Player])
def get_team_players(team_id: int, db: Session = Depends(get_db)):
    """Get all players for a specific team"""
    team = get_team_or_404(team_id, db)
    players = db.query(models.Player).filter(models.Player.team_id == team_id).all()
    return players


@router.get("/{team_id}/matches", response_model=List[schemas.MatchWithTeams])
def get_team_matches(
    team_id: int,
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get recent matches for a team (home and away)"""
    team = get_team_or_404(team_id, db)
    
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