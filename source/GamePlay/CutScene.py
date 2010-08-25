"""
pause duration
input button duration
dialog script_name
sprite setState sprite_id state
sprite create sprite_type sprite_id X Y layer state direction
sprite setdirection direction
sprite setXY sprite_id X Y duration|instant
shakescreen duration
script scriptline
"""
class CutSceneEvent:
	def __init__(self, command):
		parts = trim(command).split(' ')
		args = parts[1:]
		name = parts[0].lower()
		self.expiration = -1
		self.key_pressed = ''
		self.render_offset = 0
		self.instant = False
		if name == 'pause':
			self.do = self.pause
			self.expiration = int(args[0])
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
		elif name == 'shakescreen':
			self.expiration = int(args[0])
			self.play_sound_on = self.expiration
			self.do = self.shake_screen
		elif name == 'sprite':
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
	
	def do_script(self, game_scene):
		go_script_go(self.script)
	
	def shake_screen(self, game_scene):
		if self.expiration == self.play_sound_on:
			print("TODO: play shaking sound")
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
		sprite.x = (self.x << 4)
		sprite.y = (self.y << 4)
		sprite.state = self.state
		sprite.layer = self.layer
		sprite.direction = self.direction
		game_scene.add_sprite(sprite)
	
	def show_dialog(self, game_scene):
		game_scene.next = DialogScene(
			Dialog(Parser.LoadFile(scriptPath(self.dialog_script))), game_scene)
	
	def setspritestate(self, game_scene):
		sprite = game_scene.get_sprite_by_id(self.sprite_id)
		sprite.direction = self.direction
	
	def setspriteloc(self, game_scene):
		pass
	
	
		
		

class CutScene:
	
	def __init__(self, command_script):
		lines = trim(command_script).split('\n')
		commands = []
		for line in lines:
			command_line = trim(line)
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

_cutSceneStore = {
'test' : """
	input left 30
	dialog test
	input down 30
	input B 4
""",

'interrogation' : """
	sprite create meyer meyer 7 4 A walking left
	dialog transport1
	shakescreen 60
	pause 20
	dialog transport2
	pause 20
	sprite create pierce pierce 8 1 A walking down
	script [remove tile][to_north][doodad]
	dialog transport3
""",

'maple_crashes_in' : """
	script [remove tile][water_stone][doodad]
	pause 15
	shakescreen 30
	pause 10
	script [remove tile][to_north][doodad]
	pause 12
	sprite create maple maple 7 1 A walking down
	dialog transport4
"""
}


_play_once = {
	'interrogation' : False
}

def get_cutscene(name):
	global _cutSceneStore
	script = _cutSceneStore[name]
	return CutScene(script)
	
def get_cutscene_for_map(map_name):
	global _play_once
	cs = None
	if map_name == 'world_D':
		cs = get_cutscene('test')
	elif map_name == 'transport_1':
		cs = get_cutscene('interrogation')
	played_already = _play_once.get(cs)
	if played_already != None:
		_play_once[cs] = True
		if played_already:
			cs = None
			
	return cs
	