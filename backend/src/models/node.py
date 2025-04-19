import json

class TreeNode:
    def __init__(self, move=None, score=None, player=None, depth=0, board_str=None):
        self.move = move              # Column index (0-6)
        self.score = score            # Evaluation score
        self.player = player          # 1 or 2
        self.depth = depth            # Depth in tree
        self.board_str = board_str    # Board string representation (compact)
        self.children = []            # Child nodes
        self.best_child = None        # Best child node (for minimax)

    def to_dict(self):
        return {
            "move": self.move,
            "score": self.score,
            "player": self.player,
            "depth": self.depth,
            "board": self.board_str,
            "children": self.children,
            "best_child": self.best_child if self.best_child else None
        }
    
    def add_child(self, child_node):
        # self.children.append(child_node)
        self.children.append(child_node.to_dict())

    def set_best_child(self, best_child_node):
        self.best_child = best_child_node.to_dict()

    def print_tree(self, indent=0):
        print("=" * indent + f"Move: {self.move}, Score: {self.score}, Player: {self.player}, Depth: {self.depth}")
        for child in self.children:
            if isinstance(child, TreeNode):
                child.print_tree(indent + 2)
            else:
                print("=" * (indent + 2) + f"(Serialized Child): {child}")
