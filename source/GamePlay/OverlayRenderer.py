class OverlayRenderer:
	def __init__(self):
		self.compass = CompassRenderer()
	
	def Render(self, screen):
		self.compass.Render(screen, None)
		
		life = get_life()
		max_life = get_max_life()
		
		
		top = 8
		left = 150
		width = 10
		height = 12
		i = 0
		while i < max_life:
			x = left + i * width
			y = top
			pygame.draw.rect(screen, (50, 50, 50), Rect(x, y, width - 1, height))
			pygame.draw.rect(screen, (0, 0, 0),    Rect(x + 1, y + 1, width - 3, height - 2))
			pygame.draw.rect(screen, (255, 0, 0),  Rect(x + 2, y + 2, width - 5, height - 4))
			pygame.draw.rect(screen, (140, 0, 0),  Rect(x + 2, y + 7, width - 5, height - 9))  
			i += 1
		