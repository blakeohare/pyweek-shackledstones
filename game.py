# The world is a happy place

import pygame
from pygame.locals import *

import os
import math
import time
import re
import sys

def trim(string):
	if string == None: return ''
	while len(string) > 0 and string[0] in ' \n\r\t':
		string = string[1:]
	while len(string) > 0 and string[-1] in ' \r\n\t':
		string = string[:-1]
	return string

def min(a, b):
	if a < b: return a
	return b
def max(a, b):
	if a < b: return b
	return a

def go_script_go(script_contents):
	MapScript(ScriptIter(script_contents.split('\n'))).Exec()

def scriptPath(*path):
   p = os.path.join('data', 'scripts', *path)
   p = '%s.scr' % (p)
   return p

def portraitPath(*path):
   p = os.path.join('images', 'portraits', *path)
   p = '%s.png' % p
   return p

def uiImgPath(*path):
   p = os.path.join('images', 'ui', *path)
   p = '%s.png' % p
   return p
### .\source\aaaa.py

testSet = []

class Test:
   def __init__(self, name, fn):
      self._name = name
      self._fn = fn
   
   def __call__(self):
      print('\n%s\n------------------------------------------------------------' % self._name)
      self._fn()

def AddTest(name, fn):
   testSet.append(Test(name, fn))
   
def RunTests():
   for test in testSet:
      test()

### .\source\aScripted.py

class Scripted:
   def __init__(self, scriptIter):
      if not isinstance(scriptIter, ScriptIter):
         raise Exception("scriptIter must be an object of type ScriptIter")
      self._script = scriptIter
      self._fnTable = {}
      
      self._addFn('comment', self._noop)
      self._addFn('label', self._noop)
      self._addFn('jump', self._jump)
      self._addFn('check', self._checkVar)
      self._addFn('set', self._set)

   def _parse(self):
      for line in self._script:
         if Parser.IsCommand(line):
            (cmd, args) = Parser.Segment(line)
            c = self._call(cmd, args)
            
            if not c:
               break
         else:
            self._parseInternal(line)

   def _parseInternal(self, line):
      print('NOT_IMPLEMENTED')
   
   def _addFn(self, name, fn):
      self._fnTable[name] = fn
   
   def _call(self, name, args):
      if name in self._fnTable:
         return self._fnTable[name](*args)
      else:
         print('%s not registered' % name)

   # Move the script on it it's a multi-part deal.  Override this if you want
   # take special actions on script resume
   def Advance(self):
      self._parse()

   # function implementations
   # return indicates if script execution should continue (True) or stop until
   # the next call to Advance(False)
   def _checkVar(self, var, test, val, label, failLabel=None):
      sval = globalState.get(var)
      if test == 'eq':
         ret = (sval == val)
      elif test == 'lt':
         ret = (sval < val)
      elif test == 'lte.':
         ret = (sval <= val)
      elif test == 'gt':
         ret = (sval > val)
      elif test == 'gte':
         ret = (sval >= val)
      if ret:
         self._script.FindLabel(label)
      else:
         if failLabel:
            self._script.FindLabel(failLabel)
      return True
   
   def _set(self, var, val):
      globalState[var] = val
      return True

   def _jump(self, label):
      self._script.FindLabel(label)
      return True

   def _noop(self, *args):
      return True

### .\source\constants.py

testCode = True
testCode = False

WARP_NSCROLL  = "north scroll"
WARP_SSCROLL  = "south scroll"
WARP_ESCROLL  = "east scroll"
WARP_WSCROLL  = "west scroll"
WARP_PIXELATE = "pixelate"
WARP_INSTANT  = "instant"

KEY_LEFT  = 'left'
KEY_RIGHT = 'right'
KEY_UP    = 'up'
KEY_DOWN  = 'down'

WHITE = pygame.Color('#ffffff')
BLACK = pygame.Color('#000000')
BLUE = pygame.Color('#0000ff')

D_TEXT_OFFSET_X = 13
D_ANSWER_OFFSET_X = 25
D_TEXT_OFFSET_Y = 198



### .\source\Dialog.py

D_NORMAL   = 0
D_SCAN     = 1
D_PAUSE    = 2
D_QUESTION = 3
D_CHECKVAR = 4 
D_END      = 5

class Dialog(Scripted):
   # script -- ScriptIter
   def __init__(self, script):
      Scripted.__init__(self, script)
      self._profile = None
      self._state = D_NORMAL
      
      # What we should be displaying
      self._buffer = ''
      # When we're in question mode
      self._question = None
      # when we have a question what are the choices?
      self._choices = []
      
      self._addFn('profile', self._setProfile)
      self._addFn('pause', self._pause)
      self._addFn('question', self._beginQuestion)
      self._addFn('choice', self._addChoice)
      self._addFn('/question', self._poseQuestion)
      self._addFn('end', self._end)
      
      # perform the initial parse (fill the buffer)
      self.Advance()
   
   # Get the path to the current profile
   def Profile(self):
      return self._profile
   
   # Find out what mode the dialog is in
   def State(self):
      return self._state
   
   # get the next bit of stuff to display
   def Advance(self):
      # do not allow resuming if the dialog is finished
      if self.State() == D_END:
         return
      
      self._buffer = ''
      Scripted.Advance(self)
   
   # What we should be displaying if we're in "talk" mode (D_NORMAL)
   def Text(self):
      return trim(self._buffer)
   
   # what choices are available
   def Choices(self):
      if self.State() != D_QUESTION:
         print("ERR: Not in Question mode")
      options = []
      for a in self._choices:
         options.append(a.Text())
      return options
   
   # Answer a question
   # resp - which choice the user went with
   def Answer(self, resp):
      c = self._choices[resp]
      self._choices = []
      self._state = D_NORMAL
      self._script.FindLabel(c.Label())
   
   def _parseInternal(self, line):
      if len(line) == 0:
         return
         
      if line == '\\n':
         line = '$nl$'
      self._buffer += line + '\n'

   # function implementations
   # return indicates if script execution should continue (True) or stop until
   # the next Advance (False)
   def _beginQuestion(self, text):
      self._state = D_QUESTION
      self._choices = []
      self._buffer = text
      return True
   
   def _addChoice(self, label, text):
      self._choices.append(Choice(text, label))
      return True
   
   def _poseQuestion(self):
      return False
   
   def _setProfile(self, file):
      self._profile = file
      return True
   
   def _end(self):
      self._state = D_END
      return False
   
   def _pause(self):
      return False

class Choice:
   def __init__(self, txt, label):
      self._text = txt
      self._label = label
   def __str__(self):
      return '[%s] %s' % (self.Label(), self.Text())
   
   def Text(self):
      return self._text
   def Label(self):
      return self._label
   
###############################################################################
# Testing Code

def testDialog():
   si = Parser.LoadFile(scriptPath('test'))
   d = Dialog(si)
   
   print('----------------------')
   print('current dialog text:')
   print("'%s'" % d.Text())
   print('----------------------')
   
   d.Advance()
   print('----------------------')
   print('current dialog text:')
   print("'%s'" % d.Text())
   print('----------------------')
   
AddTest('testDialog', testDialog)

### .\source\GamePlay\GamePlayScene.py

class Player:
	def __init__(self):
		self.x = 100
		self.y = 100
		self.layer = 'A'
		self.r = 8
		self.direction = 'right'
	
	def DrawingCoords(self):
		return (self.x - self.r, self.y - self.r - 13)
	
	def CurrentImage(self, render_counter):
		if self.direction == 'right':
			return get_image('sprites/maincharacter/right0')
		if self.direction == 'left':
			return get_image('sprites/maincharacter/left0')
		if self.direction == 'up':
			return get_image('sprites/maincharacter/up0')
		if self.direction == 'down':
			return get_image('sprites/maincharacter/down0')
		return get_image('sprites/maincharacter/down0')
		
class GamePlayScene:
	
	def __init__(self, level_name, startX, startY):
		self.render_counter = 0
		self.next = self
		self.player = Player()
		self.player.x = startX
		self.player.y = startY
		self.level = Level(level_name)
	
	def ProcessInput(self, events):
		v = 3
		vx = 0
		vy = 0
		if is_pressed('left'):
			self.player.direction = 'left'
			vx = -v
		elif is_pressed('right'):
			self.player.direction = 'right'
			vx = v
		if is_pressed('up'):
			self.player.direction = 'up'
			vy = -v
		elif is_pressed('down'):
			self.player.direction = 'down'
			vy = v
		
		self.do_sprite_move(self.player, vx, vy)
		
	def Update(self, game_counter):
		pass
	
	def Render(self, screen):
		
		offset = self.get_camera_offset()
		
		self.level.Render('Stairs', screen, offset[0], offset[1], self.render_counter)
		for layerName in 'A B C D E F Stairs'.split(' '):
			if layerName != 'Stairs':
				self.level.Render(layerName, screen, offset[0], offset[1], self.render_counter)
			
			for sprite in self.get_renderable_sprites(layerName):
				img = sprite.CurrentImage(self.render_counter)
				coords = sprite.DrawingCoords()
				screen.blit(img, (coords[0] + offset[0], coords[1] + offset[1]))
		self.render_counter += 1
	
	def get_camera_offset(self):
		
		width = self.level.width * 16
		height = self.level.height * 16
		
		screen_width = 24 * 16
		screen_height = 18 * 16
		
		offset_x = 0
		offset_y = 0
		
		player_x = self.player.x
		player_y = self.player.y
		
		if width < screen_width:
			offset_x = (screen_width - width) / 2
		elif width > screen_width:
			offset_x = screen_width / 2 - player_x
			offset_x = min(offset_x, 0)
			offset_x = max(offset_x, -width)
			
		if height < screen_height:
			offset_y = (screen_height - height) / 2
		elif height > screen_height:
			offset_y = screen_height / 2 - player_y
			offset_y = min(offset_y, 0)
			offset_y = max(offset_y, -height)
		return (offset_x, offset_y)
	
	def get_renderable_sprites(self, layer):
		if self.player.layer == layer:
			return [self.player]
		else:
			return []
	
	def do_sprite_move(self, sprite, vx, vy):
		
		# returns (final layer, final x, final y)
		params = self.level.move_request(sprite.layer, sprite.x, sprite.y, vx, vy, sprite.r - 3)
		sprite.layer = params[0]
		sprite.x = params[1]
		sprite.y = params[2]
		

### .\source\GamePlay\Level.py


class TileTemplate:
	def __init__(self, parts):
		self.id = parts[0]
		self.physics = parts[2]
		self.imagefiles = parts[3].split('|')
		
		images = []
		for img in self.imagefiles:
			images.append(get_image('tiles' + os.sep + trim(img)))
		self.images = images
		
		if len(parts) == 5:
			self.anim_delay = int(parts[4])
		else:
			self.anim_delay = 4
		self.num_images = len(self.images)
		
	def Render(self, screen, x, y, render_counter):
		if self.num_images == 1:
			screen.blit(self.images[0], (x, y))
		else:
			screen.blit(
				self.images[(render_counter // self.anim_delay) % self.num_images],
				(x, y))


class TileStore:
	def __init__(self):
		tile_file = 'data' + os.sep + 'tiles.txt'
		c = open(tile_file, 'rt')
		lines = c.read().split('\n')
		c.close()
		
		self.templates = {}
		for line in lines:
			tline = trim(line)
			if len(tline) > 0 and tline[0] != '#':
				parts = tline.split('\t')
				if len(parts) == 4 or len(parts) == 5:
					template = TileTemplate(parts)
					self.templates[template.id] = template
	
	def GetTile(self, id):
		return self.templates.get(id)
			


class Tile:
	def __init__(self, id_list):
		tile_stack = []
		no_animations = True
		for id in id_list:
			if trim(id) != '':
				tile = _tileStore.GetTile(id)
				if tile.physics == 'floor':
					tile_stack = []
					no_animations = True
				tile_stack.append(tile)
				if tile.num_images > 1:
					no_animations = False
		self.stack = tile_stack
		if no_animations:
			self.Render = self._static_render
		#elif len(tile_stack) == 0:
		#	self.Render = self._dont_render
		else:
			self.Render = self._animation_render
		
		self.submerged = False
		self.ice = False
		self.keytype = None
		
		self.composite_physics()
	
	def composite_physics(self):
		if len(self.stack) == 0:
			self.physics = 'xxxx'
			return
		
		physics = [True, True, True, True]
		for tile in self.stack:
			tphys = tile.physics
			if tphys == 'floor': tphys = 'oooo'
			
			if len(tphys) == 4 and tphys[0] in 'ox' and tphys[1] in 'ox' and tphys[2] in 'ox' and tphys[3] in 'ox':
				for i in (0,1,2,3):
					physics[i] = physics[i] and tphys[i] == 'o'
			else:
				if tphys == 'water': self.submerged = True
				elif tphys == 'ice': self.ice = True
				
				elif tphys == 'redkey': self.keytype = 'red'
				elif tphys == 'bluekey': self.keytype = 'blue'
				elif tphys == 'greenkey': self.keytype = 'green'
				elif tphys == 'yellowkey': self.keytype = 'yellow'
				
				if self.keytype != None:
					physics = [False, False, False, False]
					break
		
		self.physics = 'xo'[physics[0]] + 'xo'[physics[1]] + 'xo'[physics[2]] + 'xo'[physics[3]]
	
	def is_stair_tile(self):
		self.physics = 'xxxx'
		self.Render = self._dont_render

	def _animation_render(self, screen, x, y, render_counter):
		for tile in self.stack:
			tile.Render(screen, x, y, render_counter)
	
	def _static_render(self, screen, x, y, render_counter):
		for tile in self.stack:
			screen.blit(tile.images[0], (x, y))
	
	def _dont_render(self, screen, x, y, render_counter):
		pass
			
class Layer:
	def __init__(self, width, height):
		self.contains_stuff = False
		self.width = width
		self.height = height
	def SetTiles(self, tile_list):
		self.tiles = make_table(self.width, self.height)
		self.contains_stuff = True
		y = 0
		while y < self.height:
			x = 0
			while x < self.width:
				self.tiles[x][y] = tile_list[x + y * self.width]
				x += 1
			y += 1

	def MarkStairTile(self, x, y):
		self.tiles[x][y].is_stair_tile()
		
	def Render(self, screen, x_offset, y_offset, render_counter):
		width = self.width
		height = self.height
		tiles = self.tiles
		
		left = max(0, int(x_offset / -16) - 2)
		top = max(0, int(y_offset / -16) - 2)
		right = min(left + 24 + 4, width)
		bottom = min(top + 18 + 4, height)
		
		y = top
		while y < bottom:
			x = left
			while x < right:
				tiles[x][y].Render(screen, x * 16 + x_offset, y * 16 + y_offset, render_counter)
				x += 1
			y += 1
	
def make_list(size):
	return [None] * size
def make_table(width, height):
	cols = make_list(width)
	i = 0
	while i < height:
		cols[i] = make_list(height)
		i += 1
	return cols
	
_tileStore = None
def get_tile_store():
	global _tileStore
	if _tileStore == None:
		_tileStore = TileStore()
	return _tileStore
	
class Level:
	def __init__(self, name):
		get_tile_store()
		self.parse_file(name)
	
	def parse_file(self, file):
		c = open('maps' + os.sep + file + '.txt', 'rt')
		lines = c.read().split('\n')
		c.close()
		
		values = {}
		for line in lines:
			parts = trim(line).split(':')
			if len(parts) >= 2:
				
				name = parts[0].split('#')[-1]
				value = trim(':'.join(parts[1:]))
				values[name] = value

		self.width = int(values['width'])
		self.height = int(values['height'])
		self.layers = {}
		for layerName in 'A B C D E F Stairs'.split(' '):
			content = values.get('Layer' + layerName)
			layer = Layer(self.width, self.height)
			if content != None:
				spots = trim(content).split(',')
				raw_tile_list = []
				for spot in spots:
					tiles = spot.split('|')
					raw_tile_list.append(Tile(tiles))
				layer.SetTiles(raw_tile_list)
			self.layers[layerName] = layer
		
		stair_layer = self.layers['Stairs']
		if stair_layer.contains_stuff:
			other_layers = 'A B C D E F'.split(' ')
			y = 0
			while y < self.height:
				x = 0
				while x < self.width:
					if stair_layer.tiles[x][y].physics != 'xxxx':
						for layerName in other_layers:
							layer = self.layers[layerName]
							if layer.contains_stuff:
								layer.tiles[x][y].is_stair_tile()
					x += 1
				y += 1
	def Render(self, layername, screen, x_offset, y_offset, render_counter):
		layer = self.layers[layername]
		if layer.contains_stuff:
			layer.Render(screen, x_offset, y_offset, render_counter)
	
	
	def is_stair_tile(self, x, y):
		stairs = self.layers['Stairs']
		if stairs.contains_stuff:
			return stairs.tiles[x][y].physics == 'oooo'
		return False
	
	def move_request(self, orig_layer, orig_x, orig_y, dx, dy, radius):
		dest_x = orig_x + dx
		dest_y = orig_y + dy
		
		left = orig_x
		right = orig_x
		top = orig_y
		bottom = orig_y
		
		if orig_x < dest_x:
			right = dest_x
		else:
			left = dest_x
		
		if orig_y < dest_y:
			bottom = dest_y
		else:
			top = dest_y
		
		left -= radius
		top -= radius
		right += radius
		bottom += radius
		
		walls = self.get_walls(orig_layer, left, top, right, bottom)

		if not self.rectangle_touches_walls(dest_x - radius, dest_y - radius, dest_x + radius, dest_y + radius, walls):
			coords = (dest_x, dest_y)
		else:
		
			coords = (orig_x, orig_y)
		tile_x = coords[0] >> 4
		tile_y = coords[1] >> 4
		if self.is_stair_tile(tile_x, tile_y):
			final_layer = "Stairs"
		else:
			if orig_layer == "Stairs":
				final_layer = 'A' # default value that ought to never get hit.
				# if there's every a bug where you get stuck in the stairs, start looking here
				for layerName in 'A B C D E F'.split(' '):
					layer = self.layers[layerName]
					if layer.contains_stuff:
						if layer.tiles[tile_x][tile_y].physics != 'xxxx':
							final_layer = layerName
							break
					
			else:
				final_layer = orig_layer
			
		return (final_layer, coords[0], coords[1])
	
	def rectangle_touches_walls(self, left, top, right, bottom, walls):
		
		for wall in walls:
			if left > wall[2] + wall[0] or top > wall[1] + wall[3] or right < wall[0] or bottom < wall[1]:
				continue
			return True
		return False
	
	# pixel coordinates
	def get_walls(self, layer, left, top, right, bottom):
		
		tile_left = (left - 4) >> 4
		tile_right = (right + 4) >> 4
		tile_top = (top - 4) >> 4
		tile_bottom = (bottom + 4) >> 4
		
		walls = []
		
		if layer != 'Stairs':
			layer = self.layers[layer]
			
			y = tile_top
			while y <= tile_bottom:
				x = tile_left
				while x <= tile_right:
					if not self.is_stair_tile(x, y):
						phys = layer.tiles[x][y].physics
						if phys == 'oooo':
							pass
						elif phys == 'xxxx':
							walls.append((x << 4, y << 4, 16, 16))
						else:
							if phys[0] == 'x':
								walls.append((x << 4, y << 4, 8, 8))
							if phys[1] == 'x':
								walls.append(((x << 4) + 8, y << 4, 8, 8))
							if phys[2] == 'x':
								walls.append((x << 4, (y << 4) + 8, 8, 8))
							if phys[3] == 'x':
								walls.append(((x << 4) + 8, (y << 4) + 8, 8, 8))
							
					x += 1
				y += 1
		else:
			layerNames = 'A B C D E F'.split(' ')
			y = tile_top
			while y <= tile_bottom:
				x = tile_left
				while x <= tile_right:
					if not self.is_stair_tile(x, y):
						for layerName in layerNames:
							other_layer = self.layers[layerName]
							any_found = False
							if other_layer.contains_stuff:
								phys = other_layer.tiles[x][y].physics 
								if phys == 'oooo':
									any_found = True
								elif phys == 'xxxx':
									pass
								else:
									any_found = True
									if phys[0] == 'x':
										walls.append((x << 4, y << 4, 8, 8))
									if phys[1] == 'x':
										walls.append(((x << 4) + 8, y << 4, 8, 8))
									if phys[2] == 'x':
										walls.append((x << 4, (y << 4) + 8, 8, 8))
									if phys[3] == 'x':
										walls.append(((x << 4) + 8, (y << 4) + 8, 8, 8))
							if any_found:
								break
						if not any_found:
							walls.append((x << 4, y << 4, 16, 16))
						
					x += 1
				y += 1
			
			
		
		return walls
		
		


### .\source\GamePlay\LevelStore.py



### .\source\ImageLib.py

class ImageLibraryClass:
   def __init__(self):
      self._lib = {} # stores name -> path
      self._pathLib = {} # stores path -> surface
   
   def Add(self, name, path):
      if self._lib.get(name):
         print("ImageLibrary already loaded %s" % name)
         return FromFile(self._lib[name])
         
      surf = self.FromFile(path)
      if surf:
         self._lib[name] = path
         return surf
      return None
      

   def Get(self, name):
      p = self._lib.get(name)
      if p:
         return self.FromFile(p)
      return None
   
   def FromFile(self, path):
      surf = self._pathLib.get(path)
      if surf:
         return surf

      if not os.path.exists(path):
         print('Could not load %s' % path)
         return None
      
      surf = pygame.image.load(path)
      if surf:
         self._pathLib[path] = surf
         return surf
      else:
         print('Could not load %s' % path)
         return None



### .\source\ImageLibrary.py


class ImageLibrary:

	def __init__(self):
		self.images = {}
	
	def get_image(self, path):
		img = self.images.get(path)
		if img == None:
			file_path = 'images' + os.sep + path.replace('/', os.sep).replace('\\', os.sep)
			if not file_path.endswith('.png'):
				file_path += '.png'
			
			self.images[path] = pygame.image.load(file_path)
		return self.images[path]



### .\source\Input\InputManager.py

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
				




### .\source\MapScript.py

class MapScript(Scripted):
   # script -- ScriptIter
   def __init__(self, scriptIter):
      Scripted.__init__(self, scriptIter)
   
   # get the next bit of stuff to display
   def Advance(self):
      return Scripted.Advance(self)
   
   # fancy name so it makes more sense
   def Exec(self):
      return self.Advance()
   
   def _parseInternal(self, line):
      print('MapScript._parseInternal(%s)' % line)

   # function implementations
   # return indicates if script execution should continue (True) or stop until
   # the next Advance (False)

### .\source\scriptybit.py

# uncomment for testing

class ParserClass:
   def __init__(self):
      self._re_bracket = re.compile('\s*\[(.*?)\]')
   
   # Is the input line a command?
   # Returns:
   #  False if not
   #  The command name if so
   def IsCommand(self, string):
      m = self._re_bracket.match(string)
      if m:
         return m.group(1)
      return False
   
   # Parse a script line into a tuple containing cmd and an array of args
   # Returns:
   #  False if not a command
   #  ($cmd, $args), where args is a list
   def Segment(self, string):
      if not self.IsCommand(string):
         return False
      
      p = self._re_bracket
      m = p.match(string)
      cmd = trim(m.group(1))
      args = []
      
      while True:
         m = p.match(string, m.end())
         if not m:
            break
         args.append(trim(m.group(1)))
      
      return (cmd, args)
   
   # Loads a file into a ScriptIter
   def LoadFile(self, path):
      if not path or not os.path.exists(path):
         print("ERR: %s could not be found" % (str(path)))
         return None
      f = open(path)
      
      scr = []
      for line in f:
         scr.append(trim(line))
      return ScriptIter(scr)
Parser = ParserClass()

# Abstration for the varying sources a script could come from
class ScriptIter:
      # script - an array of strings from any source
      def __init__(self, script):
         self._i = 0
         self._script = script

      # Utility to scan the script for a label.
      # Return:
      #  True - If the label is found, sets index such that Next 
      #         or __next__ will return the label
      #  False - If there is no label
      def FindLabel(self, label):
         idx = 0
         
         tgt = '\s*\[label\]\s*\[%s\]\s*' % (label)
         
         while (idx < len(self._script)):
            if re.match(tgt, self._script[idx]):
               self._i = idx
               return True
            idx += 1
         
         return False

      # Return the next line and step through the script
      def Next(self):
         return self.__next__()

      # Reset the script to the top
      def Reset(self):
         self._i = 0

      def __iter__(self):
         return self
      
      def next(self):
         return self.__next__()

      def __next__(self):
         idx = self._i
         if (idx >= len(self._script)):
            raise StopIteration
         
         self._i += 1
         return self._script[idx]


# encapsulates information about a script command
class Command:
   # cmd ------ text name
   # fn ------- a function pointer
   # argCount - how many args to expect, basic runtime validation
   def __init__(self, cmd, fn, argCount):
      self._name = cmd
      self._fnPtr = fn
      self._argCount = argCount
   
   def Name(self):
      return self._name
   
   def FnPtr(self):
      return self._fnPtr
   
   def ArgCount(self):
      return self._argCount

   # Call this function
   # args - a list of the arguments to call the function with
   def Call(self, args):
      if (len(args) != self.ArgCount()):
         print("ArgMismatch Exception...")
         print("    %s expects %d args" % (self.Name(), self.ArgCount()))
         print("    got '%s'" % (str(args)))
         
      return self.FnPtr().__call__(*args)


# associates strings with function pointers
class CommandRegistry:
   def __init__(self):
      self._commands = {}
   
   # Registers a new command with the scripting engine
   # cmd ------ text name
   # fn ------- a function pointer
   # argCount - how many args to expect, basic runtime validation
   def Register(self, cmd, fn, argCount):
      self._commands[cmd] = Command(cmd, fn, argCount)
   
   # Get a ScriptCommand based on it's name or None if we can't find it
   # cmd - the command to retrieve
   def GetCmd(self, cmd):
      if cmd in self._commands:
         return self._commands[cmd]
      else:
         print("Could not find command %s" % (str(cmd)))
         return None

class ScriptEngine:
   def __init__(self):
      pass
   
# declare globals
cr = CommandRegistry()
se = ScriptEngine()

###############################################################################
# Testing code

def do_test0():
   print("test0")

def do_test1(a):
   print("test1 arg: %s" % (str(a)))

def do_test2(a, b):
   print("test2 arg: %s and %s" % (str(a), str(b)))

def testScript():
   c = CommandRegistry()
   c.Register("test0", do_test0, 0)
   c.Register("test1", do_test1, 1)
   c.Register("test2", do_test2, 2)
   
   args = []
   c.GetCmd("test0").Call(args)
   args.append(1)
   c.GetCmd("test1").Call(args)
   args.append(3)
   c.GetCmd("test2").Call(args)

AddTest('testScript', testScript)

def testScriptIter():
   scr = ['aoeu1', 'aoeu2', 'aoeu3', '[label]  [testing]    ', 'aoeu4', 'aoeu5', 'aoeu6', 'aoeu7']
   si = ScriptIter(scr)
   
   for a in si:
      print(a)
   
   print("---------------------------")
   
   si.FindLabel('testing')
   print(si.Next())
   print(si.Next())
   print(si.Next())
   print("---------------------------")
   si.FindLabel('aoeuaoeu')
   
   for a in si:
      print(a)

AddTest('testScriptIter', testScriptIter)

def testParser():
   tests = ['[jump][fin]', '[check][script-state][eq][done][script-code-done]', 'test', '[end]']
   for a in tests:
      ret = Parser.Segment(a)
      print(ret)
   
   p = scriptPath('test')
   print('loading: %s' % p)
   si = Parser.LoadFile(p)
   print(si)

AddTest('testParser', testParser)

### .\source\script_commands.py

# warp: implement for player warping
# mapFile --------- file path (relative, from base directory)
# tileId ---------- the id of the tile to warp to (alpha numeric)
# transitionStyle - how the warp is displayed, will be one of WARP_X from constants.py
def do_warp(mapFile, tileId, transitionStyle = WARP_INSTANT):
   pass

cr.Register("warp", do_warp, 3)


# dialogue: transitions to a dialogue scene using the indicated file as script
# scriptFile - file path (relative, from base directory)
def do_dialogue(scriptFile):
   pass
   
cr.Register("dialogue", do_dialogue, 1)

### .\source\view\DialogScene.py

class DialogScene:
   def __init__(self, dlg):
      if not isinstance(dlg, Dialog):
         raise Exception("dlg must an object of type Dialog")
      ImageLib.Add('d-frame', uiImgPath('dframe'))
      
      self.next = self
      self._dlg = dlg
      self._choice = 0
      
   def ProcessInput(self, events):
      d = self._dlg
      
      if 0 != len(events):
         for e in events:
            if e.down:
               if e.key == 'up' and d.State() == D_QUESTION:
                  self._choice -= 1
                  self._choice %= len(self._dlg.Choices())
               
               if e.key == 'down' and d.State() == D_QUESTION:
                  self._choice += 1
                  self._choice %= len(self._dlg.Choices())
            else:
               if e.key == 'B':
                  if self._dlg.State() == D_QUESTION:
                     self._dlg.Answer(self._choice)
                  self._dlg.Advance()

   def Update(self, game_counter):
      pass

   def Render(self, screen):
      d = self._dlg
      
      if d.State() == D_END:
         print("TODO: Advance to next scene")
         return
      
      p = d.Profile()
      pSurf = None

      if p:
         p = portraitPath(p)
         if p:
            pSurf = ImageLib.FromFile(p)
      if pSurf:
         screen.blit(pSurf, (4, 120))
      
      df = ImageLib.Get('d-frame')
      screen.blit(df, (0,screen.get_height() - df.get_height() - 4))

      txt = d.Text()
      txt = txt.split('\n')
      tSurf = []
      for t in txt:
         if t == '$nl$':
            t = ''
         tSurf.append(_font.render(t, True, BLACK))
      
      lineNo = 0
      for t in tSurf:
         screen.blit(t, (D_TEXT_OFFSET_X, D_TEXT_OFFSET_Y + lineNo * _font.get_height()))
         lineNo += 1

      if D_QUESTION == d.State():
         cy = int(D_TEXT_OFFSET_Y + (lineNo + self._choice) * _font.get_height() + (.5 * _font.get_height()))
         cx = D_TEXT_OFFSET_X + 6
         
         # draw choice indicator
         pygame.draw.circle(screen, BLUE, (cx, cy), 4)
         
         # print choice text
         for c in d.Choices():
            cSurf = _font.render(c, True, BLACK)
            screen.blit(cSurf, (D_ANSWER_OFFSET_X, D_TEXT_OFFSET_Y + lineNo * _font.get_height()))
            lineNo += 1
         

### .\source\aaaa.py statics



### .\source\aScripted.py statics



### .\source\constants.py statics



_font = None

### .\source\Dialog.py statics



### .\source\GamePlay\GamePlayScene.py statics



### .\source\GamePlay\Level.py statics





### .\source\GamePlay\LevelStore.py statics



### .\source\ImageLib.py statics


ImageLib = ImageLibraryClass()

### .\source\ImageLibrary.py statics



_imageLibrary = ImageLibrary()
def get_image(path):
	return _imageLibrary.get_image(path)

### .\source\Input\InputManager.py statics



_inputManager = InputManager()
def is_pressed(key):
	return _inputManager.is_pressed[key]

### .\source\MapScript.py statics



### .\source\scriptybit.py statics



### .\source\script_commands.py statics



### .\source\view\DialogScene.py statics




TILE_COLUMN_COUNT = 24
TILE_ROW_COUNT = 18

globalState = {}
globalState['script-state'] = 'done'


def main():
	
	counter = 0
	global _font
	
	pygame.init()
	_font = pygame.font.Font(os.path.join('media', 'fortunaschwein.ttf'), 13)	
	_font = pygame.font.Font(os.path.join('media', 'rm_typewriter_old.ttf'), 13)	
	
	width = TILE_COLUMN_COUNT * 16
	height = TILE_ROW_COUNT * 16
	
	screen = pygame.display.set_mode((width * 2, height * 2))
		
	virtual_screen = pygame.Surface((width, height))
	
	if os.path.exists('map_test.txt'):
		c = open('map_test.txt', 'rt')
		t = c.read().split('\n')
		c.close()
		map_name = trim(t[0])
		coords = trim(t[1]).split(',')
		scene = GamePlayScene(map_name, int(coords[0]) << 4, int(coords[1]) << 4)
	else:
		scene = GamePlayScene('test_level', 100, 100)
	
	#scene = TextTest(Dialog(Parser.LoadFile(scriptPath('test'))))
	
	while scene != None:
			
		begin = time.time()
		
		scene.ProcessInput(_inputManager.get_events())
		
		scene.Update(counter)
		
		virtual_screen.fill((0,0,0))
		
		scene.Render(virtual_screen)
		
		pygame.transform.scale(virtual_screen, (width * 2, height * 2), screen)
		
		scene = scene.next
		
		if _inputManager.escape_attempted:
			scene = None
		
		counter += 1
		
		pygame.display.flip()
		
		end = time.time()
		
		duration = end - begin
		difference = 1 / 30.0 - duration
		if difference > 0:
			time.sleep(difference)

if testCode:
   RunTests()
else:
   main()