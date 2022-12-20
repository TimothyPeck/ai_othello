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

        (val, move) = self.alpha_beta(
            board, self.MAX_DEPTH, -math.inf, math.inf, True)

        return move

    # Evaluate the board
    def evaluate(self, board: othello.OthelloGame) -> int:
        (black_tokens, white_tokens) = board.compute_scores()
        color = board.get_turn()
        coin_parity, mobility, corners = 0, 0, 0
        player_moves = board.get_possible_move()
        board.switch_turn()
        opp_moves = board.get_possible_move()
        board.switch_turn()

        if color == "B":
            coin_parity = 100*(black_tokens-white_tokens) / \
                (black_tokens+white_tokens)
        elif color == "W":
            coin_parity = 100*(white_tokens-black_tokens) / \
                (white_tokens+black_tokens)

        if len(player_moves)+len(opp_moves) != 0:
            mobility = 100*(len(player_moves)-len(opp_moves)) / \
                (len(player_moves)+len(opp_moves))
        else:
            mobility = 0

        player_corners = 0
        opp_corners = 0

        if board.current_board[0][0] == self.player_color:
            player_corners += 1
        elif board.current_board[0][0] == self.opp_color:
            opp_corners += 1

        if board.current_board[self.ROWS-1][0] == self.player_color:
            player_corners += 1
        elif board.current_board[self.ROWS-1][0] == self.opp_color:
            opp_corners += 1

        if board.current_board[0][self.COLS-1] == self.player_color:
            player_corners += 1
        elif board.current_board[0][self.COLS-1] == self.opp_color:
            opp_corners += 1

        if board.current_board[self.ROWS-1][self.COLS-1] == self.player_color:
            player_corners += 1
        elif board.current_board[self.ROWS-1][self.COLS-1] == self.opp_color:
            opp_corners += 1

        if player_corners+opp_corners != 0:
            corners = 100*(player_corners-opp_corners) / \
                (player_corners + opp_corners)

        score = (coin_parity+mobility+corners)/3
        print(f"Score: {score}")
        return score

        score = 0
        for row, col in product(range(self.ROWS), range(self.COLS)):
            turn = board.get_turn()
            opp = "W" if turn == "B" else "B"
            if board.current_board[row][col] == turn:
                score += self.WEIGHTS[row][col]
            elif board.current_board[row][col] == opp:
                score -= self.WEIGHTS[row][col]
        return score

    def alpha_beta(self, board: othello.OthelloGame, depth: int, alpha: int, beta: int, maximizing_player: bool) -> tuple[int, int]:
        if depth == 0 or board.is_game_over():
            return self.evaluate(board), None

        if maximizing_player:
            best_score = -math.inf
            best_move = None
            for move in board.get_possible_move():
                board_copy = board.copy_game()
                board_copy.move(move[0], move[1])
                score = self.alpha_beta(
                    board_copy, depth - 1, alpha, beta, False)[0]
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
                    board_copy, depth - 1, alpha, beta, True)[0]
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if best_score == score:
                    best_move = move
                if beta <= alpha:
                    break
            return best_score, best_move
