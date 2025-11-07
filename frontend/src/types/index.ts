export interface User {
  user_id: number;
  username: string;
  email: string;
  full_name?: string;
  is_admin: boolean;
  profile_picture_url?: string;
  created_at: string;
  total_points: number;
  total_predictions: number;
  correct_predictions: number;
  accuracy_percentage: number;
  rank?: number;
}

export interface Team {
  team_id: number;
  name: string;
  founded_year?: number;
  stadium_name?: string;
  city?: string;
  logo_url?: string;
  fbref_id?: string;
}

export interface Player {
  player_id: number;
  full_name: string;
  dob?: string;
  nationality?: string;
  position?: string;
  height_cm?: number;
  weight_kg?: number;
  shirt_number?: number;
  team_id?: number;
  fbref_id?: string;
}

export interface Match {
  match_id: number;
  match_date: string;
  venue?: string;
  home_score_final?: number;
  away_score_final?: number;
  home_xg?: number;
  away_xg?: number;
  attendance?: number;
  season_id: number;
  home_team_id: number;
  away_team_id: number;
  fbref_id?: string;
  home_team?: Team;
  away_team?: Team;
}

export interface MatchPrediction {
  home_team_id: number;
  away_team_id: number;
  home_win_probability: number;
  draw_probability: number;
  away_win_probability: number;
  predicted_outcome: 'H' | 'D' | 'A';
}

export interface SeasonPrediction {
  team_id: number;
  predicted_points: number;
  predicted_position: number;
}

export interface UserPrediction {
  prediction_id: number;
  user_id: number;
  prediction_type: string;
  predicted_value?: number;
  predicted_team_id?: number;
  predicted_player_id?: number;
  created_at: string;
  is_correct?: boolean;
  points_earned: number;
  ml_prediction?: any;
}

export interface LeaderboardEntry {
  rank: number;
  username: string;
  total_points: number;
  total_predictions: number;
  correct_predictions: number;
  accuracy_percentage: number;
}

