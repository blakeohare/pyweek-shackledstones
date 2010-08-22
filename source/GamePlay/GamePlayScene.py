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
		v = 2
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
	
		self.level.Render(screen, 0, 0, self.render_counter)
		
		for sprite in self.get_renderable_sprites():
			img = sprite.CurrentImage(self.render_counter)
			coords = sprite.DrawingCoords()
			screen.blit(img, coords)
		#pygame.draw.rect(screen, (255, 0, 0), Rect(self.x - r, self.y - r, r * 2, r * 2))
		self.render_counter += 1
	
	def get_renderable_sprites(self):
		return [self.player]