class Player:
	def __init__(self):
		self.x = 100
		self.y = 100
		self.layer = 'A'
		self.r = 8
		self.direction = 'right'
	
	def DrawingCoords(self):
		return (self.x - self.r, self.y - self.r)
	
	def CurrentImage(self, render_counter):
		if self.direction == 'right':
			return get_image('sprites/maincharacter/right0')
		if self.direction == 'left':
			return get_image('sprites/maincharacter/left0')
		if self.direction == 'up':
			return get_image('sprites/maincharacter/up0')
		if self.direction == 'down':
			return get_image('sprites/maincharacter/down0')
		return get_image('sprites/maincharacter/down0')
		
class GamePlayScene:
	
	def __init__(self):
		self.render_counter = 0
		self.next = self
		self.player = Player()
		self.level = Level('test_level')
	
	def ProcessInput(self, events):
		v = 3
		if is_pressed('left'):
			self.player.direction = 'left'
			self.player.x -= v
		elif is_pressed('right'):
			self.player.direction = 'right'
			self.player.x += v
		if is_pressed('up'):
			self.player.direction = 'up'
			self.player.y -= v
		elif is_pressed('down'):
			self.player.direction = 'down'
			self.player.y += v
		
	def Update(self, game_counter):
		pass
	
	def Render(self, screen):
		
		offset = self.get_camera_offset()
		
		for layerName in 'A B C D E F Stairs'.split(' '):
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
			offset_x = min(offset_x, 0)
			offset_x = max(offset_x, -width)
			
		if height < screen_height:
			offset_y = (screen_height - height) / 2
		elif height > screen_height:
			offset_y = screen_height / 2 - player_y
			offset_y = min(offset_y, 0)
			offset_y = max(offset_y, -height)
		return (offset_x, offset_y)
	
	def get_renderable_sprites(self, layer):
		if self.player.layer == layer:
			return [self.player]
		else:
			return []