import { FC } from 'react'
import './StatsPanel.css'

interface Stats {
  ticker: string
  total_return_pct: number
  daily_volatility_pct: number
  max_drawdown_pct: number
}

interface StatsPanelProps {
  stats: Stats
}

const StatsPanel: FC<StatsPanelProps> = ({ stats }) => {
  const getReturnColor = (value: number) => {
    return value >= 0 ? '#4caf50' : '#d32f2f'
  }

  const getDrawdownColor = (value: number) => {
    return value <= 5 ? '#4caf50' : value <= 10 ? '#ff9800' : '#d32f2f'
  }

  return (
    <div className="stats-panel">
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Total Return</div>
          <div
            className="stat-value"
            style={{ color: getReturnColor(stats.total_return_pct) }}
          >
            {stats.total_return_pct > 0 ? '+' : ''}
            {stats.total_return_pct.toFixed(2)}%
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Daily Volatility</div>
          <div className="stat-value">{stats.daily_volatility_pct.toFixed(2)}%</div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Max Drawdown</div>
          <div
            className="stat-value"
            style={{ color: getDrawdownColor(stats.max_drawdown_pct) }}
          >
            -{stats.max_drawdown_pct.toFixed(2)}%
          </div>
        </div>
      </div>
    </div>
  )
}

export default StatsPanel
