class InputEvent:
	def __init__(self, key, down):
		self.key = key
		self.down = down
		self.up = not down
	
	def __str__(self):
		if self.up:
			p = 'not '
		else:
			p = ''
		return 'key: %s, %spressed' % (str(self.key), p)

#TODO: Joystick management
class InputManager:
	
	def __init__(self):
		self.is_pressed = {
			'up' : False,
			'down' : False,
			'left' : False,
			'right' : False,
			'start' : False,
			'A' : False,
			'B' : False,
			'Y' : False,
			'X' : False,
			'L' : False,
			'R' : False
		}
		self.escape_attempted = False
		
	def get_events(self):
		events = []
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				self.escape_attempted = True
			elif event.type == KEYDOWN:
				if event.key == K_UP:
					events.append(InputEvent('up', True))
				elif event.key == K_DOWN:
					events.append(InputEvent('down', True))
				elif event.key == K_RIGHT:
					events.append(InputEvent('right', True))
				elif event.key == K_LEFT:
					events.append(InputEvent('left', True))
				elif event.key == K_SPACE:
					events.append(InputEvent('B', True))
				elif event.key == K_a:
					events.append(InputEvent('A', True))
				elif event.key == K_s:
					events.append(InputEvent('Y', True))
				elif event.key == K_d:
					events.append(InputEvent('X', True))
			elif event.type == KEYUP:
				if event.key == K_UP:
					events.append(InputEvent('up', False))
				elif event.key == K_DOWN:
					events.append(InputEvent('down', False))
				elif event.key == K_RIGHT:
					events.append(InputEvent('right', False))
				elif event.key == K_LEFT:
					events.append(InputEvent('left', False))
				elif event.key == K_SPACE:
					events.append(InputEvent('B', False))
				elif event.key == K_a:
					events.append(InputEvent('A', False))
				elif event.key == K_s:
					events.append(InputEvent('Y', False))
				elif event.key == K_d:
					events.append(InputEvent('X', False))
		
		for event in events:
			self.is_pressed[event.key] = event.down
		
		return events
				


### STATIC ###

_inputManager = InputManager()
def is_pressed(key):
	return _inputManager.is_pressed[key]