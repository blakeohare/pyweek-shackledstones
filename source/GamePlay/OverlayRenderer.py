class OverlayRenderer:
	def __init__(self):
		self.compass = CompassRenderer()
		self.keys = KeyRenderer()
	
	def Render(self, screen):
		self.compass.Render(screen, None)
		self.keys.Render(screen,ActiveGame().GetActiveGameScene())
		
		life = get_life()
		max_life = get_max_life()
		
		top = 8
		left = 150
		width = 10
		height = 12
		i = 0
		
		surf = get_image('ui/health/h' + str(life) + '.png')
		screen.blit(surf, (5, 5))
