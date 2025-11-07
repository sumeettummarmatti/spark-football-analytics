import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { viewAPI } from '../services/api';
import type { Player } from '../types';

export default function PlayerDetail() {
  const { id } = useParams();
  const [player, setPlayer] = useState<Player | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      viewAPI.getPlayer(Number(id)).then((data) => {
        setPlayer(data);
        setLoading(false);
      });
    }
  }, [id]);

  if (loading || !player) return <div>Loading...</div>;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h1 className="text-3xl font-bold mb-4">{player.full_name}</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {player.position && (
          <div>
            <span className="font-semibold">Position:</span> {player.position}
          </div>
        )}
        {player.nationality && (
          <div>
            <span className="font-semibold">Nationality:</span> {player.nationality}
          </div>
        )}
        {player.dob && (
          <div>
            <span className="font-semibold">Date of Birth:</span> {new Date(player.dob).toLocaleDateString()}
          </div>
        )}
        {player.height_cm && (
          <div>
            <span className="font-semibold">Height:</span> {player.height_cm} cm
          </div>
        )}
      </div>
    </div>
  );
}

