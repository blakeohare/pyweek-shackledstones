class CutSceneEvent:
	def __init__(self, command):
		parts = command.strip().split(' ')
		args = parts[1:]
		name = parts[0].lower()
		self.expiration = -1
		self.key_pressed = ''
		self.render_offset = 0
		self.direction = 'xxxxxxxxxx'
		self.first_time_through = True
		self.instant = False
		if name == 'pause':
			self.do = self.pause
			self.expiration = int(args[0])
		elif name == 'clearbg':
			self.do = self.do_clearbg
			self.instant = True
		elif name == 'setbg':
			self.do = self.do_setbg
			self.instant = True
			self.image = args[0]
		elif name == 'flash':
			self.do = self.do_flash
			self.expiration = int(args[0])
			self.full_length = self.expiration
		elif name == 'save':
			self.do = self.save
		elif name == 'script':
			self.do = self.do_script
			self.script = ' '.join(args)
			self.instant = True
		elif name == 'input':
			self.do = self.do_input
			self.button = args[0]
			self.key_pressed = self.button
			self.expiration = int(args[1])
		elif name == 'dialog':
			self.do = self.show_dialog
			self.dialog_script = args[0]
			self.expiration = -1
		elif name == 'playsound':
			self.do = self.do_play_sound
			self.sound = args[0]
			self.instant = True
		elif name == 'shakescreen':
			self.expiration = int(args[0])
			self.play_sound_on = self.expiration
			self.do = self.shake_screen
		elif name == 'relighttorches':
			self.instant = True
			self.do = self.do_relighttorches
		elif name == 'turnlightswitchesoff':
			self.instant = True
			self.do = self.do_turnlightswitchesoff
		elif name == 'sprite':
			if args[0].lower() == 'delete':
				self.sprite_id =args[1]
				self.do = self.deletesprite
				self.instant=True
			if args[0].lower() == 'setstate':
				self.sprite_id = args[1]
				self.sprite_state = args[2]
				self.do = self.setspritestate
				self.instant = True
			elif args[0].lower() == 'create':
				self.sprite_name = args[1]
				self.sprite_id = args[2]
				self.x = int(args[3])
				self.y = int(args[4])
				self.layer = args[5]
				self.state = args[6]
				self.do = self.createsprite
				self.direction = args[7]
				self.instant = True
			elif args[0].lower() == 'setdirection':
				self.sprite_id = args[1]
				self.direction = args[2]
				#print self.direction
				self.do = self.setspritedirection
				self.instant = True
			elif args[0].lower() == 'setxy':
				self.sprite_id = args[1]
				self.do = self.setspriteloc
				self.x = int(args[2])
				self.y = int(args[3])
				self.instant = args[4].lower() == 'instant'
				self.expiration = -1
				if not self.instant:
					self.expiration = int(args[4])
					self.total = self.expiration
	
	def do_turnlightswitchesoff(self, game_scene):
		game_scene.turnlightswitchesoff()
	
	def do_script(self, game_scene):
		go_script_go(self.script)
	
	def do_setbg(self, game_scene):
		game_scene.bg = get_image(self.image)
	
	def do_clearbg(self, game_scene):
		game_scene.bg = None
	
	def do_flash(self, game_scene):
		antiprogress = min(1.0, max(0.0, (0.0 + self.expiration) / self.full_length))
		
		antiprogress = antiprogress * 2 - 1
		
		antiprogress = 1.0 - abs(antiprogress)
		#antiprogress = 1.0 - antiprogress
		game_scene.flash_amount = abs(antiprogress)
	
	def do_play_sound(self, game_scene):
		play_sound(self.sound)
	
	def do_relighttorches(self, game_scene):
		game_scene.torch_puzzle_relight()
	
	def save(self, game_scene):
		ActiveGame().SetSavedVar('save_map', game_scene.name)
		ActiveGame().SetSavedVar('save_x', game_scene.player.x)
		ActiveGame().SetSavedVar('save_y', game_scene.player.y)
		ActiveGame().SaveToFile()
	
	def shake_screen(self, game_scene):
		if self.expiration == self.play_sound_on:
			pass
			#print("TODO: play shaking sound")
		self.render_offset = (-2,2)[(self.expiration & 1) == 0]
		
	def is_key_pressed(self, key):
		return self.key_pressed == key
		
	def pause(self, game_scene):
		pass
	
	def do_input(self, game_scene):
		pass
	
	def setspritedirection(self, game_scene):
		sprite = game_scene.get_sprite_by_id(self.sprite_id)
		sprite.direction = self.direction
	
	def createsprite(self, game_scene):
		sprite = create_sprite(self.sprite_name, self.sprite_id)
		sprite.x = (self.x << 4) + 8
		sprite.y = (self.y << 4) + 8
		sprite.state = self.state
		sprite.layer = self.layer
		sprite.direction = self.direction
		game_scene.add_sprite(sprite)
	
	def deletesprite(self, game_scene):
		sprite = game_scene.get_sprite_by_id(self.sprite_id)
		sprite.expired=True
	
	def show_dialog(self, game_scene):
		game_scene.next = DialogScene(
			Dialog(Parser.LoadFile('data/scripts/' + self.dialog_script + '.txt')), game_scene)
	
	def setspritestate(self, game_scene):
		sprite = game_scene.get_sprite_by_id(self.sprite_id)
		sprite.state = self.sprite_state
		
	def setspriteloc(self, game_scene):
		sprite = game_scene.get_sprite_by_id(self.sprite_id)
		if not sprite:
			return
		if self.first_time_through:
			self.source_x = sprite.x
			self.source_y = sprite.y
		target_x = (self.x << 4) + 8
		target_y = (self.y << 4) + 8
		if self.instant:
			sprite.x = target_x
			sprite.y = target_y
		else:
			progress = 1 - ((0.0 + self.expiration) / self.total)
			anti_progress = 1 - progress
			sprite.x = target_x * progress + anti_progress * self.source_x
			sprite.y = target_y * progress + anti_progress * self.source_y
			
		self.first_time_through = False

class CutScene:
	
	def __init__(self, command_script, name):
		self.name = name
		lines = command_script.strip().split('\n')
		commands = []
		for line in lines:
			command_line = line.strip()
			if len(command_line) > 0:
				commands.append(CutSceneEvent(command_line))
		self.commands = commands
		self.event_queue = []
	
	def render_offset(self):
		if len(self.commands) > 0:
			return self.commands[0].render_offset
	
	def is_done(self):
		return len(self.commands) == 0
	
	def is_key_pressed(self, key):
		return len(self.commands) > 0 and self.commands[0].is_key_pressed(key)
	
	def get_input_events(self):
		events = self.event_queue
		self.event_queue = []
		return events
	
	def do(self, game_scene):
		game_scene.flash_amount = 0
		while not self.is_done():
			command = self.commands[0]
			command.do(game_scene)
			command.expiration -= 1
			do_again = command.instant
			
			if command.expiration < 0:
				if command.key_pressed != '':
					self.event_queue.append(InputEvent(command.key_pressed, False))
				self.commands = self.commands[1:]
				if len(self.commands) > 0 and self.commands[0].key_pressed != '':
					self.event_queue.append(InputEvent(self.commands[0].key_pressed, True))
			if not do_again:
				return

### STATIC ###

_cutSceneStore = { }

_play_once = {
	'interrogation' : False,
	'at_water_temple' : False,
}

def get_cutscene(name):
	global _cutSceneStore
	script = _cutSceneStore.get(name)
	if script == None:
		script = read_text_file('data/cutscenes/' + name + '.txt').strip()
		_cutSceneStore[name] = script
	return CutScene(script, name)
	
def get_cutscene_for_map(map_name):
	global _play_once
	cs = None
	cs_name = None
	if map_name == 'transport_1':
		cs_name = 'interrogation'
	elif map_name == 'escape_pod':
		cs_name = 'to_water_temple'
	elif map_name == 'world_A':
		cs_name = 'at_water_temple'
	
	if cs_name != None:
		cs = get_cutscene(cs_name)
	played_already = _play_once.get(cs_name)
	if played_already != None:
		key = 'cut_scene_play_once_' + cs_name
		if ActiveGame().GetVar(key) == 1:
			cs = None
		else:
			ActiveGame().SetSavedVar(key, 1)
			
	return cs
