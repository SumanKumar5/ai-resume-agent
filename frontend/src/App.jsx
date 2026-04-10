import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Run from './pages/Run'
import History from './pages/History'
import Analytics from './pages/Analytics'

export default function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Run />} />
          <Route path="/history" element={<History />} />
          <Route path="/analytics" element={<Analytics />} />
        </Routes>
      </main>
    </div>
  )
}