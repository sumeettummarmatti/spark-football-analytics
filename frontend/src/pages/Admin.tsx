import { useState } from 'react';

export default function Admin() {
  const [activeTab, setActiveTab] = useState<'teams' | 'players' | 'matches'>('teams');

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Admin Panel</h1>
      
      <div className="border-b">
        <nav className="flex space-x-8">
          <button
            onClick={() => setActiveTab('teams')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'teams'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Teams
          </button>
          <button
            onClick={() => setActiveTab('players')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'players'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Players
          </button>
          <button
            onClick={() => setActiveTab('matches')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'matches'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Matches
          </button>
        </nav>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <p className="text-gray-600 dark:text-gray-400">
          Admin CRUD operations for {activeTab} will be implemented here.
        </p>
        <p className="text-sm text-gray-500 mt-2">
          Use the API endpoints at /admin/{activeTab} to manage {activeTab}.
        </p>
      </div>
    </div>
  );
}

