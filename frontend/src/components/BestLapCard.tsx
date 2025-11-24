interface BestLapCardProps {
  bestLap: any
}

const BestLapCard = ({ bestLap }: BestLapCardProps) => {
  if (!bestLap || bestLap.error) {
    return (
      <div className="bg-gray-900 p-6 rounded-lg shadow-lg">
        <h3 className="text-xl font-bold mb-4">🏆 Best Lap</h3>
        <p className="text-gray-400">No data available</p>
      </div>
    )
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = (seconds % 60).toFixed(3)
    return `${mins}:${secs.padStart(6, '0')}`
  }

  return (
    <div className="bg-gradient-to-br from-gr-red to-red-900 p-6 rounded-lg shadow-lg">
      <h3 className="text-xl font-bold mb-4">🏆 Best Lap</h3>
      
      <div className="space-y-3">
        <div>
          <p className="text-sm opacity-80">Lap Time</p>
          <p className="text-4xl font-bold">{formatTime(bestLap.best_lap_time)}</p>
        </div>
        
        <div className="grid grid-cols-2 gap-4 pt-4 border-t border-white/20">
          <div>
            <p className="text-sm opacity-80">Driver</p>
            <p className="text-lg font-semibold">{bestLap.driver_id}</p>
          </div>
          <div>
            <p className="text-sm opacity-80">Lap Number</p>
            <p className="text-lg font-semibold">#{bestLap.lap_number}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default BestLapCard
