


class JoystickConfigScene:
	def __init__(self):
		global _inputManager
		self.keys = 'up down left right start X Y A B'.split(' ')
		
		self.text = render_text_size(45, "Push this button", WHITE, MENU_FONT)
		self.error = render_text_size(20, "No Gamepads are plugged in!", WHITE, MENU_FONT)
		self.error_explain = render_text_size(14, "Plug in a USB game pad and relaunch the game", WHITE, MENU_FONT)
		self.is_error = _inputManager.active_joystick == None
		self.render_counter = 1
		self.active_key_index = 0
		self.joystick = _inputManager.active_joystick
		self.done = False
		self.next = self
		
		self.hackery = False
		
		self.images = {
			'up' : get_image('ui/joystick/control_up'),
			'down' : get_image('ui/joystick/control_down'),
			'left' : get_image('ui/joystick/control_left'),
			'right' : get_image('ui/joystick/control_right'),
			'start' : get_image('ui/joystick/control_start'),
			'A' : get_image('ui/joystick/control_A'),
			'B' : get_image('ui/joystick/control_B'),
			'X' : get_image('ui/joystick/control_X'),
			'Y' : get_image('ui/joystick/control_Y')
			}
		
		if not self.is_error:
			self.joystick.js.init()
		
	def get_bg_for_key(self, key):
		return self.images[key]
		
	def ProcessInput(self, events):
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
							
		
	def Update(self, conter):
		if not self.is_error:
			if self.active_key_index < len(self.keys):
				active_key = self.keys[self.active_key_index]
				if self.joystick.configure_key(active_key):
					self.active_key_index += 1
					if self.active_key_index == len(self.keys):
						self.text = render_text_size(45, "Done!", WHITE, MENU_FONT)
						self.done = True
					
				
		
	def Render(self, screen):
		if self.is_error:
			screen.blit(self.error, (10, 10))
			screen.blit(self.error_explain, (10, 60))
			return
		
		image = get_image('ui/joystick/base_control')
		if self.active_key_index < len(self.keys) and (self.render_counter // 15) % 2 == 0:
			image = self.get_bg_for_key(self.keys[self.active_key_index])
		
		screen.blit(image, (0, 0))
		
		screen.blit(self.text, (10, 10))
		
		
		self.render_counter += 1