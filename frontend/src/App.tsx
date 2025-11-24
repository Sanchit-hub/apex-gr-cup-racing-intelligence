import { useState, useEffect } from 'react'
import axios from 'axios'
import Dashboard from './components/Dashboard'
import TrackSelector from './components/TrackSelector'

const API_BASE = '/api'

function App() {
  const [tracks, setTracks] = useState<string[]>([])
  const [selectedTrack, setSelectedTrack] = useState<string>('')
  const [selectedSession, setSelectedSession] = useState<string>('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadTracks()
  }, [])

  const loadTracks = async () => {
    try {
      const response = await axios.get(`${API_BASE}/analytics/tracks`)
      setTracks(response.data)
      if (response.data.length > 0) {
        setSelectedTrack(response.data[0])
      }
    } catch (error) {
      console.error('Failed to load tracks:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-2xl">Loading GR Cup Data...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gr-black">
      <header className="bg-gr-red text-white p-6 shadow-lg">
        <h1 className="text-4xl font-bold">🏁 GR Cup Racing Intelligence</h1>
        <p className="text-sm mt-2 opacity-90">Real-Time Analytics & Strategy Engine</p>
      </header>

      <main className="container mx-auto p-6">
        {tracks.length === 0 ? (
          <div className="bg-yellow-900 border border-yellow-600 text-yellow-100 p-6 rounded-lg">
            <h2 className="text-xl font-bold mb-2">⚠️ No Data Found</h2>
            <p>Please extract race data first:</p>
            <code className="block mt-2 bg-black p-2 rounded">python scripts/extract_data.py</code>
          </div>
        ) : (
          <>
            <TrackSelector
              tracks={tracks}
              selectedTrack={selectedTrack}
              selectedSession={selectedSession}
              onTrackChange={setSelectedTrack}
              onSessionChange={setSelectedSession}
            />
            
            {selectedTrack && selectedSession && (
              <Dashboard track={selectedTrack} session={selectedSession} />
            )}
          </>
        )}
      </main>

      <footer className="bg-gr-black border-t border-gray-800 p-4 text-center text-gray-500 mt-12">
        <p>Toyota GR Cup Hackathon 2025 | Built with React + FastAPI</p>
      </footer>
    </div>
  )
}

export default App
