import { useState, useEffect } from 'react'

const AMICOSSimulator = () => {
  // Vehicle inputs
  const [mass, setMass] = useState(1270) // kg
  const [power, setPower] = useState(228) // HP
  const [tireTemp, setTireTemp] = useState(85) // °C
  const [tirePressure, setTirePressure] = useState(32) // PSI
  
  // Track inputs
  const [cornerRadius, setCornerRadius] = useState(50) // meters
  const [trackGrip, setTrackGrip] = useState(1.1) // coefficient
  const [elevation, setElevation] = useState(0) // degrees
  
  // Live telemetry inputs
  const [entrySpeed, setEntrySpeed] = useState(120) // km/h
  const [brakeForce, setBrakeForce] = useState(80) // %
  const [steeringAngle, setSteeringAngle] = useState(45) // degrees
  const [throttle, setThrottle] = useState(60) // %
  
  // Calculated outputs
  const [outputs, setOutputs] = useState<any>({})
  
  // Real-time calculation
  useEffect(() => {
    calculatePhysics()
  }, [mass, power, tireTemp, tirePressure, cornerRadius, trackGrip, elevation, entrySpeed, brakeForce, steeringAngle, throttle])
  
  const calculatePhysics = () => {
    const g = 9.81 // m/s²
    
    // Tire grip adjustment based on temp and pressure
    const optimalTemp = 85
    const optimalPressure = 32
    const tempFactor = 1 - Math.abs(tireTemp - optimalTemp) / 100
    const pressureFactor = 1 - Math.abs(tirePressure - optimalPressure) / 50
    const effectiveGrip = trackGrip * tempFactor * pressureFactor
    
    // Maximum cornering speed: V_max = sqrt(μ × g × R)
    const maxCorneringSpeed = Math.sqrt(effectiveGrip * g * cornerRadius) * 3.6 // km/h
    
    // Lateral G-force: a = v² / r
    const entrySpeedMs = entrySpeed / 3.6
    const lateralG = (entrySpeedMs * entrySpeedMs) / (cornerRadius * g)
    
    // Braking G-force (simplified): proportional to brake force
    const brakingG = (brakeForce / 100) * effectiveGrip * 1.2
    
    // Combined G-force (traction circle)
    const combinedG = Math.sqrt(lateralG * lateralG + brakingG * brakingG)
    
    // Yaw rate: ω = v / r
    const yawRate = entrySpeedMs / cornerRadius
    
    // Angular momentum: L = I × ω (simplified)
    const momentOfInertia = mass * 1.5 // simplified
    const angularMomentum = momentOfInertia * yawRate
    
    // Lateral load transfer: ΔF = (m × a_y × h) / t
    const cgHeight = 0.48 // meters
    const trackWidth = 1.52 // meters
    const lateralLoadTransfer = (mass * lateralG * g * cgHeight) / trackWidth
    
    // Apex speed prediction (simplified)
    const apexSpeed = Math.min(entrySpeed * 0.7, maxCorneringSpeed)
    
    // Exit speed prediction
    const exitSpeed = apexSpeed + (throttle / 100) * 30
    
    // Time to apex (simplified)
    const distanceToApex = cornerRadius * (steeringAngle / 90) * Math.PI / 2
    const timeToApex = distanceToApex / entrySpeedMs
    
    // Grip utilization
    const gripUtilization = (combinedG / effectiveGrip) * 100
    
    // Safety margin
    const safetyMargin = Math.max(0, 100 - gripUtilization)
    
    // Optimal recommendation
    let recommendation = ""
    if (gripUtilization > 95) {
      recommendation = "⚠️ DANGER: Exceeding grip limits! Reduce speed or brake force"
    } else if (gripUtilization > 85) {
      recommendation = "🔥 Pushing hard! Excellent grip utilization"
    } else if (gripUtilization > 70) {
      recommendation = "✅ Good balance between speed and safety"
    } else {
      recommendation = "💡 Can push harder! Increase entry speed or brake later"
    }
    
    setOutputs({
      maxCorneringSpeed: maxCorneringSpeed.toFixed(1),
      lateralG: lateralG.toFixed(2),
      brakingG: brakingG.toFixed(2),
      combinedG: combinedG.toFixed(2),
      yawRate: yawRate.toFixed(3),
      angularMomentum: angularMomentum.toFixed(1),
      lateralLoadTransfer: lateralLoadTransfer.toFixed(1),
      apexSpeed: apexSpeed.toFixed(1),
      exitSpeed: exitSpeed.toFixed(1),
      timeToApex: timeToApex.toFixed(2),
      gripUtilization: gripUtilization.toFixed(1),
      safetyMargin: safetyMargin.toFixed(1),
      effectiveGrip: effectiveGrip.toFixed(2),
      recommendation
    })
  }
  
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-900 via-emerald-900 to-teal-900 p-8 rounded-lg border-2 border-green-500 shadow-2xl">
        <h3 className="text-4xl font-bold mb-2 bg-gradient-to-r from-green-300 to-teal-300 bg-clip-text text-transparent">
          🎮 Real-Time AMICOS Simulator
        </h3>
        <p className="text-sm text-gray-300">Interactive Physics Engine • Adjust inputs to see instant calculations</p>
        <p className="text-xs text-gray-400 mt-1">Perfect for race strategy planning and driver training</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Panel */}
        <div className="space-y-6">
          {/* Vehicle Setup */}
          <div className="bg-gray-900 p-6 rounded-lg border-l-4 border-blue-500">
            <h4 className="text-xl font-bold mb-4 flex items-center gap-2">
              🏎️ Vehicle Setup
              <span className="text-xs bg-blue-500/30 px-2 py-1 rounded">GR86 Cup</span>
            </h4>
            
            <div className="space-y-4">
              <div>
                <label className="text-sm text-gray-400 flex justify-between">
                  <span>Mass (kg)</span>
                  <span className="text-white font-bold">{mass} kg</span>
                </label>
                <input
                  type="range"
                  min="1200"
                  max="1350"
                  value={mass}
                  onChange={(e) => setMass(Number(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
                />
              </div>
              
              <div>
                <label className="text-sm text-gray-400 flex justify-between">
                  <span>Power (HP)</span>
                  <span className="text-white font-bold">{power} HP</span>
                </label>
                <input
                  type="range"
                  min="200"
                  max="250"
                  value={power}
                  onChange={(e) => setPower(Number(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
                />
              </div>
              
              <div>
                <label className="text-sm text-gray-400 flex justify-between">
                  <span>Tire Temperature (°C)</span>
                  <span className={`font-bold ${Math.abs(tireTemp - 85) < 10 ? 'text-green-400' : 'text-yellow-400'}`}>
                    {tireTemp}°C
                  </span>
                </label>
                <input
                  type="range"
                  min="60"
                  max="110"
                  value={tireTemp}
                  onChange={(e) => setTireTemp(Number(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-green-500"
                />
                <p className="text-xs text-gray-500 mt-1">Optimal: 85°C</p>
              </div>
              
              <div>
                <label className="text-sm text-gray-400 flex justify-between">
                  <span>Tire Pressure (PSI)</span>
                  <span className={`font-bold ${Math.abs(tirePressure - 32) < 3 ? 'text-green-400' : 'text-yellow-400'}`}>
                    {tirePressure} PSI
                  </span>
                </label>
                <input
                  type="range"
                  min="28"
                  max="36"
                  value={tirePressure}
                  onChange={(e) => setTirePressure(Number(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-green-500"
                />
                <p className="text-xs text-gray-500 mt-1">Optimal: 32 PSI</p>
              </div>
            </div>
          </div>

          {/* Track Conditions */}
          <div className="bg-gray-900 p-6 rounded-lg border-l-4 border-purple-500">
            <h4 className="text-xl font-bold mb-4">🏁 Track Conditions</h4>
            
            <div className="space-y-4">
              <div>
                <label className="text-sm text-gray-400 flex justify-between">
                  <span>Corner Radius (m)</span>
                  <span className="text-white font-bold">{cornerRadius}m</span>
                </label>
                <input
                  type="range"
                  min="20"
                  max="200"
                  value={cornerRadius}
                  onChange={(e) => setCornerRadius(Number(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
                />
                <p className="text-xs text-gray-500 mt-1">Tight: 20-50m | Medium: 50-100m | Fast: 100-200m</p>
              </div>
              
              <div>
                <label className="text-sm text-gray-400 flex justify-between">
                  <span>Track Grip (μ)</span>
                  <span className="text-white font-bold">{trackGrip.toFixed(2)}</span>
                </label>
                <input
                  type="range"
                  min="0.7"
                  max="1.3"
                  step="0.05"
                  value={trackGrip}
                  onChange={(e) => setTrackGrip(Number(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
                />
                <p className="text-xs text-gray-500 mt-1">Wet: 0.7 | Dry: 1.1 | Ideal: 1.3</p>
              </div>
              
              <div>
                <label className="text-sm text-gray-400 flex justify-between">
                  <span>Elevation Change (°)</span>
                  <span className="text-white font-bold">{elevation > 0 ? '+' : ''}{elevation}°</span>
                </label>
                <input
                  type="range"
                  min="-10"
                  max="10"
                  value={elevation}
                  onChange={(e) => setElevation(Number(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
                />
                <p className="text-xs text-gray-500 mt-1">Uphill: + | Downhill: -</p>
              </div>
            </div>
          </div>

          {/* Live Telemetry */}
          <div className="bg-gray-900 p-6 rounded-lg border-l-4 border-red-500">
            <h4 className="text-xl font-bold mb-4 flex items-center gap-2">
              📡 Live Telemetry
              <span className="text-xs bg-red-500/30 px-2 py-1 rounded animate-pulse">LIVE</span>
            </h4>
            
            <div className="space-y-4">
              <div>
                <label className="text-sm text-gray-400 flex justify-between">
                  <span>Entry Speed (km/h)</span>
                  <span className="text-white font-bold">{entrySpeed} km/h</span>
                </label>
                <input
                  type="range"
                  min="50"
                  max="200"
                  value={entrySpeed}
                  onChange={(e) => setEntrySpeed(Number(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-red-500"
                />
              </div>
              
              <div>
                <label className="text-sm text-gray-400 flex justify-between">
                  <span>Brake Force (%)</span>
                  <span className="text-white font-bold">{brakeForce}%</span>
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={brakeForce}
                  onChange={(e) => setBrakeForce(Number(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-red-500"
                />
              </div>
              
              <div>
                <label className="text-sm text-gray-400 flex justify-between">
                  <span>Steering Angle (°)</span>
                  <span className="text-white font-bold">{steeringAngle}°</span>
                </label>
                <input
                  type="range"
                  min="0"
                  max="90"
                  value={steeringAngle}
                  onChange={(e) => setSteeringAngle(Number(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-yellow-500"
                />
              </div>
              
              <div>
                <label className="text-sm text-gray-400 flex justify-between">
                  <span>Throttle (%)</span>
                  <span className="text-white font-bold">{throttle}%</span>
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={throttle}
                  onChange={(e) => setThrottle(Number(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-green-500"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Output Panel */}
        <div className="space-y-6">
          {/* Real-Time Calculations */}
          <div className="bg-gradient-to-br from-purple-900 to-pink-900 p-6 rounded-lg border-2 border-purple-500">
            <h4 className="text-xl font-bold mb-4">⚡ Real-Time Physics Output</h4>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-black/30 p-4 rounded">
                <p className="text-xs text-gray-400">Max Corner Speed</p>
                <p className="text-3xl font-bold text-purple-300">{outputs.maxCorneringSpeed}</p>
                <p className="text-xs text-gray-500">km/h</p>
              </div>
              
              <div className="bg-black/30 p-4 rounded">
                <p className="text-xs text-gray-400">Lateral G-Force</p>
                <p className="text-3xl font-bold text-red-300">{outputs.lateralG}</p>
                <p className="text-xs text-gray-500">G</p>
              </div>
              
              <div className="bg-black/30 p-4 rounded">
                <p className="text-xs text-gray-400">Braking G-Force</p>
                <p className="text-3xl font-bold text-orange-300">{outputs.brakingG}</p>
                <p className="text-xs text-gray-500">G</p>
              </div>
              
              <div className="bg-black/30 p-4 rounded">
                <p className="text-xs text-gray-400">Combined G</p>
                <p className="text-3xl font-bold text-yellow-300">{outputs.combinedG}</p>
                <p className="text-xs text-gray-500">G</p>
              </div>
            </div>
          </div>

          {/* Grip Utilization */}
          <div className="bg-gray-900 p-6 rounded-lg">
            <h4 className="text-xl font-bold mb-4">🎯 Grip Utilization</h4>
            
            <div className="mb-4">
              <div className="flex justify-between text-sm mb-2">
                <span>Current Utilization</span>
                <span className={`font-bold ${
                  Number(outputs.gripUtilization) > 95 ? 'text-red-400' :
                  Number(outputs.gripUtilization) > 85 ? 'text-yellow-400' :
                  'text-green-400'
                }`}>
                  {outputs.gripUtilization}%
                </span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-6">
                <div 
                  className={`h-6 rounded-full transition-all duration-300 ${
                    Number(outputs.gripUtilization) > 95 ? 'bg-red-500' :
                    Number(outputs.gripUtilization) > 85 ? 'bg-yellow-500' :
                    'bg-green-500'
                  }`}
                  style={{width: `${Math.min(Number(outputs.gripUtilization), 100)}%`}}
                ></div>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-800 p-3 rounded">
                <p className="text-xs text-gray-400">Safety Margin</p>
                <p className="text-2xl font-bold text-green-400">{outputs.safetyMargin}%</p>
              </div>
              <div className="bg-gray-800 p-3 rounded">
                <p className="text-xs text-gray-400">Effective Grip</p>
                <p className="text-2xl font-bold text-blue-400">{outputs.effectiveGrip}</p>
              </div>
            </div>
          </div>

          {/* Speed Profile */}
          <div className="bg-gray-900 p-6 rounded-lg">
            <h4 className="text-xl font-bold mb-4">🏎️ Speed Profile</h4>
            
            <div className="flex items-center justify-between mb-4">
              <div className="text-center">
                <p className="text-xs text-gray-400">Entry</p>
                <p className="text-3xl font-bold text-green-400">{entrySpeed}</p>
                <p className="text-xs text-gray-500">km/h</p>
              </div>
              <div className="text-4xl text-gray-600">→</div>
              <div className="text-center">
                <p className="text-xs text-gray-400">Apex</p>
                <p className="text-3xl font-bold text-yellow-400">{outputs.apexSpeed}</p>
                <p className="text-xs text-gray-500">km/h</p>
              </div>
              <div className="text-4xl text-gray-600">→</div>
              <div className="text-center">
                <p className="text-xs text-gray-400">Exit</p>
                <p className="text-3xl font-bold text-blue-400">{outputs.exitSpeed}</p>
                <p className="text-xs text-gray-500">km/h</p>
              </div>
            </div>
            
            <div className="bg-gray-800 p-3 rounded">
              <p className="text-xs text-gray-400">Time to Apex</p>
              <p className="text-2xl font-bold">{outputs.timeToApex}s</p>
            </div>
          </div>

          {/* Advanced Physics */}
          <div className="bg-gray-900 p-6 rounded-lg">
            <h4 className="text-xl font-bold mb-4">🔬 Advanced Physics</h4>
            
            <div className="space-y-3 text-sm">
              <div className="flex justify-between bg-gray-800 p-3 rounded">
                <span className="text-gray-400">Angular Momentum</span>
                <span className="font-bold text-purple-300">{outputs.angularMomentum} kg⋅m²/s</span>
              </div>
              <div className="flex justify-between bg-gray-800 p-3 rounded">
                <span className="text-gray-400">Yaw Rate</span>
                <span className="font-bold text-blue-300">{outputs.yawRate} rad/s</span>
              </div>
              <div className="flex justify-between bg-gray-800 p-3 rounded">
                <span className="text-gray-400">Lateral Load Transfer</span>
                <span className="font-bold text-red-300">{outputs.lateralLoadTransfer} N</span>
              </div>
            </div>
          </div>

          {/* AI Recommendation */}
          <div className={`p-6 rounded-lg border-2 ${
            Number(outputs.gripUtilization) > 95 ? 'bg-red-900 border-red-500' :
            Number(outputs.gripUtilization) > 85 ? 'bg-yellow-900 border-yellow-500' :
            'bg-green-900 border-green-500'
          }`}>
            <h4 className="text-xl font-bold mb-3">💡 AI Recommendation</h4>
            <p className="text-lg">{outputs.recommendation}</p>
          </div>
        </div>
      </div>

      {/* Physics Formulas */}
      <div className="bg-gray-800 p-4 rounded-lg text-xs text-gray-400">
        <p className="font-bold mb-2">🔬 Physics Calculations Used:</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          <p>• V_max = √(μ × g × R) - Maximum cornering speed</p>
          <p>• a_lateral = v² / (R × g) - Lateral acceleration</p>
          <p>• L = I × ω - Angular momentum</p>
          <p>• ΔF = (m × a_y × h) / t - Lateral load transfer</p>
        </div>
      </div>
    </div>
  )
}

export default AMICOSSimulator
