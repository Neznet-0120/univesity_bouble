import React, { useEffect, useState } from 'react'
import api from '../lib/api'

export default function Profile(){
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(()=>{
    let mounted = true
    api.get('/profiles/me/').then(r=>{ if(mounted){ setProfile(r.data); setLoading(false) } }).catch(()=>setLoading(false))
    return ()=> mounted = false
  },[])

  if(loading) return <div>Загрузка профиля...</div>
  if(!profile) return <div className="text-muted">Профиль не найден</div>

  return (
    <div className="card">
      <div className="card-body">
        <h4>{profile.first_name} {profile.last_name}</h4>
        <div><strong>Username:</strong> {profile.username}</div>
        <div><strong>Role:</strong> {profile.role}</div>
        <div><strong>Group:</strong> {profile.group || '—'}</div>
      </div>
    </div>
  )
}
