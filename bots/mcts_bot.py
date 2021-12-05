import copy
import random
import numpy as np
from player import Player
from game_board import InvalidPlayException
from MCTSNode import MonteCarloTreeSearchNode
from game_board import GameBoard, Piece, SHAPES, COLORS


class MctsBot(Player):
    #def __init__(self, name, bag_of_tiles):
    #    super().__init__(name)
    #    self.bag_of_tiles = bag_of_tiles
    def _generate_new_bag_of_tiles(self):
        all_tiles = []

        shapes = [
            SHAPES.CIRCLE,
            SHAPES.DIAMOND,
            SHAPES.SPARKLE,
            SHAPES.SQUARE,
            SHAPES.STAR,
            SHAPES.TRIANGLE
        ]

        colors = [
            COLORS.BLUE,
            COLORS.CYAN,
            COLORS.GREEN,
            COLORS.MAGENTA,
            COLORS.RED,
            COLORS.YELLOW
        ]

        for i in range(3):
            for c in range(len(colors)):
                for s in range(len(shapes)):
                    all_tiles.append(Piece(color=colors[c], shape=shapes[s]))

        return all_tiles

    def play_turn(self, board, bag_of_tiles):

        #plays = self.get_plays(board)
        board_copy = copy.deepcopy(board)

        all_tiles = self._generate_new_bag_of_tiles()
        tiles_copy = copy.deepcopy(self._tiles)
        bag_of_tiles = copy.deepcopy(bag_of_tiles)
        tiles_on_board = board.get_tiles_on_board()

        # get all the tiles including the unknown ones
        possible_tiles = list(set(all_tiles) - set(tiles_copy + tiles_on_board))

        randomized_tiles_from_other_player = list(np.random.choice(possible_tiles, size=6, replace=False))
        randomized_bag_of_tiles = list(set(possible_tiles) - set(randomized_tiles_from_other_player))

        #breakpoint()
        root = MonteCarloTreeSearchNode(state=board_copy, player_tiles=tiles_copy, opp_tiles=randomized_tiles_from_other_player, bag_of_tiles=randomized_bag_of_tiles)
        selected_node = root.best_action()
        breakpoint()
        # To do: take action that maximizes avg value
        random_play = plays[random.randint(0, len(plays)-1)]

        for (x, y, tile) in random_play['plays']:
            board.play(tile, x, y)
            self._tiles.pop(self._tiles.index(tile))