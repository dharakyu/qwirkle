import numpy as np
from collections import defaultdict
import copy
from game_board import InvalidPlayException
from random import Random

class MonteCarloTreeSearchNode():
	def __init__(self, state, player_tiles, opp_tiles, bag_of_tiles, parent=None, parent_action=None):
		self.state = state
		self.tiles = player_tiles
		#self.possible_tiles = possible_tiles
		#random_indices = list(np.random.choice(len(possible_tiles), size=6, replace=False))
		#self.tiles_from_other_player = [_, tile for i, tile in enumerate(possible_tiles) if i in random_indices]
		self.tiles_from_other_player = opp_tiles
		self.bag_of_tiles = bag_of_tiles
		self.parent = parent
		self.parent_action = parent_action
		self.children = []
		self._number_of_visits = 0
		self._score = 0
		self._untried_actions = self.get_plays(self.state, self.tiles)

	def untried_actions(self):
		return self._untried_actions

	def q(self):
		return self._score

	def n(self):
		return self._number_of_visits

	def get_plays(self, board, tiles):
		valid_starts = board.valid_plays()

		plays = []
		for (x, y) in valid_starts:
			tiles = tiles.copy()

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

	def pick_tiles(self, player_tiles, bag_of_tiles):
		rnd = Random()
		while len(player_tiles) < 6 and len(bag_of_tiles) > 0:
			i = rnd.randint(0, len(bag_of_tiles) - 1)

			player_tiles.append(bag_of_tiles.pop(i))

	def expand(self):
		action = self._untried_actions.pop()

		#board_copy = copy.deepcopy(self.state)
		#tiles_copy = copy.deepcopy(self.tiles)
		for (x, y, tile) in action['plays']:
			#if tile not in tiles_copy:
			#	breakpoint()
			self.state.play(tile, x, y)
			self.tiles.pop(self.tiles.index(tile))

		# replenish tiles for the player
		self.pick_tiles(self.tiles, self.bag_of_tiles)
		child_node = MonteCarloTreeSearchNode(self.state, self.tiles, self.tiles_from_other_player, self.bag_of_tiles, parent=self, parent_action=action)

		self.children.append(child_node)
		return child_node

	def is_terminal_node(self):
		return len(self.tiles) == 0 or len(self.tiles_from_other_player) == 0

	def rollout(self):
		breakpoint()
		current_rollout_state = copy.deepcopy(self.state)
		tiles_copy = copy.deepcopy(self.tiles)
		tiles_from_other_player_copy = copy.deepcopy(self.tiles_from_other_player)
		bag_of_tiles_copy = copy.deepcopy(self.bag_of_tiles)
		
		move = 0
		while True:
			#breakpoint()
			# opponent goes
			print(move)
			#breakpoint()
			state_copy = copy.deepcopy(current_rollout_state)
			opp_possible_moves = self.get_plays(state_copy, tiles_from_other_player_copy)
			if len(opp_possible_moves) == 0:
				#breakpoint()
				# replace all the tiles
				bag_of_tiles_copy += tiles_from_other_player_copy
				tiles_from_other_player_copy = []

			else:
				opp_action = self.rollout_policy(opp_possible_moves)

				for (x, y, tile) in opp_action['plays']:
					current_rollout_state.play(tile, x, y)
					tiles_from_other_player_copy.pop(tiles_from_other_player_copy.index(tile))

			#print(current_rollout_state._board)
			self.pick_tiles(tiles_from_other_player_copy, bag_of_tiles_copy)

			if len(tiles_from_other_player_copy) == 0:
				break

			breakpoint()
			state_copy = copy.deepcopy(current_rollout_state)
			possible_moves = self.get_plays(state_copy, tiles_copy)
			if len(possible_moves) == 0:
				#breakpoint()
				# replace all the tiles
				bag_of_tiles_copy += tiles_copy
				tiles_copy = []
			else:
				action = self.rollout_policy(possible_moves)

				for (x, y, tile) in action['plays']:
					current_rollout_state.play(tile, x, y)
					tiles_copy.pop(tiles_copy.index(tile))
			
			#print(current_rollout_state._board)
			self.pick_tiles(tiles_copy, bag_of_tiles_copy)

			if len(tiles_copy) == 0:
				break

			move += 1
		#breakpoint()
		return current_rollout_state.score()

	def backpropagate(self, reward):
		self._number_of_visits += 1.
		self._score += reward
		if self.parent:
			self.parent.backpropagate(reward)

	def is_fully_expanded(self):
		return len(self._untried_actions) == 0

	def best_child(self, c_param=0.1):
		choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
		return self.children[np.argmax(choices_weights)]

	def rollout_policy(self, possible_moves):
		return possible_moves[np.random.randint(len(possible_moves))]

	def _tree_policy(self):
		current_node = self
		while not current_node.is_terminal_node():
			
			if not current_node.is_fully_expanded():
				return current_node.expand()
			else:
				current_node = current_node.best_child()
		return current_node

	def best_action(self):
		simulation_no = 100
		
		#breakpoint()
		for i in range(simulation_no):
			
			v = self._tree_policy()
			reward = v.rollout()
			v.backpropagate(reward)
		
		return self.best_child(c_param=0.)


