class GamePlayScene:
	
	def __init__(self):
		self.next = self
		self.x = 100
		self.y = 100
	
	def ProcessInput(self, events):
		v = 2
		if is_pressed('left'):
			self.x -= v
		elif is_pressed('right'):
			self.x += v
		if is_pressed('up'):
			self.y -= v
		elif is_pressed('down'):
			self.y += v
		
		
				
	
	def Update(self, game_counter):
		pass
		
	def Render(self, screen):
		r = 8
		pygame.draw.rect(screen, (255, 0, 0), Rect(self.x - r, self.y - r, r * 2, r * 2))
	