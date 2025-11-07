import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Trophy, Users, BarChart3 } from 'lucide-react';
import { viewAPI, profileAPI } from '../services/api';
import type { Team, LeaderboardEntry } from '../types';

export default function Home() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);

  useEffect(() => {
    viewAPI.getTeams(0, 6).then(setTeams);
    profileAPI.getTopLeaderboard(5).then(setLeaderboard);
  }, []);

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 rounded-lg p-8 text-white">
        <h1 className="text-4xl font-bold mb-4">Welcome to SPARK</h1>
        <p className="text-xl mb-6">Football Analytics & Prediction Platform</p>
        <div className="flex space-x-4">
          <Link
            to="/teams"
            className="bg-white text-primary-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100"
          >
            Explore Teams
          </Link>
          <Link
            to="/predictions"
            className="bg-primary-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-400"
          >
            Make Predictions
          </Link>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 dark:text-gray-400">Total Teams</p>
              <p className="text-3xl font-bold">{teams.length}+</p>
            </div>
            <Users className="h-12 w-12 text-primary-600" />
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 dark:text-gray-400">Active Users</p>
              <p className="text-3xl font-bold">{leaderboard.length}+</p>
            </div>
            <Trophy className="h-12 w-12 text-primary-600" />
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 dark:text-gray-400">Predictions</p>
              <p className="text-3xl font-bold">1000+</p>
            </div>
            <BarChart3 className="h-12 w-12 text-primary-600" />
          </div>
        </div>
      </div>

      {/* Top Teams */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Featured Teams</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {teams.map((team) => (
            <Link
              key={team.team_id}
              to={`/teams/${team.team_id}`}
              className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow hover:shadow-lg transition"
            >
              <h3 className="font-semibold text-lg">{team.name}</h3>
              {team.city && <p className="text-gray-600 dark:text-gray-400">{team.city}</p>}
            </Link>
          ))}
        </div>
      </div>

      {/* Leaderboard */}
      {leaderboard.length > 0 && (
        <div>
          <h2 className="text-2xl font-bold mb-4">Top Players</h2>
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Rank</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Username</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Points</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Accuracy</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {leaderboard.map((entry) => (
                  <tr key={entry.rank}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">#{entry.rank}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">{entry.username}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold">{entry.total_points}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">{entry.accuracy_percentage.toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <Link to="/leaderboard" className="block text-center mt-4 text-primary-600 hover:text-primary-700">
            View Full Leaderboard →
          </Link>
        </div>
      )}
    </div>
  );
}

