
class GameContext:
	
	def __init__(self):
		for i in (1, 2, 3):
			file = 'saves/slot' + str(i) + '.txt'
			if not file_exists(file):
				write_text_file(file, ' ')
		self.slots = [GameInstance(1), GameInstance(2), GameInstance(3)]
		self.active_game = None

	def setActiveGame(self, slot_num):
		self.active_game = self.slots[slot_num - 1]
	
	def getPlayerName(self, slot_num):
		return self.slots[slot_num - 1].getVar('name')

	def getStones(self, slot_num):
		r = []
		s = self.slots[slot_num - 1]
		for st in ['water', 'light', 'dark', 'fire', 'life', 'death']:
			if s.getVar('stone_' + st):
				r.append(st)
		return r

	def deletePlayer(self, slot_num):
		game = self.slots[slot_num - 1]
		
		game.temp_vars = {}
		game.values = {}
		
		game.saveToFile()

def getActiveGame():
	global _gameContext
	if _gameContext == None:
		_gameContext = GameContext()
	return _gameContext.active_game

def getGameContext():
	global _gameContext
	if _gameContext == None:
		_gameContext = GameContext()
	return _gameContext
