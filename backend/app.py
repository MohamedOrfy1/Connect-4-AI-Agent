from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.models.board import ConnectFourBoard
from src.algorithms.minimax import decision
import traceback
import logging
import numpy as np

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GameState(BaseModel):
    board: list[list[int]]
    current_player: int
    algorithm: str = "minimax"  # Default to standard minimax
    depth: int = 4  # Default depth

@app.get("/")
async def root():
    return {"message": "Connect 4 AI API is running"}

@app.post("/ai/move")
async def get_ai_move(game_state: GameState):
    try:
        logger.debug(f"Received game state: {game_state}")
        
        # Convert the board state to ConnectFourBoard
        board = ConnectFourBoard()
        # Convert list of lists to numpy array
        board.board = np.array(game_state.board, dtype=int)
        board.current_player = game_state.current_player
        
        logger.debug(f"Created board with current player: {board.current_player}")
        logger.debug(f"Board state:\n{board}")
        
        # Get AI move based on selected algorithm
        use_alpha_beta = game_state.algorithm == "alphabeta"
        use_expected_minimax = game_state.algorithm == "expectimax"
        
        move = decision(
            state=board,
            k=game_state.depth,
            use_alpha_beta=use_alpha_beta,
            use_expected_minimax=use_expected_minimax
        )
        
        logger.debug(f"AI chose move: {move}")
        
        if move == -1:
            raise HTTPException(status_code=400, detail="No valid moves available")
            
        return {"move": move}
    except Exception as e:
        logger.error(f"Error in get_ai_move: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)