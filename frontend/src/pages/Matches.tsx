import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { viewAPI } from '../services/api';
import type { Match } from '../types';

export default function Matches() {
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    viewAPI.getMatches().then((data) => {
      setMatches(data);
      setLoading(false);
    });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Matches</h1>
      <div className="space-y-4">
        {matches.map((match) => (
          <Link
            key={match.match_id}
            to={`/matches/${match.match_id}`}
            className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 hover:shadow-lg transition block"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="font-semibold text-lg">
                  {match.home_team?.name || 'Home'} vs {match.away_team?.name || 'Away'}
                </p>
                <p className="text-gray-600 dark:text-gray-400">
                  {new Date(match.match_date).toLocaleDateString()} - {match.venue}
                </p>
              </div>
              {match.home_score_final !== null && match.away_score_final !== null && (
                <div className="text-3xl font-bold">
                  {match.home_score_final} - {match.away_score_final}
                </div>
              )}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

