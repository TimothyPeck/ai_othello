''' Example of a random AI. The class name has to be the same as the module name.
'''

# postpones the evaluation of the type hints, hence they do not need to be imported
from __future__ import annotations
import random

import othello


class Random:
    '''The name of this class must be the same as its file.

    '''

    def __init__(self):
        pass

    def next_move(self, board: othello.OthelloGame) -> tuple[int, int]:
        """Returns the next move to play.

        Args:
            board (othello.OthelloGame): _description_

        Returns:
            tuple[int, int]: the next move (for instance: (2, 3) for (row, column), starting from 0)
        """

        legal_moves = board.get_possible_move()
        return random.choice(legal_moves)

    def __str__(self):
        return "Random"
