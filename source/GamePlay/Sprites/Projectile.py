def clear_grapple():
	global _grapple_singleton
	_grapple_singleton = None

def set_grapple(grapple):
	global _grapple_singleton
	_grapple_singleton = grapple

def grapple_exists():
	global _grapple_singleton
	return _grapple_singleton != None

class Projectile:
	def __init__(self, type, friendly, layer, x, y, direction, game_scene):
		self.name = ''
		self.game_scene = game_scene
		self.id = ''
		self.is_enemy = not friendly
		self.x = x
		self.y = y
		self.dx = 0
		self.dy = 0
		self.is_goody = False
		self.grapple_start_x = self.x
		self.grapple_start_y = self.y
		self.grapple_duration = 15
		self.grapple_counter = 0
		self.grappled = False
		
		self.layer = layer
		self.r = 4
		if type == 'grapple':
			self.r = 8
		self.direction = direction
		self.walking = False
		self.expired = False
		self.velocity = 6
		self.state = 'standing'
		self.state_counter = 0
		self.explode_on_impact = True
		self.flying = True
		self.end_x = None
		self.end_y = None
		self.kind = type
	
	def drawingCoords(self):
	
		coords = (self.x - self.r, self.y - self.r)
		return coords
	
	def update(self):
		tiles = _bulletSwitches.get(self.game_scene.name, [])
		for tile in tiles:
			tile = self.game_scene.level.ids[tile]
			x = abs((tile.x << 4) + 8 - self.x)
			y = abs((tile.y << 4) + 8 - self.y)
			layer = tile.layer
			if self.layer == layer and x < 8 and y < 8:
				self.expired = True
				go_script_go(tile.script)
				break
		
		for sprite in self.game_scene.sprites:
			if sprite.is_enemy:
				dx = sprite.x - self.x
				dy = sprite.y - self.y
				if dx ** 2 + dy ** 2 < (self.r + sprite.r) ** 2:
					
					self.expired = True
					sprite.life -= 1
					if self.kind == 'fire':
						sprite.life -= 1
					elif self.kind == 'ice':
						sprite.life += 1
						sprite.expired = False
						sprite.frozen = True
		
		self.state_counter -= 1
		if self.state_counter <= 0 and self.state != 'walking' and self.state != 'standing':
			self.state = 'standing'
		
		if self.direction == 'left':
			self.dx = -self.velocity
			if self.end_x != None and self.x < self.end_x:
				self.expired = True
		elif self.direction == 'right':
			self.dx = self.velocity
			if self.end_x != None and self.x > self.end_x:
				self.expired = True
		elif self.direction == 'up':
			self.dy = -self.velocity
			if self.end_y != None and self.y < self.end_y:
				self.expired = True
		else:
			self.dy = self.velocity
			if self.end_y != None and self.y > self.end_y:
				self.expired = True
		
		
		
	
	def currentImage(self, render_counter):
		if self.kind == 'grapple':
			return get_image('sprites/magnet/' + self.direction)
		elif self.kind == 'ice':
			return get_image('sprites/bullets/ice')
		elif self.kind == 'fire':
			return get_image('sprites/bullets/fire')
		return get_image('sprites/bullets/basic')
