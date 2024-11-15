import React from 'react'
import logo from "../assets/logo.png"

const Navbar = () => {
  return (
    <div className='flex gap-1 items-center p-3 bg-slate-800 text-white'>
        <img className='h-12' src={logo} alt="logo" />
        <p className="font-semibold text-2xl">Solutions</p>
    </div>
  )
}

export default Navbar