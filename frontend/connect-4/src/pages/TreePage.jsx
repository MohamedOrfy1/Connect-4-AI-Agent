import React from 'react';
import Tree from 'react-d3-tree';
import '../App.css';

const renderMiniBoard = (board) => (
    <table className="mini-board">
        <tbody>
            {board.map((row, i) => (
                <tr key={i}>
                    {row.map((cell, j) => (
                        <td key={j} className={`cell ${cell === 1 ? 'red' : cell === 2 ? 'yellow' : ''}`}></td>
                    ))}
                </tr>
            ))}
        </tbody>
    </table>
);

const renderCustomNode = ({ nodeDatum }) => {
    return (
        <foreignObject width={200} height={160}>
            <div style={{ border: '1px solid black', background: 'white', borderRadius: 4, padding: 4 }}>
                <h4 style={{ margin: 0 }}>{nodeDatum.name}</h4>
                {nodeDatum.board && renderMiniBoard(nodeDatum.board)}
            </div>
        </foreignObject>
    );
};

const sampleTree = {
    name: 'Root',
    board: [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 2, 1, 0, 0, 0],
        [0, 0, 2, 1, 0, 0, 0],
        [0, 1, 1, 2, 0, 0, 0],
        [2, 2, 1, 1, 0, 0, 0],
    ],
    children: [
        {
            name: 'Move 0',
            board: [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 2, 1, 0, 0, 0],
                [0, 0, 2, 1, 0, 0, 0],
                [1, 1, 1, 2, 0, 0, 0],
                [2, 2, 1, 1, 0, 0, 0],
            ],
            children: []
        },
        {
            name: 'Move 1',
            board: [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 2, 1, 0, 0, 0],
                [0, 1, 2, 1, 0, 0, 0],
                [0, 1, 1, 2, 0, 0, 0],
                [2, 2, 1, 1, 0, 0, 0],
            ],
            children: []
        },
        {
            name: 'Move 2',
            board: [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0, 0, 0],
                [0, 0, 2, 1, 0, 0, 0],
                [0, 0, 2, 1, 0, 0, 0],
                [0, 1, 1, 2, 0, 0, 0],
                [2, 2, 1, 1, 0, 0, 0],
            ],
            children: []
        },
    ]
};

function TreeVisualizer() {
    return (
        <div style={{ width: '100vw', height: '100vh' }}>
            <h1>Minimax Tree Visualization</h1>
            <Tree
                data={sampleTree}
                orientation="vertical"
                renderCustomNodeElement={renderCustomNode}
                nodeSize={{ x: 220, y: 200 }}
            />
        </div>
    );
}

export default TreeVisualizer;
