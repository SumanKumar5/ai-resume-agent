import { Link, useLocation } from 'react-router-dom'
import { Sparkles, History, BarChart3 } from 'lucide-react'

export default function Navbar() {
  const location = useLocation()

  const links = [
    { to: '/', label: 'Run Pipeline', icon: Sparkles },
    { to: '/history', label: 'History', icon: History },
    { to: '/analytics', label: 'Analytics', icon: BarChart3 },
  ]

  return (
    <nav className="border-b border-gray-800 bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center">
            <Sparkles size={16} className="text-white" />
          </div>
          <span className="font-bold text-lg text-white">AI Resume Agent</span>
          <span className="text-xs bg-indigo-900 text-indigo-300 px-2 py-0.5 rounded-full">v3.0</span>
        </div>
        <div className="flex items-center gap-1">
          {links.map(({ to, label, icon: Icon }) => (
            <Link
              key={to}
              to={to}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors
                ${location.pathname === to
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-400 hover:text-white hover:bg-gray-800'
                }`}
            >
              <Icon size={15} />
              {label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  )
}