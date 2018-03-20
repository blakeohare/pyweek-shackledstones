class KeyRegistry:
	def __init__(self):
		self.doors = {}
		
	def RegisterDoor(self, map, dungeon, x, y, color):
		index = self.GetIndexForDoor(map, dungeon, x, y, color)
		above = self.GetIndexForDoor(map, dungeon, x, y - 1, color)
		if self.doors.get(index) == None:
			if self.doors.get(above) == None:
				self.doors[index] = 'registered'
				return True
		return False
		
	def GetIndexForDoor(self, map, dungeon, x, y, color):
		return 'keyregistry_' + '[' + map + ']' + dungeon + '_' + str(x) + '_' + str(y) + '_' + color
	
	def GetPreferredIndexForDoor(self, map, dungeon, x, y, color):
		index = self.GetIndexForDoor(map, dungeon, x, y, color)
		if self.doors.get(index) == None:
			index = self.GetIndexForDoor(map, dungeon, x, y - 1, color)
		return index
	
	def IsDoorLocked(self, map, dungeon, x, y, color):
		return self.GetVar(self.GetPreferredIndexForDoor(map, dungeon, x, y, color)) != 1
	
	def UseKey(self, dungeon, color, map, x, y):
		if self.GetKeyCount(dungeon, color) > 0:
			if self.IsDoorLocked(map, dungeon, x, y, color):
				self.SetVar(self.GetKeyCountIndex(dungeon, color), self.GetKeyCount(dungeon, color) - 1)
				self.SetVar(self.GetPreferredIndexForDoor(map, dungeon, x, y, color), 1)
				play_sound("unlock")
				return True
		return False
	
	def GetKeyCountIndex(self, dungeon, color):
		return 'key_registry_count_' + dungeon + '_' + color
	
	def GetKeyCount(self, dungeon, color):
		index = self.GetKeyCountIndex(dungeon, color)
		count = self.GetVar(index)
		if count == None:
			return 0
		return count
	
	def AddKey(self, dungeon, color):
		index = self.GetKeyCountIndex(dungeon, color)
		count = self.GetVar(index)
		if count == None: count = 0
		self.SetVar(index, count + 1)
	
	def GetVar(self, var):
		return ActiveGame().GetVar(var)
	def SetVar(self, var, value):
		ActiveGame().SetSavedVar(var, value)

### STATIC ###

_key_registry = KeyRegistry()
def GetKeyRegistry():
	global _key_registry
	return _key_registry
