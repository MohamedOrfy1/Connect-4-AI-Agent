import './Player.css';

export default function Player({ color, isActive }) {

    return (
        <li className={isActive ? 'active' : undefined}>
            <span className="player">
                <span className="player-color">{color}</span>
            </span>
        </li>
    );
}