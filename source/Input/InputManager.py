
class InputEvent:
	def __init__(self, key, down):
		self.key = key
		self.down = down
		self.up = not down
	
	def Up(self):
		return self.key == 'up'
	def Down(self):
		return self.key == 'down'
	def Right(self):
		return self.key == 'right'
	def Left(self):
		return self.key == 'left'
	def A(self):
		return self.key == 'A'
	def B(self):
		return self.key == 'B'
	def X(self):
		return self.key == 'X'
	def Y(self):
		return self.key == 'Y'
	def Start(self):
		return self.key == 'start'
	
	def __str__(self):
		if self.up:
			p = 'not '
		else:
			p = ''
		return 'key: %s, %spressed' % (str(self.key), p)

class Joystick:
	def __init__(self, pygameJoystick):
		self.js = pygameJoystick
		self.name = self.js.get_name()
		
		self.config = {
			'start' : None,
			'A' : None,
			'B' : None,
			'Y' : None,
			'X' : None,
			'up' : None,
			'down' : None,
			'left' : None,
			'right' : None
		}
		
		self.is_pressed = {
			'start' : False,
			'A' : False,
			'B' : False,
			'X' : False,
			'Y' : False,
			'up' : False,
			'down' : False,
			'left' : False,
			'right' : False
		}
		self.prev_config = None
		
	# returns None when state doesn't change
	# returns True when key is pushed
	# returns False when key is released
	def state_changed(self, key):
		config = self.config[key]
		if config == None: return None
		
		pressed = False
		if config[0] == 'hat':
			hat_status = self.js.get_hat(config[1])
			if hat_status[0] == 1 and config[2] == 'right':
				pressed = True
			elif hat_status[0] == -1 and config[2] == 'left':
				pressed = True
			elif hat_status[1] == 1 and config[2] == 'up':
				pressed = True
			elif hat_status[1] == -1 and config[2] == 'down':
				pressed = True
			else:
				pressed = False
		elif config[0] == 'axis':
			axis_status = self.js.get_axis(config[1])
			if config[2]:
				if axis_status > .5:
					pressed = True
			else:
				if axis_status < -.5:
					pressed = True
		elif config[0] == 'button':
			pressed = self.js.get_button(config[1])
			
		if pressed != self.is_pressed[key]:
			self.is_pressed[key] = pressed
			return pressed
		return None
		
	
	def configure_key(self, keyname):
		key = self.get_first_pressed()
		if key != None and key != self.prev_config:
			self.config[keyname] = key
			self.prev_config = key
			return True
		return False
	
	def get_first_pressed(self):
		for hat_num in range(self.js.get_numhats()):
			hat = self.js.get_hat(hat_num)
			if hat != (0,0):
				if hat[0] == -1:
					return ('hat', hat_num, 'left')
				elif hat[0] == 1:
					return ('hat', hat_num, 'right')
				if hat[1] == -1:
					return ('hat', hat_num, 'down')
				elif hat[1] == 1:
					return ('hat', hat_num, 'up')
		for but_num in range(self.js.get_numbuttons()):
			button = self.js.get_button(but_num)
			if button:
				return ('button', but_num)
		
		for ax_num in range(self.js.get_numaxes()):
			axis = self.js.get_axis(ax_num)
			if axis > .5:
				return ('axis', ax_num, 1)
			elif axis < -.5:
				return ('axis', ax_num, -1)
		return None

class InputManager:
	
	def __init__(self):
		self.key_pressed_now = ''
		
		self.is_pressed = {
			'up' : False,
			'down' : False,
			'left' : False,
			'right' : False,
			'start' : False,
			'A' : False,
			'B' : False,
			'Y' : False,
			'X' : False
		}
		self.escape_attempted = False
		self.active_joystick = None
		
		self.keys = 'up down left right start A B X Y'.split(' ')
		
	def initializeJoystick(self):
		
		joysticks = []
		for i in range(pygame.joystick.get_count()):
			joysticks.append(Joystick(pygame.joystick.Joystick(i)))
		
		self.joysticks = joysticks
		if len(joysticks) >= 1:
			self.active_joystick = self.joysticks[0]
	
	def get_events(self):
		
		self.key_pressed_now = ''
		events = []
		joystick = self.active_joystick
		if joystick != None:
			for key in self.keys:
				state = joystick.state_changed(key)
				if state != None:
					events.append(InputEvent(key, state))
		
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
				elif event.key == K_RETURN:
					events.append(InputEvent('start', True))
				
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
				elif event.key == K_RETURN:
					events.append(InputEvent('start', False))
			
		for event in events:
			self.is_pressed[event.key] = event.down
		
		return events

def getInputManager():
	global _inputManager
	if _inputManager == None:
		_inputManager = InputManager()
	return _inputManager

def is_pressed(key):
	return getInputManager().is_pressed[key]
