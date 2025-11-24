import { useEffect, useState } from 'react'
import axios from 'axios'

interface TrackSelectorProps {
  tracks: string[]
  selectedTrack: string
  selectedSession: string
  onTrackChange: (track: string) => void
  onSessionChange: (session: string) => void
}

const TrackSelector = ({
  tracks,
  selectedTrack,
  selectedSession,
  onTrackChange,
  onSessionChange
}: TrackSelectorProps) => {
  const [sessions, setSessions] = useState<string[]>([])

  useEffect(() => {
    if (selectedTrack) {
      loadSessions(selectedTrack)
    }
  }, [selectedTrack])

  const loadSessions = async (track: string) => {
    try {
      const response = await axios.get(`/api/analytics/track/${track}/sessions`)
      setSessions(response.data)
      if (response.data.length > 0) {
        onSessionChange(response.data[0])
      }
    } catch (error) {
      console.error('Failed to load sessions:', error)
    }
  }

  return (
    <div className="bg-gray-900 p-6 rounded-lg shadow-lg mb-6">
      <h2 className="text-2xl font-bold mb-4">Select Track & Session</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-2">Track</label>
          <select
            value={selectedTrack}
            onChange={(e) => onTrackChange(e.target.value)}
            className="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white"
          >
            {tracks.map(track => (
              <option key={track} value={track}>
                {track.replace(/_/g, ' ').toUpperCase()}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Session</label>
          <select
            value={selectedSession}
            onChange={(e) => onSessionChange(e.target.value)}
            className="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white"
            disabled={sessions.length === 0}
          >
            {sessions.map(session => (
              <option key={session} value={session}>
                {session}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  )
}

export default TrackSelector
