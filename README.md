# 📈 Instrument Price Dashboard

A full-stack web application for tracking and displaying instrument prices with interactive charts, statistics, and comparison features.

## 🎯 Features

- **Browse Instruments**: Search through 200+ instruments with real-time search-as-you-type
- **Price Charts**: Interactive 30-day price line charts with Recharts
- **Statistics**: View computed metrics including:
  - **Total Return %**: (last_price / first_price - 1) × 100
  - **Daily Volatility %**: Standard deviation of daily returns
  - **Max Drawdown %**: Largest peak-to-trough decline over the window
- **Multi-Select Comparison**: Compare 2-3 instruments side-by-side on overlay charts
- **Responsive Design**: Works on desktop and tablet
- **Error Handling**: Graceful handling of API errors and edge cases

## 📋 Project Structure

```
InstrumentPriceDashboard/
├── frontend/                      # React + TypeScript + Vite
│   ├── src/
│   │   ├── components/
│   │   │   ├── InstrumentList.tsx    # Ticker list & search
│   │   │   ├── PriceChart.tsx        # Single instrument chart
│   │   │   ├── StatsPanel.tsx        # Statistics display
│   │   │   └── ComparisonChart.tsx   # Multi-ticker overlay chart
│   │   ├── App.tsx                   # Main app component
│   │   ├── App.css                   # App styling
│   │   ├── index.css                 # Global styles
│   │   └── main.tsx                  # Entry point
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── .eslintrc.cjs
│
├── backend/                       # Python + FastAPI
│   ├── main.py                    # API endpoints
│   ├── data_loader.py             # CSV loader & stats calculator
│   ├── requirements.txt           # Python dependencies
│   └── .env.example              # Environment variables template
│
├── prices.csv                     # Sample price data (200 instruments, 30 days)
├── package.json                   # Root package.json
├── .gitignore
└── README.md
```

## 🤖 AI-Assisted Setup Notes

This project benefited from AI help in a few practical ways:

- creating the initial repo structure and starter files
- generating the base config files such as TypeScript configs, Vite setup, .gitignore, and package metadata
- writing the first pass of the CSS and layout styling
- helping clean up the README and setup instructions
- iterating on helper files and project wiring so the app could run quickly
- Creating boilerplate code for the various chart libraries used

This was especially useful for the scaffold and boilerplate work, while the app logic and business behavior were still written manually and refined with the help of AI.

## 🚀 Quick Start

### Prerequisites

- **Node.js** v18+ (for frontend)
- **Python** 3.8+ (for backend)
- **npm** or **yarn**

### 1. Clone & Install

```bash
# Clone the repository
git clone https://github.com/ujjaval1995/InstrumentPriceDashboard.git
cd InstrumentPriceDashboard

# Install all dependencies
npm run install:all
```

Or install manually:

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
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

### 2. Run the Application

Open **two terminal windows** in the repository root:

**Terminal 1 - Start Backend:**
```bash
npm run backend
```
Backend will start at `http://localhost:8000`

**Terminal 2 - Start Frontend:**
```bash
npm run frontend
```
Frontend will start at `http://localhost:5173`

Then open your browser to **http://localhost:5173**

### Alternative: Run Services Separately

**Frontend:**
```bash
cd frontend
npm run dev
```

**Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```

## 📡 API Endpoints

### Base URL: `http://localhost:8000/api`

#### Get All Instruments
```
GET /instruments
```
Returns a list of all 200+ available tickers.

**Response:**
```json
[
  { "ticker": "INST001" },
  { "ticker": "INST002" },
  ...
]
```

#### Get Price Series
```
GET /prices/{ticker}
```
Get full 30-day price time series for a specific ticker.

**Example:**
```
GET /prices/INST001
```

**Response:**
```json
{
  "ticker": "INST001",
  "prices": [
    { "date": "2024-01-01", "price": 145.32 },
    { "date": "2024-01-02", "price": 147.81 },
    ...
  ]
}
```

#### Get Statistics
```
GET /prices/{ticker}/stats
```
Get computed statistics for a ticker.

**Example:**
```
GET /prices/INST001/stats
```

**Response:**
```json
{
  "ticker": "INST001",
  "total_return_pct": 17.22,
  "daily_volatility_pct": 1.85,
  "max_drawdown_pct": 2.34
}
```

## 🛠️ Technology Stack

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool & dev server (lightning fast)
- **Recharts** - Interactive charting library
- **CSS3** - Responsive styling

### Backend
- **FastAPI** - Modern, fast Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **CSV** - In-memory price data (no database required)

## 📊 CSV Format

The `prices.csv` file contains daily closing prices with columns:
```
date,ticker,price
2024-01-01,INST001,145.32
2024-01-02,INST001,147.81
...
```

To use your own data:
1. Replace `prices.csv` with your file (same format)
2. Restart the backend
3. It will automatically load the new data

## 🎨 Key UI Components

### InstrumentList
- Search box with real-time filtering
- Clickable ticker buttons
- Multi-select checkboxes for comparison (max 3)
- Scrollable list

### PriceChart
- 30-day line chart for a single instrument
- Interactive tooltip on hover
- Date range on X-axis, price on Y-axis
- Loading and error states

### StatsPanel
- Displays return %, volatility, and max drawdown
- Color-coded metrics (green for positive return, red for drawdown)
- Responsive grid layout

### ComparisonChart
- Overlay chart for 2-3 selected instruments
- Different colors for each instrument
- Same interactive features as single chart

## 🔧 Configuration

### Backend Environment Variables

Create a `backend/.env` file (copy from `.env.example`):

```bash
DEBUG=True
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend Proxy

The frontend is configured to proxy API requests to the backend. See `frontend/vite.config.ts`:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
}
```

## 📚 Development

### Frontend Development

```bash
cd frontend
npm run dev      # Start dev server
npm run build    # Build for production
npm run lint     # Run ESLint
```

### Backend Development

```bash
cd backend
source venv/bin/activate
python main.py   # Run with auto-reload
```

For API documentation, visit `http://localhost:8000/docs` (Swagger UI)

## 🐛 Troubleshooting

### Port Already in Use

**Frontend (5173):**
- Change port in `frontend/vite.config.ts`
- Or stop the process using the port

**Backend (8000):**
- Change port in `backend/main.py`
- Update `CORS_ORIGINS` if changing port

### CORS Issues

Update `allowed_origins` in `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    ...
)
```

### Python Virtual Environment Not Activating

```bash
# Linux/Mac
source backend/venv/bin/activate

# Windows
backend\Scripts\activate

# Windows (PowerShell)
backend\Scripts\Activate.ps1
```

### Missing CSV File

If `prices.csv` is not found, the backend will automatically generate synthetic data for testing.

### API Returns 404

- Ensure ticker is in UPPERCASE (e.g., `INST001`)
- Check that the backend is running on port 8000
- Verify the CSV has been loaded (check backend console output)

## 📈 Statistics Calculations

### Total Return %
```
(last_price / first_price - 1) × 100
```
Example: If price goes from $100 to $110, return = 10%

### Daily Volatility %
```
Standard deviation of daily returns × 100
```
Calculated as: sqrt(mean((daily_return - mean_return)²)) × 100

### Max Drawdown %
```
(Peak - Trough) / Peak × 100
```
The largest peak-to-trough percentage decline during the 30-day window

## 🚢 Production Deployment

### Frontend

```bash
cd frontend
npm run build
# Output: frontend/dist/ (ready to deploy to any static host)
```

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Consider using:
- **Docker** for containerization
- **Nginx** for reverse proxy
- **PM2** or **systemd** for process management

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

- GitHub: [@ujjaval1995](https://github.com/ujjaval1995)

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Additional Resources

- [React Documentation](https://react.dev)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Vite Documentation](https://vitejs.dev)
- [Recharts Documentation](https://recharts.org)

## 🎓 Learning Path

If you're new to this stack:

1. **Frontend**: Start with `frontend/src/App.tsx` to understand the main component
2. **Backend**: Check `backend/main.py` for API endpoint definitions
3. **Data Loading**: See `backend/data_loader.py` for statistics calculations
4. **Charts**: Explore `frontend/src/components/ComparisonChart.tsx` for Recharts usage

---

**Happy Trading! 📊📈**
