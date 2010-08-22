
class TileTemplate:
	def __init__(self, parts):
		self.id = parts[0]
		self.physics = parts[2]
		self.imagefiles = parts[3].split('|')
		
		images = []
		for img in self.imagefiles:
			images.append(get_image('tiles' + os.sep + trim(img)))
		self.images = images
		
		if len(parts) == 5:
			self.anim_delay = int(parts[4])
		else:
			self.anim_delay = 4
		self.num_images = len(self.images)
		
	def Render(self, screen, x, y, render_counter):
		if self.num_images == 1:
			screen.blit(self.images[0], (x, y))
		else:
			screen.blit(
				self.images[(render_counter // self.anim_delay) % self.num_images],
				(x, y))


class TileStore:
	def __init__(self):
		tile_file = 'data' + os.sep + 'tiles.txt'
		c = open(tile_file, 'rt')
		lines = c.read().split('\n')
		c.close()
		
		self.templates = {}
		for line in lines:
			tline = trim(line)
			if len(tline) > 0 and tline[0] != '#':
				parts = tline.split('\t')
				if len(parts) == 4 or len(parts) == 5:
					template = TileTemplate(parts)
					self.templates[template.id] = template
	
	def GetTile(self, id):
		return self.templates.get(id)
			


class Tile:
	def __init__(self, id_list):
		tile_stack = []
		no_animations = True
		for id in id_list:
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
		else:
			self.Render = self._animation_render
		
		self.submerged = False
		self.ice = False
		self.keytype = None
		
		self.composite_physics()
	
	def composite_physics(self):
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
				
	def _animation_render(self, screen, x, y, render_counter):
		for tile in self.stack:
			tile.Render(screen, x, y, render_counter)
	
	def _static_render(self, screen, x, y, render_counter):
		for tile in self.stack:
			screen.blit(tile.images[0], (x, y))
			
class Layer:
	def __init__(self, width, height):
		self.contains_stuff = False
		self.width = width
		self.height = height
	def SetTiles(self, tile_list):
		self.tiles = make_table(self.width, self.height)
		self.contains_stuff = True
		y = 0
		while y < self.height:
			x = 0
			while x < self.width:
				self.tiles[x][y] = tile_list[x + y * self.width]
				x += 1
			y += 1

	def Render(self, screen, x_offset, y_offset, render_counter):
		width = self.width
		height = self.height
		tiles = self.tiles
		y = 0
		while y < height:
			x = 0
			while x < width:
				tiles[x][y].Render(screen, x * 16, y * 16, render_counter)
				x += 1
			y += 1
	
def make_list(size):
	return [None] * size
def make_table(width, height):
	cols = make_list(width)
	i = 0
	while i < height:
		cols[i] = make_list(height)
		i += 1
	return cols
	
_tileStore = None
def get_tile_store():
	global _tileStore
	if _tileStore == None:
		_tileStore = TileStore()
	return _tileStore
	
class Level:
	def __init__(self, name):
		get_tile_store()
		self.parse_file(name)
	
	def parse_file(self, file):
		c = open('maps' + os.sep + file + '.txt', 'rt')
		lines = c.read().split('\n')
		c.close()
		
		values = {}
		for line in lines:
			parts = trim(line).split(':')
			if len(parts) >= 2:
				
				name = parts[0].split('#')[-1]
				value = trim(':'.join(parts[1:]))
				values[name] = value

		self.width = int(values['width'])
		self.height = int(values['height'])
		self.layers = {}
		for layerName in 'A B C D E F Stairs'.split(' '):
			content = values.get('Layer' + layerName)
			layer = Layer(self.width, self.height)
			if content != None:
				spots = trim(content).split(',')
				raw_tile_list = []
				for spot in spots:
					tiles = spot.split('|')
					raw_tile_list.append(Tile(tiles))
				layer.SetTiles(raw_tile_list)
			self.layers[layerName] = layer

	def Render(self, layername, screen, x_offset, y_offset, render_counter):
		layer = self.layers[layername]
		if layer.contains_stuff:
			layer.Render(screen, x_offset, y_offset, render_counter)

### STATIC ###

