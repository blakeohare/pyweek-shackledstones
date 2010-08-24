"""
common variables:

name - player name

The following indicate which items the player has. They are either 1 or None

item_sabre
item_hammer
item_drill
item_hook
item_cannon
item_cannon_fire
item_cannon_ice
item_cannon_multi

The following holds one of the above to indicate what each button has assigned
equipped_a
equipped_b
equipped_x
equipped_y

"""
class GameInstance:
	def __init__(self, slot):
		self.slot = slot
		self.values = self.parse(slot)
		self.temp_vars = {}
		self.active_game_scene = None
	
	def GetVar(self, varName):
		value = self.temp_vars.get(varName)
		if value == None:
			return self.values.get(varName)
		return None
	
	def SetActiveGameScene(self, game_scene):
		self.active_game_scene = game_scene
	def GetActiveGameScene(self):
		return self.active_game_scene
	
	def SetSavedVar(self, name, value):
		self.values[name] = value
	def SetTempVar(self, name, value):
		self.temp_vars[name] = value
	
	def parse(self, slot):
		values = {}
		c = open('saves' + os.sep + 'slot' + str(slot) + '.txt', 'rt')
		lines = trim(c.read()).split('\n')
		c.close()
		for line in lines:
			parts = trim(line).split(':')
			if len(parts) > 1:
				name = trim(parts[0])
				value = trim(':'.join(parts[1:]))
				if len(name) > 1 and name[0] in '$#':
					if name[0] == '#':
						value = int(value)
					name = name[1:]
					values[name] = value
		return values
	
	def SaveToFile(self):
		output = []
		for key in self.values.keys():
			value = self.values[key]
			if str(value) == value:
				name = '$' + key
			else:
				name = '#' + key
			
			output.append(name + ':' + str(value))
		c = open('saves' + os.sep + 'slot' + str(self.slot) + '.txt', 'wt')
		c.write('\r\n'.join(output))
		c.close()

class GameContext:
	
	def __init__(self):
		for i in (1, 2, 3):
			file = 'saves' + os.sep + 'slot' + str(i) + '.txt'
			if not os.path.exists(file):
				c = open(file, 'wt')
				c.write(' ')
				c.close()
		self.slots = [GameInstance(1), GameInstance(2), GameInstance(3)]
		self.active_game = None

	def SetActiveGame(self, slot_num):
		self.active_game = self.slots[slot_num - 1]
		
	def GetActiveGame(self):
		return self.active_game
	
	def SetPlayerName(self, slot_num, name):
		self.slots[slot_num - 1].SetSavedVar('name', name)
	
	def GetPlayerName(self, slot_num):
		return self.slots[slot_num - 1].GetVar('name')
	
	def DeletePlayer(self, slot_num):
		game = self.slots[slot_num - 1]
		
		#shut up
		game.temp_vars = {}
		game.values = {}
		
		game.SaveToFile()
	
	def CopyPlayer(self, from_slot, to_slot):
		if from_slot != to_slot:
			from_game = self.slots[from_slot - 1]
			to_game = self.slots[to_slot - 1]
			
			to_game.values = from_game.values
			to_game.SaveToFile()
			
			# this will ensure that the dictionary instance is different from from_game
			self.slots[to_slot - 1] = GameInstance(to_slot)
			
### STATIC ###

_gameContext = GameContext()

def ActiveGame():
	global _gameContext
	return _gameContext.GetActiveGame()

def GameContext():
	global _gameContext
	return _gameContext