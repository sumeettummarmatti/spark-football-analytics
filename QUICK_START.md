# Quick Start Guide

## 🚀 Fast Setup

Run the setup script to install all dependencies:

```bash
chmod +x setup.sh
./setup.sh
```

Or install manually:

### Frontend
```bash
cd frontend
npm install
```

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Running the Application

### 1. Start Database
```bash
docker-compose up -d postgres
```

### 2. Start Backend
```bash
cd backend
source venv/bin/activate  # If using virtual environment
python -m uvicorn src.main:app --reload
```

Backend will run on: http://localhost:8000

### 3. Start Frontend
```bash
cd frontend
npm run dev
```

Frontend will run on: http://localhost:3000

## ✅ Verify Installation

1. **Check Backend:**
   - Visit: http://localhost:8000/docs
   - You should see the FastAPI Swagger documentation

2. **Check Frontend:**
   - Visit: http://localhost:3000
   - You should see the SPARK homepage

## 🔧 Troubleshooting

### Frontend Issues

**Red squiggly lines in IDE:**
- Run `npm install` in the frontend directory
- Restart your IDE/editor
- Install Node types: `npm install --save-dev @types/node`

**Build errors:**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

### Backend Issues

**Import errors:**
- Make sure you're in the virtual environment
- Run: `pip install -r requirements.txt`

**Database connection errors:**
- Start PostgreSQL: `docker-compose up -d postgres`
- Check credentials in `backend/src/core/config.py`

## 📝 First Steps

1. Register a new account at http://localhost:3000/register
2. Login and explore teams, players, and matches
3. Make a prediction to earn points
4. Check your profile and the leaderboard

## 📚 Documentation

- API Documentation: http://localhost:8000/docs
- Frontend README: `frontend/README.md`
- Backend Testing Guide: `backend/TESTING_GUIDE.md`

