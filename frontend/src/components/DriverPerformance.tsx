import { useState, useEffect } from 'react'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface DriverPerformanceProps {
  track: string
  session: string
  driverId: string
}

const DriverPerformance = ({ track, session, driverId }: DriverPerformanceProps) => {
  const [performance, setPerformance] = useState<any>(null)
  const [consistency, setConsistency] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadPerformance()
  }, [track, session, driverId])

  const loadPerformance = async () => {
    setLoading(true)
    try {
      const [perfResponse, consResponse] = await Promise.all([
        axios.get(`/api/analytics/track/${track}/session/${session}/driver/${driverId}/performance`),
        axios.get(`/api/strategy/track/${track}/session/${session}/driver/${driverId}/consistency`)
      ])
      setPerformance(perfResponse.data)
      setConsistency(consResponse.data)
    } catch (error) {
      console.error('Failed to load performance:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-4">Loading driver data...</div>
  }

  if (performance?.error) {
    return <div className="text-red-400">{performance.error}</div>
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = (seconds % 60).toFixed(3)
    return `${mins}:${secs.padStart(6, '0')}`
  }

  const chartData = performance?.lap_times?.map((time: number, index: number) => ({
    lap: index + 1,
    time: time
  })) || []

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-800 p-4 rounded-lg">
          <p className="text-sm text-gray-400">Best Lap</p>
          <p className="text-2xl font-bold text-green-400">{formatTime(performance.best_lap)}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg">
          <p className="text-sm text-gray-400">Average Lap</p>
          <p className="text-2xl font-bold">{formatTime(performance.average_lap)}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg">
          <p className="text-sm text-gray-400">Consistency</p>
          <p className="text-2xl font-bold text-blue-400">{consistency?.consistency_score?.toFixed(1)}%</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg">
          <p className="text-sm text-gray-400">Total Laps</p>
          <p className="text-2xl font-bold">{performance.total_laps}</p>
        </div>
      </div>

      {chartData.length > 0 && (
        <div className="bg-gray-800 p-4 rounded-lg">
          <h4 className="font-bold mb-4">Lap Time Progression</h4>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="lap" stroke="#9CA3AF" />
              <YAxis stroke="#9CA3AF" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1F2937', border: 'none' }}
                formatter={(value: number) => formatTime(value)}
              />
              <Line type="monotone" dataKey="time" stroke="#ef4444" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}

export default DriverPerformance
