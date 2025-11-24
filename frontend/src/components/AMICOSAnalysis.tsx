import { useState, useEffect } from 'react'
import axios from 'axios'

interface AMICOSProps {
  track: string
  session: string
  driverId: string
}

const AMICOSAnalysis = ({ track, session, driverId }: AMICOSProps) => {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [track, session, driverId])

  const loadData = async () => {
    setLoading(true)
    try {
      const response = await axios.get(`/api/analytics/track/${track}/session/${session}/driver/${driverId}/amicos-analysis`)
      setData(response.data)
    } catch (error) {
      console.error('Failed to load AMICOS analysis:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mb-4"></div>
        <p className="text-xl">🔬 Analyzing cornering physics...</p>
        <p className="text-sm text-gray-400 mt-2">Processing 200+ data points per corner</p>
      </div>
    )
  }

  // Don't render if no data
  if (data?.error || !data?.corners_detected) {
    return null
  }

  return (
    <div className="space-y-6">
      {/* Header with Animation */}
      <div className="bg-gradient-to-r from-purple-900 via-blue-900 to-purple-900 p-8 rounded-lg border-2 border-purple-500 shadow-2xl transform hover:scale-[1.02] transition-all duration-300">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-4xl font-bold mb-2 bg-gradient-to-r from-purple-300 to-blue-300 bg-clip-text text-transparent">
              🧬 AMICOS Analysis
            </h3>
            <p className="text-sm text-gray-300">Adaptive Momentum-Inertia Cornering Optimization System</p>
            <p className="text-xs text-gray-400 mt-1">Physics-based cornering intelligence • {data.corners_detected} corners analyzed</p>
          </div>
          <div className="text-right">
            <div className="text-5xl font-bold text-purple-400">{data.corners_detected}</div>
            <div className="text-xs text-gray-400">Corners Detected</div>
          </div>
        </div>
      </div>

      {/* Driver DNA with Hover Effects */}
      {data.driver_dna && !data.driver_dna.message && (
        <div className="bg-gradient-to-br from-indigo-900 to-purple-900 p-6 rounded-lg border-l-4 border-purple-400 hover:shadow-2xl transition-all duration-300">
          <h4 className="text-2xl font-bold mb-4 flex items-center gap-2">
            🧬 Driver DNA / Fingerprint
            <span className="text-xs bg-purple-500/30 px-2 py-1 rounded">Unique Signature</span>
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-black/20 p-6 rounded-lg">
              <p className="text-sm text-gray-300 mb-2">Driving Style Classification</p>
              <p className="text-5xl font-bold text-purple-300 mb-2">{data.driver_dna.driving_style}</p>
              <p className="text-sm text-gray-400 mt-2">{data.driver_dna.signature}</p>
              <div className="mt-4 flex gap-2">
                {data.driver_dna.driving_style === 'Aggressive' && <span className="px-3 py-1 bg-red-500/30 text-red-300 rounded-full text-xs">High Risk</span>}
                {data.driver_dna.driving_style === 'Conservative' && <span className="px-3 py-1 bg-blue-500/30 text-blue-300 rounded-full text-xs">Safe</span>}
                {data.driver_dna.driving_style === 'Smooth & Fast' && <span className="px-3 py-1 bg-green-500/30 text-green-300 rounded-full text-xs">Optimal</span>}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-black/30 p-4 rounded hover:bg-black/40 transition-all cursor-pointer group">
                <p className="text-xs text-gray-400 group-hover:text-gray-300">Brake Aggression</p>
                <p className="text-3xl font-bold text-red-400 group-hover:scale-110 transition-transform">{data.driver_dna.brake_aggression_pct}%</p>
                <div className="w-full bg-gray-700 rounded-full h-1 mt-2">
                  <div className="bg-red-500 h-1 rounded-full transition-all duration-500" style={{width: `${data.driver_dna.brake_aggression_pct}%`}}></div>
                </div>
              </div>
              <div className="bg-black/30 p-4 rounded hover:bg-black/40 transition-all cursor-pointer group">
                <p className="text-xs text-gray-400 group-hover:text-gray-300">Throttle Smoothness</p>
                <p className="text-3xl font-bold text-green-400 group-hover:scale-110 transition-transform">{data.driver_dna.throttle_smoothness_pct}%</p>
                <div className="w-full bg-gray-700 rounded-full h-1 mt-2">
                  <div className="bg-green-500 h-1 rounded-full transition-all duration-500" style={{width: `${data.driver_dna.throttle_smoothness_pct}%`}}></div>
                </div>
              </div>
              <div className="bg-black/30 p-4 rounded hover:bg-black/40 transition-all cursor-pointer group">
                <p className="text-xs text-gray-400 group-hover:text-gray-300">Grip Utilization</p>
                <p className="text-3xl font-bold text-yellow-400 group-hover:scale-110 transition-transform">{data.driver_dna.avg_grip_utilization_pct}%</p>
                <div className="w-full bg-gray-700 rounded-full h-1 mt-2">
                  <div className="bg-yellow-500 h-1 rounded-full transition-all duration-500" style={{width: `${data.driver_dna.avg_grip_utilization_pct}%`}}></div>
                </div>
              </div>
              <div className="bg-black/30 p-4 rounded hover:bg-black/40 transition-all cursor-pointer group">
                <p className="text-xs text-gray-400 group-hover:text-gray-300">Speed Efficiency</p>
                <p className="text-3xl font-bold text-blue-400 group-hover:scale-110 transition-transform">{data.driver_dna.avg_speed_efficiency_pct}%</p>
                <div className="w-full bg-gray-700 rounded-full h-1 mt-2">
                  <div className="bg-blue-500 h-1 rounded-full transition-all duration-500" style={{width: `${data.driver_dna.avg_speed_efficiency_pct}%`}}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Grip Utilization - Traction Circle */}
      {data.grip_utilization && !data.grip_utilization.message && (
        <div className="bg-gray-900 p-6 rounded-lg">
          <h4 className="text-2xl font-bold mb-4">⭕ Traction Circle Analysis</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <div className="relative w-64 h-64 mx-auto">
                {/* Traction circle visualization */}
                <svg viewBox="0 0 200 200" className="w-full h-full">
                  {/* Outer circle (theoretical limit) */}
                  <circle cx="100" cy="100" r="90" fill="none" stroke="#374151" strokeWidth="2" />
                  <circle cx="100" cy="100" r="60" fill="none" stroke="#374151" strokeWidth="1" strokeDasharray="4" />
                  <circle cx="100" cy="100" r="30" fill="none" stroke="#374151" strokeWidth="1" strokeDasharray="4" />
                  
                  {/* Actual utilization circle */}
                  <circle 
                    cx="100" 
                    cy="100" 
                    r={90 * (data.grip_utilization.grip_efficiency_pct / 100)} 
                    fill="rgba(139, 92, 246, 0.3)" 
                    stroke="#8b5cf6" 
                    strokeWidth="3" 
                  />
                  
                  {/* Center point */}
                  <circle cx="100" cy="100" r="3" fill="#8b5cf6" />
                  
                  {/* Axes */}
                  <line x1="100" y1="10" x2="100" y2="190" stroke="#4b5563" strokeWidth="1" />
                  <line x1="10" y1="100" x2="190" y2="100" stroke="#4b5563" strokeWidth="1" />
                  
                  {/* Labels */}
                  <text x="100" y="20" textAnchor="middle" fill="#9ca3af" fontSize="10">Accel</text>
                  <text x="100" y="195" textAnchor="middle" fill="#9ca3af" fontSize="10">Brake</text>
                  <text x="15" y="105" textAnchor="start" fill="#9ca3af" fontSize="10">Left</text>
                  <text x="185" y="105" textAnchor="end" fill="#9ca3af" fontSize="10">Right</text>
                </svg>
                <p className="text-center mt-2 text-sm text-gray-400">
                  {data.grip_utilization.grip_efficiency_pct}% of theoretical limit
                </p>
              </div>
            </div>
            <div className="space-y-4">
              <div className="bg-gray-800 p-4 rounded">
                <p className="text-sm text-gray-400">Max Combined G-Force</p>
                <p className="text-3xl font-bold text-purple-400">{data.grip_utilization.max_combined_g}G</p>
                <p className="text-xs text-gray-500">Limit: {data.grip_utilization.theoretical_limit_g}G</p>
              </div>
              <div className="bg-gray-800 p-4 rounded">
                <p className="text-sm text-gray-400 mb-2">Time in Grip Zones</p>
                <div className="space-y-2">
                  <div>
                    <div className="flex justify-between text-xs mb-1">
                      <span>High Grip (&gt;0.8G)</span>
                      <span className="text-red-400">{data.grip_utilization.time_in_high_grip_pct}%</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div className="bg-red-500 h-2 rounded-full" style={{width: `${data.grip_utilization.time_in_high_grip_pct}%`}}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-xs mb-1">
                      <span>Mid Grip (0.4-0.8G)</span>
                      <span className="text-yellow-400">{data.grip_utilization.time_in_mid_grip_pct}%</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div className="bg-yellow-500 h-2 rounded-full" style={{width: `${data.grip_utilization.time_in_mid_grip_pct}%`}}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-xs mb-1">
                      <span>Low Grip (&lt;0.4G)</span>
                      <span className="text-blue-400">{data.grip_utilization.time_in_low_grip_pct}%</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div className="bg-blue-500 h-2 rounded-full" style={{width: `${data.grip_utilization.time_in_low_grip_pct}%`}}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Momentum Efficiency */}
      {data.momentum_efficiency && !data.momentum_efficiency.message && (
        <div className="bg-gray-900 p-6 rounded-lg">
          <h4 className="text-2xl font-bold mb-4">⚡ Momentum Management</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gradient-to-br from-green-900 to-emerald-900 p-6 rounded-lg border-l-4 border-green-400">
              <p className="text-sm text-gray-300">Momentum Efficiency Score</p>
              <p className="text-4xl font-bold text-green-300">{data.momentum_efficiency.momentum_efficiency_score}</p>
              <p className="text-sm text-gray-400 mt-2">{data.momentum_efficiency.rating}</p>
            </div>
            <div className="bg-gray-800 p-6 rounded-lg">
              <p className="text-sm text-gray-400">Avg Momentum Gain</p>
              <p className="text-3xl font-bold">{data.momentum_efficiency.avg_momentum_gain_pct}%</p>
              <p className="text-xs text-gray-500 mt-2">Exit vs Entry</p>
            </div>
            <div className="bg-gray-800 p-6 rounded-lg">
              <p className="text-sm text-gray-400">Avg Speed Efficiency</p>
              <p className="text-3xl font-bold">{data.momentum_efficiency.avg_speed_efficiency_pct}%</p>
              <p className="text-xs text-gray-500 mt-2">vs Theoretical Max</p>
            </div>
          </div>
        </div>
      )}

      {/* Corner Analysis with Interactive Cards */}
      {data.corner_analysis && data.corner_analysis.length > 0 && (
        <div className="bg-gray-900 p-6 rounded-lg">
          <h4 className="text-2xl font-bold mb-4 flex items-center gap-2">
            🏁 Corner-by-Corner Physics Analysis
            <span className="text-xs bg-blue-500/30 px-2 py-1 rounded">{data.corners_detected} detected</span>
          </h4>
          <p className="text-sm text-gray-400 mb-6">Showing top 5 corners with highest lateral G-forces</p>
          <div className="space-y-4">
            {data.corner_analysis.map((corner: any, idx: number) => (
              <div key={idx} className="bg-gradient-to-r from-gray-800 to-gray-900 p-5 rounded-lg border-l-4 border-blue-500 hover:border-purple-500 hover:shadow-xl transition-all duration-300 cursor-pointer group">
                <div className="flex justify-between items-center mb-3">
                  <span className="text-2xl font-bold text-blue-400">Corner #{idx + 1}</span>
                  <div className="flex gap-2">
                    {corner.speed_efficiency_pct > 90 && <span className="px-2 py-1 bg-green-500/30 text-green-300 rounded text-xs">Excellent</span>}
                    {corner.momentum_gain_pct > 50 && <span className="px-2 py-1 bg-purple-500/30 text-purple-300 rounded text-xs">High Momentum</span>}
                    {corner.max_lateral_g > 0.9 && <span className="px-2 py-1 bg-red-500/30 text-red-300 rounded text-xs">High G</span>}
                  </div>
                </div>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                  <div className="bg-black/30 p-3 rounded group-hover:bg-black/50 transition-all">
                    <p className="text-xs text-gray-400 mb-1">Speed Profile</p>
                    <div className="flex items-center gap-1 text-sm font-mono">
                      <span className="text-green-400">{corner.entry_speed_kmh}</span>
                      <span className="text-gray-500">→</span>
                      <span className="text-yellow-400">{corner.apex_speed_kmh}</span>
                      <span className="text-gray-500">→</span>
                      <span className="text-blue-400">{corner.exit_speed_kmh}</span>
                      <span className="text-xs text-gray-500">km/h</span>
                    </div>
                  </div>
                  <div className="bg-black/30 p-3 rounded group-hover:bg-black/50 transition-all">
                    <p className="text-xs text-gray-400 mb-1">Theoretical Max</p>
                    <p className="text-xl font-bold text-purple-400">{corner.theoretical_max_speed_kmh}</p>
                    <p className="text-xs text-gray-500">{corner.speed_efficiency_pct}% efficiency</p>
                  </div>
                  <div className="bg-black/30 p-3 rounded group-hover:bg-black/50 transition-all">
                    <p className="text-xs text-gray-400 mb-1">Lateral G-Force</p>
                    <p className="text-xl font-bold text-red-400">{corner.max_lateral_g}G</p>
                    <p className="text-xs text-gray-500">R={corner.corner_radius_m}m</p>
                  </div>
                  <div className="bg-black/30 p-3 rounded group-hover:bg-black/50 transition-all">
                    <p className="text-xs text-gray-400 mb-1">Momentum</p>
                    <p className="text-xl font-bold text-yellow-400">{corner.momentum_gain_pct > 0 ? '+' : ''}{corner.momentum_gain_pct}%</p>
                    <p className="text-xs text-gray-500">gain/loss</p>
                  </div>
                </div>
                
                <div className="grid grid-cols-3 gap-2 text-xs bg-black/20 p-3 rounded">
                  <div className="flex flex-col">
                    <span className="text-gray-400">Angular Momentum</span>
                    <span className="font-bold text-purple-300">{corner.angular_momentum} kg⋅m²/s</span>
                  </div>
                  <div className="flex flex-col">
                    <span className="text-gray-400">Yaw Rate</span>
                    <span className="font-bold text-blue-300">{corner.yaw_rate_rad_s} rad/s</span>
                  </div>
                  <div className="flex flex-col">
                    <span className="text-gray-400">Load Transfer</span>
                    <span className="font-bold text-red-300">{corner.lateral_load_transfer_n} N</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* AI Recommendations with Animation */}
      {data.recommendations && data.recommendations.length > 0 && (
        <div className="bg-gradient-to-r from-yellow-900 via-orange-900 to-red-900 p-6 rounded-lg border-2 border-yellow-500 shadow-2xl animate-pulse-slow">
          <h4 className="text-2xl font-bold mb-4 flex items-center gap-2">
            💡 AI-Powered Recommendations
            <span className="text-xs bg-yellow-500/30 px-2 py-1 rounded animate-bounce">Action Required</span>
          </h4>
          <div className="space-y-3">
            {data.recommendations.map((rec: string, idx: number) => (
              <div key={idx} className="bg-black/40 p-5 rounded-lg flex items-start gap-4 hover:bg-black/60 hover:scale-[1.02] transition-all duration-300 cursor-pointer border-l-4 border-transparent hover:border-yellow-400">
                <div className="flex-shrink-0 w-8 h-8 bg-yellow-500 rounded-full flex items-center justify-center font-bold text-black">
                  {idx + 1}
                </div>
                <p className="text-lg flex-1">{rec}</p>
                <div className="text-2xl">→</div>
              </div>
            ))}
          </div>
          <div className="mt-4 p-3 bg-black/30 rounded text-sm text-gray-300">
            <span className="font-bold">💡 Pro Tip:</span> Implementing these recommendations could improve lap times by 0.5-2 seconds
          </div>
        </div>
      )}

      {/* Physics Info Footer */}
      <div className="bg-gray-800 p-4 rounded-lg text-xs text-gray-400">
        <p className="font-bold mb-2">🔬 Physics Calculations Used:</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          <p>• V_max = √(μ × g × R) - Maximum cornering speed</p>
          <p>• L = I × ω - Angular momentum (yaw inertia)</p>
          <p>• ΔF = (m × a_y × h) / t - Lateral load transfer</p>
          <p>• a_total = √(a_x² + a_y²) - Combined acceleration (traction circle)</p>
        </div>
      </div>
    </div>
  )
}

export default AMICOSAnalysis
