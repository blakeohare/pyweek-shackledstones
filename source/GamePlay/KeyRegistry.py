class KeyRegistry:
	def __init__(self):
		self.doors = {}
		
	def registerDoor(self, map, dungeon, x, y, color):
		index = self.getIndexForDoor(map, dungeon, x, y, color)
		above = self.getIndexForDoor(map, dungeon, x, y - 1, color)
		if self.doors.get(index) == None:
			if self.doors.get(above) == None:
				self.doors[index] = 'registered'
				return True
		return False
		
	def getIndexForDoor(self, map, dungeon, x, y, color):
		return 'keyregistry_' + '[' + map + ']' + dungeon + '_' + str(x) + '_' + str(y) + '_' + color
	
	def getPreferredIndexForDoor(self, map, dungeon, x, y, color):
		index = self.getIndexForDoor(map, dungeon, x, y, color)
		if self.doors.get(index) == None:
			index = self.getIndexForDoor(map, dungeon, x, y - 1, color)
		return index
	
	def isDoorLocked(self, map, dungeon, x, y, color):
		return self.getVar(self.getPreferredIndexForDoor(map, dungeon, x, y, color)) != 1
	
	def useKey(self, dungeon, color, map, x, y):
		if self.getKeyCount(dungeon, color) > 0:
			if self.isDoorLocked(map, dungeon, x, y, color):
				self.SetVar(self.getKeyCountIndex(dungeon, color), self.getKeyCount(dungeon, color) - 1)
				self.SetVar(self.getPreferredIndexForDoor(map, dungeon, x, y, color), 1)
				play_sound("unlock")
				return True
		return False
	
	def getKeyCountIndex(self, dungeon, color):
		return 'key_registry_count_' + dungeon + '_' + color
	
	def getKeyCount(self, dungeon, color):
		index = self.getKeyCountIndex(dungeon, color)
		count = self.getVar(index)
		if count == None:
			return 0
		return count
	
	def addKey(self, dungeon, color):
		index = self.getKeyCountIndex(dungeon, color)
		count = self.getVar(index)
		if count == None: count = 0
		self.SetVar(index, count + 1)
	
	def getVar(self, var):
		return getActiveGame().getVar(var)
	def SetVar(self, var, value):
		getActiveGame().setSavedVar(var, value)

### STATIC ###

_key_registry = KeyRegistry()
def getKeyRegistry():
	global _key_registry
	return _key_registry
