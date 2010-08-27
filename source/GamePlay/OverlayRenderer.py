class OverlayRenderer:
	def __init__(self):
		self.compass = CompassRenderer()
	
	def Render(self, screen):
		pygame.draw.rect(screen, (0,0,255), Rect(4, 4, 10, 3))
		self.compass.Render(screen, None)
		