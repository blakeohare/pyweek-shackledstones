
class GameContext:
	
	def __init__(self):
		for i in (1, 2, 3):
			file = 'slot' + str(i) + '.txt'
			if not UserData.fileExists(file):
				UserData.fileWriteText(file, ' ')
		self.slots = [GameInstance(1), GameInstance(2), GameInstance(3)]
		self.active_game = None

	def setActiveGame(self, slot_num):
		self.active_game = self.slots[slot_num - 1]
	
	def getPlayerName(self, slot_num):
		return self.slots[slot_num - 1].getString('name')

	def getStones(self, slot_num):
		r = []
		s = self.slots[slot_num - 1]
		for st in ['water', 'light', 'dark', 'fire', 'life', 'death']:
			if s.getBool('stone_' + st):
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
