import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './components/Login'
import Dashboard from './components/Dashboard'
import News from './components/News'
import Schedule from './components/Schedule'
import Profile from './components/Profile'
import Navbar from './components/Navbar'
import { getToken } from './lib/auth'

function Protected({ children }){
  const token = getToken()
  if(!token) return <Navigate to="/login" replace />
  return children
}

export default function App(){
  return (
    <div>
      <Navbar />
      <div className="container mt-4">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Protected><Dashboard/></Protected>} />
          <Route path="/news" element={<Protected><News/></Protected>} />
          <Route path="/schedule" element={<Protected><Schedule/></Protected>} />
          <Route path="/profile" element={<Protected><Profile/></Protected>} />
        </Routes>
      </div>
    </div>
  )
}
