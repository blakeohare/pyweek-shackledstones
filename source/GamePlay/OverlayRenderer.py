class OverlayRenderer:
	def __init__(self):
		pass
	
	def Render(self, screen):
		pygame.draw.rect(screen, (0,0,255), Rect(4, 4, 10, 3))