class KeyRegistry:
	def __init__(self):
		self.doors = {}
		
	def RegisterDoor(self, map, dungeon, x, y, color):
		index = GetIndexForDoor(self, map, dungeon, x, y, color)
		above = GetIndexForDoor(self, map, dungeon, x, y - 1, color)
		if self.doors.get(index) == None:
			if self.doors.get(above) == None:
				self.doors[index] = 'registered'
		
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
		if GetKeyCount(dungeon, color) > 0:
			if self.IsDoorLocked(map, dungeon, x, y, color):
				self.SetVar(GetKeyCountIndex(dungeon, color), GetKeyCount(dungeon, color) - 1)
				self.SetVar(GetPreferredIndexForDoor(map, dungeon, x, y, color), 1)
				return True
		return False
	
	def GetKeyCountIndex(self, dungeon, color):
		return 'key_registry_count_' + dungeon + '_' + color
	
	def GetKeyCount(self, dungeon, color):
		index = self.GetKeyCountIndex(dungeon, color)
		count = GetVar(index)
		if count == None:
			return 0
		return count
	
	def GetVar(self, var):
		return ActiveGameContext().GetVar(var)
	def SetVar(self, var, value):
		ActiveGameContext().SetSavedVar(var, value)