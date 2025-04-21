import React, { useEffect, useState } from 'react';
import Tree from 'react-d3-tree';
import '../App.css';

// Util: Convert board string to 2D array
function parseBoardString(boardStr) {
    const lines = boardStr.trim().split('\n');
    const board = lines.slice(0, 6).map(line =>
        line.trim().split(' ').map(cell => {
            if (cell === 'X') return 1;
            if (cell === 'O') return 2;
            return 0;
        })
    );
    return board;
}

// Util: Convert raw node to d3-tree-compatible node
function convertToTreeNode(aiNode) {
    return {
        name: `Move ${aiNode.move ?? '-'} | Player${aiNode.player} | Score: ${aiNode.score}`,
        board: parseBoardString(aiNode.board),
        children: aiNode.children?.map(convertToTreeNode) || []
    };
}

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

const renderCustomNode = ({ nodeDatum }) => (
    <foreignObject width={220} height={160}>
        <div style={{ border: '1px solid black', background: 'white', borderRadius: 4, padding: 4 , marginRight: 4}}>
            <h4 style={{ margin: 0 }}>{nodeDatum.name}</h4>
            {nodeDatum.board && renderMiniBoard(nodeDatum.board)}
        </div>
    </foreignObject>
);

function TreeVisualizer() {
    const [treeData, setTreeData] = useState(null);

    useEffect(() => {
        const storedTree = localStorage.getItem('tree');
        if (storedTree) {
            try {
                const parsed = JSON.parse(storedTree);
                const tree = convertToTreeNode(parsed);
                setTreeData(tree);
            } catch (err) {
                console.error('Failed to parse AI tree from localStorage:', err);
            }
        }
    }, []);

    return (
        <div style={{ width: '100vw', height: '100vh' }}>
            <h1>Minimax Tree Visualization</h1>
            {treeData ? (
                <Tree
                    data={treeData}
                    orientation="vertical"
                    renderCustomNodeElement={renderCustomNode}
                    nodeSize={{ x: 220, y: 200 }}
                />
            ) : (
                <p>No tree data found in localStorage.</p>
            )}
        </div>
    );
}

export default TreeVisualizer;
