from ai.Random import Random
import othello
import random
import math


class Michel_Peck:
    PB_FEINT = 0.05
    heuristics = [
        [100, -10, 11, 6, 6, 6, 11, -10, 100],
        [-10, -20, 1, 2, 2, 2, 1, -20, -10],
        [10, 1, 5, 4, 4, 4, 5, 1, 10],
        [6, 2, 4, 2, 2, 2, 4, 2, 6],
        [10, 1, 5, 4, 4, 4, 5, 1, 10],
        [-10, -20, 1, 2, 2, 2, 1, -20, -10],
        [100, -10, 11, 6, 6, 6, 11, -10, 100]
    ]

    def __init__(self) -> None:
        pass

    def next_move(self, board: othello.OthelloGame) -> tuple[int, int]:
        self.board = board
        self.legal_moves = board.get_possible_move()

        return self.get_best_move()

    def get_best_move(self) -> tuple[int, int]:
        pb = random.random()
        best_move = random.choice(self.legal_moves)
        best_weight = -100
        first_move = self.board.compute_scores() == (2, 2)
        print(f"First move: {first_move}")
        for move in self.legal_moves:
            if first_move or pb > self.PB_FEINT:
                if self.heuristics[move[0]][move[1]] > best_weight:
                    best_weight = self.heuristics[move[0]][move[1]]
                    best_move = move
            else:
                if self.heuristics[move[0]][move[1]] <= best_weight:
                    best_weight = self.heuristics[move[0]][move[1]]
                    best_move = move
        return best_move

    def ab_max(self, root, parentMin, depth=5):
        if (depth == 0 or root.final()):
            return root.eval(), None
        maxVal = -math.inf
        maxOp = None
        for op in root.ops():
            new = root.apply(op)
            val, _ = self.ab_min(new, maxVal, depth-1)
            if val > maxVal:
                maxVal = val
                maxOp = op
                if maxVal > parentMin:
                    break
        return maxVal, maxOp

    def ab_min(self, root, parentMax, depth=5):
        if (depth == 0 or root.final()):
            return root.eval(), None
        minVal = -math.inf
        minOp = None
        for op in root.ops():
            new = root.apply(op)
            val, _ = self.ab_max(new, minVal, depth-1)
            if val > minVal:
                minVal = val
                minOp = op
                if minVal > parentMax:
                    break
        return minVal, minOp
