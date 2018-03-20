class Layer:
	def __init__(self, width, height):
		self.contains_stuff = False
		self.width = width
		self.height = height

	def SetTiles(self, tile_list):
		self.tiles = make_table(self.width, self.height)
		self.contains_stuff = True
		
		top = self.height - 1
		bottom = 0
		left = self.width - 1
		right = 0
		
		y = 0
		while y < self.height:
			x = 0
			while x < self.width:
				tl = tile_list[x + y * self.width]
				self.tiles[x][y] = tl
				if not tl.is_blank:
					top = min(y, top)
					bottom = max(y, bottom)
					left = min(x, left)
					right = max(x, right)
				x += 1
			y += 1
		
		self.top = top
		self.bottom = bottom
		self.left = left
		self.right = right

	def MarkStairTile(self, x, y):
		self.tiles[x][y].is_stair_tile()
	
	def GetPhysics(self, x, y, blank_blocked):
		if x >= 0 and x < self.width and y >= 0 and y < self.height:
			
			if not blank_blocked and self.tiles[x][y].is_blank:
				return 'oooo'
			return self.tiles[x][y].physics
		return 'xxxx'
	
	def RunScript(self, x, y):
		if self.contains_stuff:
			if x >= 0 and x < self.width and y >= 0 and y < self.height:
				tile = self.tiles[x][y]
				if tile.id != None:
					script = tile.id.script
					if script != None and script != '':
						go_script_go(script)
	
	def Render(self, screen, x_offset, y_offset, render_counter):
		width = self.width
		height = self.height
		tiles = self.tiles
		
		left = max(self.left, int(x_offset / -16) - 2)
		top = max(self.top, int(y_offset / -16) - 2)
		right = min(left + 24 + 4, self.right + 1)
		bottom = min(top + 18 + 4, self.bottom + 1)
		
		y = top
		while y < bottom:
			x = left
			while x < right:
				tiles[x][y].Render(screen, x * 16 + x_offset, y * 16 + y_offset, render_counter)
				x += 1
			y += 1
