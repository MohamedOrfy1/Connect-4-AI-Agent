import { useState } from 'react'
import './App.css'
function App() {
  const [count, setCount] = useState(0)

  return (
    <div className='App'>
      <h1>Connect 4 game</h1>
    </div>
  )
}

export default App
