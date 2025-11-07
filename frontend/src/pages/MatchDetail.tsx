import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { viewAPI } from '../services/api';
import type { Match } from '../types';

export default function MatchDetail() {
  const { id } = useParams();
  const [match, setMatch] = useState<Match | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      viewAPI.getMatch(Number(id)).then((data) => {
        setMatch(data);
        setLoading(false);
      });
    }
  }, [id]);

  if (loading || !match) return <div>Loading...</div>;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h1 className="text-3xl font-bold mb-4">
        {match.home_team?.name || 'Home'} vs {match.away_team?.name || 'Away'}
      </h1>
      <div className="space-y-4">
        <div>
          <span className="font-semibold">Date:</span> {new Date(match.match_date).toLocaleDateString()}
        </div>
        {match.venue && (
          <div>
            <span className="font-semibold">Venue:</span> {match.venue}
          </div>
        )}
        {match.home_score_final !== null && match.away_score_final !== null && (
          <div className="text-4xl font-bold">
            {match.home_score_final} - {match.away_score_final}
          </div>
        )}
        {match.home_xg && match.away_xg && (
          <div>
            <span className="font-semibold">xG:</span> {match.home_xg} - {match.away_xg}
          </div>
        )}
      </div>
    </div>
  );
}

