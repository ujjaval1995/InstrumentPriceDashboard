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
import './PriceChart.css'

interface PricePoint {
  date: string
  price: number
}

interface ChartData {
  date: string
  price: number
}

interface PriceChartProps {
  ticker: string
}

const PriceChart: FC<PriceChartProps> = ({ ticker }) => {
  const [data, setData] = useState<ChartData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchPrices = async () => {
      try {
        setLoading(true)
        setError(null)
        const response = await fetch(`/api/prices/${ticker}`)
        if (!response.ok) throw new Error('Failed to load price data')
        const result = await response.json()
        const chartData = result.prices.map((p: PricePoint) => ({
          date: p.date.split('-').slice(1).join('-'),
          price: p.price,
        }))
        setData(chartData)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchPrices()
  }, [ticker])

  if (loading) return <div className="chart-container">Loading chart...</div>
  if (error) return <div className="chart-container error">{error}</div>
  if (!data.length) return <div className="chart-container">No data available</div>

  return (
    <div className="chart-container">
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
          <Line
            type="monotone"
            dataKey="price"
            stroke="#1976d2"
            dot={false}
            strokeWidth={2}
            name={`${ticker} Price`}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default PriceChart
