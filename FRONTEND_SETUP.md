# SPARK Frontend Setup Guide

## Quick Start

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Access the app:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## Features Implemented

### ✅ Authentication
- User registration
- User login/logout
- JWT token management
- Protected routes

### ✅ Public Views
- Teams listing and details
- Players listing and details
- Matches listing and details
- Leaderboard

### ✅ User Features
- Make match predictions (24-hour cooldown)
- Make season predictions
- Follow/unfollow teams and players
- View personal profile with statistics
- View prediction history

### ✅ Admin Features
- Admin panel (admin-only access)
- CRUD operations for teams, players, matches

## API Endpoints Used

All endpoints are prefixed with `/api/v1`:

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user profile
- `GET /view/teams` - Get all teams
- `GET /view/teams/:id` - Get team details
- `GET /view/players` - Get all players
- `GET /view/matches` - Get all matches
- `POST /predictions/match` - Submit match prediction
- `POST /predictions/season` - Submit season prediction
- `GET /predictions/my-predictions` - Get user predictions
- `POST /follow/team` - Follow a team
- `DELETE /follow/team/:id` - Unfollow a team
- `GET /profile/me` - Get user profile
- `GET /profile/leaderboard` - Get leaderboard
- `GET /admin/*` - Admin endpoints (CRUD operations)

## Key Components

- **Layout** - Main layout with navigation
- **ProtectedRoute** - Route guard for authenticated routes
- **Login/Register** - Authentication pages
- **Home** - Dashboard with stats and featured content
- **Teams/Players/Matches** - List and detail views
- **Predictions** - Prediction submission form
- **Profile** - User profile with statistics
- **Leaderboard** - Global leaderboard
- **Admin** - Admin panel

## State Management

Using Zustand for state management:
- `authStore` - User authentication state
- Token stored in localStorage
- Automatic token refresh on page load

## Styling

- Tailwind CSS for styling
- Responsive design
- Dark mode support
- Modern, clean UI

## Next Steps

1. Install dependencies: `npm install`
2. Start backend server (from backend directory)
3. Start frontend: `npm run dev`
4. Register a new account or login
5. Explore the platform!

## Troubleshooting

- **CORS errors:** Make sure backend CORS is configured to allow `http://localhost:3000`
- **401 errors:** Check if token is stored in localStorage
- **API errors:** Verify backend is running on port 8000

