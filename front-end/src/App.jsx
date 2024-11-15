import './App.css'
import Navbar from './Components/Navbar'
import { BrowserRouter, Route, Routes } from "react-router-dom"
import MainDashboard from './pages/MainDashboard'
import CheckIn from './Components/CheckIn'
import VisitorCheckIn from './Components/VisitorCheckIn'

function App() {
  return (
    <BrowserRouter>
      <Navbar />
        <Routes>
          <Route path='/' element ={<MainDashboard/>}/>
          <Route path='/checkin' element = { <CheckIn/>}/>
          <Route path='/checkin-visitor' element = { <VisitorCheckIn/>}/>
        </Routes>
    </BrowserRouter>
  )
}

export default App
