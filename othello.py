"""
This is the file with the Othello game logic. It contains the OthelloGame class that represents the game state
"""

import copy

# Game Constants
NONE = '.'
BLACK = 'B'
WHITE = 'W'


class InvalidMoveException(Exception):
    """ Raised whenever an exception arises from an invalid move """
    pass


class InvalidTypeException(Exception):
    """ Raised whenever an exception arises from an invalid type """
    pass


class OthelloGame:
    """
    Class that creates the Othello game and deals with all its game logic
    """

    def __init__(self, rows: int, cols: int, turn: str):
        """ Initialize all of the games settings and creates the board. """
        self.rows = rows
        self.cols = cols
        self.current_board = self._new_game_board(rows, cols, WHITE)
        self.turn = turn
        self.scores = self.compute_scores()

    def copy_game(self):
        """ Returns a copy of the current game """
        copy_game = OthelloGame(self.rows, self.cols, self.turn)
        copy_game.current_board = self.copy_board()
        copy_game.scores = self.scores
        return copy_game

    def copy_board(self):
        """ Returns a copy of the current game's 2D board """
        return copy.deepcopy(self.current_board)

    def _new_game_board(self, rows: int, cols: int, top_left: str) -> list[list[str]]:
        """ Creates the Othello Game board with specified dimensions. """
        board = []

        # Create an empty board
        for row in range(rows):
            board.append([])
            for col in range(cols):
                board[-1].append(NONE)

        board[rows // 2 - 1][cols // 2 - 1] = top_left
        board[rows // 2 - 1][cols // 2] = self._opposite_turn(top_left)
        board[rows // 2][cols // 2 - 1] = self._opposite_turn(top_left)
        board[rows // 2][cols // 2] = top_left

        return board

    def move(self, row: int, col: int, fake_move: bool = False):
        """ Attempts to make a move at given row/col position.
            Current player/turn is the one that makes the move.
            If the player cannot make a move it raises an exception.
            If the player can make a move, the player finally plays
            the valid move and switches turn. """

        # Check to see if the move is in a valid empty space
        # within the board's boundary
        if type(row) is not int or type(col) is not int:
            raise InvalidTypeException

        if fake_move:
            temp_board = self.copy_board()
        self._require_valid_empty_space_to_move(row, col)
        possible_directions = self._adjacent_opposite_color_directions(
            row, col, self.turn)

        next_turn = self.turn
        for direction in possible_directions:
            if self._is_valid_directional_move(row, col, direction[0], direction[1], self.turn):
                next_turn = self._opposite_turn(self.turn)
            self._convert_adjacent_cells_in_direction(
                row, col, direction[0], direction[1], self.turn)

        if next_turn != self.turn:
            self.current_board[row][col] = self.turn
            if self.can_move(next_turn):
                self.switch_turn()
            self.scores = self.compute_scores()
        else:
            raise InvalidMoveException()

        if fake_move:
            fake_board = self.current_board
            self.current_board = temp_board
            return fake_board

    def _is_valid_directional_move(self, row: int, col: int, rowdelta: int, coldelta: int, turn: str) -> bool:
        """ Given a move at specified row/col, checks in the given direction to see if
            a valid move can be made. Returns True if it can; False otherwise.
            Only supposed to be used in conjunction with _adjacent_opposite_color_directions()"""
        current_row = row + rowdelta
        current_col = col + coldelta

        last_cell_color = self._opposite_turn(turn)

        while True:
            # Immediately return false if the board reaches the end (b/c there's no blank
            # space for the cell to sandwich the other colored cell(s)
            if not self._is_valid_cell(current_row, current_col):
                break
            if self._cell_color(current_row, current_col) == NONE:
                break
            if self._cell_color(current_row, current_col) == turn:
                last_cell_color = turn
                break

            current_row += rowdelta
            current_col += coldelta

        return last_cell_color == turn

    def _adjacent_opposite_color_directions(self, row: int, col: int, turn: str) -> list[tuple]:
        """ Looks up to a possible of 8 directions surrounding the given move. If any of the
            move's surrounding cells is the opposite color of the move itself, then record
            the direction it is in and store it in a list of tuples [(rowdelta, coldelta)].
            Return the list of the directions at the end. """
        dir_list = []
        for rowdelta in range(-1, 2):
            for coldelta in range(-1, 2):
                if self._is_valid_cell(row + rowdelta, col + coldelta):
                    if self.current_board[row + rowdelta][col + coldelta] == self._opposite_turn(turn):
                        dir_list.append((rowdelta, coldelta))
        return dir_list

    def _convert_adjacent_cells_in_direction(self, row: int, col: int,
                                             rowdelta: int, coldelta: int, turn: str) -> None:
        """ If it can, converts all the adjacent/contiguous cells on a turn in
            a given direction until it finally reaches the specified cell's original color """
        if self._is_valid_directional_move(row, col, rowdelta, coldelta, turn):
            current_row = row + rowdelta
            current_col = col + coldelta

            while self._cell_color(current_row, current_col) == self._opposite_turn(turn):
                self._flip_cell(current_row, current_col)
                current_row += rowdelta
                current_col += coldelta

    def get_possible_move(self):
        """ Looks at all the empty cells in the board and return possible moves """
        possible_move = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self._cell_color(row, col) == NONE:
                    possible_directions = self._adjacent_opposite_color_directions(
                        row, col, self.turn)
                    for direction in possible_directions:
                        if self._is_valid_directional_move(row, col, direction[0], direction[1], self.turn):
                            possible_move.append((row, col))
        return possible_move

    def is_game_over(self) -> bool:
        """ Looks through every empty cell and determines if there are
            any valid moves left. If not, returns True; otherwise returns False """
        return self.can_move(BLACK) is False and self.can_move(WHITE) is False

    def can_move(self, turn: str) -> bool:
        """ Looks at all the empty cells in the board and checks to
            see if the specified player can move in any of the cells.
            Returns True if it can move; False otherwise. """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.current_board[row][col] == NONE:
                    for direction in self._adjacent_opposite_color_directions(row, col, turn):
                        if self._is_valid_directional_move(row, col, direction[0], direction[1], turn):
                            return True
        return False

    def return_winner(self) -> str:
        """ Returns the winner. ONLY to be called once the game is over.
            Returns None if the game is a TIE game."""
        black_cells, white_cells = self.compute_scores()

        if black_cells == white_cells:
            return None
        if black_cells > white_cells:
            return BLACK
        else:
            return WHITE

    def switch_turn(self) -> None:
        """ Switches the player's turn from the current one to
            the other. Only to be called if the current player
            cannot move at all. """
        self.turn = self._opposite_turn(self.turn)

    def get_board(self) -> list[list[str]]:
        """ Returns the current game's 2D board """
        return self.current_board

    def get_rows(self) -> int:
        """ Returns the number of rows the game currently has """
        return self.rows

    def get_columns(self) -> int:
        """ Returns the number of columns the game currently has """
        return self.cols

    def get_turn(self) -> str:
        """ Returns the current game's turn """
        return self.turn

    def get_scores(self, color=None):
        """ Returns the current games scores"""
        if color == BLACK:
            return self.scores[0]
        elif color == WHITE:
            return self.scores[1]
        else:
            return self.scores

    def compute_scores(self) -> tuple[int, int]:
        """ Returns the total cell count of the specified colored player """
        black = 0
        white = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.current_board[row][col] == BLACK:
                    black += 1
                elif self.current_board[row][col] == WHITE:
                    white += 1
        return black, white

    # The rest of the functions are private functions only to be used within this module
    def _flip_cell(self, row: int, col: int) -> None:
        """ Flips the specified cell over to the other color """
        self.current_board[row][col] = self._opposite_turn(
            self.current_board[row][col])

    def _cell_color(self, row: int, col: int) -> str:
        """ Determines the color/player of the specified cell """
        return self.current_board[row][col]

    def _opposite_turn(self, turn: str) -> str:
        """ Returns the player of the opposite player """
        return {BLACK: WHITE, WHITE: BLACK}[turn]

    def _require_valid_empty_space_to_move(self, row: int, col: int) -> bool:
        """ In order to move, the specified cell space must be within board boundaries
            AND the cell has to be empty """
        if self._is_valid_cell(row, col) and self._cell_color(row, col) != NONE:
            raise InvalidMoveException()

    def _is_valid_cell(self, row: int, col: int) -> bool:
        """ Returns True if the given cell move position is invalid due to
            position (out of bounds) """
        return self._is_valid_row_number(row) and self._is_valid_col_number(col)

    def _is_valid_row_number(self, row: int) -> bool:
        """ Returns True if the given row number is valid; False otherwise """
        return 0 <= row < self.rows

    def _is_valid_col_number(self, col: int) -> bool:
        """ Returns True if the given col number is valid; False otherwise """
        return 0 <= col < self.cols
