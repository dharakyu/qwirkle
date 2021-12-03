import copy
import random
import numpy as np
from player import Player
from game_board import InvalidPlayException


class MctsBot(Player):

    def get_plays(self, board):
        valid_starts = board.valid_plays()

        plays = []
        for (x, y) in valid_starts:
            tiles = self._tiles.copy()

            for i in range(len(tiles)):
                tile_played = False
                try:
                    board.play(tiles[i], x=x, y=y)
                    plays.append({
                        'plays': [(x, y, tiles[i])],
                        'score': board.score()
                    })
                    tiles_remaining = tiles.copy()
                    tiles_remaining.pop(i)
                    tile_played = True
                except InvalidPlayException:
                    pass

                while tile_played:
                    tile_played = False
                    for (nx, ny) in board.valid_plays():
                        for j in range(len(tiles_remaining)):
                            try:
                                board.play(tiles_remaining[j], x=nx, y=ny)
                                plays[-1]['plays'].append((nx, ny, tiles_remaining[j]))
                                plays[-1]['score'] = board.score()
                                tiles_remaining.pop(j)
                                tile_played = True
                                break
                            except InvalidPlayException:
                                pass

            board.reset_turn()
        return plays


    def calc_ucb1(s, a, Q, N):
        
        # Exploration parameter
        c = 2

        if N[(s, a)] == 0:
            return np.inf
        Ns = sum([N[pair] for pair in N.keys() if pair[0]==s])
        return Q[(s, a)] + c*np.sqrt(np.log(Ns) / N[(s, a)])
        

    def play_turn(self, board, bag_of_tiles):

        plays = self.get_plays(board)

        # Iterations parameter
        m = 10


        ucb1_vals = []
        Q = {}
        N = {}

        for i in range(m):
            while True:
                A = get_plays()
                if N[curr_state][curr_action] == 0:
                    pass
                    # do a rollout


        if len(plays) == 0:
            return

        # To do: take action that maximizes avg value
        random_play = plays[random.randint(0, len(plays)-1)]

        for (x, y, tile) in random_play['plays']:
            board.play(tile, x, y)
            self._tiles.pop(self._tiles.index(tile))