import React from 'react'
import './Board.css'
import Cell from '../Cell/Cell'

export default function Board({ tiles, onDrop, disabled }) {
    return (
        <div className={`board ${disabled ? 'disabled' : ''}`}>
            {tiles.map((row, rowIndex) =>
                row.map((cell, colIndex) => (
                    <Cell
                        key={`${rowIndex}-${colIndex}`}
                        value={cell}
                        rowIndex={rowIndex}
                        colIndex={colIndex}
                        onClick={() => onDrop(colIndex)}
                        disabled={disabled}
                    />
                ))
            )}
        </div>
    );
}

