
_new_enemies = []

def reserializeEnemies():
	global _new_enemies
	active_game = ActiveGame()
	if active_game != None:
		gs = active_game.GetActiveGameScene()
		if gs != None:
			file = gs.name
			c = open('maps' + os.sep + file  + '.txt', 'rt')
			lines = c.read().split('\n')
			c.close()
			
			output = []
			current = []
			for rline in lines:
				line = trim(rline)
				pieces = line.split(':')
				if pieces[0] != '#enemies':
					output.append(line)
				else:
					value = trim(pieces[1])
					if len(value) > 0:
						current = value.split(',') + _new_enemies
					else:
						current = _new_enemies[:]
			output.append('#enemies:' + ','.join(current))
			output = '\n'.join(output)
			c = open('maps' + os.sep + file + '.txt', 'wt')
			c.write(output)
			c.close()
			
					
def start_enemy_insertion_session():
	global _new_enemies
	_new_enmies = []

def insert_enemy(key):
	global _new_enemies
	active_game = ActiveGame()
	if active_game != None:
		gs = active_game.GetActiveGameScene()
		if gs != None:
			x = gs.player.x >> 4
			y = gs.player.y >> 4
			layer = gs.player.layer
			if key == '1':
				type = 'blob'
			elif key == '2':
				type = 'mechanicalman'
			elif key == '3':
				type = 'eyeball'
			else:
				type = None
			
			if type != None:
				_new_enemies.append(type + '|' + layer + '|' + str(x) + '|' + str(y))
				sprite = Enemy(type)
				sprite.x = (x << 4) + 8
				sprite.y = (y << 4) + 8
				sprite.layer = layer
				gs.sprites.append(sprite)
			

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
					
	
_allowEnemyEdit = True
_enemyEditMode = False

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
		self.video_mode = None
		
	def initializeJoystick(self):
		
		joysticks = []
		for i in range(pygame.joystick.get_count()):
			joysticks.append(Joystick(pygame.joystick.Joystick(i)))
		
		self.joysticks = joysticks
		if len(joysticks) >= 1:
			self.active_joystick = self.joysticks[0]
	
	def VideoModeChange(self):
		return self.video_mode
	
	def get_events(self):
		
		global _allowEnemyEdit, _enemyEditMode
		
		self.key_pressed_now = ''
		events = []
		joystick = self.active_joystick
		if joystick != None:
			for key in self.keys:
				state = joystick.state_changed(key)
				if state != None:
					events.append(InputEvent(key, state))
		
		self.video_mode = None
		
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
				elif event.key == K_f:
					self.video_mode = 'full'
				elif event.key == K_w:
					self.video_mode = 'wide'
				if _allowEnemyEdit:
					if event.key == K_e:
						_enemyEditMode = not _enemyEditMode
						if _enemyEditMode:
							start_enemy_insertion_session()
						else:
							reserializeEnemies()
							
					elif _enemyEditMode:
						if event.key == K_1:
							insert_enemy('1')
						elif event.key == K_2:
							insert_enemy('2')
						elif event.key == K_3:
							insert_enemy('3')
						elif event.key == K_4:
							insert_enemy('4')
						elif event.key == K_5:
							insert_enemy('5')
						elif event.key == K_6:
							insert_enemy('6')
						elif event.key == K_7:
							insert_enemy('7')
						elif event.key == K_8:
							insert_enemy('8')
						elif event.key == K_9:
							insert_enemy('9')
						elif event.key == K_0:
							insert_enemy('0')
						
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
				


### STATIC ###

_inputManager = InputManager()
def is_pressed(key):
	return _inputManager.is_pressed[key]