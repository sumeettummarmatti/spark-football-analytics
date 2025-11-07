import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { Users, Trophy, Calendar, BarChart3, User, LogOut, Settings } from 'lucide-react';

export default function Layout() {
  const { isAuthenticated, user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-2">
              <Trophy className="h-8 w-8 text-primary-600" />
              <span className="text-2xl font-bold text-gray-900 dark:text-white">SPARK</span>
            </Link>

            <nav className="hidden md:flex space-x-8">
              <Link to="/teams" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 flex items-center space-x-1">
                <Users className="h-4 w-4" />
                <span>Teams</span>
              </Link>
              <Link to="/players" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 flex items-center space-x-1">
                <Users className="h-4 w-4" />
                <span>Players</span>
              </Link>
              <Link to="/matches" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 flex items-center space-x-1">
                <Calendar className="h-4 w-4" />
                <span>Matches</span>
              </Link>
              <Link to="/leaderboard" className="text-gray-700 dark:text-gray-300 hover:text-primary-600 flex items-center space-x-1">
                <BarChart3 className="h-4 w-4" />
                <span>Leaderboard</span>
              </Link>
              {isAuthenticated && (
                <Link to="/predictions" className="text-gray-700 dark:text-gray-300 hover:text-primary-600">
                  Predictions
                </Link>
              )}
            </nav>

            <div className="flex items-center space-x-4">
              {isAuthenticated ? (
                <>
                  <Link to="/profile" className="flex items-center space-x-2 text-gray-700 dark:text-gray-300 hover:text-primary-600">
                    <User className="h-5 w-5" />
                    <span className="hidden md:inline">{user?.username}</span>
                    {user?.total_points !== undefined && (
                      <span className="hidden md:inline text-primary-600 font-semibold">{user.total_points} pts</span>
                    )}
                  </Link>
                  {user?.is_admin && (
                    <Link to="/admin" className="text-gray-700 dark:text-gray-300 hover:text-primary-600">
                      <Settings className="h-5 w-5" />
                    </Link>
                  )}
                  <button
                    onClick={handleLogout}
                    className="flex items-center space-x-1 text-gray-700 dark:text-gray-300 hover:text-red-600"
                  >
                    <LogOut className="h-5 w-5" />
                    <span className="hidden md:inline">Logout</span>
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" className="text-gray-700 dark:text-gray-300 hover:text-primary-600">
                    Login
                  </Link>
                  <Link
                    to="/register"
                    className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700"
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-white dark:bg-gray-800 border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <p className="text-center text-gray-600 dark:text-gray-400">
            © 2024 SPARK Football Analytics. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}

