class OverlayRenderer:
	def __init__(self):
		self.compass = CompassRenderer()
		self.keys = KeyRenderer()
	
	def render(self, screen):
		self.compass.render(screen, None)
		self.keys.render(screen,getActiveGame().getActiveGameScene())
		
		life = get_life()
		max_life = get_max_life()
		
		top = 8
		left = 150
		width = 10
		height = 12
		i = 0
		
		surf = get_image('ui/health/h' + str(life) + '.png')
		surf.draw(5, 5)
