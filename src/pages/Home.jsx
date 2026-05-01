import { useState } from 'react'
import axios from 'axios'
import { Send } from 'lucide-react'
import { API_BASE } from '../config'

export default function Home() {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const analyzeMessage = async () => {
    if (!message.trim()) return
    
    setLoading(true)
    try {
      const response = await axios.post(`${API_BASE}/analyze-message`, {
        message: message,
        time: new Date().toISOString()
      })
      setResult(response.data)
    } catch {
      alert("Backend not running. Ask Person 1 to start the server.")
    }
    setLoading(false)
  }

  return (
    <div className="max-w-5xl mx-auto px-6 py-10">
      <h1 className="text-3xl font-bold text-center mb-8">Silent Safety Check</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left side - Message input */}
        <div>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message here..."
            rows={6}
            className="w-full bg-gray-900 border border-gray-700 rounded-xl p-4 text-white"
          />
          
          <button
            onClick={analyzeMessage}
            disabled={loading}
            className="w-full mt-4 bg-red-600 hover:bg-red-700 text-white font-bold py-3 rounded-xl"
          >
            {loading ? "Analyzing..." : <><Send size={16} /> Analyze Message</>}
          </button>
        </div>

        {/* Right side - Results */}
        <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
          {!result && !loading && (
            <p className="text-gray-500 text-center">Results will appear here</p>
          )}
          
          {result && (
            <div>
              <div className="text-center mb-4">
                <p className="text-4xl font-bold text-red-500">{result.final_score}</p>
                <p className="text-gray-400">Risk Score (0-100)</p>
              </div>
              
              <div className={`text-center p-3 rounded-lg ${
                result.risk_level === 'high' ? 'bg-red-900/30 text-red-400' :
                result.risk_level === 'medium' ? 'bg-yellow-900/30 text-yellow-400' :
                'bg-green-900/30 text-green-400'
              }`}>
                Risk Level: {result.risk_level.toUpperCase()}
              </div>
              
              {result.alert_triggered && (
                <div className="mt-3 text-center text-red-400">
                  ⚠️ Alert sent to your contacts!
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
