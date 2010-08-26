
class GamePlayScene:
	
	def __init__(self, level_name, startX, startY):
	
		ActiveGame().SetActiveGameScene(self)
		
		self.render_counter = 0
		self.next = self
		self.player = Player()
		self.player.x = startX
		self.player.y = startY
		self.level = Level(level_name)
		self.death_circles = []
		self.name = level_name
		self.player_invisible = False
		self.sprites = []
		self.cutscene = get_cutscene_for_map(level_name)
		on_load_script = trim(self.level.on_load)
		if len(on_load_script) > 0:
			go_script_go(on_load_script)
		
		self.light_puz = level_name == 'light_puzzle1_f1'
		self.initialize_enemies()
	
	def initialize_enemies(self):
		for enemy in self.level.enemies:
			data = trim(enemy)
			if len(data) > 0:
				parts = data.split('|')
				kind = parts[0]
				x = int(parts[2])
				y = int(parts[3])
				layer = parts[1]
				sprite = create_sprite(kind)
				sprite.x = (x << 4) + 8
				sprite.y = (y << 4) + 8
				sprite.layer = layer
				self.sprites.append(sprite)
				
	def place_player(self, layer, x, y):
		self.player.layer = layer
		self.player.x = (x << 4) + 8
		self.player.y = (y << 4) + 8
		self.level.synch_stand_key(layer, self.player.x >> 4, self.player.y >> 4)
	
	def is_key_pressed(self, key):
		if self.cutscene != None and not self.cutscene.is_done():
			return self.cutscene.is_key_pressed(key)
		return is_pressed(key)
			
	def add_sprite(self, sprite):
		self.sprites.append(sprite)
	
	def get_sprite_by_id(self, sprite_id):
		for sprite in self.sprites:
			if sprite.id == sprite_id:
				return sprite
		return None
	
	def place_death_circle(self, type, x, y, radius, duration):
		self.death_circles.append(DeathCircle(x, y, radius, duration, type))
		
		if type == 'sword':
			tile_x = x >> 4
			tile_y = y >> 4
			layer = self.level.layers[self.player.layer]
			if layer.contains_stuff and tile_x >= 0 and tile_y >= 0 and tile_x < layer.width and tile_y < layer.height:
				layer.tiles[tile_x][tile_y].ChopTheBushes()
	def ProcessInput(self, events):
	
		if self.cutscene != None and not self.cutscene.is_done():
			events = self.cutscene.get_input_events()
		
		actions = {
			'stab' : False,
			'shoot' : False,
			'drill' : False,
			'hammer' : False
		}
		for event in events:
			if event.down and event.key == 'B':
				if self.player.state == 'walking':
					actions['stab'] = True
			elif event.down and event.key == 'A':
				self.player.Shoot('basic', self)
			elif event.down and event.key == 'start':
				self.next = InventoryScene(self)
		
		if actions['stab']:
			self.player.Stab()
		
		v = 3
		vx = 0
		vy = 0
		
		if self.player.state == 'walking':
			if self.is_key_pressed('left'):
				self.player.direction = 'left'
				vx = -v
			elif self.is_key_pressed('right'):
				self.player.direction = 'right'
				vx = v
			if self.is_key_pressed('up'):
				self.player.direction = 'up'
				vy = -v
			elif self.is_key_pressed('down'):
				self.player.direction = 'down'
				vy = v
		
		self.player.walking = False
		if vx != 0 or vy != 0:
			self.player.walking = True
		
		self.do_sprite_move(self.player, vx, vy, False)
		
	def Update(self, game_counter):
		play_music('highlightsoflight')
		self.level.update_tile_standing_on(self.player.layer, self.player.x, self.player.y)
		
		if self.level.dungeon != None and len(self.level.locked_doors) > 0:
			tile_x = self.player.x >> 4
			tile_y = self.player.y >> 4
			door = self.level.locked_doors.get(str(tile_x) + '_' + str(tile_y))
			if door != None:
				x = door[0]
				y = door[1]
				color = door[2]
				if GetKeyRegistry().UseKey(self.level.dungeon, color, self.level.name, x, y):
					self.level.RemoveLockedDoor(x, y)
		
		if self.cutscene != None and not self.cutscene.is_done():
			self.cutscene.do(self)
		
		for sprite in self.get_sprites():
			sprite.Update()
			if sprite.dx != 0 or sprite.dy != 0:
				if self.do_sprite_move(sprite, sprite.dx, sprite.dy, sprite.flying):
					if sprite.explode_on_impact:
						sprite.expired = True
		
		dcs = []
		for dc in self.death_circles:
			dc.update()
			if not dc.expired:
				dcs.append(dc)
		self.death_circles = dcs
		
		
		enemy_count = self.get_enemy_count()
		self.gc_sprites()
		if enemy_count > 0 and self.get_enemy_count() == 0:
			enemy_kill_script = self.level.on_enemies_killed
			if len(enemy_kill_script) > 0:
				go_script_go(enemy_kill_script)

	def get_enemy_count(self):
		count = 0
		for sprite in self.sprites:
			if sprite.is_enemy: count += 1
		return count
		
	def Render(self, screen):
		
		offset = self.get_camera_offset()
		
		if self.cutscene != None and not self.cutscene.is_done():
			r_offset = self.cutscene.render_offset()
			offset = (offset[0] + r_offset, offset[1])
		
		self.level.Render('Stairs', screen, offset[0], offset[1], self.render_counter)
		for layerName in 'A B C D E F Stairs'.split(' '):
			if layerName != 'Stairs':
				self.level.Render(layerName, screen, offset[0], offset[1], self.render_counter)
			
			for sprite in self.get_renderable_sprites(layerName):
				img = sprite.CurrentImage(self.render_counter)
				if img != None:
					coords = sprite.DrawingCoords()
					screen.blit(img, (coords[0] + offset[0], coords[1] + offset[1]))
		
		if self.light_puz:
			self.render_light_puzzle(screen, offset)
		
		self.render_counter += 1
	
	def render_light_puzzle(self, screen, offset):
		get_var = ActiveGame().GetVar
		ids = self.level.ids
		
		mirror_states = self.light_puzzle_get_mirror_states()
		mirror_images = {
			'mirror1' : get_image('tiles/mirrors/topright'),
			'mirror2' : get_image('tiles/mirrors/topleft'),
			'mirror3' : get_image('tiles/mirrors/bottomleft'),
			'mirror4' : get_image('tiles/mirrors/bottomright')
		}
		for mirror_key in mirror_states.keys():
			loc = ids[mirror_key]
			x = (loc.x << 4) + offset[0]
			y = (loc.y << 4) + offset[1]
			screen.blit(mirror_images[mirror_states[mirror_key]], (x, y))
		
		if get_var('light_puzzle_on') == None:
			return
		
		self.draw_light_beam(screen, 'source', 'A', offset, ids, mirror_states)
		
	def draw_light_beam(self, screen, start, end, offset, ids, mirror_states):
		start_id = ids[start]
		end_id = ids[end]
		start_x = (start_id.x << 4) + 8
		start_y = (start_id.y << 4) + 8
		end_x = (end_id.x << 4) + 8
		end_y = (end_id.y << 4) + 8
		
		pygame.draw.line(screen, (255, 255, 255), (start_x + offset[0], start_y + offset[1]), (end_x + offset[0], end_y + offset[1]))
		
		next = None
		if end == 'A':
			if mirror_states['A'] == 'mirror1':
				next = 'B'
			elif mirror_states['A'] == 'mirror2':
				next = 'G'
		elif end == 'B':
			if mirror_states['B'] == 'mirror2':
				next = 'C'
			elif mirror_states['B'] == 'mirror3':
				next = 'fail1'
		elif end == 'C':
			if mirror_states['C'] == 'mirror3':
				next = 'D'
			elif mirror_states['C'] == 'mirror4':
				next = 'fail2'
		elif end == 'D':
			if mirror_states['D'] == 'mirror1':
				next = 'E'
			elif mirror_states['D'] == 'mirror4':
				next = 'fail8'
		elif end == 'E':
			if mirror_states['E'] == 'mirror3':
				next = 'F'
			elif mirror_states['E'] == 'mirror4':
				next = 'fail9'
		elif end == 'F':
			if mirror_states['F'] == 'mirror1':
				next = 'blue_door'
			elif mirror_states['F'] == 'mirror4':
				next = 'fail10'
		elif end == 'G':
			if mirror_states['G'] == 'mirror1':
				next = 'H'
			elif mirror_states['G'] == 'mirror4':
				next = 'fail3'
		elif end == 'H':
			if mirror_states['H'] == 'mirror3':
				next = 'I'
			elif mirror_states['H'] == 'mirror4':
				next = 'bs_light_to_mainroom_f_puzzle'
		elif end == 'I':
			if mirror_states['I'] == 'mirror1':
				next = 'J'
			elif mirror_states['I'] == 'mirror4':
				next = 'L'
		elif end == 'J':
			if mirror_states['J'] == 'mirror4':
				next = 'K'
			elif mirror_states['J'] == 'mirror3':
				next = 'fail6'
		elif end == 'K':
			if mirror_states['K'] == 'mirror2':
				next = 'red_door'
			elif mirror_states['K'] == 'mirror3':
				next = 'fail7'
		elif end == 'L':
			if mirror_states['L'] == 'mirror1':
				next = 'M'
			elif mirror_states['L'] == 'mirror2':
				next = 'fail4'
		elif end == 'M':
			if mirror_states['M'] == 'mirror2':
				next = 'N'
			elif mirror_states['M'] == 'mirror3':
				next = 'fail5'
		elif end == 'N':
			next = 'yellow_door'
		
		if next != None:
			self.draw_light_beam(screen, end, next, offset, ids, mirror_states)
	
	def light_puzzle_get_mirror_states(self):
		global _defaultMirror
		get_var = ActiveGame().GetVar
		mirrors = {}
		for mirror in 'ABCDEFGHIJKLMN':
			state = get_var('mirror_state_' + mirror)
			if state == None:
				state = _defaultMirror[mirror]
				ActiveGame().SetSavedVar('mirror_state_' + mirror, _defaultMirror[mirror])
			mirrors[mirror] = state
		return mirrors
	
	
	
	def get_camera_offset(self):
		
		width = self.level.width * 16
		height = self.level.height * 16
		
		screen_width = 24 * 16
		screen_height = 18 * 16
		
		offset_x = 0
		offset_y = 0
		
		player_x = self.player.x
		player_y = self.player.y
		
		if width < screen_width:
			offset_x = (screen_width - width) / 2
		elif width > screen_width:
			offset_x = screen_width / 2 - player_x
			offset_x = min(offset_x, 0)
			offset_x = max(offset_x, -(width - screen_width))
			
		if height < screen_height:
			offset_y = (screen_height - height) / 2
		elif height > screen_height:
			offset_y = screen_height / 2 - player_y
			offset_y = min(offset_y, 0)
			offset_y = max(offset_y, -(height - screen_height))
		return (offset_x, offset_y)
	
	def gc_sprites(self):
		sprites = []
		for sprite in self.sprites:
			if not sprite.expired:
				sprites.append(sprite)
		self.sprites = sprites
	
	def get_sprites(self):
		return [self.player] + self.sprites
	
	def get_renderable_sprites(self, layer):
		sprites = []
		for sprite in self.sprites:
			if sprite.layer == layer:
				sprites.append(sprite)
		
		if self.player.layer == layer and not self.player_invisible:
			
			return [self.player] + sprites
		else:
			return sprites
	
	def do_sprite_move(self, sprite, vx, vy, is_flying_sprite):
		params = self.level.move_request(sprite.layer, sprite.x, sprite.y, vx, vy, sprite.r - 4, is_flying_sprite)
		sprite.layer = params[0]
		sprite.x = params[1]
		sprite.y = params[2]
		return params[3]

### STATIC ###
_defaultMirror = {
	'A' : 'mirror1',
	'B' : 'mirror2',
	'C' : 'mirror3',
	'D' : 'mirror4',
	'E' : 'mirror1',
	'F' : 'mirror2',
	'G' : 'mirror3',
	'H' : 'mirror4',
	'I' : 'mirror1',
	'J' : 'mirror2',
	'K' : 'mirror3',
	'L' : 'mirror4',
	'M' : 'mirror1',
	'N' : 'mirror3'
}