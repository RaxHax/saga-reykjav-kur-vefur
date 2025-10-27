import HexagonCard from './HexagonCard'
import './HoneycombGrid.css'

/**
 * HoneycombGrid Component
 *
 * Arranges hexagonal cards in a honeycomb pattern.
 * The layout automatically adjusts for different screen sizes.
 *
 * @param {Object} props
 * @param {Array} props.cards - Array of card configurations
 */
const HoneycombGrid = ({ cards }) => {
  return (
    <div className="honeycomb-container">
      <div className="honeycomb-grid">
        {cards.map((card, index) => (
          <div key={index} className={`honeycomb-cell cell-${index + 1}`}>
            <HexagonCard
              title={card.title}
              description={card.description}
              icon={card.icon}
              accentColor={card.accentColor}
              href={card.href}
              delay={index * 0.1}
            />
          </div>
        ))}
      </div>
    </div>
  )
}

export default HoneycombGrid
