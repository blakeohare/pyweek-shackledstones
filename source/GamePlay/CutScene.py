"""
pause duration
input button duration
dialog script_name
sprite setState sprite_id state
sprite create sprite_type sprite_id X Y layer state direction
sprite setdirection direction
sprite setXY sprite_id X Y duration|instant
shakescreen duration
save
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
		self.direction = 'xxxxxxxxxx'
		self.first_time_through = True
		self.instant = False
		if name == 'pause':
			self.do = self.pause
			self.expiration = int(args[0])
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
		elif name == 'shakescreen':
			self.expiration = int(args[0])
			self.play_sound_on = self.expiration
			self.do = self.shake_screen
		elif name == 'relighttorches':
			self.instant = True
			self.do = self.do_relighttorches
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
	
	def do_script(self, game_scene):
		go_script_go(self.script)
	
	def do_relighttorches(self, game_scene):
		game_scene.torch_puzzle_relight()
	
	def save(self, game_scene):
		ActiveGame().SaveToFile()
	
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
		#print sprite
		#print self.direction
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
		sprite = game_scene.get_sprite_by_id(self.sprite_id)
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
	sprite create meyer meyer 7 4 A standing left
	dialog transport1
	shakescreen 60
	pause 20
	dialog transport2
	pause 20
	sprite create pierce pierce 8 1 A standing down
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
	sprite create maple maple 7 1 A standing down
	dialog transport4
""",

'to_water_temple' : """
	sprite create maple maple 8 2 A standing left
	sprite create hanlon hanlon 7 7 A standing left
	sprite create pierce pierce 3 6 A standing right
	pause 15
	dialog to_water_temple1
	pause 90
	dialog to_water_temple2
	script [remove tile][door][doodad]
""",

'at_water_temple' : """
	input right 50
	input up 1
	
	sprite create hanlon hanlon 16 13 A walking right
	sprite setxy hanlon 22 13 30
	sprite setdirection hanlon right
	sprite setstate hanlon standing
	sprite setdirection hanlon up
	
	sprite create pierce pierce 16 13 A walking right
	sprite setxy pierce 20 13 30
	sprite setdirection pierce right
	sprite setstate pierce standing
	sprite setdirection pierce up
	
	sprite create maple maple 16 13 A walking right
	sprite setxy maple 18 13 10
	sprite setdirection maple right
	sprite setstate maple standing
	sprite setdirection maple up
	
	dialog water_temple_explain
""",

#TODO: play noise
'heard_mainroom_noise': """
	pause 15
	dialog heard_mainroom_noise
""",
#TODO: play noise
'loud_switch_noise': """
	pause 10
	
""",
#TODO: play TADA
'sword_found' : """
	dialog sword_found
""",

'water_elemental' : """
	pause 60
	dialog water_elemental
	pause 10
	script [set][stone_water][1]
	script [warp][world_A][water_entrance][pixelate]
""",
'save_point_routine' : """
	dialog do_save
""",
'torch_fail' : """
	pause 60
	relighttorches
""",
'torch_win' : """
	shakescreen 30
"""
}


_play_once = {
	'interrogation' : False,
	'at_water_temple' : False,
	
}

def get_cutscene(name):
	global _cutSceneStore
	script = _cutSceneStore[name]
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
	