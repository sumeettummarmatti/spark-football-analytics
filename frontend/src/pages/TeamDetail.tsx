import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { viewAPI, followAPI } from '../services/api';
import { useAuthStore } from '../store/authStore';
import type { Team, Player, Match } from '../types';
import { Heart, Users, Calendar } from 'lucide-react';

export default function TeamDetail() {
  const { id } = useParams();
  const { isAuthenticated } = useAuthStore();
  const [team, setTeam] = useState<Team | null>(null);
  const [players, setPlayers] = useState<Player[]>([]);
  const [matches, setMatches] = useState<Match[]>([]);
  const [isFollowing, setIsFollowing] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      Promise.all([
        viewAPI.getTeam(Number(id)).then(setTeam),
        viewAPI.getTeamPlayers(Number(id)).then(setPlayers),
        viewAPI.getTeamMatches(Number(id), 10).then(setMatches),
      ]).then(() => {
        setLoading(false);
      });

      if (isAuthenticated) {
        followAPI.checkFollowingTeam(Number(id)).then(setIsFollowing);
      }
    }
  }, [id, isAuthenticated]);

  const handleFollow = async () => {
    if (!id) return;
    try {
      if (isFollowing) {
        await followAPI.unfollowTeam(Number(id));
      } else {
        await followAPI.followTeam(Number(id));
      }
      setIsFollowing(!isFollowing);
    } catch (error) {
      console.error('Follow error:', error);
    }
  };

  if (loading || !team) return <div>Loading...</div>;

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">{team.name}</h1>
            {team.city && <p className="text-gray-600 dark:text-gray-400">{team.city}</p>}
            {team.stadium_name && <p className="text-gray-600 dark:text-gray-400">{team.stadium_name}</p>}
          </div>
          {isAuthenticated && (
            <button
              onClick={handleFollow}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg ${
                isFollowing
                  ? 'bg-red-100 text-red-600 hover:bg-red-200'
                  : 'bg-primary-100 text-primary-600 hover:bg-primary-200'
              }`}
            >
              <Heart className={`h-5 w-5 ${isFollowing ? 'fill-current' : ''}`} />
              <span>{isFollowing ? 'Following' : 'Follow'}</span>
            </button>
          )}
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold mb-4 flex items-center space-x-2">
          <Users className="h-6 w-6" />
          <span>Players</span>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {players.map((player) => (
            <Link
              key={player.player_id}
              to={`/players/${player.player_id}`}
              className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 hover:shadow-lg transition"
            >
              <h3 className="font-semibold">{player.full_name}</h3>
              {player.position && <p className="text-sm text-gray-600 dark:text-gray-400">{player.position}</p>}
            </Link>
          ))}
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold mb-4 flex items-center space-x-2">
          <Calendar className="h-6 w-6" />
          <span>Recent Matches</span>
        </h2>
        <div className="space-y-2">
          {matches.map((match) => (
            <Link
              key={match.match_id}
              to={`/matches/${match.match_id}`}
              className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 hover:shadow-lg transition block"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-semibold">
                    {match.home_team?.name || 'Home'} vs {match.away_team?.name || 'Away'}
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {new Date(match.match_date).toLocaleDateString()}
                  </p>
                </div>
                {match.home_score_final !== null && match.away_score_final !== null && (
                  <div className="text-2xl font-bold">
                    {match.home_score_final} - {match.away_score_final}
                  </div>
                )}
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

