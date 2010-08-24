
class Tile:
	def __init__(self, id_list):
		self.orig_stack = id_list[:]
		self.id = None
		self.is_blank = False
		self.initialize()
		
	def SetTile(self, detaillayer, id):
		index = {'base' : 0, 'baseadorn' : 1, 'baseextra' : 2, 'doodad' : 3, 'doodadadorn' : 4, 'excessive' : 5 }[detaillayer]
		self.orig_stack[index] = id
		self.initialize()
		
	
	def initialize(self):
		tile_stack = []
		no_animations = True
		for id in self.orig_stack:
			if trim(id) != '':
				tile = _tileStore.GetTile(id)
				if tile.physics == 'floor':
					tile_stack = []
					no_animations = True
				tile_stack.append(tile)
				if tile.num_images > 1:
					no_animations = False
		self.stack = tile_stack
		if no_animations:
			self.Render = self._static_render
		elif len(tile_stack) == 0:
			self.Render = self._dont_render
			self.is_blank = True
		else:
			self.Render = self._animation_render
		
		self.submerged = False
		self.ice = False
		self.keytype = None
		
		self.composite_physics()
	
	def SetId(self, id):
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
			else:
				if tphys == 'water': self.submerged = True
				elif tphys == 'ice': self.ice = True
				
				elif tphys == 'redkey': self.keytype = 'red'
				elif tphys == 'bluekey': self.keytype = 'blue'
				elif tphys == 'greenkey': self.keytype = 'green'
				elif tphys == 'yellowkey': self.keytype = 'yellow'
				
				if self.keytype != None:
					physics = [False, False, False, False]
					break

		self.physics = 'xo'[physics[0]] + 'xo'[physics[1]] + 'xo'[physics[2]] + 'xo'[physics[3]]
	
	def is_stair_tile(self):
		self.physics = 'xxxx'
		self.Render = self._dont_render

	def _animation_render(self, screen, x, y, render_counter):
		for tile in self.stack:
			tile.Render(screen, x, y, render_counter)
	
	def _static_render(self, screen, x, y, render_counter):
		for tile in self.stack:
			screen.blit(tile.images[0], (x, y))
	
	def _dont_render(self, screen, x, y, render_counter):
		pass
			