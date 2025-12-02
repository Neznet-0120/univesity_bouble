import React, { useEffect, useState } from 'react'
import api from '../lib/api'

export default function News({ compact=false }){
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(()=>{
    let mounted = true
    api.get('/news/').then(r=>{ if(mounted){ setItems(r.data); setLoading(false) } }).catch(()=>setLoading(false))
    return ()=> mounted = false
  },[])

  if(loading) return <div>Загрузка новостей...</div>
  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-2">
        <h4>Новости</h4>
        {!compact && <a className="btn btn-sm btn-outline-primary" href="/news">Все</a>}
      </div>
      {items.length===0 && <div className="text-muted">Нет новостей</div>}
      {items.slice(0, compact?5:100).map(n=> (
        <div key={n.id} className="card mb-2">
          <div className="card-body">
            <h5 className="card-title">{n.title}</h5>
            <p className="card-text text-truncate">{n.content}</p>
            <div className="text-muted small">Автор: {n.author_name || n.author || '—'}</div>
          </div>
        </div>
      ))}
    </div>
  )
}
