import { FC } from 'react'
import './InstrumentList.css'

interface Instrument {
  ticker: string
}

interface InstrumentListProps {
  instruments: Instrument[]
  selectedTicker: string | null
  selectedForComparison: string[]
  onSelect: (ticker: string) => void
  onToggleComparison: (ticker: string) => void
}

const InstrumentList: FC<InstrumentListProps> = ({
  instruments,
  selectedTicker,
  selectedForComparison,
  onSelect,
  onToggleComparison,
}) => {
  return (
    <div className="instrument-list">
      <div className="list-header">
        <h3>Instruments ({instruments.length})</h3>
      </div>
      <ul className="instruments">
        {instruments.map((inst) => (
          <li key={inst.ticker} className="instrument-item">
            <button
              className={`instrument-button ${
                selectedTicker === inst.ticker ? 'active' : ''
              }`}
              onClick={() => onSelect(inst.ticker)}
            >
              {inst.ticker}
            </button>
            {selectedTicker !== inst.ticker && (
              <button
                className={`compare-btn ${
                  selectedForComparison.includes(inst.ticker) ? 'selected' : ''
                }`}
                onClick={(e) => {
                  e.stopPropagation()
                  onToggleComparison(inst.ticker)
                }}
                title={selectedForComparison.includes(inst.ticker) ? 'Remove from comparison' : 'Add to comparison (max 3)'}
              >
                {selectedForComparison.includes(inst.ticker) ? '✓' : '+'}
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default InstrumentList
