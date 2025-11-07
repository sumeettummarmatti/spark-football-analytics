import axios from 'axios';
import type { User, Team, Player, Match, MatchPrediction, SeasonPrediction, UserPrediction, LeaderboardEntry } from '../types';

const API_BASE_URL = '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: async (data: { username: string; email: string; password: string; full_name?: string }) => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },
  
  login: async (username: string, password: string) => {
    // FastAPI OAuth2PasswordRequestForm expects form data
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    const response = await api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return response.data;
  },
  
  logout: async () => {
    const response = await api.post('/auth/logout');
    return response.data;
  },
  
  getMe: async (): Promise<User> => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// View API (public)
export const viewAPI = {
  getTeams: async (skip = 0, limit = 100): Promise<Team[]> => {
    const response = await api.get('/view/teams', { params: { skip, limit } });
    return response.data;
  },
  
  getTeam: async (teamId: number): Promise<Team> => {
    const response = await api.get(`/view/teams/${teamId}`);
    return response.data;
  },
  
  getTeamPlayers: async (teamId: number): Promise<Player[]> => {
    const response = await api.get(`/view/teams/${teamId}/players`);
    return response.data;
  },
  
  getPlayers: async (skip = 0, limit = 100, teamId?: number): Promise<Player[]> => {
    const response = await api.get('/view/players', { params: { skip, limit, team_id: teamId } });
    return response.data;
  },
  
  getPlayer: async (playerId: number): Promise<Player> => {
    const response = await api.get(`/view/players/${playerId}`);
    return response.data;
  },
  
  getMatches: async (skip = 0, limit = 100, teamId?: number): Promise<Match[]> => {
    const response = await api.get('/view/matches', { params: { skip, limit, team_id: teamId } });
    return response.data;
  },
  
  getMatch: async (matchId: number): Promise<Match> => {
    const response = await api.get(`/view/matches/${matchId}`);
    return response.data;
  },
  
  getTeamMatches: async (teamId: number, limit = 10): Promise<Match[]> => {
    const response = await api.get(`/view/teams/${teamId}/matches`, { params: { limit } });
    return response.data;
  },
};

// Analytics API (ML predictions)
export const analyticsAPI = {
  predictMatch: async (data: any): Promise<MatchPrediction> => {
    const response = await api.post('/analytics/predict/match', data);
    return response.data;
  },
  
  predictSeason: async (data: any): Promise<SeasonPrediction> => {
    const response = await api.post('/analytics/predict/season', data);
    return response.data;
  },
};

// Predictions API (user predictions)
export const predictionsAPI = {
  submitMatchPrediction: async (data: any): Promise<UserPrediction> => {
    const response = await api.post('/predictions/match', data);
    return response.data;
  },
  
  submitSeasonPrediction: async (data: any): Promise<UserPrediction> => {
    const response = await api.post('/predictions/season', data);
    return response.data;
  },
  
  getMyPredictions: async (skip = 0, limit = 50): Promise<UserPrediction[]> => {
    const response = await api.get('/predictions/my-predictions', { params: { skip, limit } });
    return response.data;
  },
  
  checkEligibility: async (predictionType: string) => {
    const response = await api.get('/predictions/can-predict', { params: { prediction_type: predictionType } });
    return response.data;
  },
};

// Follow API
export const followAPI = {
  followTeam: async (teamId: number) => {
    const response = await api.post('/follow/team', { team_id: teamId });
    return response.data;
  },
  
  unfollowTeam: async (teamId: number) => {
    const response = await api.delete(`/follow/team/${teamId}`);
    return response.data;
  },
  
  getFollowedTeams: async (): Promise<Team[]> => {
    const response = await api.get('/follow/teams');
    return response.data;
  },
  
  followPlayer: async (playerId: number) => {
    const response = await api.post('/follow/player', { player_id: playerId });
    return response.data;
  },
  
  unfollowPlayer: async (playerId: number) => {
    const response = await api.delete(`/follow/player/${playerId}`);
    return response.data;
  },
  
  getFollowedPlayers: async (): Promise<Player[]> => {
    const response = await api.get('/follow/players');
    return response.data;
  },
  
  checkFollowingTeam: async (teamId: number): Promise<boolean> => {
    const response = await api.get(`/follow/team/${teamId}/is-following`);
    return response.data.is_following;
  },
  
  checkFollowingPlayer: async (playerId: number): Promise<boolean> => {
    const response = await api.get(`/follow/player/${playerId}/is-following`);
    return response.data.is_following;
  },
};

// Profile API
export const profileAPI = {
  getMyProfile: async (): Promise<User> => {
    const response = await api.get('/profile/me');
    return response.data;
  },
  
  getLeaderboard: async (skip = 0, limit = 100): Promise<LeaderboardEntry[]> => {
    const response = await api.get('/profile/leaderboard', { params: { skip, limit } });
    return response.data;
  },
  
  getTopLeaderboard: async (limit = 10): Promise<LeaderboardEntry[]> => {
    const response = await api.get('/profile/leaderboard/top', { params: { limit } });
    return response.data;
  },
};

// Admin API
export const adminAPI = {
  // Teams
  createTeam: async (data: any): Promise<Team> => {
    const response = await api.post('/admin/teams', data);
    return response.data;
  },
  
  updateTeam: async (teamId: number, data: any): Promise<Team> => {
    const response = await api.put(`/admin/teams/${teamId}`, data);
    return response.data;
  },
  
  deleteTeam: async (teamId: number) => {
    const response = await api.delete(`/admin/teams/${teamId}`);
    return response.data;
  },
  
  // Players
  createPlayer: async (data: any): Promise<Player> => {
    const response = await api.post('/admin/players', data);
    return response.data;
  },
  
  updatePlayer: async (playerId: number, data: any): Promise<Player> => {
    const response = await api.put(`/admin/players/${playerId}`, data);
    return response.data;
  },
  
  deletePlayer: async (playerId: number) => {
    const response = await api.delete(`/admin/players/${playerId}`);
    return response.data;
  },
  
  // Matches
  createMatch: async (data: any): Promise<Match> => {
    const response = await api.post('/admin/matches', data);
    return response.data;
  },
  
  updateMatch: async (matchId: number, data: any): Promise<Match> => {
    const response = await api.put(`/admin/matches/${matchId}`, data);
    return response.data;
  },
  
  deleteMatch: async (matchId: number) => {
    const response = await api.delete(`/admin/matches/${matchId}`);
    return response.data;
  },
  
  // Users
  getUsers: async (skip = 0, limit = 100): Promise<User[]> => {
    const response = await api.get('/admin/users', { params: { skip, limit } });
    return response.data;
  },
};

export default api;

