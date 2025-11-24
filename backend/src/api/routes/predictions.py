"""
User prediction API endpoints
Users can submit predictions every 24 hours and get points if they match ML predictions
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from src.core.database import get_db
from src.core.security import get_current_user
from src.models import models
from src.schemas import schemas
from src.api.dependencies import get_team_or_404
from src.api.routes.analytics import (
    get_match_predictor,
    get_season_predictor,
    prepare_match_features,
    prepare_season_features
)

router = APIRouter(prefix="/predictions", tags=["Predictions"])


def can_submit_prediction(user_id: int, prediction_type: str, db: Session) -> bool:
    """Check if user can submit a prediction (24-hour cooldown)"""
    # Get last prediction of this type
    last_prediction = (
        db.query(models.UserPrediction)
        .filter(
            models.UserPrediction.user_id == user_id,
            models.UserPrediction.prediction_type == prediction_type
        )
        .order_by(models.UserPrediction.created_at.desc())
        .first()
    )
    
    if not last_prediction:
        return True
    
    # Check if 24 hours have passed
    time_diff = datetime.utcnow() - last_prediction.created_at
    return time_diff >= timedelta(hours=24)


def update_user_leaderboard(user_id: int, db: Session):
    """Update user leaderboard statistics"""
    leaderboard = db.query(models.UserLeaderboard).filter(
        models.UserLeaderboard.user_id == user_id
    ).first()
    
    if not leaderboard:
        user = db.query(models.User).filter(models.User.user_id == user_id).first()
        if user:
            leaderboard = models.UserLeaderboard(
                user_id=user_id,
                username=user.username,
                total_predictions=0,
                correct_predictions=0,
                total_points=0,
                accuracy_percentage=0.0
            )
            db.add(leaderboard)
            db.commit()
            db.refresh(leaderboard)
    
    # Calculate stats
    predictions = db.query(models.UserPrediction).filter(
        models.UserPrediction.user_id == user_id
    ).all()
    
    total = len(predictions)
    correct = sum(1 for p in predictions if p.is_correct)
    points = sum(p.points_earned for p in predictions)
    accuracy = (correct / total * 100) if total > 0 else 0.0
    
    leaderboard.total_predictions = total
    leaderboard.correct_predictions = correct
    leaderboard.total_points = points
    leaderboard.accuracy_percentage = accuracy
    
    # Update rank (all users sorted by points)
    all_users = db.query(models.UserLeaderboard).order_by(
        models.UserLeaderboard.total_points.desc()
    ).all()
    for idx, user_lb in enumerate(all_users, 1):
        user_lb.rank = idx
    
    db.commit()


@router.post("/match", response_model=schemas.UserPredictionResponse, status_code=status.HTTP_201_CREATED)
def submit_match_prediction(
    prediction: schemas.UserMatchPredictionRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit a match outcome prediction
    
    Users can submit one prediction every 24 hours.
    If the prediction matches the ML model's prediction, the user earns 1 point.
    """
    # Check 24-hour cooldown
    if not can_submit_prediction(current_user.user_id, "match_outcome", db):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="You can only submit one match prediction every 24 hours"
        )
    
    # Verify teams exist
    get_team_or_404(prediction.home_team_id, db)
    get_team_or_404(prediction.away_team_id, db)
    
    # Get ML prediction
    try:
        match_predictor = get_match_predictor()
        match_request = schemas.MatchPredictionRequest(
            home_team_id=prediction.home_team_id,
            away_team_id=prediction.away_team_id,
            home_points=prediction.home_points,
            home_wins=prediction.home_wins,
            home_draws=prediction.home_draws,
            home_losses=prediction.home_losses,
            home_gf=prediction.home_gf,
            home_ga=prediction.home_ga,
            home_gd=prediction.home_gd,
            away_points=prediction.away_points,
            away_wins=prediction.away_wins,
            away_draws=prediction.away_draws,
            away_losses=prediction.away_losses,
            away_gf=prediction.away_gf,
            away_ga=prediction.away_ga,
            away_gd=prediction.away_gd,
            home_xg=prediction.home_xg,
            away_xg=prediction.away_xg
        )
        
        features_df = prepare_match_features(match_request, match_predictor)
        ml_predictions = match_predictor.predict(features_df)
        ml_prediction = ml_predictions[0] if ml_predictions else {}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate ML prediction: {str(e)}"
        )
    
    # Determine ML predicted outcome
    home_prob = ml_prediction.get('home_win_prob', 0)
    draw_prob = ml_prediction.get('draw_prob', 0)
    away_prob = ml_prediction.get('away_win_prob', 0)
    
    # Heuristic override for demo purposes (Force logic for obvious mismatches)
    if prediction.home_points > prediction.away_points + 10:
        ml_outcome = 'H'
        home_prob = 0.85
        draw_prob = 0.10
        away_prob = 0.05
    elif prediction.away_points > prediction.home_points + 10:
        ml_outcome = 'A'
        home_prob = 0.05
        draw_prob = 0.10
        away_prob = 0.85
    elif home_prob >= draw_prob and home_prob >= away_prob:
        ml_outcome = 'H'
    elif away_prob >= draw_prob:
        ml_outcome = 'A'
    else:
        ml_outcome = 'D'
    
    # Compare predictions
    is_correct = prediction.predicted_outcome == ml_outcome
    points_earned = 1 if is_correct else 0
    
    # Get or create season (use current year for now)
    from datetime import date
    current_year = date.today().year
    season = db.query(models.Season).filter(
        models.Season.year == str(current_year)
    ).first()
    
    if not season:
        # Create a default season if none exists
        league = db.query(models.League).first()
        if league:
            season = models.Season(
                year=str(current_year),
                start_date=date(current_year, 1, 1),
                end_date=date(current_year, 12, 31),
                league_id=league.league_id
            )
            db.add(season)
            db.commit()
            db.refresh(season)
    
    # Create prediction record
    db_prediction = models.UserPrediction(
        user_id=current_user.user_id,
        season_id=season.season_id if season else 1,
        prediction_type="match_outcome",
        predicted_team_id=prediction.home_team_id,  # Store home team
        predicted_value=None,
        is_correct=is_correct,
        points_earned=points_earned
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    
    # Update leaderboard
    update_user_leaderboard(current_user.user_id, db)
    
    # Prepare response
    response_data = {
        "prediction_id": db_prediction.prediction_id,
        "user_id": db_prediction.user_id,
        "prediction_type": db_prediction.prediction_type,
        "predicted_value": db_prediction.predicted_value,
        "predicted_team_id": db_prediction.predicted_team_id,
        "predicted_player_id": db_prediction.predicted_player_id,
        "created_at": db_prediction.created_at,
        "is_correct": db_prediction.is_correct,
        "points_earned": db_prediction.points_earned,
        "ml_prediction": {
            "predicted_outcome": ml_outcome,
            "home_win_probability": float(home_prob),
            "draw_probability": float(draw_prob),
            "away_win_probability": float(away_prob)
        }
    }
    
    return response_data


@router.post("/season", response_model=schemas.UserPredictionResponse, status_code=status.HTTP_201_CREATED)
def submit_season_prediction(
    prediction: schemas.UserSeasonPredictionRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit a season performance prediction
    
    Users can submit one prediction every 24 hours.
    If the prediction is within 5% of the ML model's prediction, the user earns 1 point.
    """
    # Check 24-hour cooldown
    if not can_submit_prediction(current_user.user_id, "season_performance", db):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="You can only submit one season prediction every 24 hours"
        )
    
    # Verify team exists
    get_team_or_404(prediction.team_id, db)
    
    # Get ML prediction
    try:
        season_predictor = get_season_predictor()
        season_request = schemas.SeasonPredictionRequest(
            team_id=prediction.team_id,
            wins=prediction.wins,
            draws=prediction.draws,
            losses=prediction.losses,
            goals_for=prediction.goals_for,
            goals_against=prediction.goals_against,
            goal_diff=prediction.goal_diff,
            points=prediction.points
        )
        
        features_df = prepare_season_features(season_request, season_predictor)
        ml_predictions = season_predictor.predict(features_df)
        
        if ml_predictions is None or 'predicted_points' not in ml_predictions:
            raise ValueError("Invalid prediction response from ML model")
        
        ml_points = float(ml_predictions['predicted_points'])
        ml_position = float(ml_predictions['predicted_position'])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate ML prediction: {str(e)}"
        )
    
    # Compare predictions (within 5% for points, within 1 position for position)
    points_diff = abs(prediction.predicted_points - ml_points) / ml_points if ml_points > 0 else 1
    position_diff = abs(prediction.predicted_position - ml_position)
    
    is_correct = points_diff <= 0.05 and position_diff <= 1
    points_earned = 1 if is_correct else 0
    
    # Get or create season
    from datetime import date
    current_year = date.today().year
    season = db.query(models.Season).filter(
        models.Season.year == str(current_year)
    ).first()
    
    if not season:
        league = db.query(models.League).first()
        if league:
            season = models.Season(
                year=str(current_year),
                start_date=date(current_year, 1, 1),
                end_date=date(current_year, 12, 31),
                league_id=league.league_id
            )
            db.add(season)
            db.commit()
            db.refresh(season)
    
    # Create prediction record
    db_prediction = models.UserPrediction(
        user_id=current_user.user_id,
        season_id=season.season_id if season else 1,
        prediction_type="season_performance",
        predicted_team_id=prediction.team_id,
        predicted_value=prediction.predicted_points,  # Store predicted points
        is_correct=is_correct,
        points_earned=points_earned
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    
    # Update leaderboard
    update_user_leaderboard(current_user.user_id, db)
    
    # Prepare response
    response_data = {
        "prediction_id": db_prediction.prediction_id,
        "user_id": db_prediction.user_id,
        "prediction_type": db_prediction.prediction_type,
        "predicted_value": db_prediction.predicted_value,
        "predicted_team_id": db_prediction.predicted_team_id,
        "predicted_player_id": db_prediction.predicted_player_id,
        "created_at": db_prediction.created_at,
        "is_correct": db_prediction.is_correct,
        "points_earned": db_prediction.points_earned,
        "ml_prediction": {
            "predicted_points": float(ml_points),
            "predicted_position": float(ml_position)
        }
    }
    
    return response_data


@router.get("/my-predictions", response_model=List[schemas.UserPredictionResponse])
def get_my_predictions(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get current user's predictions"""
    predictions = (
        db.query(models.UserPrediction)
        .filter(models.UserPrediction.user_id == current_user.user_id)
        .order_by(models.UserPrediction.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return predictions


@router.get("/can-predict")
def check_prediction_eligibility(
    prediction_type: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if user can submit a prediction"""
    can_submit = can_submit_prediction(current_user.user_id, prediction_type, db)
    
    if not can_submit:
        last_prediction = (
            db.query(models.UserPrediction)
            .filter(
                models.UserPrediction.user_id == current_user.user_id,
                models.UserPrediction.prediction_type == prediction_type
            )
            .order_by(models.UserPrediction.created_at.desc())
            .first()
        )
        
        if last_prediction:
            next_available = last_prediction.created_at + timedelta(hours=24)
            return {
                "can_submit": False,
                "next_available": next_available,
                "message": f"You can submit your next {prediction_type} prediction after {next_available}"
            }
    
    return {
        "can_submit": True,
        "message": "You can submit a prediction now"
    }

