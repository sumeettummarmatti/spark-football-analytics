"""
Follow/Unfollow API endpoints for teams and players
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.core.security import get_current_user
from src.models import models
from src.schemas import schemas
from src.api.dependencies import get_team_or_404, get_player_or_404

router = APIRouter(prefix="/follow", tags=["Follow"])


@router.post("/team", response_model=schemas.MessageResponse)
def follow_team(
    request: schemas.FollowTeamRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Follow a team"""
    # Verify team exists
    team = get_team_or_404(request.team_id, db)
    
    # Check if already following
    existing = db.query(models.UserFollowsTeam).filter(
        models.UserFollowsTeam.user_id == current_user.user_id,
        models.UserFollowsTeam.team_id == request.team_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You are already following {team.name}"
        )
    
    # Create follow relationship
    follow = models.UserFollowsTeam(
        user_id=current_user.user_id,
        team_id=request.team_id
    )
    db.add(follow)
    db.commit()
    
    return schemas.MessageResponse(
        message=f"Successfully followed {team.name}",
        detail=f"You are now following {team.name}"
    )


@router.delete("/team/{team_id}", response_model=schemas.MessageResponse)
def unfollow_team(
    team_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Unfollow a team"""
    follow = db.query(models.UserFollowsTeam).filter(
        models.UserFollowsTeam.user_id == current_user.user_id,
        models.UserFollowsTeam.team_id == team_id
    ).first()
    
    if not follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not following this team"
        )
    
    team_name = follow.team.name if follow.team else "this team"
    db.delete(follow)
    db.commit()
    
    return schemas.MessageResponse(
        message=f"Successfully unfollowed {team_name}",
        detail=f"You are no longer following {team_name}"
    )


@router.get("/teams", response_model=List[schemas.Team])
def get_followed_teams(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all teams followed by current user"""
    follows = db.query(models.UserFollowsTeam).filter(
        models.UserFollowsTeam.user_id == current_user.user_id
    ).all()
    
    teams = [follow.team for follow in follows if follow.team]
    return teams


@router.post("/player", response_model=schemas.MessageResponse)
def follow_player(
    request: schemas.FollowPlayerRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Follow a player"""
    # Verify player exists
    player = get_player_or_404(request.player_id, db)
    
    # Check if already following
    existing = db.query(models.UserFollowsPlayer).filter(
        models.UserFollowsPlayer.user_id == current_user.user_id,
        models.UserFollowsPlayer.player_id == request.player_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You are already following {player.full_name}"
        )
    
    # Create follow relationship
    follow = models.UserFollowsPlayer(
        user_id=current_user.user_id,
        player_id=request.player_id
    )
    db.add(follow)
    db.commit()
    
    return schemas.MessageResponse(
        message=f"Successfully followed {player.full_name}",
        detail=f"You are now following {player.full_name}"
    )


@router.delete("/player/{player_id}", response_model=schemas.MessageResponse)
def unfollow_player(
    player_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Unfollow a player"""
    follow = db.query(models.UserFollowsPlayer).filter(
        models.UserFollowsPlayer.user_id == current_user.user_id,
        models.UserFollowsPlayer.player_id == player_id
    ).first()
    
    if not follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not following this player"
        )
    
    player_name = follow.player.full_name if follow.player else "this player"
    db.delete(follow)
    db.commit()
    
    return schemas.MessageResponse(
        message=f"Successfully unfollowed {player_name}",
        detail=f"You are no longer following {player_name}"
    )


@router.get("/players", response_model=List[schemas.Player])
def get_followed_players(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all players followed by current user"""
    follows = db.query(models.UserFollowsPlayer).filter(
        models.UserFollowsPlayer.user_id == current_user.user_id
    ).all()
    
    players = [follow.player for follow in follows if follow.player]
    return players


@router.get("/team/{team_id}/is-following")
def check_following_team(
    team_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if user is following a team"""
    follow = db.query(models.UserFollowsTeam).filter(
        models.UserFollowsTeam.user_id == current_user.user_id,
        models.UserFollowsTeam.team_id == team_id
    ).first()
    
    return {"is_following": follow is not None}


@router.get("/player/{player_id}/is-following")
def check_following_player(
    player_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if user is following a player"""
    follow = db.query(models.UserFollowsPlayer).filter(
        models.UserFollowsPlayer.user_id == current_user.user_id,
        models.UserFollowsPlayer.player_id == player_id
    ).first()
    
    return {"is_following": follow is not None}

