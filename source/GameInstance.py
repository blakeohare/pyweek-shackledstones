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
item_compass
item_shovel

The following holds one of the above to indicate what each button has assigned
equipped_a
equipped_b
equipped_x
equipped_y

The following will be used to track which stones a play has acquired
stone_water
stone_light
stone_life
stone_fire
stone_dark
stone_death

The following will be used to track which temples have been completed
A temple is complete when the stone is replaced on the altar
finish_water
finish_light
finish_dark
finish_fire
finish_life
finish_death

Used to indicate which area of the world we're in (stores the map name)
current_zone
"""
class GameInstance:
	def __init__(self, slot):
		self.slot = slot
		self.values = self.parse(slot)
		self.temp_vars = {}
		self.active_game_scene = None
	
	def getBool(self, varName):
		value = self.temp_vars.get(varName)
		if value == None:
			value = self.values.get(varName)
		if value == None: return False
		if value == '': return False
		if value == 0: return False
		return True
		
	
	def getInt(self, varName, defaultValue = 0):
		value = self.temp_vars.get(varName)
		if value == None:
			value = self.values.get(varName)
		if value == None:
			return defaultValue
		if Core.isString(value):
			return Core.parseInt(value)
		return value
	
	def getString(self, varName):
		value = self.temp_vars.get(varName)
		if value == None:
			value = self.values.get(varName)
		if value == None:
			return ''
		return str(value)
	
	def _getVar(self, varName):
		value = self.temp_vars.get(varName)
		if value == None:
			return self.values.get(varName)
		return value
	
	def setActiveGameScene(self, game_scene):
		self.active_game_scene = game_scene

	def getActiveGameScene(self):
		return self.active_game_scene
	
	def setSavedVar(self, name, value):
		self.values[name] = value

	def setTempVar(self, name, value):
		self.temp_vars[name] = value
   
	def parse(self, slot = None):
		if slot == None:
			slot = self.slot
		values = {}
		lines = UserData.fileReadText('slot' + str(slot) + '.txt').strip().split('\n')
		
		for line in lines:
			parts = line.strip().split(':')
			if len(parts) > 1:
				name = parts[0].strip()
				value = ':'.join(parts[1:]).strip()
				if len(name) > 1 and name[0] in '$#':
					if name[0] == '#':
						value = int(value)
					name = name[1:]
					values[name] = value
		return values

	def setZone(self, newVal):
		self.setTempVar('current_zone', newVal)
	
	def saveToFile(self):
		output = []
		for key in self.values.keys():
			value = self.values[key]
			if str(value) == value:
				name = '$' + key
			else:
				name = '#' + key
			output.append(name + ':' + str(value))
		UserData.fileWriteText('slot' + str(self.slot) + '.txt', '\n'.join(output))
