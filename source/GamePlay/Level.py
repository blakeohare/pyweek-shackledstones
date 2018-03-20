class Level:
	def __init__(self, name):
		self.name = name
		get_tile_store()
		self.parse_file(name)
		self.playerStandingOn = None
	
	def synch_stand_key(self, layer, x, y):
		key = layer + str(x) + '_' + str(y)
		if self.playerStandingOn == key:
			self.playerStandingOn = key
			return False
		self.playerStandingOn = key
		return True
	
	def update_tile_standing_on(self, layer, x, y):
		tile_x = x >> 4
		tile_y = y >> 4
		if self.synch_stand_key(layer, tile_x, tile_y):
			layer = self.layers[layer]
			layer.RunScript(tile_x, tile_y)
	
	def parse_file(self, file):
		c = open('maps' + os.sep + file + '.txt', 'rt')
		lines = c.read().split('\n')
		c.close()
		
		values = {}
		for line in lines:
			parts = line.strip().split(':')
			if len(parts) >= 2:
				name = parts[0].split('#')[-1]
				value = ':'.join(parts[1:]).strip()
				values[name] = value

		self.width = int(values['width'])
		self.height = int(values['height'])
		self.music = values.get('music', None)
		self.layers = {}
		self.dungeon = values.get('dungeon', '').strip()
		
		GetKeyRegistry().doors = {}
		
		for layerName in 'A B C D E F Stairs'.split(' '):
			
			content = values.get('Layer' + layerName)
			layer = Layer(self.width, self.height)
			if content != None:
				spots = content.strip().split(',')
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
		
		kr = GetKeyRegistry()
		self.locked_doors = {}
		self.unique_locked_doors = []
		if self.dungeon != None:
			for layerName in 'A B C D E F'.split(' '):
				layer = self.layers[layerName]
				if layer.contains_stuff:
					y = 0
					while y < self.height:
						x = 0
						while x < self.width:
							tile = layer.tiles[x][y]
							dc = tile.door_color
							if dc != None:
								kr.RegisterDoor(self.name, self.dungeon, x, y, dc)
								for ofs in [(0,1),(0,-1),(1,0),(-1,0)]:
									self.locked_doors[str(x + ofs[0]) + '_' + str(y + ofs[1])] = [x, y, dc]
								self.unique_locked_doors.append([x, y, dc])
								
							x += 1
						y += 1
		
			for locked_door in self.unique_locked_doors:
				x = locked_door[0]
				y = locked_door[1]
				color = locked_door[2]
				if not kr.IsDoorLocked(self.name, self.dungeon, x, y, color):
					self.RemoveLockedDoor(x, y)
	
		script_strings = values.get('scripts')
		scripts = {}
		if script_strings != None:
			scripts_banana = script_strings.strip().split('|||')
			for banana in scripts_banana:
				lines = banana.strip().split('|')
				if len(lines) > 1:
					name = lines[0]
					body = '\n'.join(lines[1:])
					scripts[name] = body
		id_strings = values.get('IDs')
		ids = {}
		if id_strings != None:
			id_strings = id_strings.strip().split(',')
			for id_string in id_strings:
				parts = id_string.strip().split('|')
				if len(parts) == 4:
					name = parts[0]
					layer = parts[1]
					x = int(parts[2])
					y = int(parts[3])
					script = scripts.get(name)
					id = IdMarker(name, layer, x, y, script)
					self.layers[layer].tiles[x][y].SetId(id)
					ids[name] = id
		self.ids = ids
		self.enemies = values.get('enemies', '').strip().split(',')
		self.on_load = values.get('on_load', '').replace("\\n", "\n").replace("\\\\", "\\").strip()
		self.on_enemies_killed = values.get('on_enemies_killed', '').replace("\\n", "\n").replace("\\\\", "\\").strip()
		
	def RemoveLockedDoor(self, x, y):
		for layerName in 'A B C D E F'.split(' '):
			layer = self.layers[layerName]
			if layer.contains_stuff:
				if layer.tiles[x][y].door_color != None:
					layer.tiles[x][y].RemoveKey()
					if y > 0:
						layer.tiles[x][y - 1].RemoveKey()
					if y < self.height - 1:
						layer.tiles[x][y + 1].RemoveKey()
				
	def Render(self, layername, screen, x_offset, y_offset, render_counter):
		layer = self.layers[layername]
		if layer.contains_stuff:
			layer.Render(screen, x_offset, y_offset, render_counter)
	
	
	def is_stair_tile(self, x, y):
		stairs = self.layers['Stairs']
		if stairs.contains_stuff and x>=0 and y >= 0 and x < self.width and y < self.height:
			return stairs.tiles[x][y].physics == 'oooo'
		return False
	
	def move_request(self, orig_layer, orig_x, orig_y, dx, dy, radius, is_flying):
		orig_x = int(orig_x)
		orig_y = int(orig_y)
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
		
		walls = self.get_walls(orig_layer, left, top, right, bottom, not is_flying)
		
		collided = False
		
		if not self.rectangle_touches_walls(dest_x - radius, dest_y - radius, dest_x + radius, dest_y + radius, walls):
			coords = (dest_x, dest_y)
		else:
			collided = True
			final_x = orig_x
			final_y = orig_y
			
			# check x component
			for x in self.get_between_values(orig_x, dest_x):
				if not self.rectangle_touches_walls(x - radius, final_y - radius, x + radius, final_y + radius, walls):
					final_x = x
					break
			
			# check y component
			for y in self.get_between_values(orig_y, dest_y):
				if not self.rectangle_touches_walls(final_x - radius, y - radius, final_x + radius, y + radius, walls):
					final_y = y
					break
			
			coords = (final_x, final_y)
			
			
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
			
		return (final_layer, coords[0], coords[1], collided)
	
	def get_between_values(self, start, end):
		values = []
		if end > start:
			for i in range(end, start - 1, -1):
				values.append(i)
		else:
			for i in range(end, start + 1):
				values.append(i)
		return values
	
	def rectangle_touches_walls(self, left, top, right, bottom, walls):
		
		for wall in walls:
			if left > wall[2] + wall[0] or top > wall[1] + wall[3] or right < wall[0] or bottom < wall[1]:
				continue
			return True
		return False
	
	# pixel coordinates
	def get_walls(self, layer, left, top, right, bottom, blank_blocked):
		
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
						phys = layer.GetPhysics(x, y, blank_blocked)
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
