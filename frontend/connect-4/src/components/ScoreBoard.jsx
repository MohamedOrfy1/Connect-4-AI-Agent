export default function ScoreBoard({ scores, currentPlayer, gameOver , PLAYER_1, PLAYER_2 }) {
    return (
        <div className="scores">
            <div className={`score red ${currentPlayer === PLAYER_1 && !gameOver ? 'active' : ''}`}>
                Red: {scores.red}
            </div>
            <div className={`score yellow ${currentPlayer === PLAYER_2 && !gameOver ? 'active' : ''}`}>
                Yellow: {scores.yellow}
            </div>
        </div>
    );
}