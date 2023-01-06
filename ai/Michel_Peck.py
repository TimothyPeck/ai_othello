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
    ]  # taken from https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/O-Thell-Us/Othellus.pdf and modified to our needs

    MAX_DEPTH = 5

    ROWS, COLS = None, None

    player_color = None

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

        self.ROWS, self.COLS = board.get_rows(), board.get_columns()

        self.init_board = board

        (val, move) = self.alpha_beta(
            board, self.MAX_DEPTH, -math.inf, math.inf, True)

        return move

    def compare_boards(self, board: othello.OthelloGame, move: tuple[int, int]) -> int:
        """
        Takes the new board and calculates the difference between the scores of the boards, 
        adds the value of the weight to the score therefor ensuring that the move is pretty good.

        :param board: the board after the move has been made
        :type board: othello.OthelloGame
        :param move: tuple[int, int]
        :type move: tuple[int, int]
        :return: The score of the move.
        """

        (new_black_tiles, new_white_tiles) = board.get_scores() # Gets the score for the current board
        (old_black_tiles, old_white_tiles) = self.init_board.get_scores() # Gets the score for the inital board

        weight = self.WEIGHTS[move[0]][move[1]] # Get the weight of the current board
        player_score = 0 # Initialises the score to 0
        if self.player_color == "B": # Changes how the score is calculated depending on the colour of the player
            player_score = (new_black_tiles-old_black_tiles) - \
                (new_white_tiles-old_white_tiles) # Difference between the new and old board
        else:
            player_score = (new_white_tiles-old_white_tiles) - \
                (new_black_tiles-old_black_tiles) # Difference between the new and old board

        player_score += weight # Adds the weight od the move to the score
        return player_score

    def alpha_beta(self, board: othello.OthelloGame, depth: int, alpha: int, beta: int, maximizing_player: bool, test_move: tuple[int, int] = None) -> tuple[int, tuple[int, int]]:
        """
        Using the alpha-beta algorithm, gets the "best" move for the current board going to a max depth definied in the initial called and decremented with every recursive call

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
        if depth == 0 or board.is_game_over(): # Run when we reach max depth or the game is over (last possible move, no need to go further)
            return self.compare_boards(board, test_move), None # Return the score for the tested move, and None, which is the move itself.

        if maximizing_player: # If we are maximising the player
            best_score = -math.inf # Make the best score as low as possible, it can only get better from here
            best_move = None # no move yet
            for move in board.get_possible_move(): # Get all the possible moves on the board, maybe for the current player, hard to tell, never complains though so who knows
                board_copy = board.copy_game() # Copy of the board, uses deepcopy, slow
                board_copy.move(move[0], move[1]) # Play the move on the copied board
                score = self.alpha_beta(
                    board_copy, depth - 1, alpha, beta, not maximizing_player, move)[0] # call self again, gets the score for this move and future possbible moves from this one, saves just the score not the move
                best_score = max(score, best_score) # Gets the best of the scores
                alpha = max(alpha, best_score) # Takes the best between alpha and the score
                if best_score == score: # if the best score is the same as the score, take that move
                    best_move = move
                if best_score > beta: # stop if the value is greater than beta
                    break
            return best_score, best_move
        else:
            best_score = math.inf # Make the best score as high as possible, since technically it can only get worse from here
            best_move = None # no move yet
            for move in board.get_possible_move(): # ditto
                board_copy = board.copy_game() # ditto
                board_copy.move(move[0], move[1]) # ditto
                score = self.alpha_beta(
                    board_copy, depth - 1, alpha, beta, not maximizing_player, move)[0] # call self again, gets the score for this move and future possbible moves from this one, saves just the score not the move
                best_score = min(score, best_score) # gets the lowest
                beta = min(beta, best_score) # opposite to alpha
                if best_score == score: # same as alpha
                    best_move = move
                if best_score < alpha: # stop if the value is less than alpha
                    break
            return best_score, best_move
