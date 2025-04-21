import { useState, useEffect } from 'react'
import '../App.css'
import Board from '../components/Board/Board'
import Player from '../components/Player/Player'
import Settings from '../components/Settings'
import ScoreBoard from '../components/ScoreBoard'

const ROWS = 6
const COLS = 7
const EMPTY = ''

const PLAYER_1 = 'red'
const PLAYER_2 = 'yellow'

const INITIAL_TILES = Array(ROWS).fill(EMPTY).map(() => Array(COLS).fill(EMPTY))

function GamePage() {
    const [tiles, setTiles] = useState(INITIAL_TILES);
    const [currentPlayer, setCurrentPlayer] = useState(PLAYER_1);
    const [gameOver, setGameOver] = useState(false);
    const [isAITurn, setIsAITurn] = useState(false);
    const [scores, setScores] = useState({ red: 0, yellow: 0 });
    const [gameStarted, setGameStarted] = useState(false);
    const [gameSettings, setGameSettings] = useState({
        algorithm: 'minimax',
        depth: 4,
        starter: 'player'
    });

    // Handle settings submission
    const handleStartGame = (settings) => {
        setGameSettings(settings);
        setGameStarted(true);
        resetGame();
        if (settings.starter === 'ai') {
            setCurrentPlayer(PLAYER_2);
            setIsAITurn(true);
        }
    };

    // Convert color to number for API
    const colorToNumber = (color) => color === PLAYER_1 ? 1 : 2;

    // Count all connected fours in the board for a given player
    const countConnectedFours = (board, player) => {
        let count = 0;

        // Check horizontal
        for (let row = 0; row < ROWS; row++) {
            for (let col = 0; col < COLS - 3; col++) {
                if (board[row][col] === player &&
                    board[row][col + 1] === player &&
                    board[row][col + 2] === player &&
                    board[row][col + 3] === player) {
                    count++;
                }
            }
        }

        // Check vertical
        for (let row = 0; row < ROWS - 3; row++) {
            for (let col = 0; col < COLS; col++) {
                if (board[row][col] === player &&
                    board[row + 1][col] === player &&
                    board[row + 2][col] === player &&
                    board[row + 3][col] === player) {
                    count++;
                }
            }
        }

        // Check diagonal (positive slope)
        for (let row = 0; row < ROWS - 3; row++) {
            for (let col = 0; col < COLS - 3; col++) {
                if (board[row][col] === player &&
                    board[row + 1][col + 1] === player &&
                    board[row + 2][col + 2] === player &&
                    board[row + 3][col + 3] === player) {
                    count++;
                }
            }
        }

        // Check diagonal (negative slope)
        for (let row = 3; row < ROWS; row++) {
            for (let col = 0; col < COLS - 3; col++) {
                if (board[row][col] === player &&
                    board[row - 1][col + 1] === player &&
                    board[row - 2][col + 2] === player &&
                    board[row - 3][col + 3] === player) {
                    count++;
                }
            }
        }

        return count;
    };

    // Check if board is full
    const isBoardFull = (board) => {
        return board.every(row => row.every(cell => cell !== EMPTY));
    };

    // Update scores after each move
    const updateScores = (board) => {
        const redCount = countConnectedFours(board, PLAYER_1);
        const yellowCount = countConnectedFours(board, PLAYER_2);
        setScores({ red: redCount, yellow: yellowCount });
    };

    // Handle AI move
    const handleAIMove = async () => {
        try {
            const response = await fetch('http://localhost:8000/ai/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    board: tiles.map(row =>
                        row.map(cell => cell === EMPTY ? 0 : (cell === PLAYER_1 ? 1 : 2))
                    ),
                    current_player: colorToNumber(currentPlayer),
                    algorithm: gameSettings.algorithm,
                    depth: gameSettings.depth
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to get AI move');
            }

            const data = await response.json();
            const aiMove = data.move;

            // Make the AI move
            const newTiles = tiles.map(row => [...row]);
            for (let row = ROWS - 1; row >= 0; row--) {
                if (newTiles[row][aiMove] === EMPTY) {
                    newTiles[row][aiMove] = currentPlayer;
                    setTiles(newTiles);
                    updateScores(newTiles);

                    if (isBoardFull(newTiles)) {
                        setGameOver(true);
                    } else {
                        setCurrentPlayer(PLAYER_1);
                        setIsAITurn(false);
                    }
                    return;
                }
            }
        } catch (error) {
            console.error('Error getting AI move:', error);
            setIsAITurn(false);
        }
    };

    // Handle player move
    const handleDrop = (col) => {
        if (gameOver || isAITurn) return;

        const newTiles = tiles.map(row => [...row]);
        for (let row = ROWS - 1; row >= 0; row--) {
            if (tiles[row][col] === EMPTY) {
                newTiles[row][col] = currentPlayer;
                setTiles(newTiles);
                updateScores(newTiles);

                if (isBoardFull(newTiles)) {
                    setGameOver(true);
                } else {
                    setCurrentPlayer(PLAYER_2);
                    setIsAITurn(true);
                }
                return;
            }
        }
    };

    // Reset game
    const resetGame = () => {
        setTiles(INITIAL_TILES);
        setCurrentPlayer(gameSettings.starter === 'ai' ? PLAYER_2 : PLAYER_1);
        setGameOver(false);
        setIsAITurn(gameSettings.starter === 'ai');
        setScores({ red: 0, yellow: 0 });
    };

    // Handle AI turn
    useEffect(() => {
        if (isAITurn && !gameOver) {
            handleAIMove();
        }
    }, [isAITurn, gameOver]);

    if (!gameStarted) {
        return (
            <div className='App'>
                <h1>Connect Four</h1>
                <Settings onStart={handleStartGame} />
            </div>
        );
    }

    return (
        <div className='App'>
            <h1>Connect Four</h1>
            <ScoreBoard
                scores={scores}
                currentPlayer={currentPlayer}
                gameOver={gameOver}
                PLAYER_1={PLAYER_1}
                PLAYER_2={PLAYER_2}
            />
            {gameOver ? (
                <div className="game-over">
                    <h2>Game Over!</h2>
                    <h3>
                        {scores.red > scores.yellow ? 'Red wins!' :
                            scores.yellow > scores.red ? 'Yellow wins!' :
                                'It\'s a tie!'}
                    </h3>
                    <p>Final Score - Red: {scores.red}, Yellow: {scores.yellow}</p>
                    <button onClick={resetGame}>Play Again</button>
                </div>
            ) : (
                <div className="game-status">
                    <h2>{currentPlayer === PLAYER_1 ? 'Your' : 'AI\'s'} turn</h2>
                </div>
            )}
            <Board tiles={tiles} onDrop={handleDrop} />
            <div id="players">
                <Player color={PLAYER_1} active={currentPlayer === PLAYER_1} />
                <Player color={PLAYER_2} active={currentPlayer === PLAYER_2} />
            </div>
            <button onClick={() => {
                setGameStarted(false);
                resetGame();
            }}>Change Settings</button>
        </div>
    );
}

export default GamePage;
