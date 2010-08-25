
class GamePlayScene:
	
	def __init__(self, level_name, startX, startY):
		GameContext().SetActiveGame(1)
		GameContext().SetPlayerName(1, 'SUE')
		ActiveGame().SetActiveGameScene(self)
		self.render_counter = 0
		self.next = self
		self.player = Player()
		self.player.x = startX
		self.player.y = startY
		self.level = Level(level_name)
		self.player_invisible = False
	
	def place_player(self, layer, x, y):
		self.player.layer = layer
		self.player.x = (x << 4) + 8
		self.player.y = (y << 4) + 8
		self.level.synch_stand_key(layer, self.player.x >> 4, self.player.y >> 4)
	
	def ProcessInput(self, events):
	
		for event in events:
			if event.down and event.key == 'B':
				if self.player.state == 'walking':
					self.player.Stab()
			elif event.down and event.key == 'start':
				self.next = InventoryScene(self)
		v = 3
		vx = 0
		vy = 0
		
		if self.player.state == 'walking':
			if is_pressed('left'):
				self.player.direction = 'left'
				vx = -v
			elif is_pressed('right'):
				self.player.direction = 'right'
				vx = v
			if is_pressed('up'):
				self.player.direction = 'up'
				vy = -v
			elif is_pressed('down'):
				self.player.direction = 'down'
				vy = v
		
		self.player.walking = False
		if vx != 0 or vy != 0:
			self.player.walking = True
		
		self.do_sprite_move(self.player, vx, vy)
		
	def Update(self, game_counter):
		play_music('highlightsoflight')
		self.level.update_tile_standing_on(self.player.layer, self.player.x, self.player.y)
		
		for sprite in self.get_sprites():
			sprite.Update()
	
	def Render(self, screen):
		
		offset = self.get_camera_offset()
		
		self.level.Render('Stairs', screen, offset[0], offset[1], self.render_counter)
		for layerName in 'A B C D E F Stairs'.split(' '):
			if layerName != 'Stairs':
				self.level.Render(layerName, screen, offset[0], offset[1], self.render_counter)
			
			for sprite in self.get_renderable_sprites(layerName):
				img = sprite.CurrentImage(self.render_counter)
				coords = sprite.DrawingCoords()
				screen.blit(img, (coords[0] + offset[0], coords[1] + offset[1]))
		self.render_counter += 1
	
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
			print offset_x
			offset_x = min(offset_x, 0)
			offset_x = max(offset_x, -(width - screen_width))
			
		if height < screen_height:
			offset_y = (screen_height - height) / 2
		elif height > screen_height:
			offset_y = screen_height / 2 - player_y
			offset_y = min(offset_y, 0)
			offset_y = max(offset_y, -(height - screen_height))
		return (offset_x, offset_y)
	
	def get_sprites(self):
		return [self.player]
	
	def get_renderable_sprites(self, layer):
		if self.player.layer == layer and not self.player_invisible:
			return [self.player]
		else:
			return []
	
	def do_sprite_move(self, sprite, vx, vy):
		
		# returns (final layer, final x, final y)
		params = self.level.move_request(sprite.layer, sprite.x, sprite.y, vx, vy, sprite.r - 3)
		sprite.layer = params[0]
		sprite.x = params[1]
		sprite.y = params[2]
		