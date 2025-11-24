import { useState, useEffect } from 'react'
import axios from 'axios'

interface DetailedAnalyticsProps {
  track: string
  session: string
  driverId: string
}

const DetailedAnalytics = ({ track, session, driverId }: DetailedAnalyticsProps) => {
  const [data, setData] = useState<any>(null)
  const [speedData, setSpeedData] = useState<any>(null)
  const [brakingData, setBrakingData] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [track, session, driverId])

  const loadData = async () => {
    setLoading(true)
    try {
      const [detailedResponse, speedResponse, brakingResponse] = await Promise.all([
        axios.get(`/api/analytics/track/${track}/session/${session}/driver/${driverId}/detailed-performance`),
        axios.get(`/api/analytics/track/${track}/session/${session}/driver/${driverId}/speed-analysis`),
        axios.get(`/api/analytics/track/${track}/session/${session}/driver/${driverId}/braking-analysis`)
      ])
      setData(detailedResponse.data)
      setSpeedData(speedResponse.data)
      setBrakingData(brakingResponse.data)
    } catch (error) {
      console.error('Failed to load detailed analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-4">Loading detailed analytics...</div>
  }

  if (data?.error) {
    return <div className="text-red-400">{data.error}</div>
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = (seconds % 60).toFixed(3)
    return `${mins}:${secs.padStart(6, '0')}`
  }

  return (
    <div className="space-y-6">
      {/* Track & Vehicle Info */}
      <div className="bg-gradient-to-r from-red-900 to-gray-900 p-6 rounded-lg">
        <h3 className="text-2xl font-bold mb-4">🏁 {data.track}</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <p className="text-gray-400">Vehicle</p>
            <p className="font-bold">{data.vehicle}</p>
          </div>
          <div>
            <p className="text-gray-400">Track Length</p>
            <p className="font-bold">{data.track_info?.length_km} km</p>
          </div>
          <div>
            <p className="text-gray-400">Turns</p>
            <p className="font-bold">{data.track_info?.turns}</p>
          </div>
          <div>
            <p className="text-gray-400">Elevation</p>
            <p className="font-bold">{data.track_info?.elevation_change_m}m</p>
          </div>
        </div>
      </div>

      {/* Performance Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gray-900 p-6 rounded-lg border-l-4 border-green-500">
          <p className="text-sm text-gray-400">Best Lap</p>
          <p className="text-3xl font-bold text-green-400">{formatTime(data.performance?.best_lap)}</p>
          <p className="text-xs text-gray-500 mt-2">
            {data.performance?.delta_to_record > 0 
              ? `+${data.performance.delta_to_record.toFixed(3)}s from record`
              : 'Track record!'}
          </p>
        </div>

        <div className="bg-gray-900 p-6 rounded-lg border-l-4 border-blue-500">
          <p className="text-sm text-gray-400">Consistency Rating</p>
          <p className="text-3xl font-bold text-blue-400">{data.consistency?.rating}</p>
          <p className="text-xs text-gray-500 mt-2">
            {data.consistency?.score.toFixed(1)}% within 0.5s
          </p>
        </div>

        <div className="bg-gray-900 p-6 rounded-lg border-l-4 border-purple-500">
          <p className="text-sm text-gray-400">Theoretical Best</p>
          <p className="text-3xl font-bold text-purple-400">{formatTime(data.performance?.theoretical_best)}</p>
          <p className="text-xs text-gray-500 mt-2">
            -{(data.performance?.best_lap - data.performance?.theoretical_best).toFixed(3)}s potential
          </p>
        </div>
      </div>

      {/* Pace Analysis */}
      {data.pace_analysis && !data.pace_analysis.message && (
        <div className="bg-gray-900 p-6 rounded-lg">
          <h4 className="text-xl font-bold mb-4">📊 Pace Evolution</h4>
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-gray-800 p-4 rounded">
              <p className="text-sm text-gray-400">Early Stint</p>
              <p className="text-2xl font-bold">{formatTime(data.pace_analysis.early_stint?.avg_lap_time)}</p>
              <p className="text-xs text-green-400">Best: {formatTime(data.pace_analysis.early_stint?.best_lap)}</p>
            </div>
            <div className="bg-gray-800 p-4 rounded">
              <p className="text-sm text-gray-400">Mid Stint</p>
              <p className="text-2xl font-bold">{formatTime(data.pace_analysis.mid_stint?.avg_lap_time)}</p>
              <p className="text-xs text-green-400">Best: {formatTime(data.pace_analysis.mid_stint?.best_lap)}</p>
            </div>
            <div className="bg-gray-800 p-4 rounded">
              <p className="text-sm text-gray-400">Late Stint</p>
              <p className="text-2xl font-bold">{formatTime(data.pace_analysis.late_stint?.avg_lap_time)}</p>
              <p className="text-xs text-red-400">
                +{data.pace_analysis.degradation?.early_to_late_delta.toFixed(3)}s degradation
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Speed Analysis */}
      {speedData && !speedData.error && (
        <div className="bg-gray-900 p-6 rounded-lg">
          <h4 className="text-xl font-bold mb-4">🚀 Speed Analysis</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gray-800 p-4 rounded">
              <p className="text-sm text-gray-400">Top Speed</p>
              <p className="text-2xl font-bold text-red-400">{speedData.speed_metrics?.vmax_kmh.toFixed(1)} km/h</p>
              <p className="text-xs text-gray-500">
                {speedData.vehicle_comparison?.speed_utilization_pct.toFixed(1)}% of max
              </p>
            </div>
            <div className="bg-gray-800 p-4 rounded">
              <p className="text-sm text-gray-400">Avg Speed</p>
              <p className="text-2xl font-bold">{speedData.speed_metrics?.vavg_kmh.toFixed(1)} km/h</p>
            </div>
            <div className="bg-gray-800 p-4 rounded">
              <p className="text-sm text-gray-400">Min Speed</p>
              <p className="text-2xl font-bold">{speedData.speed_metrics?.vmin_kmh.toFixed(1)} km/h</p>
            </div>
            <div className="bg-gray-800 p-4 rounded">
              <p className="text-sm text-gray-400">Vehicle Max</p>
              <p className="text-2xl font-bold text-gray-500">{speedData.vehicle_comparison?.theoretical_max_kmh} km/h</p>
              <p className="text-xs text-gray-500">GR86 Cup limit</p>
            </div>
          </div>
          
          <div className="mt-4 grid grid-cols-3 gap-4">
            <div className="bg-gray-800 p-3 rounded">
              <p className="text-xs text-gray-400">High Speed (&gt;150 km/h)</p>
              <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
                <div 
                  className="bg-red-500 h-2 rounded-full" 
                  style={{width: `${speedData.speed_distribution?.high_speed_pct}%`}}
                ></div>
              </div>
              <p className="text-xs mt-1">{speedData.speed_distribution?.high_speed_pct.toFixed(1)}%</p>
            </div>
            <div className="bg-gray-800 p-3 rounded">
              <p className="text-xs text-gray-400">Mid Speed (100-150 km/h)</p>
              <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
                <div 
                  className="bg-yellow-500 h-2 rounded-full" 
                  style={{width: `${speedData.speed_distribution?.mid_speed_pct}%`}}
                ></div>
              </div>
              <p className="text-xs mt-1">{speedData.speed_distribution?.mid_speed_pct.toFixed(1)}%</p>
            </div>
            <div className="bg-gray-800 p-3 rounded">
              <p className="text-xs text-gray-400">Low Speed (&lt;100 km/h)</p>
              <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
                <div 
                  className="bg-blue-500 h-2 rounded-full" 
                  style={{width: `${speedData.speed_distribution?.low_speed_pct}%`}}
                ></div>
              </div>
              <p className="text-xs mt-1">{speedData.speed_distribution?.low_speed_pct.toFixed(1)}%</p>
            </div>
          </div>
        </div>
      )}

      {/* Braking Analysis */}
      {brakingData && !brakingData.error && !brakingData.message && (
        <div className="bg-gray-900 p-6 rounded-lg">
          <h4 className="text-xl font-bold mb-4">🛑 Professional Braking Analysis</h4>
          
          {/* G-Forces */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div className="bg-gray-800 p-4 rounded border-l-4 border-red-500">
              <p className="text-sm text-gray-400">Max Braking G</p>
              <p className="text-3xl font-bold text-red-400">{brakingData.g_forces?.max_braking_g}G</p>
              <p className="text-xs text-gray-500">{brakingData.g_forces?.utilization_pct}% of limit</p>
            </div>
            <div className="bg-gray-800 p-4 rounded">
              <p className="text-sm text-gray-400">Avg Braking G</p>
              <p className="text-2xl font-bold">{brakingData.g_forces?.avg_braking_g}G</p>
            </div>
            <div className="bg-gray-800 p-4 rounded">
              <p className="text-sm text-gray-400">Vehicle Limit</p>
              <p className="text-2xl font-bold text-gray-500">{brakingData.g_forces?.vehicle_limit_g}G</p>
              <p className="text-xs text-gray-500">GR86 Cup max</p>
            </div>
            <div className="bg-gray-800 p-4 rounded border-l-4 border-green-500">
              <p className="text-sm text-gray-400">Efficiency</p>
              <p className="text-2xl font-bold text-green-400">{brakingData.efficiency?.overall_efficiency_pct}%</p>
            </div>
          </div>

          {/* Brake Pressure */}
          <div className="bg-gray-800 p-4 rounded mb-4">
            <h5 className="font-bold mb-3">Brake Pressure (bar)</h5>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-xs text-gray-400">Max Front</p>
                <p className="text-xl font-bold text-red-400">{brakingData.braking_metrics?.max_front_pressure_bar} bar</p>
                <p className="text-xs text-gray-500">of {brakingData.brake_system?.max_pressure_front_bar} bar</p>
              </div>
              <div>
                <p className="text-xs text-gray-400">Max Rear</p>
                <p className="text-xl font-bold text-orange-400">{brakingData.braking_metrics?.max_rear_pressure_bar} bar</p>
                <p className="text-xs text-gray-500">of {brakingData.brake_system?.max_pressure_rear_bar} bar</p>
              </div>
              <div>
                <p className="text-xs text-gray-400">Avg Front</p>
                <p className="text-xl font-bold">{brakingData.braking_metrics?.avg_front_pressure_bar} bar</p>
              </div>
              <div>
                <p className="text-xs text-gray-400">Avg Rear</p>
                <p className="text-xl font-bold">{brakingData.braking_metrics?.avg_rear_pressure_bar} bar</p>
              </div>
            </div>
          </div>

          {/* Brake Bias & Technique */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div className="bg-gray-800 p-4 rounded">
              <h5 className="font-bold mb-2">Brake Bias</h5>
              <div className="flex items-center gap-2">
                <div className="flex-1">
                  <div className="w-full bg-gray-700 rounded-full h-4">
                    <div 
                      className="bg-red-500 h-4 rounded-full flex items-center justify-center text-xs font-bold"
                      style={{width: `${brakingData.braking_metrics?.brake_bias_front_pct}%`}}
                    >
                      {brakingData.braking_metrics?.brake_bias_front_pct}%
                    </div>
                  </div>
                  <div className="flex justify-between text-xs mt-1">
                    <span>Front</span>
                    <span>Rear ({(100 - brakingData.braking_metrics?.brake_bias_front_pct).toFixed(1)}%)</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-gray-800 p-4 rounded">
              <h5 className="font-bold mb-2">Trail Braking</h5>
              <p className="text-3xl font-bold text-purple-400">{brakingData.technique?.trail_braking_pct}%</p>
              <p className="text-sm text-gray-400">Rating: <span className="text-white font-bold">{brakingData.technique?.rating}</span></p>
              <p className="text-xs text-gray-500 mt-1">Braking while cornering</p>
            </div>
          </div>

          {/* Brake Applications */}
          <div className="bg-gray-800 p-4 rounded">
            <div className="flex justify-between items-center">
              <div>
                <p className="text-sm text-gray-400">Brake Applications</p>
                <p className="text-2xl font-bold">{brakingData.braking_metrics?.brake_applications}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Expected per Lap</p>
                <p className="text-2xl font-bold text-gray-500">{brakingData.braking_metrics?.expected_per_lap}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Consistency</p>
                <p className="text-2xl font-bold">{brakingData.braking_metrics?.consistency_bar} bar</p>
                <p className="text-xs text-gray-500">Lower is better</p>
              </div>
            </div>
          </div>

          {/* Brake System Info */}
          <div className="mt-4 bg-gray-800 p-4 rounded border-l-4 border-blue-500">
            <h5 className="font-bold mb-2">🔧 Brembo Brake System</h5>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-gray-400">Front Calipers</p>
                <p className="font-bold">{brakingData.brake_system?.front}</p>
              </div>
              <div>
                <p className="text-gray-400">Rear Calipers</p>
                <p className="font-bold">{brakingData.brake_system?.rear}</p>
              </div>
              <div>
                <p className="text-gray-400">ABS</p>
                <p className="font-bold">{brakingData.brake_system?.abs ? 'Enabled' : 'Disabled'}</p>
              </div>
              <div>
                <p className="text-gray-400">Front Efficiency</p>
                <p className="font-bold text-green-400">{brakingData.efficiency?.front_brake_efficiency_pct}%</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Vehicle Specs */}
      <div className="bg-gray-900 p-6 rounded-lg">
        <h4 className="text-xl font-bold mb-4">🏎️ Toyota GR86 Cup Specifications</h4>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
          <div>
            <p className="text-gray-400">Power</p>
            <p className="font-bold">{data.vehicle_specs?.horsepower} HP</p>
          </div>
          <div>
            <p className="text-gray-400">Weight</p>
            <p className="font-bold">{data.vehicle_specs?.weight_kg} kg</p>
          </div>
          <div>
            <p className="text-gray-400">Top Speed</p>
            <p className="font-bold">{data.vehicle_specs?.top_speed_kmh} km/h</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DetailedAnalytics
