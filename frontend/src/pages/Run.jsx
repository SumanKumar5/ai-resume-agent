import { useState, useRef, useEffect } from 'react'
import { Upload, Play, CheckCircle, XCircle, Loader2, FileText, File } from 'lucide-react'
import { runPipeline } from '../lib/api'

export default function Run() {
  const [files, setFiles] = useState({ excel: null, json: null, resume: null })
  const [receiverEmail, setReceiverEmail] = useState('')
  const [taskId, setTaskId] = useState(null)
  const [logs, setLogs] = useState([])
  const [status, setStatus] = useState('idle')
  const [result, setResult] = useState(null)
  const wsRef = useRef(null)
  const logsEndRef = useRef(null)

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [logs])

  useEffect(() => {
    if (!taskId) return

    const ws = new WebSocket(`ws://localhost:8000/api/ws/${taskId}`)
    wsRef.current = ws

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setLogs((prev) => [...prev, { message: data.log, level: data.level || 'info' }])
      if (data.done) {
        setStatus(data.result?.successful > 0 ? 'success' : 'error')
        setResult(data.result)
        ws.close()
      }
    }

    ws.onerror = () => {
      setLogs((prev) => [...prev, { message: 'WebSocket connection error.', level: 'error' }])
      setStatus('error')
    }

    return () => ws.close()
  }, [taskId])

  const handleFileChange = (key, file) => {
    setFiles((prev) => ({ ...prev, [key]: file }))
  }

  const handleRun = async () => {
    setLogs([])
    setStatus('running')
    setResult(null)

    const formData = new FormData()
    if (files.excel) formData.append('excel_file', files.excel)
    if (files.json) formData.append('json_file', files.json)
    if (files.resume) formData.append('resume_file', files.resume)
    if (receiverEmail) formData.append('receiver_email', receiverEmail)

    try {
      const res = await runPipeline(formData)
      setTaskId(res.data.task_id)
      setLogs([{ message: `Pipeline started. Task ID: ${res.data.task_id}`, level: 'info' }])
    } catch (err) {
      setLogs([{ message: `Failed to start pipeline: ${err.message}`, level: 'error' }])
      setStatus('error')
    }
  }

  const logColors = {
    info: 'text-gray-300',
    warning: 'text-yellow-400',
    error: 'text-red-400',
    success: 'text-green-400',
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Run Pipeline</h1>
        <p className="text-gray-400 mt-1">Upload your files or use the defaults already configured.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-900 rounded-xl border border-gray-800 p-6 space-y-5">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Input Files</h2>

          {[
            { key: 'excel', label: 'Job Links Excel', accept: '.xlsx', icon: FileText },
            { key: 'json', label: 'Jobs JSON', accept: '.json', icon: File },
            { key: 'resume', label: 'Candidate Resume', accept: '.docx,.pdf', icon: FileText },
          ].map(({ key, label, accept, icon: Icon }) => (
            <div key={key}>
              <label className="block text-sm text-gray-400 mb-2">{label}</label>
              <label className="flex items-center gap-3 border border-dashed border-gray-700 rounded-lg px-4 py-3 cursor-pointer hover:border-indigo-500 hover:bg-gray-800 transition-colors">
                <Icon size={16} className="text-gray-500" />
                <span className="text-sm text-gray-400 truncate">
                  {files[key] ? files[key].name : `Upload ${label} (optional — uses default if empty)`}
                </span>
                <input
                  type="file"
                  accept={accept}
                  className="hidden"
                  onChange={(e) => handleFileChange(key, e.target.files[0])}
                />
              </label>
            </div>
          ))}

          <div>
            <label className="block text-sm text-gray-400 mb-2">Receiver Email (optional)</label>
            <input
              type="email"
              value={receiverEmail}
              onChange={(e) => setReceiverEmail(e.target.value)}
              placeholder="Uses default from .env if empty"
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2.5 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <button
            onClick={handleRun}
            disabled={status === 'running'}
            className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-indigo-900 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-lg transition-colors"
          >
            {status === 'running' ? (
              <>
                <Loader2 size={16} className="animate-spin" />
                Pipeline Running...
              </>
            ) : (
              <>
                <Play size={16} />
                Run Pipeline
              </>
            )}
          </button>

          {result && (
            <div className={`rounded-lg p-4 flex items-center gap-3 ${status === 'success' ? 'bg-green-900/30 border border-green-800' : 'bg-red-900/30 border border-red-800'}`}>
              {status === 'success' ? (
                <CheckCircle size={18} className="text-green-400" />
              ) : (
                <XCircle size={18} className="text-red-400" />
              )}
              <span className="text-sm font-medium">
                {result.successful}/{result.successful + result.failed} resumes sent successfully
              </span>
            </div>
          )}
        </div>

        <div className="bg-gray-900 rounded-xl border border-gray-800 p-6 flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Live Logs</h2>
            {status === 'running' && (
              <span className="flex items-center gap-1.5 text-xs text-indigo-400">
                <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse" />
                Live
              </span>
            )}
          </div>

          <div className="flex-1 bg-gray-950 rounded-lg p-4 font-mono text-xs overflow-y-auto min-h-80 max-h-96 space-y-1">
            {logs.length === 0 ? (
              <p className="text-gray-600">Waiting for pipeline to start...</p>
            ) : (
              logs.map((log, i) => (
                <div key={i} className={`${logColors[log.level] || 'text-gray-300'} leading-relaxed`}>
                  <span className="text-gray-600 mr-2">›</span>
                  {log.message}
                </div>
              ))
            )}
            <div ref={logsEndRef} />
          </div>
        </div>
      </div>
    </div>
  )
}