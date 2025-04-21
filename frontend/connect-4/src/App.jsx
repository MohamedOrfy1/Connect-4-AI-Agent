import {
    BrowserRouter as Router,
    Routes,
    Route
  } from 'react-router-dom';
import './App.css'
import GamePage from './pages/GamePage'
import TreePage from './pages/TreePage'

const ROWS = 6
const COLS = 7
const EMPTY = ''

const PLAYER_1 = 'red'
const PLAYER_2 = 'yellow'

const INITIAL_TILES = Array(ROWS).fill(EMPTY).map(() => Array(COLS).fill(EMPTY))

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<GamePage />} />
                <Route path="/tree" element={<TreePage />} />
            </Routes>
        </Router>
    );
}

export default App;
