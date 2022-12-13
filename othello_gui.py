''' This is the main file for the Othello game. It creates the game and the GUI and starts the game.
'''

import importlib
import othello
import othello_models
import tkinter

# Default / Initial Game Settings
DEFAULT_ROWS = 7
DEFAULT_COLUMNS = 9

# GUI Constants
BACKGROUND_COLOR = othello_models.BACKGROUND_COLOR
GAME_HEIGHT = 400
GAME_WIDTH = 400
WAITING_TIME = 400 # adding a extra time in ms to see better the development

class OthelloGUI:
    def __init__(self):
        # Initial Game Settings
        self._rows = DEFAULT_ROWS
        self._columns = DEFAULT_COLUMNS
        self._black_name = "Human"
        self._white_name = "Human"
        self._white_ai = None
        self._black_ai = None

        # Create my othello gamestate here (drawn from the original othello game code)
        self._game_state = othello.OthelloGame(self._rows, self._columns,
                                               othello.BLACK)

        # Initialize all my widgets and window here
        self._root_window = tkinter.Tk()
        self._root_window.configure(background=BACKGROUND_COLOR)
        self._black_player = othello_models.Player(self._black_name, self._root_window)
        self._white_player = othello_models.Player(self._white_name, self._root_window)
        self._board = othello_models.GameBoard(self._game_state, GAME_WIDTH, GAME_HEIGHT, self._root_window)
        self._black_score = othello_models.Score(othello.BLACK, self._game_state, self._root_window)
        self._white_score = othello_models.Score(othello.WHITE, self._game_state, self._root_window)
        self._player_turn = othello_models.Turn(self._game_state, self._root_window)

        # Bind my game board with these two events.
        self._board.get_board().bind('<Configure>', self._on_board_resized)
        self._board.get_board().bind('<Button-1>', self._on_board_clicked)

        # Create our menu that can be accessed at the top of the GUI
        self._menu_bar = tkinter.Menu(self._root_window)
        self._game_menu = tkinter.Menu(self._menu_bar, tearoff=0)
        self._game_menu.add_command(label='New Game', command=self._new_game)
        self._game_menu.add_command(label='Game Settings', command=self._configure_game_settings)
        self._game_menu.add_separator()
        self._game_menu.add_command(label='Exit', command=self._root_window.destroy)
        self._menu_bar.add_cascade(label='Game', menu=self._game_menu)

        # Layout all the widgets here using grid layout
        self._root_window.config(menu=self._menu_bar)
        self._black_player.get_player_label().grid(row=0, column=0, sticky=tkinter.S)
        self._white_player.get_player_label().grid(row=0, column=1, sticky=tkinter.S)
        self._black_score.get_score_label().grid(row=1, column=0,
                                                 sticky=tkinter.S)
        self._white_score.get_score_label().grid(row=1, column=1,
                                                 sticky=tkinter.S)
        self._board.get_board().grid(row=2, column=0, columnspan=2,
                                     padx=50, pady=10,
                                     sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W)
        self._player_turn.get_turn_label().grid(row=3, column=0, columnspan=2,
                                                padx=10, pady=10)

        # Configure the root window's row/column weight (from the grid layout)
        self._root_window.rowconfigure(0, weight=1)
        self._root_window.rowconfigure(1, weight=1)
        self._root_window.rowconfigure(2, weight=1)
        self._root_window.columnconfigure(0, weight=1)
        self._root_window.columnconfigure(1, weight=1)

    def start(self) -> None:
        ''' Runs the mainloop of the root window '''
        self._root_window.mainloop()

    def _configure_game_settings(self) -> None:
        ''' Pops out an options window to configure the game settings '''
        dialog = othello_models.OptionDialog(self._rows, self._columns, self._black_name, self._white_name)
        dialog.show()
        if dialog.was_ok_clicked():
            self._rows = dialog.get_rows()
            self._columns = dialog.get_columns()
            self._black_name = dialog.get_black_name()
            self._white_name = dialog.get_white_name()
            self._black_ai = None
            self._white_ai = None
            # Create a new game with these settings now
            self._new_game()

    def _new_game(self) -> None:
        ''' Creates a new game with current _game_state settings '''
        self._game_state = othello.OthelloGame(self._rows, self._columns,
                                               othello.BLACK)
        self._board.new_game_settings(self._game_state)
        self._board.redraw_board()
        self._black_player.update_name(self._black_name)
        self._white_player.update_name(self._white_name)
        self._black_score.update_score(self._game_state)
        self._white_score.update_score(self._game_state)
        self._player_turn.update_turn(self._game_state.get_turn())
        if self._white_name != "Human": # import the ai module if not human
            self._white_ai = getattr(importlib.import_module(f"ai.{self._white_name}"), f"{self._white_name}")()
        if self._black_name != "Human": # imports the ai module if not human
            self._black_ai = getattr(importlib.import_module(f"ai.{self._black_name}"), f"{self._black_name}")()
            self._play_ai()

    def _on_board_clicked(self, event: tkinter.Event) -> None:
        ''' Attempt to play a move on the board if it's valid '''
        if self._game_state.get_turn() == othello.BLACK and self._black_name == "Human":
            move = self._convert_point_coord_to_move(event.x, event.y)
            row = move[0]
            col = move[1]
            self._play(row, col)
        elif self._game_state.get_turn() == othello.WHITE and self._white_name == "Human":
            move = self._convert_point_coord_to_move(event.x, event.y)
            row = move[0]
            col = move[1]
            self._play(row, col)

    def _play(self, row, col):
        try:
            self._game_state.move(row, col)
            self._board.update_game_state(self._game_state)
            self._board.redraw_board()
            self._black_score.update_score(self._game_state)
            self._white_score.update_score(self._game_state)

            if self._game_state.is_game_over():
                self._player_turn.display_winner(self._game_state.return_winner())
            else:
                self._player_turn.switch_turn(self._game_state)
                self._root_window.after(WAITING_TIME, self._play_ai)
                # self._play_ai()

        except othello.InvalidMoveException:
            if self._game_state.get_turn() == othello.BLACK and self._black_name != "Human":
                self._player_turn.display_cheater(othello.BLACK, row, col)
            elif self._game_state.get_turn() == othello.WHITE and self._white_name != "Human":
                self._player_turn.display_cheater(othello.WHITE, row, col)
        except othello.InvalidTypeException:
            if self._game_state.get_turn() == othello.BLACK and self._black_name != "Human":
                self._player_turn.display_type_error(othello.BLACK, row, col)
            elif self._game_state.get_turn() == othello.WHITE and self._white_name != "Human":
                self._player_turn.display_type_error(othello.WHITE, row, col)
            pass

    def _convert_point_coord_to_move(self, pointx: int, pointy: int):
        ''' Converts canvas point to a move that can be inputted in the othello game '''
        row = int(pointy // self._board.get_cell_height())
        if row == self._board.get_rows():
            row -= 1
        col = int(pointx // self._board.get_cell_width())
        if col == self._board.get_columns():
            col -= 1
        return row, col

    def _on_board_resized(self, event: tkinter.Event) -> None:
        ''' Called whenever the canvas is resized '''
        self._board.redraw_board()

    def _play_ai(self):
        ''' Plays an AI move '''
        if self._game_state.get_turn() == othello.BLACK and self._black_ai is not None:
            move = self._black_ai.next_move(self._game_state.copy_game())
            self._play(move[0], move[1])
        elif self._game_state.get_turn() == othello.WHITE and self._white_ai is not None:
            move = self._white_ai.next_move(self._game_state.copy_game())
            self._play(move[0], move[1])


if __name__ == '__main__':
    OthelloGUI().start()
