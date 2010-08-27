_bulletSwitches = {
	'Fire_Room2' : ['switch'],
	'Fire_Key1' : ['switch_B'],
	'light_rightroom_b1' : ['switch'],
	'light_south_southroom' : ['switch_left','switch_right'],
	'light_southroom_b1' : ['switch']
}

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
		self.layer = layer
		self.r = 4
		self.direction = direction
		self.walking = False
		self.expired = False
		self.velocity = 6
		self.state = 'standing'
		self.state_counter = 0
		self.explode_on_impact = True
		self.flying = True
	
	def DrawingCoords(self):
	
		coords = (self.x - self.r, self.y - self.r)
		return coords
	
	def Update(self):
		global _bulletSwitches
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
		
		self.state_counter -= 1
		if self.state_counter <= 0 and self.state != 'walking' and self.state != 'standing':
			self.state = 'standing'
		if self.direction == 'left':
			self.dx = -self.velocity
		elif self.direction == 'right':
			self.dx = self.velocity
		elif self.direction == 'up':
			self.dy = -self.velocity
		else:
			self.dy = self.velocity
		
		
	
	def CurrentImage(self, render_counter):
		return get_image('sprites/bullets/basic')
		