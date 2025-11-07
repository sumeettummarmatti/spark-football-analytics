"""
Authentication API endpoints
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user
)
from src.models import models
from src.schemas import schemas

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=schemas.UserProfile, status_code=status.HTTP_201_CREATED)
def register(user_data: schemas.UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    
    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address
    - **password**: Password (minimum 6 characters)
    - **full_name**: Optional full name
    """
    # Check if username already exists
    existing_user = db.query(models.User).filter(
        models.User.username == user_data.username
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    existing_email = db.query(models.User).filter(
        models.User.email == user_data.email
    ).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = models.User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name,
        is_admin=False,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Initialize leaderboard entry
    leaderboard_entry = models.UserLeaderboard(
        user_id=db_user.user_id,
        username=db_user.username,
        total_predictions=0,
        correct_predictions=0,
        total_points=0,
        accuracy_percentage=0.0
    )
    db.add(leaderboard_entry)
    db.commit()
    
    return db_user


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login user and get access token
    
    - **username**: Your username
    - **password**: Your password
    """
    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/logout", response_model=schemas.MessageResponse)
def logout(current_user: models.User = Depends(get_current_user)):
    """
    Logout user (client should discard token)
    """
    return schemas.MessageResponse(
        message="Successfully logged out",
        detail="Please discard your access token"
    )


@router.get("/me", response_model=schemas.UserProfile)
def get_current_user_profile(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user profile with statistics
    """
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

