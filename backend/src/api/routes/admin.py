"""
Admin API endpoints for CRUD operations
Only accessible to admin users
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.core.security import get_current_admin_user
from src.models import models
from src.schemas import schemas
from src.api.dependencies import get_team_or_404, get_player_or_404, get_match_or_404

router = APIRouter(prefix="/admin", tags=["Admin"])


# ============================================
# TEAM ADMIN ENDPOINTS
# ============================================

@router.post("/teams", response_model=schemas.Team, status_code=status.HTTP_201_CREATED)
def create_team(
    team: schemas.TeamCreate,
    current_user: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new team (Admin only)"""
    existing_team = db.query(models.Team).filter(models.Team.name == team.name).first()
    if existing_team:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team with name '{team.name}' already exists"
        )
    
    db_team = models.Team(**team.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


@router.put("/teams/{team_id}", response_model=schemas.Team)
def update_team(
    team_id: int,
    team_update: schemas.TeamUpdate,
    current_user: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update an existing team (Admin only)"""
    db_team = get_team_or_404(team_id, db)
    
    update_data = team_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_team, key, value)
    
    db.commit()
    db.refresh(db_team)
    return db_team


@router.delete("/teams/{team_id}", response_model=schemas.MessageResponse)
def delete_team(
    team_id: int,
    current_user: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a team (Admin only)"""
    db_team = get_team_or_404(team_id, db)
    team_name = db_team.name
    
    db.delete(db_team)
    db.commit()
    
    return schemas.MessageResponse(
        message="Team deleted successfully",
        detail=f"Team '{team_name}' has been removed"
    )


# ============================================
# PLAYER ADMIN ENDPOINTS
# ============================================

@router.post("/players", response_model=schemas.Player, status_code=status.HTTP_201_CREATED)
def create_player(
    player: schemas.PlayerCreate,
    current_user: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new player (Admin only)"""
    if player.team_id:
        get_team_or_404(player.team_id, db)  # Verify team exists
    
    db_player = models.Player(**player.model_dump())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


@router.put("/players/{player_id}", response_model=schemas.Player)
def update_player(
    player_id: int,
    player_update: schemas.PlayerUpdate,
    current_user: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update an existing player (Admin only)"""
    db_player = get_player_or_404(player_id, db)
    
    if player_update.team_id:
        get_team_or_404(player_update.team_id, db)  # Verify team exists
    
    update_data = player_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_player, key, value)
    
    db.commit()
    db.refresh(db_player)
    return db_player


@router.delete("/players/{player_id}", response_model=schemas.MessageResponse)
def delete_player(
    player_id: int,
    current_user: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a player (Admin only)"""
    db_player = get_player_or_404(player_id, db)
    player_name = db_player.full_name
    
    db.delete(db_player)
    db.commit()
    
    return schemas.MessageResponse(
        message="Player deleted successfully",
        detail=f"Player '{player_name}' has been removed"
    )


# ============================================
# MATCH ADMIN ENDPOINTS
# ============================================

@router.post("/matches", response_model=schemas.Match, status_code=status.HTTP_201_CREATED)
def create_match(
    match: schemas.MatchCreate,
    current_user: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new match (Admin only)"""
    get_team_or_404(match.home_team_id, db)
    get_team_or_404(match.away_team_id, db)
    
    db_match = models.Match(**match.model_dump())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


@router.put("/matches/{match_id}", response_model=schemas.Match)
def update_match(
    match_id: int,
    match_update: schemas.MatchUpdate,
    current_user: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update an existing match (Admin only)"""
    db_match = get_match_or_404(match_id, db)
    
    update_data = match_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_match, key, value)
    
    db.commit()
    db.refresh(db_match)
    return db_match


@router.delete("/matches/{match_id}", response_model=schemas.MessageResponse)
def delete_match(
    match_id: int,
    current_user: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a match (Admin only)"""
    db_match = get_match_or_404(match_id, db)
    
    db.delete(db_match)
    db.commit()
    
    return schemas.MessageResponse(
        message="Match deleted successfully",
        detail=f"Match {match_id} has been removed"
    )


# ============================================
# USER ADMIN ENDPOINTS
# ============================================

@router.get("/users", response_model=List[schemas.UserProfile])
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all users (Admin only)"""
    users = db.query(models.User).offset(skip).limit(limit).all()
    
    result = []
    for user in users:
        leaderboard = db.query(models.UserLeaderboard).filter(
            models.UserLeaderboard.user_id == user.user_id
        ).first()
        
        result.append({
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_admin": user.is_admin,
            "profile_picture_url": user.profile_picture_url,
            "created_at": user.created_at,
            "total_points": leaderboard.total_points if leaderboard else 0,
            "total_predictions": leaderboard.total_predictions if leaderboard else 0,
            "correct_predictions": leaderboard.correct_predictions if leaderboard else 0,
            "accuracy_percentage": float(leaderboard.accuracy_percentage) if leaderboard else 0.0,
            "rank": leaderboard.rank if leaderboard else None
        })
    
    return result

