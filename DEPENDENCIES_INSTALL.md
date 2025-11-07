# Dependencies Installation Guide

## Frontend Dependencies

### Install Node.js dependencies:
```bash
cd frontend
npm install
```

This will install all required packages including:
- React 18
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Zustand
- Axios
- And all other dependencies

### Verify installation:
```bash
cd frontend
npm run dev
```

The frontend should start on http://localhost:3000

## Backend Dependencies

### Option 1: Using pip (if Python 3 is available)
```bash
cd backend
pip install -r requirements.txt
```

### Option 2: Using pip3
```bash
cd backend
pip3 install -r requirements.txt
```

### Option 3: Using Python module
```bash
cd backend
python3 -m pip install -r requirements.txt
```

### Option 4: Using virtual environment (Recommended)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Verify installation:
```bash
cd backend
python -m uvicorn src.main:app --reload
```

The backend should start on http://localhost:8000

## Common Issues & Solutions

### Frontend Issues:

1. **TypeScript errors (red squiggly lines):**
   - Run: `npm install` in the frontend directory
   - Restart your IDE/editor
   - Make sure `@types/node` is installed: `npm install --save-dev @types/node`

2. **Module not found errors:**
   - Delete `node_modules` and `package-lock.json`
   - Run `npm install` again

3. **Vite errors:**
   - Clear Vite cache: `rm -rf node_modules/.vite`
   - Reinstall: `npm install`

### Backend Issues:

1. **Module not found errors:**
   - Make sure you're in a virtual environment
   - Run: `pip install -r requirements.txt`

2. **Import errors:**
   - Check that all route files are in `backend/src/api/routes/`
   - Verify `__init__.py` files exist in each package directory

3. **Database connection errors:**
   - Start PostgreSQL: `docker-compose up -d postgres`
   - Check database credentials in `backend/src/core/config.py`

## Quick Start Checklist

- [ ] Install frontend dependencies: `cd frontend && npm install`
- [ ] Install backend dependencies: `cd backend && pip install -r requirements.txt`
- [ ] Start database: `docker-compose up -d postgres`
- [ ] Start backend: `cd backend && python -m uvicorn src.main:app --reload`
- [ ] Start frontend: `cd frontend && npm run dev`
- [ ] Access frontend at http://localhost:3000
- [ ] Access backend API docs at http://localhost:8000/docs

