import { useEffect, useState } from 'react';
import { useAuthStore } from '../store/authStore';
import { profileAPI, predictionsAPI } from '../services/api';
import type { User, UserPrediction } from '../types';
import { CheckCircle, XCircle } from 'lucide-react';

export default function Profile() {
  const { user } = useAuthStore();
  const [profile, setProfile] = useState<User | null>(null);
  const [predictions, setPredictions] = useState<UserPrediction[]>([]);

  useEffect(() => {
    if (user) {
      profileAPI.getMyProfile().then(setProfile);
      predictionsAPI.getMyPredictions().then(setPredictions);
    }
  }, [user]);

  if (!profile) return <div>Loading...</div>;

  return (
    <div className="space-y-8">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold">{profile.username}</h1>
            <p className="text-gray-600 dark:text-gray-400">{profile.email}</p>
          </div>
          <div className="text-right">
            <div className="text-4xl font-bold text-primary-600">{profile.total_points}</div>
            <div className="text-gray-600 dark:text-gray-400">Total Points</div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
            <div className="text-2xl font-bold">{profile.total_predictions}</div>
            <div className="text-gray-600 dark:text-gray-400">Predictions</div>
          </div>
          <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
            <div className="text-2xl font-bold">{profile.correct_predictions}</div>
            <div className="text-gray-600 dark:text-gray-400">Correct</div>
          </div>
          <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
            <div className="text-2xl font-bold">{profile.accuracy_percentage.toFixed(1)}%</div>
            <div className="text-gray-600 dark:text-gray-400">Accuracy</div>
          </div>
          <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
            <div className="text-2xl font-bold">#{profile.rank || '-'}</div>
            <div className="text-gray-600 dark:text-gray-400">Rank</div>
          </div>
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold mb-4">My Predictions</h2>
        <div className="space-y-4">
          {predictions.map((pred) => (
            <div key={pred.prediction_id} className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-semibold">{pred.prediction_type}</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    {new Date(pred.created_at).toLocaleDateString()}
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  {pred.is_correct !== null && (
                    pred.is_correct ? (
                      <CheckCircle className="h-6 w-6 text-green-500" />
                    ) : (
                      <XCircle className="h-6 w-6 text-red-500" />
                    )
                  )}
                  <div className="text-right">
                    <div className="font-semibold text-primary-600">+{pred.points_earned} pts</div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

