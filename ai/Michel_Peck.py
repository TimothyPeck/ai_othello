import time
from ai.Random import Random
import othello
import random
import math
from copy import deepcopy
from itertools import product


class Michel_Peck:
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
        """
        The function takes in a board, and returns the best move for the player
        
        :param board: the current state of the game
        :type board: othello.OthelloGame
        :return: The move that the AI will make.
        """
        self.board = board
        self.legal_moves = board.get_possible_move()

        self.player_color = board.get_turn()
        self.opp_color = "W" if self.player_color == "B" else "B"

        self.ROWS, self.COLS = board.get_rows(), board.get_columns()

        self.init_board = board

        (val, move) = self.alpha_beta(
            board, self.MAX_DEPTH, -math.inf, math.inf, True)

        print(f"Score of the played move: {val}")
        return move

    def evaluate(self, board: othello.OthelloGame) -> int:
        """
        The function takes in a board and returns a score based on the weights of the board, really slow
        
        :param board: othello.OthelloGame
        :type board: othello.OthelloGame
        :return: The score of the board.
        """
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
        """
        The function compares the score of the current board with the score of the initial board and
        returns the difference, fast and surprisingly good
        
        :param new_board: othello.OthelloGame
        :type new_board: othello.OthelloGame
        :return: The difference between the player's score and the opponent's score.
        """
        (new_black_tiles, new_white_tiles) = new_board.get_scores()
        (old_black_tiles, old_white_tiles) = self.init_board.get_scores()
        player_score = 0
        if self.player_color == "B":
            player_score = (new_black_tiles-old_black_tiles) - \
                (new_white_tiles-old_white_tiles)
        else:
            player_score = (new_white_tiles-old_white_tiles) - \
                (new_black_tiles-old_black_tiles)
        return player_score

    def alpha_beta(self, board: othello.OthelloGame, depth: int, alpha: int, beta: int, maximizing_player: bool) -> tuple[int, int]:
        """
        It's a recursive function that returns the best move for the current player, given the current
        board state
        
        :param board: othello.OthelloGame
        :type board: othello.OthelloGame
        :param depth: The depth of the search tree
        :type depth: int
        :param alpha: the best score that the maximizing player currently can guarantee given the
        current path
        :type alpha: int
        :param beta: the best score that the maximizing player can guarantee given the current state of
        the game
        :type beta: int
        :param maximizing_player: True if the player is the maximizing player, False if the player is
        the minimizing player
        :type maximizing_player: bool
        :return: The best score and the best move
        """
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
