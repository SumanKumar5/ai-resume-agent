import { useState, useEffect } from 'react'
import { getRuns, downloadPdf } from '../lib/api'
import { CheckCircle, XCircle, ChevronDown, ChevronUp, Download, Clock, Loader2 } from 'lucide-react'

export default function History() {
  const [runs, setRuns] = useState([])
  const [loading, setLoading] = useState(true)
  const [expanded, setExpanded] = useState(null)

  useEffect(() => {
    getRuns()
      .then((res) => setRuns(res.data))
      .finally(() => setLoading(false))
  }, [])

  const toggleExpand = (id) => setExpanded(expanded === id ? null : id)

  const statusBadge = (status) => {
    const styles = {
      completed: 'bg-green-900/50 text-green-400 border border-green-800',
      failed: 'bg-red-900/50 text-red-400 border border-red-800',
      running: 'bg-indigo-900/50 text-indigo-400 border border-indigo-800',
      pending: 'bg-gray-800 text-gray-400 border border-gray-700',
    }
    return (
      <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${styles[status] || styles.pending}`}>
        {status}
      </span>
    )
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="animate-spin text-indigo-400" size={32} />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Run History</h1>
        <p className="text-gray-400 mt-1">All past pipeline executions and their results.</p>
      </div>

      {runs.length === 0 ? (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-12 text-center">
          <Clock size={40} className="text-gray-700 mx-auto mb-4" />
          <p className="text-gray-500">No runs yet. Run the pipeline to see history here.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {runs.map((run) => (
            <div key={run.id} className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
              <div
                className="flex items-center justify-between px-6 py-4 cursor-pointer hover:bg-gray-800 transition-colors"
                onClick={() => toggleExpand(run.id)}
              >
                <div className="flex items-center gap-4">
                  <div>
                    <div className="flex items-center gap-3">
                      <span className="text-sm font-semibold text-white">Run #{run.id}</span>
                      {statusBadge(run.status)}
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(run.timestamp).toLocaleString()}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-6">
                  <div className="text-right">
                    <p className="text-sm font-medium text-white">{run.successful}/{run.total_jobs}</p>
                    <p className="text-xs text-gray-500">successful</p>
                  </div>
                  {expanded === run.id ? (
                    <ChevronUp size={16} className="text-gray-500" />
                  ) : (
                    <ChevronDown size={16} className="text-gray-500" />
                  )}
                </div>
              </div>

              {expanded === run.id && (
                <div className="border-t border-gray-800 px-6 py-4">
                  <div className="space-y-3">
                    {run.jobs.map((job) => (
                      <div key={job.id} className="flex items-center justify-between bg-gray-950 rounded-lg px-4 py-3">
                        <div className="flex items-center gap-3">
                          {job.status === 'success' ? (
                            <CheckCircle size={16} className="text-green-400" />
                          ) : (
                            <XCircle size={16} className="text-red-400" />
                          )}
                          <div>
                            <p className="text-sm font-medium text-white">{job.job_title}</p>
                            <p className="text-xs text-gray-500">{job.company}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-6">
                          {job.similarity_score && (
                            <div className="text-right">
                              <p className="text-xs text-gray-500">Similarity</p>
                              <p className="text-sm font-medium text-indigo-400">
                                {(job.similarity_score * 100).toFixed(0)}%
                              </p>
                            </div>
                          )}
                          {job.processing_time && (
                            <div className="text-right">
                              <p className="text-xs text-gray-500">Time</p>
                              <p className="text-sm font-medium text-gray-300">{job.processing_time}s</p>
                            </div>
                          )}
                          {job.pdf_path && (
                            <a
                              href={downloadPdf(job.id)}
                              target="_blank"
                              rel="noreferrer"
                              className="flex items-center gap-1.5 text-xs bg-indigo-900/50 hover:bg-indigo-800 text-indigo-300 px-3 py-1.5 rounded-lg transition-colors border border-indigo-800"
                              onClick={(e) => e.stopPropagation()}
                            >
                              <Download size={12} />
                              PDF
                            </a>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}