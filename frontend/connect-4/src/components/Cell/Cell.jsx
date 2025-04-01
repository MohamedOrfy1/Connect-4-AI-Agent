import './Cell.css';

export default function Cell({ value, rowIndex, colIndex, onClick }) {
    return (
        <div
            className={`cell ${value || 'empty'}`}
            onClick={onClick}
        >

        </div>
    );
}
