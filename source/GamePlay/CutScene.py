"""
pause duration
input button duration
dialog script_name
sprite setState sprite_id state
sprite setXY sprite_id X Y duration|instant

"""
class CutSceneEvent:
	def __init__(self, command):
		parts = trim(command).split(' ')
		args = parts[1:]
		name = parts[0].lower()
		self.expiration = -1
		self.key_pressed = ''
		if name == 'pause':
			self.do = self.pause
			self.expiration = int(args[0])
		elif name == 'input':
			self.do = self.do_input
			self.button = args[0]
			self.key_pressed = self.button
			self.expiration = int(args[1])
		elif name == 'dialog':
			self.do = self.show_dialog
			self.dialog_script = args[0]
			self.expiration = -1
		elif name == 'sprite':
			if args[0].lower() == 'setstate':
				self.sprite_id = args[1]
				self.sprite_state = args[2]
				self.do = self.setspritestate
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
				
				
	def is_key_pressed(self, key):
		return self.key_pressed == key
		
	def pause(self, game_scene):
		pass
	
	def do_input(self, game_scene):
		pass
	
	def show_dialog(self, game_scene):
		game_scene.next = DialogScene(
			Dialog(Parser.LoadFile(scriptPath(self.dialog_script))), game_scene)
	
	def setspritestate(self, game_scene):
		pass
	
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
		
	def is_done(self):
		return len(self.commands) == 0
	
	def is_key_pressed(self, key):
		return len(self.commands) > 0 and self.commands[0].is_key_pressed(key)
	
	def get_input_events(self):
		events = self.event_queue
		self.event_queue = []
		return events
	
	def do(self, game_scene):
		if not self.is_done():
			command = self.commands[0]
			command.do(game_scene)
			command.expiration -= 1
			if command.expiration < 0:
				if command.key_pressed != '':
					self.event_queue.append(InputEvent(command.key_pressed, False))
				self.commands = self.commands[1:]
				if len(self.commands) > 0 and self.commands[0].key_pressed != '':
					self.event_queue.append(InputEvent(self.commands[0].key_pressed, True))
				

### STATIC ###

_cutSceneStore = {
'test' : """input left 30
dialog test
input down 30
input B 4"""
}

def get_cutscene(name):
	global _cutSceneStore
	script = _cutSceneStore[name]
	return CutScene(script)
	
def get_cutscene_for_map(map_name):
	if map_name == 'world_D':
		return get_cutscene('test')
	return None
	