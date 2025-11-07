import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { viewAPI } from '../services/api';
import type { Player } from '../types';

export default function Players() {
  const [players, setPlayers] = useState<Player[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    viewAPI.getPlayers().then((data) => {
      setPlayers(data);
      setLoading(false);
    });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Players</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {players.map((player) => (
          <Link
            key={player.player_id}
            to={`/players/${player.player_id}`}
            className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 hover:shadow-lg transition"
          >
            <h2 className="text-xl font-semibold mb-2">{player.full_name}</h2>
            {player.position && <p className="text-gray-600 dark:text-gray-400">{player.position}</p>}
            {player.nationality && <p className="text-sm text-gray-500">{player.nationality}</p>}
          </Link>
        ))}
      </div>
    </div>
  );
}

