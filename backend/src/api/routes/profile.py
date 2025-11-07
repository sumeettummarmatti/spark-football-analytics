"""
User profile and leaderboard API endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.core.security import get_current_user
from src.models import models
from src.schemas import schemas

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/me", response_model=schemas.UserProfile)
def get_my_profile(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile with statistics"""
    # Get leaderboard stats
    leaderboard = db.query(models.UserLeaderboard).filter(
        models.UserLeaderboard.user_id == current_user.user_id
    ).first()
    
    profile_data = {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_admin": current_user.is_admin,
        "profile_picture_url": current_user.profile_picture_url,
        "created_at": current_user.created_at,
        "total_points": leaderboard.total_points if leaderboard else 0,
        "total_predictions": leaderboard.total_predictions if leaderboard else 0,
        "correct_predictions": leaderboard.correct_predictions if leaderboard else 0,
        "accuracy_percentage": float(leaderboard.accuracy_percentage) if leaderboard else 0.0,
        "rank": leaderboard.rank if leaderboard else None
    }
    
    return profile_data


@router.get("/leaderboard", response_model=List[schemas.LeaderboardEntry])
def get_leaderboard(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get global leaderboard"""
    entries = (
        db.query(models.UserLeaderboard)
        .order_by(models.UserLeaderboard.total_points.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return entries


@router.get("/leaderboard/top", response_model=List[schemas.LeaderboardEntry])
def get_top_leaderboard(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get top N users on leaderboard"""
    entries = (
        db.query(models.UserLeaderboard)
        .order_by(models.UserLeaderboard.total_points.desc())
        .limit(limit)
        .all()
    )
    
    return entries

