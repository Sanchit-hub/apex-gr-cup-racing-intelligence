import { useState, useEffect } from 'react'
import axios from 'axios'
import BestLapCard from './BestLapCard'
import DriverPerformance from './DriverPerformance'
import DetailedAnalytics from './DetailedAnalytics'
import AMICOSAnalysis from './AMICOSAnalysis'
import AMICOSSimulator from './AMICOSSimulator'

interface DashboardProps {
  track: string
  session: string
}

const Dashboard = ({ track, session }: DashboardProps) => {
  const [bestLap, setBestLap] = useState<any>(null)
  const [drivers, setDrivers] = useState<string[]>([])
  const [driverId, setDriverId] = useState<string>('')
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'analysis' | 'simulator'>('analysis')

  useEffect(() => {
    loadData()
  }, [track, session])

  const loadData = async () => {
    setLoading(true)
    try {
      const [bestLapResponse, driversResponse] = await Promise.all([
        axios.get(`/api/analytics/track/${track}/session/${session}/best-lap`),
        axios.get(`/api/analytics/track/${track}/session/${session}/drivers`)
      ])
      setBestLap(bestLapResponse.data)
      setDrivers(driversResponse.data)
      if (bestLapResponse.data.driver_id) {
        setDriverId(bestLapResponse.data.driver_id)
      }
    } catch (error) {
      console.error('Failed to load data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading analytics...</div>
  }

  return (
    <div className="space-y-6">
      {/* Mode Selector */}
      <div className="bg-gray-900 p-4 rounded-lg shadow-lg">
        <div className="flex gap-4">
          <button
            onClick={() => setActiveTab('analysis')}
            className={`flex-1 py-3 px-6 rounded-lg font-bold transition-all ${
              activeTab === 'analysis'
                ? 'bg-purple-600 text-white shadow-lg'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            📊 Race Data Analysis
          </button>
          <button
            onClick={() => setActiveTab('simulator')}
            className={`flex-1 py-3 px-6 rounded-lg font-bold transition-all ${
              activeTab === 'simulator'
                ? 'bg-green-600 text-white shadow-lg'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            🎮 Real-Time Simulator
          </button>
        </div>
      </div>

      {activeTab === 'simulator' ? (
        <AMICOSSimulator />
      ) : (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <BestLapCard bestLap={bestLap} />
            
            <div className="bg-gray-900 p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-bold mb-4">Driver Analysis</h3>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">Select Driver</label>
                <select
                  value={driverId}
                  onChange={(e) => setDriverId(e.target.value)}
                  className="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white"
                >
                  <option value="">-- Select a driver --</option>
                  {drivers.map(driver => (
                    <option key={driver} value={driver}>
                      {driver}
                    </option>
                  ))}
                </select>
              </div>
              {driverId && (
                <DriverPerformance track={track} session={session} driverId={driverId} />
              )}
            </div>
          </div>

          {driverId && (
            <>
              <div className="bg-gray-900 p-6 rounded-lg shadow-lg">
                <AMICOSAnalysis track={track} session={session} driverId={driverId} />
              </div>
              
              <div className="bg-gray-900 p-6 rounded-lg shadow-lg">
                <h3 className="text-xl font-bold mb-4">🔬 Detailed Analytics</h3>
                <DetailedAnalytics track={track} session={session} driverId={driverId} />
              </div>
            </>
          )}
        </>
      )}
    </div>
  )
}

export default Dashboard
