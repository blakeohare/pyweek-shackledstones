class Tile:
	def __init__(self, id_list):
		self.orig_stack = id_list[:]
		self.id = None
		self.is_blank = False
		self.initialize()
		
	def setTile(self, detaillayer, id):
		index = {'base' : 0, 'baseadorn' : 1, 'basedetail' : 2, 'doodad' : 3, 'doodadadorn' : 4, 'excessive' : 5 }[detaillayer]
		self.orig_stack[index] = id
		self.initialize()
	
	def chopTheBushes(self):
		i = 0
		found = False
		while i < len(self.orig_stack):
			if self.orig_stack[i] == 'nature20':
				self.orig_stack[i] = 'nature21'
				found = True
			i += 1
		if found:
			self.initialize()

	def smashBoulders(self):
		i = 0
		found = False
		while i < len(self.orig_stack):
			if self.orig_stack[i] == 'boulder1':
				self.orig_stack[i] = ''
				found = True
			i += 1
		if found:
			self.initialize()

	def drillThrough(self):
		i = 0
		found = False
		while i < len(self.orig_stack):
			if self.orig_stack[i] in '49 50 51 52 124 125 126 127 d49 d50 d51 d52 r49 r50 r51 r52 green49 green50 green51 green52 indigo49 indigo50 indigo51 indigo52'.split(' '):
				self.orig_stack[i] = ''
				found = True
			i += 1
		if found:
			self.initialize()
		
	def removeKey(self):
		i = 0
		found = False
		tileStore = get_tile_store()
		while i < len(self.orig_stack):
			id = self.orig_stack[i]
			tt = tileStore.getTile(id)
			if tt != None and tt.physics.endswith('key'):
				self.orig_stack[i] = ''
				found = True
			i += 1
		if found:
			self.initialize()
	
	def initialize(self):
		tile_stack = []
		no_animations = True
		self.door_color = None
		self.is_grappleable = False
		tileStore = get_tile_store()
		for id in self.orig_stack:
			if id.strip() != '':
				if id == '63':
					self.is_grappleable = True
				tile = tileStore.getTile(id)
				if tile.physics == 'floor':
					tile_stack = []
					no_animations = True
				if tile.physics.endswith('key'):
					self.door_color = tile.physics[:-3]
					self.physics = 'xxxx'
				tile_stack.append(tile)
				if tile.num_images > 1:
					no_animations = False
		self.stack = tile_stack
		if len(tile_stack) == 0:
			self.render = self._dont_render
			self.is_blank = True
		elif no_animations:
			self.render = self._static_render
		else:
			self.render = self._animation_render
		
		self.submerged = False
		self.ice = False
		self.keytype = None
		
		self.composite_physics()
	
	def setId(self, id):
		self.id = id
	
	def composite_physics(self):
		if len(self.stack) == 0:
			self.physics = 'xxxx'
			return
		
		physics = [True, True, True, True]
		for tile in self.stack:
			tphys = tile.physics
			if tphys == 'floor': tphys = 'oooo'
			if len(tphys) == 4 and tphys[0] in 'ox' and tphys[1] in 'ox' and tphys[2] in 'ox' and tphys[3] in 'ox':
				for i in (0,1,2,3):
					physics[i] = physics[i] and tphys[i] == 'o'
				self.submerged = False
			else:
				if tphys == 'water': self.submerged = True
				elif tphys == 'ice': self.ice = True
				
				elif tphys == 'redkey': self.keytype = 'red'
				elif tphys == 'bluekey': self.keytype = 'blue'
				elif tphys == 'greenkey': self.keytype = 'green'
				elif tphys == 'yellowkey': self.keytype = 'yellow'
				elif tphys == 'whitekey': self.keytype = 'white'
				elif tphys == 'blackkey': self.keytype = 'black'
				if self.keytype != None:
					physics = [False, False, False, False]
					break

		self.physics = 'xo'[physics[0]] + 'xo'[physics[1]] + 'xo'[physics[2]] + 'xo'[physics[3]]
	
	def is_stair_tile(self):
		self.physics = 'xxxx'
		self.Render = self._dont_render

	def _animation_render(self, screen, x, y, render_counter):
		for tile in self.stack:
			tile.render(screen, x, y, render_counter)
	
	def _static_render(self, screen, x, y, render_counter):
		for tile in self.stack:
			tile.images[0].draw(x, y)
	
	def _dont_render(self, screen, x, y, render_counter):
		pass
