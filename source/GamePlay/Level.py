
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
		#elif len(tile_stack) == 0:
		#	self.Render = self._dont_render
		else:
			self.Render = self._animation_render
		
		self.submerged = False
		self.ice = False
		self.keytype = None
		
		self.composite_physics()
	
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

	def MarkStairTile(self, x, y):
		self.tiles[x][y].is_stair_tile()
		
	def Render(self, screen, x_offset, y_offset, render_counter):
		width = self.width
		height = self.height
		tiles = self.tiles
		
		left = max(0, int(x_offset / -16) - 2)
		top = max(0, int(y_offset / -16) - 2)
		right = min(left + 24 + 4, width)
		bottom = min(top + 18 + 4, height)
		
		y = top
		while y < bottom:
			x = left
			while x < right:
				tiles[x][y].Render(screen, x * 16 + x_offset, y * 16 + y_offset, render_counter)
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
		
		stair_layer = self.layers['Stairs']
		if stair_layer.contains_stuff:
			other_layers = 'A B C D E F'.split(' ')
			y = 0
			while y < self.height:
				x = 0
				while x < self.width:
					if stair_layer.tiles[x][y].physics != 'xxxx':
						for layerName in other_layers:
							layer = self.layers[layerName]
							if layer.contains_stuff:
								layer.tiles[x][y].is_stair_tile()
					x += 1
				y += 1
	def Render(self, layername, screen, x_offset, y_offset, render_counter):
		layer = self.layers[layername]
		if layer.contains_stuff:
			layer.Render(screen, x_offset, y_offset, render_counter)
	
	
	def is_stair_tile(self, x, y):
		stairs = self.layers['Stairs']
		if stairs.contains_stuff:
			return stairs.tiles[x][y].physics == 'oooo'
		return False
	
	def move_request(self, orig_layer, orig_x, orig_y, dx, dy, radius):
		dest_x = orig_x + dx
		dest_y = orig_y + dy
		
		left = orig_x
		right = orig_x
		top = orig_y
		bottom = orig_y
		
		if orig_x < dest_x:
			right = dest_x
		else:
			left = dest_x
		
		if orig_y < dest_y:
			bottom = dest_y
		else:
			top = dest_y
		
		left -= radius
		top -= radius
		right += radius
		bottom += radius
		
		walls = self.get_walls(orig_layer, left, top, right, bottom)

		if not self.rectangle_touches_walls(dest_x - radius, dest_y - radius, dest_x + radius, dest_y + radius, walls):
			coords = (dest_x, dest_y)
		else:
		
			coords = (orig_x, orig_y)
		tile_x = coords[0] >> 4
		tile_y = coords[1] >> 4
		if self.is_stair_tile(tile_x, tile_y):
			final_layer = "Stairs"
		else:
			if orig_layer == "Stairs":
				final_layer = 'A' # default value that ought to never get hit.
				# if there's every a bug where you get stuck in the stairs, start looking here
				for layerName in 'A B C D E F'.split(' '):
					layer = self.layers[layerName]
					if layer.contains_stuff:
						if layer.tiles[tile_x][tile_y].physics != 'xxxx':
							final_layer = layerName
							break
					
			else:
				final_layer = orig_layer
			
		return (final_layer, coords[0], coords[1])
	
	def rectangle_touches_walls(self, left, top, right, bottom, walls):
		
		for wall in walls:
			if left > wall[2] + wall[0] or top > wall[1] + wall[3] or right < wall[0] or bottom < wall[1]:
				continue
			return True
		return False
	
	# pixel coordinates
	def get_walls(self, layer, left, top, right, bottom):
		
		tile_left = (left - 4) >> 4
		tile_right = (right + 4) >> 4
		tile_top = (top - 4) >> 4
		tile_bottom = (bottom + 4) >> 4
		
		walls = []
		
		if layer != 'Stairs':
			layer = self.layers[layer]
			
			y = tile_top
			while y <= tile_bottom:
				x = tile_left
				while x <= tile_right:
					if not self.is_stair_tile(x, y):
						phys = layer.tiles[x][y].physics
						if phys == 'oooo':
							pass
						elif phys == 'xxxx':
							walls.append((x << 4, y << 4, 16, 16))
						else:
							if phys[0] == 'x':
								walls.append((x << 4, y << 4, 8, 8))
							if phys[1] == 'x':
								walls.append(((x << 4) + 8, y << 4, 8, 8))
							if phys[2] == 'x':
								walls.append((x << 4, (y << 4) + 8, 8, 8))
							if phys[3] == 'x':
								walls.append(((x << 4) + 8, (y << 4) + 8, 8, 8))
							
					x += 1
				y += 1
		else:
			layerNames = 'A B C D E F'.split(' ')
			y = tile_top
			while y <= tile_bottom:
				x = tile_left
				while x <= tile_right:
					if not self.is_stair_tile(x, y):
						for layerName in layerNames:
							other_layer = self.layers[layerName]
							any_found = False
							if other_layer.contains_stuff:
								phys = other_layer.tiles[x][y].physics 
								if phys == 'oooo':
									any_found = True
								elif phys == 'xxxx':
									pass
								else:
									any_found = True
									if phys[0] == 'x':
										walls.append((x << 4, y << 4, 8, 8))
									if phys[1] == 'x':
										walls.append(((x << 4) + 8, y << 4, 8, 8))
									if phys[2] == 'x':
										walls.append((x << 4, (y << 4) + 8, 8, 8))
									if phys[3] == 'x':
										walls.append(((x << 4) + 8, (y << 4) + 8, 8, 8))
							if any_found:
								break
						if not any_found:
							walls.append((x << 4, y << 4, 16, 16))
						
					x += 1
				y += 1
			
			
		
		return walls
		
		
### STATIC ###

