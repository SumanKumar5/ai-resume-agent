import { useState, useEffect } from 'react'
import { getAnalytics } from '../lib/api'
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import { Loader2, TrendingUp, CheckCircle, Clock, Layers } from 'lucide-react'

const COLORS = ['#6366f1', '#10b981', '#f59e0b', '#ef4444']

export default function Analytics() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getAnalytics()
      .then((res) => setData(res.data))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="animate-spin text-indigo-400" size={32} />
      </div>
    )
  }

  const { summary, role_stats, email_stats, runs_over_time } = data

  const emailData = [
    { name: 'Sent', value: email_stats.sent },
    { name: 'Failed', value: email_stats.failed },
  ]

  const statCards = [
    { label: 'Total Runs', value: summary.total_runs, icon: Layers, color: 'text-indigo-400' },
    { label: 'Total Jobs', value: summary.total_jobs, icon: TrendingUp, color: 'text-blue-400' },
    { label: 'Successful', value: summary.total_successful, icon: CheckCircle, color: 'text-green-400' },
    { label: 'Avg Processing Time', value: `${summary.avg_processing_time}s`, icon: Clock, color: 'text-yellow-400' },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Analytics</h1>
        <p className="text-gray-400 mt-1">Pipeline performance metrics and insights.</p>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map(({ label, value, icon: Icon, color }) => (
          <div key={label} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <div className="flex items-center justify-between mb-3">
              <p className="text-xs text-gray-500 uppercase tracking-wider">{label}</p>
              <Icon size={16} className={color} />
            </div>
            <p className="text-2xl font-bold text-white">{value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-6">
            Avg Similarity Score by Role
          </h2>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={role_stats} layout="vertical">
              <XAxis type="number" domain={[0, 1]} tick={{ fill: '#6b7280', fontSize: 11 }} />
              <YAxis type="category" dataKey="job_title" tick={{ fill: '#9ca3af', fontSize: 11 }} width={140} />
              <Tooltip
                contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px' }}
                labelStyle={{ color: '#f3f4f6' }}
                itemStyle={{ color: '#a5b4fc' }}
              />
              <Bar dataKey="avg_similarity" fill="#6366f1" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-6">
            Email Delivery Status
          </h2>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie
                data={emailData}
                cx="50%"
                cy="50%"
                innerRadius={70}
                outerRadius={110}
                paddingAngle={4}
                dataKey="value"
              >
                {emailData.map((_, index) => (
                  <Cell key={index} fill={COLORS[index]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px' }}
                itemStyle={{ color: '#a5b4fc' }}
              />
              <Legend formatter={(value) => <span style={{ color: '#9ca3af', fontSize: 12 }}>{value}</span>} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 lg:col-span-2">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-6">
            Success Rate Over Time
          </h2>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={runs_over_time}>
              <XAxis
                dataKey="timestamp"
                tick={{ fill: '#6b7280', fontSize: 11 }}
                tickFormatter={(v) => new Date(v).toLocaleDateString()}
              />
              <YAxis tick={{ fill: '#6b7280', fontSize: 11 }} />
              <Tooltip
                contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px' }}
                labelStyle={{ color: '#f3f4f6' }}
                itemStyle={{ color: '#a5b4fc' }}
                labelFormatter={(v) => new Date(v).toLocaleString()}
              />
              <Line type="monotone" dataKey="successful" stroke="#10b981" strokeWidth={2} dot={{ fill: '#10b981' }} name="Successful" />
              <Line type="monotone" dataKey="failed" stroke="#ef4444" strokeWidth={2} dot={{ fill: '#ef4444' }} name="Failed" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}