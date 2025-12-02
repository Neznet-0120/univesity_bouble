import React, { useEffect, useState } from 'react'
import api from '../lib/api'

const DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

export default function Schedule({ compact=false }){
  const [lessons, setLessons] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(()=>{
    let mounted = true
    api.get('/lessons/').then(r=>{ if(mounted){ setLessons(r.data); setLoading(false) } }).catch(()=>setLoading(false))
    return ()=> mounted = false
  },[])

  if(loading) return <div>Загрузка расписания...</div>

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-2">
        <h4>Расписание</h4>
        {!compact && <a className="btn btn-sm btn-outline-primary" href="/schedule">Полное</a>}
      </div>
      {lessons.length===0 && <div className="text-muted">Нет уроков</div>}
      {lessons.slice(0, compact?6:100).map(l=> (
        <div key={l.id} className="card mb-2">
          <div className="card-body">
            <div className="d-flex justify-content-between">
              <div>
                <strong>{l.subject_name || l.subject || l.title || 'Урок'}</strong>
                <div className="text-muted small">{l.day} • {l.time_start} — {l.time_end}</div>
              </div>
              <div className="text-end small">{l.classroom_name || l.classroom || ''}</div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
