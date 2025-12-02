import React from 'react'
import News from './News'
import Schedule from './Schedule'

export default function Dashboard(){
  return (
    <div>
      <h2>Dashboard</h2>
      <div className="row">
        <div className="col-lg-7">
          <News compact />
        </div>
        <div className="col-lg-5">
          <Schedule compact />
        </div>
      </div>
    </div>
  )
}
