import React, { useState } from 'react';
import './Settings.css';

const Settings = ({ onStart }) => {
    const [algorithm, setAlgorithm] = useState('minimax');
    const [depth, setDepth] = useState(4);
    const [starter, setStarter] = useState('player');

    const handleStart = () => {
        onStart({
            algorithm,
            depth,
            starter
        });
    };

    return (
        <div className="settings-container">
            <h2>Game Settings</h2>
            
            <div className="settings-section">
                <h3>Algorithm</h3>
                <div className="algorithm-buttons">
                    <button 
                        className={algorithm === 'minimax' ? 'active' : ''} 
                        onClick={() => setAlgorithm('minimax')}
                    >
                        Minimax
                    </button>
                    <button 
                        className={algorithm === 'alphabeta' ? 'active' : ''} 
                        onClick={() => setAlgorithm('alphabeta')}
                    >
                        Minimax with Pruning
                    </button>
                    <button 
                        className={algorithm === 'expectimax' ? 'active' : ''} 
                        onClick={() => setAlgorithm('expectimax')}
                    >
                        Expected Minimax
                    </button>
                </div>
            </div>

            <div className="settings-section">
                <h3>Search Depth</h3>
                <div className="depth-selector">
                    <input 
                        type="number" 
                        min="1" 
                        max="42" 
                        value={depth} 
                        onChange={(e) => setDepth(Number(e.target.value))}
                    />
                    <span className="depth-hint">Choose between 1-42</span>
                </div>
            </div>

            <div className="settings-section">
                <h3>Who starts?</h3>
                <div className="starter-buttons">
                    <button 
                        className={starter === 'player' ? 'active' : ''} 
                        onClick={() => setStarter('player')}
                    >
                        Player Starts
                    </button>
                    <button 
                        className={starter === 'ai' ? 'active' : ''} 
                        onClick={() => setStarter('ai')}
                    >
                        AI Starts
                    </button>
                </div>
            </div>

            <button className="start-button" onClick={handleStart}>
                START GAME
            </button>
        </div>
    );
};

export default Settings; 