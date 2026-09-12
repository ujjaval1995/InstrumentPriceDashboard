import { FC, useState, useEffect } from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import './ComparisonChart.css'

interface PricePoint {
  date: string
  price: number
}

interface PriceSeries {
  ticker: string
  prices: PricePoint[]
}

interface ChartData {
  date: string
  [key: string]: string | number
}

interface ComparisonChartProps {
  tickers: string[]
}

const COLORS = ['#1976d2', '#388e3c', '#d32f2f', '#f57c00']

const ComparisonChart: FC<ComparisonChartProps> = ({ tickers }) => {
  const [data, setData] = useState<ChartData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAllPrices = async () => {
      try {
        setLoading(true)
        setError(null)

        const responses = await Promise.all(
          tickers.map((ticker) => fetch(`/api/prices/${ticker}`))
        )

        if (responses.some((r) => !r.ok)) {
          throw new Error('Failed to load some price data')
        }

        const allPrices: PriceSeries[] = await Promise.all(
          responses.map((r) => r.json())
        )

        // Merge data by date
        const dateMap = new Map<string, ChartData>()

        allPrices.forEach((series) => {
          series.prices.forEach((p: PricePoint) => {
            const dateKey = p.date.split('-').slice(1).join('-')
            if (!dateMap.has(dateKey)) {
              dateMap.set(dateKey, { date: dateKey })
            }
            const entry = dateMap.get(dateKey)!
            entry[series.ticker] = p.price
          })
        })

        setData(Array.from(dateMap.values()))
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    if (tickers.length > 0) {
      fetchAllPrices()
    }
  }, [tickers])

  if (loading) return <div className="comparison-container">Loading chart...</div>
  if (error) return <div className="comparison-container error">{error}</div>
  if (!data.length) return <div className="comparison-container">No data available</div>

  return (
    <div className="comparison-container">
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" angle={-45} textAnchor="end" height={80} />
          <YAxis />
          <Tooltip
            formatter={(value) => `$${(value as number).toFixed(2)}`}
            labelFormatter={(label) => `Date: ${label}`}
          />
          <Legend />
          {tickers.map((ticker, idx) => (
            <Line
              key={ticker}
              type="monotone"
              dataKey={ticker}
              stroke={COLORS[idx % COLORS.length]}
              dot={false}
              strokeWidth={2}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default ComparisonChart
