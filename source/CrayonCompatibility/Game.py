
Game = EmptyObj()

_activeScreen = None

class GameWindow:
	def __init__(self, title, fps, width, height, screen_width, screen_height):
		global _activeScreen
		self.title = title
		self.fps = fps
		
		pygame.init()
		
		self.real_screen = pygame.display.set_mode((screen_width, screen_height))
		_activeScreen = pygame.Surface((width, height)).convert()
		
		pygame.display.set_caption(title)
		
		# TODO: this will need to be set in the build file
		pygame.display.set_icon(pygame.image.load("icon.png"))
		
		self.lastFrameTime = time.time()
	
	def pumpEvents(self):
		# TODO: replace with Crayon events
		return pygame.event.get()
	
	def clockTick(self):
		
		pygame.transform.scale(_activeScreen, self.real_screen.get_size(), self.real_screen)
		
		pygame.display.flip()
		
		now = time.time()
		diff = now - self.lastFrameTime
		
		delay = 1.0 / self.fps - diff
		if delay > 0:
			time.sleep(delay)
		self.lastFrameTime = time.time()
