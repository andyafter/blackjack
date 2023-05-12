import csv

class StrategyImporter(object):
	"""
	"""
	hard_strategy = {}
	soft_strategy = {}
	pair_strategy = {}
	knight_strategy={}
	dealer_strategy = {}

	def __init__(self, player_file):
		self.player_file = player_file

	def import_player_strategy(self):
		hard = 21
		soft = 21
		pair = 20
		knight = 20

		with open(self.player_file, 'r') as player_csv:
			reader = csv.DictReader(player_csv, delimiter = ';')
			for row in reader:
				if hard >= 4:
					self.hard_strategy[hard] = row
					hard -= 1 
				elif soft >= 12:
					self.soft_strategy[soft] = row
					soft -= 1
				elif pair >= 4:
					self.pair_strategy[pair] = row
					pair -= 2
				elif knight >= 4:
					self.knight_strategy[knight] = row
					knight -= 2

		return self.hard_strategy, self.soft_strategy, self.pair_strategy, self.knight_strategy