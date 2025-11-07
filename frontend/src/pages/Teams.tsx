import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { viewAPI } from '../services/api';
import type { Team } from '../types';

export default function Teams() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    viewAPI.getTeams().then((data) => {
      setTeams(data);
      setLoading(false);
    });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Teams</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {teams.map((team) => (
          <Link
            key={team.team_id}
            to={`/teams/${team.team_id}`}
            className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 hover:shadow-lg transition"
          >
            <h2 className="text-xl font-semibold mb-2">{team.name}</h2>
            {team.city && <p className="text-gray-600 dark:text-gray-400">{team.city}</p>}
            {team.stadium_name && <p className="text-sm text-gray-500">{team.stadium_name}</p>}
          </Link>
        ))}
      </div>
    </div>
  );
}

