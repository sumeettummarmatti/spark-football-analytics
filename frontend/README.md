# SPARK Frontend

Modern React frontend for SPARK Football Analytics platform.

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router** - Routing
- **Tailwind CSS** - Styling
- **Zustand** - State management
- **Axios** - HTTP client
- **Lucide React** - Icons

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Build

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── components/     # Reusable components
├── pages/          # Page components
├── services/       # API services
├── store/          # State management
├── types/          # TypeScript types
├── App.tsx         # Main app component
└── main.tsx        # Entry point
```

## Features

- ✅ User authentication (login/register)
- ✅ View teams, players, and matches
- ✅ Make predictions (24-hour cooldown)
- ✅ Follow teams and players
- ✅ View profile and leaderboard
- ✅ Admin panel (for admin users)
- ✅ Responsive design
- ✅ Dark mode support

## API Integration

The frontend communicates with the FastAPI backend at `http://localhost:8000`.

All API calls are handled through the `services/api.ts` file.

## Environment Variables

Create a `.env` file if needed:

```env
VITE_API_URL=http://localhost:8000
```

## Routes

- `/` - Home page
- `/login` - Login page
- `/register` - Registration page
- `/teams` - Teams list
- `/teams/:id` - Team details
- `/players` - Players list
- `/players/:id` - Player details
- `/matches` - Matches list
- `/matches/:id` - Match details
- `/predictions` - Make predictions (protected)
- `/profile` - User profile (protected)
- `/leaderboard` - Global leaderboard
- `/admin` - Admin panel (admin only)

