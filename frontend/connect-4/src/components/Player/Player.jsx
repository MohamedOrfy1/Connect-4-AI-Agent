import React from 'react';
import './Player.css';

export default function Player({ color, isActive }) {
    return (
        <li className={`player ${color}-player ${isActive ? 'active' : ''}`}>
            Player {color === 'red' ? '1' : '2'}
            <div className="player-token" style={{ backgroundColor: color }} />
        </li>
    );
}