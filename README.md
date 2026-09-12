# Instrument Price Dashboard

A full-stack web application for tracking and displaying instrument prices in real-time.

## 📋 Project Structure

```
InstrumentPriceDashboard/
├── frontend/                 # React + TypeScript
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   └── index.css
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── backend/                  # Python FastAPI
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
└── package.json             # Root package.json
```

## 🚀 Quick Start

### Prerequisites
- Node.js (v18+)
- Python (v3.8+)
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ujjaval1995/InstrumentPriceDashboard.git
   cd InstrumentPriceDashboard
   ```

2. **Install all dependencies**
   ```bash
   npm run install:all
   ```

   Or manually:
   
   **Frontend:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

   **Backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cd ..
   ```

### Running the Application

#### Option 1: Run Both Services (from root directory)

**Terminal 1 - Frontend:**
```bash
npm run frontend
```
Frontend will start at `http://localhost:5173`

**Terminal 2 - Backend:**
```bash
npm run backend
```
Backend will start at `http://localhost:8000`

#### Option 2: Run Services Separately

**Frontend:**
```bash
cd frontend
npm run dev
```

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### API Documentation

Once the backend is running, visit `http://localhost:8000/docs` to access the interactive Swagger UI documentation.

## 📝 Available Endpoints

- `GET /` - Health check
- `GET /instruments` - Get all instruments
- `GET /instruments/{symbol}` - Get specific instrument by symbol
- `POST /instruments` - Create a new instrument

## 🛠️ Frontend Development

The frontend uses:
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Axios** - HTTP client (optional, using fetch in starter code)

### Frontend Build
```bash
cd frontend
npm run build
```

### Frontend Linting
```bash
cd frontend
npm run lint
```

## 🔧 Backend Development

The backend uses:
- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### Backend Configuration

Copy `.env.example` to `.env` and update as needed:
```bash
cd backend
cp .env.example .env
```

## 🌐 CORS Configuration

The application is configured to accept requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Alternative React dev server)

Update `backend/main.py` if you need to add more origins.

## 📦 Building for Production

### Frontend Production Build
```bash
cd frontend
npm run build
```
Output will be in `frontend/dist/`

### Backend Deployment
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🐛 Troubleshooting

### Port Already in Use
- Frontend: Change port in `frontend/vite.config.ts`
- Backend: Change port in `backend/main.py` or `npm run backend` command

### CORS Issues
Update `allowed_origins` in `backend/main.py`

### Python Virtual Environment
Always activate the virtual environment before running backend:
```bash
cd backend
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

## 📚 Additional Resources

- [React Documentation](https://react.dev)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Vite Documentation](https://vitejs.dev)

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

- GitHub: [@ujjaval1995](https://github.com/ujjaval1995)

## 🤝 Contributing

Contributions are welcome! Feel free to open issues and pull requests.
