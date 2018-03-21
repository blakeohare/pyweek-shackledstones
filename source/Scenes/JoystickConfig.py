class JoystickConfigScene:
	def __init__(self):
		self.keys = 'up down left right start X Y A B'.split(' ')
		
		self.text = render_text_size(45, "Push this button", WHITE, MENU_FONT)
		self.error = render_text_size(20, "No Gamepads are plugged in!", WHITE, MENU_FONT)
		self.error_explain = render_text_size(14, "Plug in a USB game pad and relaunch the game", WHITE, MENU_FONT)
		self.texts = [
		'Without a gamepad, use the following keys:',
		' Space - item 1',
		' A - item 2',
		' S - item 3',
		' D - item 4',
		' Enter - inventory screen',
		' Esc - Exit'
		]
		for i in range(len(self.texts)):
			self.texts[i] =  render_text_size(14, self.texts[i], WHITE, MENU_FONT)
			
		self.keyboard = render_text_size(14, "Plug in a USB game pad and relaunch the game", WHITE, MENU_FONT)
		self.is_error = getInputManager().active_joystick == None
		self.render_counter = 1
		self.active_key_index = 0
		self.joystick = getInputManager().active_joystick
		self.done = False
		self.next = self
		
		self.hackery = False
		
		self.images = {
			'up' : get_image('ui/joystick/control_up'),
			'down' : get_image('ui/joystick/control_down'),
			'left' : get_image('ui/joystick/control_left'),
			'right' : get_image('ui/joystick/control_right'),
			'start' : get_image('ui/joystick/control_start'),
			'A' : get_image('ui/joystick/control_a'),
			'B' : get_image('ui/joystick/control_b'),
			'X' : get_image('ui/joystick/control_x'),
			'Y' : get_image('ui/joystick/control_y')
			}
		
		if not self.is_error:
			self.joystick.js.init()
		
	def get_bg_for_key(self, key):
		return self.images[key]
		
	def processInput(self, events):
		if self.is_error or self.done:
			for event in events:
				if event.down:
					if self.is_error:
						self.next = MainMenuScene()
					else:
						if not self.hackery:
							self.hackery = True
						else:
							self.next = MainMenuScene()
							
		
	def update(self, conter):
		if not self.is_error:
			if self.active_key_index < len(self.keys):
				active_key = self.keys[self.active_key_index]
				if self.joystick.configure_key(active_key):
					self.active_key_index += 1
					if self.active_key_index == len(self.keys):
						self.text = render_text_size(45, "Done!", WHITE, MENU_FONT)
						self.done = True
					
				
		
	def render(self, screen, renderOffset):
		if self.is_error:
			self.error.draw(10, 10)
			self.error_explain.draw(10, 60)
			
			for i in range(len(self.texts)):
				self.texts[i].draw(10, 100 + i * 20)
			return
		
		image = get_image('ui/joystick/base_control')
		if self.active_key_index < len(self.keys) and (self.render_counter // 15) % 2 == 0:
			image = self.get_bg_for_key(self.keys[self.active_key_index])
		
		image.draw(0, 0)
		
		self.text.draw(10, 10)
		
		self.render_counter += 1
