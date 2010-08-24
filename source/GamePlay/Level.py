
	
class Level:
	def __init__(self, name):
		get_tile_store()
		self.parse_file(name)
		self.playerStandingOn = None
	
	def update_tile_standing_on(self, layer, x, y):
		key = layer + str(x) + '_' + str(y)
		if key != self.playerStandingOn:
			self.playerStandingOn = key
			layer = self.layers[layer]
			if layer.contains_stuff:
				tile = layer.tiles[x][y]
				if tile.id != None:
					script = tile.id.script
					if script != None and script != '':
						go_script_go(script)
	
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
		self.music = values.get('music', None)
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
				
		script_strings = values.get('scripts')
		scripts = {}
		if script_strings != None:
			scripts_banana = trim(script_strings).split('|||')
			for banana in scripts_banana:
				lines = trim(banana).split('|')
				if len(lines) > 1:
					name = lines[0]
					body = '\n'.join(lines[1:])
					scripts[name] = body
		id_strings = values.get('IDs')
		ids = {}
		if id_strings != None:
			id_strings = trim(id_strings).split(',')
			for id_string in id_strings:
				parts = trim(id_string).split('|')
				name = parts[0]
				layer = parts[1]
				x = int(parts[2])
				y = int(parts[3])
				script = scripts.get(name)
				id = IdMarker(name, layer, x, y, script)
				self.layers[layer].tiles[x][y].SetId(id)
				ids[name] = id
		self.ids = ids
				
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
		