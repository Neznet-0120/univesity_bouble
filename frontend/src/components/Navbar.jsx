import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { getToken, clearToken } from '../lib/auth'
import api from '../lib/api'

export default function Navbar(){
  const navigate = useNavigate()
  const token = getToken()

  const handleLogout = async () => {
    try{
      await api.post('/auth/logout/')
    }catch(e){}
    clearToken()
    navigate('/login')
  }

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">University</Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav">
          <span className="navbar-toggler-icon" />
        </button>
        <div className="collapse navbar-collapse" id="nav">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            {token && (
              <>
                <li className="nav-item"><Link className="nav-link" to="/news">News</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/schedule">Schedule</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/profile">Profile</Link></li>
              </>
            )}
          </ul>
          <div className="d-flex">
            {!token ? (
              <Link className="btn btn-outline-light" to="/login">Login</Link>
            ) : (
              <button className="btn btn-outline-light" onClick={handleLogout}>Logout</button>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
