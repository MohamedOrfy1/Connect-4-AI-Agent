import React from 'react'
import './Cell.css';

export default function Cell({ value, rowIndex, colIndex, onClick, disabled }) {
    return (
        <div
            className={`cell ${value} ${disabled ? 'disabled' : ''}`}
            onClick={onClick}
            data-row={rowIndex}
            data-col={colIndex}
        >

        </div>
    );
}
