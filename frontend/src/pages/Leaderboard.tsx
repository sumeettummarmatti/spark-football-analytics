import { useEffect, useState } from 'react';
import { profileAPI } from '../services/api';
import type { LeaderboardEntry } from '../types';
import { Trophy } from 'lucide-react';

export default function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    profileAPI.getLeaderboard().then((data) => {
      setLeaderboard(data);
      setLoading(false);
    });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6 flex items-center space-x-2">
        <Trophy className="h-8 w-8 text-primary-600" />
        <span>Leaderboard</span>
      </h1>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Rank</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Username</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Points</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Predictions</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Correct</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Accuracy</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {leaderboard.map((entry) => (
              <tr key={entry.rank} className={entry.rank <= 3 ? 'bg-yellow-50 dark:bg-yellow-900/20' : ''}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">#{entry.rank}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold">{entry.username}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-primary-600">{entry.total_points}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">{entry.total_predictions}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">{entry.correct_predictions}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">{entry.accuracy_percentage.toFixed(1)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

