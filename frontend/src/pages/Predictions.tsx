import { useState, useEffect } from 'react';
import { predictionsAPI, viewAPI } from '../services/api';
import type { Team } from '../types';
import { AlertCircle, CheckCircle } from 'lucide-react';

export default function Predictions() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [formData, setFormData] = useState({
    home_team_id: '',
    away_team_id: '',
    predicted_outcome: 'H',
    home_points: 0,
    home_wins: 0,
    home_draws: 0,
    home_losses: 0,
    home_gf: 0,
    home_ga: 0,
    home_gd: 0,
    away_points: 0,
    away_wins: 0,
    away_draws: 0,
    away_losses: 0,
    away_gf: 0,
    away_ga: 0,
    away_gd: 0,
  });
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [eligibility, setEligibility] = useState<any>(null);

  useEffect(() => {
    viewAPI.getTeams().then(setTeams);
    predictionsAPI.checkEligibility('match_outcome').then(setEligibility);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = await predictionsAPI.submitMatchPrediction(formData);
      setResult(data);
      predictionsAPI.checkEligibility('match_outcome').then(setEligibility);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to submit prediction');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">Make a Prediction</h1>

      {!eligibility?.can_submit && (
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4 flex items-center space-x-2">
          <AlertCircle className="h-5 w-5 text-yellow-600" />
          <p className="text-yellow-800 dark:text-yellow-200">{eligibility?.message}</p>
        </div>
      )}

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 text-red-800 dark:text-red-200">
          {error}
        </div>
      )}

      {result && (
        <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-2">
            <CheckCircle className="h-5 w-5 text-green-600" />
            <p className="font-semibold text-green-800 dark:text-green-200">Prediction Submitted!</p>
          </div>
          <p className="text-green-700 dark:text-green-300">
            ML Prediction: {result.ml_prediction?.predicted_outcome}
          </p>
          <p className="text-green-700 dark:text-green-300">
            Your Prediction: {formData.predicted_outcome}
          </p>
          <p className="text-green-700 dark:text-green-300">
            Points Earned: {result.points_earned}
          </p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">Home Team</label>
            <select
              value={formData.home_team_id}
              onChange={(e) => setFormData({ ...formData, home_team_id: e.target.value })}
              className="w-full border rounded-lg px-3 py-2"
              required
            >
              <option value="">Select team</option>
              {teams.map((team) => (
                <option key={team.team_id} value={team.team_id}>
                  {team.name}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Away Team</label>
            <select
              value={formData.away_team_id}
              onChange={(e) => setFormData({ ...formData, away_team_id: e.target.value })}
              className="w-full border rounded-lg px-3 py-2"
              required
            >
              <option value="">Select team</option>
              {teams.map((team) => (
                <option key={team.team_id} value={team.team_id}>
                  {team.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Your Prediction</label>
          <select
            value={formData.predicted_outcome}
            onChange={(e) => setFormData({ ...formData, predicted_outcome: e.target.value })}
            className="w-full border rounded-lg px-3 py-2"
            required
          >
            <option value="H">Home Win</option>
            <option value="D">Draw</option>
            <option value="A">Away Win</option>
          </select>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">Home Points</label>
            <input
              type="number"
              value={formData.home_points}
              onChange={(e) => setFormData({ ...formData, home_points: parseInt(e.target.value) })}
              className="w-full border rounded-lg px-3 py-2"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Home Wins</label>
            <input
              type="number"
              value={formData.home_wins}
              onChange={(e) => setFormData({ ...formData, home_wins: parseInt(e.target.value) })}
              className="w-full border rounded-lg px-3 py-2"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Home Draws</label>
            <input
              type="number"
              value={formData.home_draws}
              onChange={(e) => setFormData({ ...formData, home_draws: parseInt(e.target.value) })}
              className="w-full border rounded-lg px-3 py-2"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Home Losses</label>
            <input
              type="number"
              value={formData.home_losses}
              onChange={(e) => setFormData({ ...formData, home_losses: parseInt(e.target.value) })}
              className="w-full border rounded-lg px-3 py-2"
              required
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading || !eligibility?.can_submit}
          className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700 disabled:opacity-50"
        >
          {loading ? 'Submitting...' : 'Submit Prediction'}
        </button>
      </form>
    </div>
  );
}

