import { Link } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="border-b border-gray-800 bg-black px-6 py-4">
      <div className="max-w-5xl mx-auto flex justify-between items-center">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-red-600 rounded-full"></div>
          <span className="font-bold text-lg">SilentSOS</span>
        </div>
        <div className="flex gap-4">
          <Link to="/" className="text-gray-400 hover:text-white">Chat</Link>
          <Link to="/contacts" className="text-gray-400 hover:text-white">Contacts</Link>
          <Link to="/dashboard" className="text-gray-400 hover:text-white">Dashboard</Link>
          <Link to="/how-it-works" className="text-gray-400 hover:text-white">How It Works</Link>
        </div>
      </div>
    </nav>
  )
}
