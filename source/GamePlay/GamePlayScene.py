class GamePlayScene:
	
	def __init__(self, level_name, startX, startY):
		global _new_enemies
		_new_enemies = []
		getActiveGame().setActiveGameScene(self)
		getActiveGame().setZone(level_name)
		self.render_counter = 0
		self.next = self
		self.player = Player()
		self.player.x = startX
		self.player.y = startY
		self.flash_amount = 0
		self.level = Level(level_name)
		self.death_circles = []
		self.disable_save = False
		self.name = level_name
		self.bg = None
		self.gotocredits = False
		self.player_invisible = False
		self.sprites = []
		self.overlayRenderer = OverlayRenderer()
		self.grapple = None
		self.cutscene = get_cutscene_for_map(level_name)
		self.last_torch_pressed = None
		self.lever_a_pressed = False
		self.lever_b_pressed = False
		self.puz_flag = False
		self.temp_screen = None
		
		self.prevTile = None
		self.firstTimeOnTile = True
		on_load_script = self.level.on_load.strip()
		self.inventory = Inventory()
		if len(on_load_script) > 0:
			run_script(on_load_script)
		
		if self.level.dungeon == 'light':
			mirrors = self.light_puzzle_get_mirror_states()
			setvar = getActiveGame().setSavedVar
			setvar('mirror_door_open', 'None')
			if str(getActiveGame().getVar('light_puzzle_on')) == '1':
				if mirrors['A'] == 'mirror1':
					if mirrors['B'] == 'mirror2' and mirrors['C'] == 'mirror3' and mirrors['D'] == 'mirror1' and mirrors['E'] == 'mirror3' and mirrors['F'] == 'mirror1':
						setvar('mirror_door_open', 'Blue')
				elif mirrors['A'] == 'mirror2':
					if mirrors['G'] == 'mirror1' and mirrors['H'] == 'mirror3':
						if mirrors['I'] == 'mirror4' and mirrors['L'] == 'mirror1' and mirrors['M'] == 'mirror2':
							setvar('mirror_door_open', 'Yellow')
						elif mirrors['I'] == 'mirror1' and mirrors['J'] == 'mirror4' and mirrors['K'] == 'mirror2':
							setvar('mirror_door_open', 'Red')
		
		self.torch_puz = level_name == 'dark_swamp'
		self.light_puz = level_name == 'light_puzzle1_f1'
		self.desert_puz = level_name == 'world_W'
		self.lever_puz = level_name == 'light_south_southroom'
		
		if self.torch_puz:
			self.swamp_opened = getActiveGame().getVar('swamp_opened') != None
			
			if self.swamp_opened:
				self.open_dark_temple()
		
		self.initialize_enemies()
		play_music(self.level.music)
	
	def open_dark_temple(self):
		ids = self.level.ids
		run_script('\n'.join([
			'[set tile][1][doodad][d9]',
			'[set tile][2][doodad][d7]',
			'[set tile][3][doodad][d10]',
			'[set tile][4][doodad][d5]',
			'[set tile][5][doodad][94]',
			'[set tile][6][doodad][d4]',
			'[set tile][7][doodad][d12]',
			'[set tile][8][doodad][d164]',
			'[set tile][9][doodad][d11]',
			'[set tile][5][excessive][d41]'
			]))
		getActiveGame().setSavedVar('swamp_opened', '1')
	
	def initialize_enemies(self):
		for enemy in self.level.enemies:
			data = enemy.strip()
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
		if self.cutscene != None and not self.cutscene.is_done() and self.cutscene.name != 'asynch':
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
		
		tile_x = x >> 4
		tile_y = y >> 4
		layer = self.level.layers[self.player.layer]
		if layer.contains_stuff and tile_x >= 0 and tile_y >= 0 and tile_x < layer.width and tile_y < layer.height:
			tile = layer.tiles[tile_x][tile_y]
			if type == 'sword':
				tile.chopTheBushes()
			elif type == 'hammer':
				tile.smashBoulders()
			elif type == 'drill':
				tile.drillThrough()
			
	def processInput(self, events):
	
		if self.cutscene != None and not self.cutscene.is_done() and self.cutscene.name != 'asynch':
			events = self.cutscene.get_input_events()
		
		actions = {
			'item_sabre' : False,
			'item_hammer' : False,
			'item_drill' : False,
			'item_hook' : False,
			'item_cannon' : False,
			'item_cannon_fire' : False,
			'item_cannon_ice' : False,
			'item_cannon_multi' : False,
			'item_compass' : False,
			'item_shovel' : False
		}
		
		items_pressed = []
		
		for event in events:
			if event.down and event.key == 'B':
				actions[self.inventory.equippedB()] = True
			elif event.down and event.key == 'A':
				actions[self.inventory.equippedA()] = True
			elif event.down and event.key == 'Y':
				actions[self.inventory.equippedY()] = True
			elif event.down and event.key == 'X':
				actions[self.inventory.equippedX()] = True
			elif event.down and event.key == 'start':
				self.next = InventoryScene(self)
		
		if self.player.state == 'walking':
			if actions['item_sabre']:
				self.player.stab()
			elif actions['item_cannon']:
				self.player.shoot('basic', self)
			elif actions['item_cannon_fire']:
				self.player.shoot('fire', self)
			elif actions['item_cannon_ice']:
				self.player.shoot('ice', self)
			elif actions['item_cannon_multi']:
				self.player.shoot('multi', self)
			elif actions['item_shovel']:
				self.player.dig()
			elif actions['item_drill']:
				self.player.drill()
			elif actions['item_hammer']:
				self.player.hammer()
			elif actions['item_hook']:
				self.player.Grapple()
			
		
		if actions['item_compass']:
			compass_active = getActiveGame().getVar('is_compass_active')
			if compass_active == None: compass_active = 0
			else: compass_active = int(compass_active)
			
			if compass_active == 1:
				getActiveGame().setTempVar('is_compass_active', 0)
			else:
				getActiveGame().setTempVar('is_compass_active', 1)
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
		
		if self.player.flying_damage > 0:
			vx = self.player.damage_dx
			vy = self.player.damage_dy
		
		self.do_sprite_move(self.player, vx, vy, False)
		
	def update(self, game_counter):
		self.level.update_tile_standing_on(self.player.layer, self.player.x, self.player.y)
		
		if self.prevTile != self.level.playerStandingOn:
			self.prevTile = self.level.playerStandingOn
			self.firstTimeOnTile = True
		else:
			self.firstTimeOnTile = False
		if self.torch_puz and not self.swamp_opened:
			self.torch_puzzle_update()
		elif self.lever_puz:
			self.light_lever_puzzle()
		if self.desert_puz:
			self.desert_puzzle_update()
		
		if self.level.dungeon != None and len(self.level.locked_doors) > 0:
			tile_x = self.player.x >> 4
			tile_y = self.player.y >> 4
			door = self.level.locked_doors.get(str(tile_x) + '_' + str(tile_y))
			if door != None:
				x = door[0]
				y = door[1]
				color = door[2]
				if getKeyRegistry().useKey(self.level.dungeon, color, self.level.name, x, y):
					self.level.removeLockedDoor(x, y)
		
		if self.gotocredits:
			self.next = CreditsScene()
		
		if self.cutscene != None and not self.cutscene.is_done():
			self.cutscene.do(self)
			if self.cutscene != None and self.cutscene.is_done():
				self.cutscene = None
		
		for sprite in self.get_sprites():
			sprite.update()
			if sprite.dx != 0 or sprite.dy != 0:
				if self.do_sprite_move(sprite, sprite.dx, sprite.dy, sprite.flying):
					if sprite.explode_on_impact:
						sprite.expired = True
						if sprite.kind == 'grapple':
							if not self.grapple.grappled and not self.try_grapple_to(self.player):
								self.grapple = None
							else:
								self.grapple.expired = False
		
		if self.grapple != None:
			if self.grapple.grappled:
				self.grapple.grapple_counter += 1
				progress = (0.0 + self.grapple.grapple_counter) / self.grapple.grapple_duration
				antiprogress = 1 - progress
				self.player.x = int(self.grapple.x * progress + self.grapple.grapple_start_x * antiprogress)
				self.player.y = int(self.grapple.y * progress + self.grapple.grapple_start_y * antiprogress)
				if self.grapple.grapple_counter >= self.grapple.grapple_duration:
					self.grapple.expired = True
					self.grapple = None
			elif self.grapple.expired:
				self.grapple = None
			
		
		dcs = []
		for dc in self.death_circles:
			dc.update()
			if not dc.expired:
				dcs.append(dc)
		self.death_circles = dcs
		
		for sprite in self.sprites:
			if sprite.is_goody:
				dx = sprite.x - self.player.x
				dy = sprite.y - self.player.y
				if dx ** 2 + dy ** 2 < 16 ** 2:
					sprite.expired = True
					if sprite.name == 'money':
						modify_money(1)
					else:
						heal_damage()
						
		
		enemy_count = self.get_enemy_count()
		self.gc_sprites()
		if enemy_count > 0 and self.get_enemy_count() == 0:
			enemy_kill_script = self.level.on_enemies_killed
			if len(enemy_kill_script) > 0:
				run_script(enemy_kill_script)

	def try_grapple_to(self, player):
		if self.grapple:
			x = self.grapple.x
			y = self.grapple.y
			d = self.grapple.direction
			if d == 'left':
				x -= 8
			elif d == 'right':
				x += 8
			elif d == 'down':
				y += 8
			else:
				y -= 8
			x = x >> 4
			y = y >> 4
			layer = self.level.layers[self.grapple.layer]
			if x >= 0 and x < layer.width and y >= 0 and y < layer.height:
				tile = layer.tiles[x][y]
				if tile.is_grappleable:
					self.grapple.grappled = True
					return True
		return False

	def light_lever_puzzle(self):
		getvar = getActiveGame().getVar
		
		if str(getvar('light_timed_lever_A')) == '1' and str(getvar('light_timed_lever_B')) == '1' and not self.puz_flag:
			run_script('[set][light_timed_lever_solved][1]')
			run_script('[remove tile][closed_door][baseadorn]')
			self.puz_flag = True
			self.cutscene = None
			
		if self.firstTimeOnTile:
			if not str(getvar('light_timed_lever_solved')) == '1':
				if str(getvar('light_timed_lever_A')) == '1' and not self.lever_a_pressed:
					self.lever_a_pressed = True
					if self.lever_b_pressed:
						run_script('[set][light_timed_lever_solved][1]')
						self.cutscene = None
					else:
						script = '[set][light_timed_lever_A][0]'
						self.cutscene = CutScene(('pause 15\nplaysound tick\n' * 8) + 'turnlightswitchesoff', 'asynch')
				if str(getvar('light_timed_lever_B')) == '1' and not self.lever_b_pressed:
					self.lever_b_pressed = True
					if self.lever_a_pressed:
						run_script('[set][light_timed_lever_solved][1]')
						self.cutscene = None
					else:
						script = '[set][light_timed_lever_B][0]'
						self.cutscene = CutScene(('pause 15\nplaysound tick\n' * 8) + 'turnlightswitchesoff', 'asynch')
				
				if str(getvar('light_timed_lever_A')) == '1' and str(getvar('light_timed_lever_B')) == '1':
					self.turnlightswitchesoff()
					run_script('[set][light_timed_lever_solved][1]')
	
	def turnlightswitchesoff(self):
		self.lever_a_pressed = False
		self.lever_b_pressed = False
		run_script('[set tile][switch_left][baseadorn][57]')
		run_script('[set tile][switch_right][baseadorn][57]')
		run_script('[set][light_timed_lever_A][0]')
		run_script('[set][light_timed_lever_B][0]')
		self.cutscene = None
		
	def desert_puzzle_update(self):
		opened = str(getActiveGame().getVar('light_temple_opened')) == '1'
		if not opened and self.player.state == 'shovelling':
			target = self.level.ids['temple']
			x = self.player.x >> 4
			y = self.player.y >> 4
			if target.x == x and target.y == y:
				getActiveGame().setSavedVar('light_temple_opened', '1')
				self.cutscene = CutScene('pause 5\nplaysound itemget\nscript [set tile][entrance][base][171]', 'open_light_temple')
			
		
		
	def get_enemy_count(self):
		count = 0
		for sprite in self.sprites:
			if sprite.is_enemy: count += 1
		return count
		
	def render(self, screen, renderOffsets):
		
		if self.bg != None:
			screen.blit(self.bg, (0,0))
		else:
			
			offset = self.get_camera_offset()
			
			
			if self.cutscene != None and not self.cutscene.is_done():
				r_offset = self.cutscene.render_offset()
				offset = (offset[0] + r_offset, offset[1])
			
			flattenedOffset = [offset[0] + renderOffsets[0], offset[1] + renderOffsets[1]]
			
			self.level.render('Stairs', screen, offset[0], offset[1], self.render_counter, renderOffsets)
			for layerName in 'A B C D E F Stairs'.split(' '):
				if layerName != 'Stairs':
					self.level.render(layerName, screen, offset[0], offset[1], self.render_counter, renderOffsets)
				
				for sprite in self.get_renderable_sprites(layerName):
					img = sprite.currentImage(self.render_counter)
					if img != None:
						coords = sprite.drawingCoords()
						screen.blit(img, (coords[0] + flattenedOffset[0], coords[1] + flattenedOffset[1]))
					
					if sprite == self.grapple:
						x = sprite.x
						y = sprite.y
						if sprite.direction == 'left':
							x += 14
						elif sprite.direction == 'right':
							x -= 14
						elif sprite.direction == 'up':
							y += 14
						else:
							y -= 14
						Graphics2D.Draw.line(sprite.x + flattenedOffset[0], sprite.y + flattenedOffset[1], self.player.x + flattenedOffset[0], self.player.y + flattenedOffset[1], 1, 255, 200, 40)
					
					if sprite.is_enemy and sprite.frozen and img != None:
						Graphics2D.Draw.rectangle(coords[0] + flattenedOffset[0] - 2, coords[1] + flattenedOffset[1] - 2, sprite.r * 2 + 4, sprite.r * 2 + 4, 100, 100, 255, 1)
			
			if self.light_puz:
				self.render_light_puzzle(screen, flattenedOffset)
			
		if self.cutscene != None:
			self.make_white(screen, self.flash_amount)
		else:
			self.flash_amount = 0
		
		self.render_counter += 1
		
		if self.overlayRenderer != None:
			self.overlayRenderer.render(screen)
	
	def make_white(self, screen, amount):
		if amount == 0: return
		value = min(255, max(0, int(255 * amount)))
		fill_screen_with_alpha(255, 255, 255, value)
		
	def torch_puzzle_update(self):
		ids = self.level.ids
		activation = 'ABCDEFGHI'
		x = self.player.x >> 4
		y = self.player.y >> 4
		current = None
		
		last = self.last_torch_pressed
		for active_tile in activation:
			tile = ids[active_tile]
			if tile.x == x and tile.y == y:
				current = active_tile
				break
		
		name = None
		if self.cutscene != None: name = self.cutscene.name
		
		if self.firstTimeOnTile and current != None and current != last and self.cutscene == None:
			if last == 'H' and current == 'I':
				self.cutscene = get_cutscene('torch_win')
				self.open_dark_temple()
			elif last == None and current == 'A':
				self.last_torch_pressed = current
				play_sound('fwuf')
				run_script('[remove tile][t' + current + '][doodad]')
			elif last != None and activation.find(last) == activation.find(current) - 1:
				self.last_torch_pressed = current
				play_sound('fwuf')
				run_script('[remove tile][t' + current + '][doodad]')
			else:
				play_sound('fwuf')
				run_script('[remove tile][t' + current + '][doodad]')
				current = None
				last = None
				self.last_torch_pressed = None
				self.cutscene = get_cutscene('torch_fail')
	
	def torch_puzzle_relight(self):
		for tile in 'ABCDEFGHI':
			run_script('[set tile][t' + tile + '][doodad][torch3]')
		play_sound('bad')
			
	
	def render_light_puzzle(self, screen, offset):
		get_var = getActiveGame().getVar
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
		
		Graphics2D.Draw.line(start_x + offset[0], start_y + offset[1], end_x + offset[0], end_y + offset[1], 1, 255, 255, 255)
		
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
		get_var = getActiveGame().getVar
		mirrors = {}
		for mirror in 'ABCDEFGHIJKLMN':
			state = get_var('mirror_state_' + mirror)
			if state == None:
				state = _defaultMirror[mirror]
				getActiveGame().setSavedVar('mirror_state_' + mirror, _defaultMirror[mirror])
			mirrors[mirror] = state
		return mirrors
	
	
	
	def get_camera_offset(self):
		
		width = self.level.width * 16
		height = self.level.height * 16
		
		screen_width = SCREEN_WIDTH
		screen_height = SCREEN_HEIGHT
		
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
			
			unsorted_spritelist = [self.player] + sprites
		else:
			unsorted_spritelist = sprites
		
		return self.sort_sprite_list(unsorted_spritelist)
	
	def sort_sprite_list(self, sprites, pivot=None):
		if pivot == None:
			if len(sprites) == 0:
				return []
			return self.sort_sprite_list(sprites[1:], sprites[0])
		
		left = []
		right = []
		for sprite in sprites:
			if sprite.y < pivot.y:
				left.append(sprite)
			else:
				right.append(sprite)
		
		left = self.sort_sprite_list(left)
		right = self.sort_sprite_list(right)
		
		return left + [pivot] + right
	
	def do_sprite_move(self, sprite, vx, vy, is_flying_sprite):
		vx = int(vx)
		vy = int(vy)
		#hacked in a lower location for the center of the sprite in the particular case of the player
		params = self.level.move_request(sprite.layer, sprite.x, sprite.y, vx, vy, sprite.r - 4, is_flying_sprite)
		sprite.layer = params[0]
		sprite.x = params[1]
		sprite.y = params[2]
		return params[3]
