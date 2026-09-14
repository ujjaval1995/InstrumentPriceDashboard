import { useState, useEffect } from 'react'
import './App.css'
import InstrumentList from './components/InstrumentList'
import PriceChart from './components/PriceChart'
import StatsPanel from './components/StatsPanel'
import ComparisonChart from './components/ComparisonChart'

interface Instrument {
  ticker: string
}

interface Stats {
  ticker: string
  total_return_pct: number
  daily_volatility_pct: number
  max_drawdown_pct: number
}

function App() {
  const [instruments, setInstruments] = useState<Instrument[]>([])
  const [selectedTicker, setSelectedTicker] = useState<string | null>(null)
  const [selectedTickers, setSelectedTickers] = useState<string[]>([])
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')

  // Load instruments on mount
  useEffect(() => {
    const fetchInstruments = async () => {
      try {
        setLoading(true)
        setError(null)
        const response = await fetch('/api/instruments')
        if (!response.ok) throw new Error('Failed to load instruments')
        const data = await response.json()
        setInstruments(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchInstruments()
  }, [])

  // Load stats when ticker changes
  useEffect(() => {
    if (!selectedTicker) {
      setStats(null)
      return
    }

    const fetchStats = async () => {
      try {
        setError(null)
        const response = await fetch(`/api/prices/${selectedTicker}/stats`)
        if (!response.ok) throw new Error('Failed to load statistics')
        const data = await response.json()
        setStats(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
        setStats(null)
      }
    }

    fetchStats()
  }, [selectedTicker])

  const handleTickerSelect = (ticker: string) => {
    setSelectedTicker(ticker)
  }

  const handleToggleComparison = (ticker: string) => {
    setSelectedTickers(prev => {
      if (prev.includes(ticker)) {
        return prev.filter(t => t !== ticker)
      } else if (prev.length < 3) {
        return [...prev, ticker]
      } else {
        return prev
      }
    })
  }

  const filteredInstruments = instruments.filter(tick =>
    tick.ticker.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="app">
      <header className="app-header">
        <h1>📈 Instrument Price Dashboard</h1>
        <p>Browse and compare instrument prices over a 30-day window</p>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <div className="app-container">
        <aside className="sidebar">
          <div className="search-box">
            <input
              type="text"
              placeholder="Search instruments..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="search-input"
            />
          </div>

          {loading ? (
            <div className="loading">Loading instruments...</div>
          ) : (
            <InstrumentList
              instruments={filteredInstruments}
              selectedTicker={selectedTicker}
              selectedForComparison={selectedTickers}
              onSelect={handleTickerSelect}
              onToggleComparison={handleToggleComparison}
            />
          )}
        </aside>

        <main className="main-content">
          {selectedTicker ? (
            <div className="content-grid">
              <div className="chart-section">
                <h2>{selectedTicker}</h2>
                {stats && <StatsPanel stats={stats} />}
                <PriceChart ticker={selectedTicker} />
              </div>

              {selectedTickers.length > 0 && (
                <div className="comparison-section">
                  <h2>Compare ({selectedTickers.length} selected)</h2>
                  <ComparisonChart tickers={[...selectedTickers, selectedTicker]} />
                </div>
              )}
            </div>
          ) : (
            <div className="empty-state">
              <div className="empty-message">
                <h2>👈 Select an instrument</h2>
                <p>Choose a ticker from the list to view its price chart and statistics</p>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}

export default App
