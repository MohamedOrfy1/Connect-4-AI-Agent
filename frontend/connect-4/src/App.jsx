import { useState } from 'react'
import './App.css'
import Board from './components/Board/Board'
import Player from './components/Player/Player'

const ROWS = 6
const COLS = 7
const EMPTY = ''

const PLAYER_1 = 'red'
const PLAYER_2 = 'yellow'

const INITIAL_TILES = Array(ROWS).fill(EMPTY).map(() => Array(COLS).fill(EMPTY))

function App() {

  const [tiles, setTiles] = useState(INITIAL_TILES);
  const [currentPlayer, setCurrentPlayer] = useState(PLAYER_1)

  function handleDrop(col) {
    const newTiles = tiles.map(row => [...row]);

    for (let row = ROWS - 1; row >= 0; row--) {
      if (tiles[row][col] === EMPTY) {
        newTiles[row][col] = currentPlayer;
        setTiles(newTiles);
        setCurrentPlayer(currentPlayer === PLAYER_1 ? PLAYER_2 : PLAYER_1);
        return;
      }
    }

  };

  return (
    <div className='App'>
      <h1>Connect 4</h1>
      <ol id="players" className="highlight-player">
        <Player color={PLAYER_1} isActive={currentPlayer === PLAYER_1} />
        <Player color={PLAYER_2} isActive={currentPlayer === PLAYER_2} />
      </ol>
      <Board tiles={tiles} onDrop={handleDrop} />
    </div>
  )
}

export default App
