import { useState, useEffect } from 'react'
import axios from 'axios'
import { API_BASE } from '../config'

export default function Dashboard() {
  const [alerts, setAlerts] = useState([])

  useEffect(() => {
    axios.get(`${API_BASE}/alerts`).then(res => setAlerts(res.data))
  }, [])

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <h2 className="text-2xl font-bold mb-6">Alert History</h2>
      
      {alerts.map(alert => (
        <div key={alert.id} className="bg-gray-900 rounded-xl p-4 mb-4">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-gray-400 text-sm">{alert.message_text}</p>
              <p className="text-xs text-gray-600 mt-1">
                {new Date(alert.created_at).toLocaleString()}
              </p>
            </div>
            <div className={`px-3 py-1 rounded-lg text-sm ${
              alert.risk_level === 'high' ? 'bg-red-900 text-red-400' :
              alert.risk_level === 'medium' ? 'bg-yellow-900 text-yellow-400' :
              'bg-green-900 text-green-400'
            }`}>
              Score: {alert.final_score}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}