import time
from ai.Random import Random
import othello
import random
import math
from copy import deepcopy
from itertools import product


class Michel_Peck:
    PB_FEINT = 0.05
    WEIGHTS = [
        [100, -10, 11, 6, 6, 6, 11, -10, 100],
        [-10, -20, 1, 2, 2, 2, 1, -20, -10],
        [10, 1, 5, 4, 4, 4, 5, 1, 10],
        [6, 2, 4, 2, 2, 2, 4, 2, 6],
        [10, 1, 5, 4, 4, 4, 5, 1, 10],
        [-10, -20, 1, 2, 2, 2, 1, -20, -10],
        [100, -10, 11, 6, 6, 6, 11, -10, 100]
    ]  # taken from https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf

    MAX_DEPTH = 5

    ROWS, COLS = None, None

    player_color = None
    opp_color = None

    init_board = None

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Michel_Peck"

    def next_move(self, board: othello.OthelloGame) -> tuple[int, int]:
        self.board = board
        self.legal_moves = board.get_possible_move()

        self.player_color = board.get_turn()
        self.opp_color = "W" if self.player_color == "B" else "B"

        self.ROWS, self.COLS = board.get_rows(), board.get_columns()

        self.init_board = board

        (val, move) = self.alpha_beta(
            board, self.MAX_DEPTH, -math.inf, math.inf, True)

        return move

    def evaluate(self, board: othello.OthelloGame) -> int:
        score = 0
        for row, col in product(range(self.ROWS), range(self.COLS)):
            turn = board.get_turn()
            opp = "W" if turn == "B" else "B"
            if board.current_board[row][col] == turn:
                score += self.WEIGHTS[row][col]
            elif board.current_board[row][col] == opp:
                score -= self.WEIGHTS[row][col]
        return score

    def compare_boards(self, new_board: othello.OthelloGame) -> int:
        (new_black_tiles, new_white_tiles) = new_board.get_scores()
        (old_black_tiles, old_white_tiles) = self.init_board.get_scores()
        old_turn = self.init_board.get_turn()
        player_score = 0
        if old_turn == "B":
            player_score = new_black_tiles-old_black_tiles
        else:
            player_score = new_white_tiles-old_white_tiles
        return player_score

    def alpha_beta(self, board: othello.OthelloGame, depth: int, alpha: int, beta: int, maximizing_player: bool) -> tuple[int, int]:
        if depth == 0 or board.is_game_over():
            return self.compare_boards(board), None

        if maximizing_player:
            best_score = -math.inf
            best_move = None
            for move in board.get_possible_move():
                board_copy = board.copy_game()
                board_copy.move(move[0], move[1])
                score = self.alpha_beta(
                    board_copy, depth - 1, alpha, beta, not maximizing_player)[0]
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if best_score == score:
                    best_move = move
                if beta <= alpha:
                    break
            return best_score, best_move
        else:
            best_score = math.inf
            best_move = None
            for move in board.get_possible_move():
                board_copy = board.copy_game()
                board_copy.move(move[0], move[1])
                score = self.alpha_beta(
                    board_copy, depth - 1, alpha, beta, not maximizing_player)[0]
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if best_score == score:
                    best_move = move
                if beta <= alpha:
                    break
            return best_score, best_move
