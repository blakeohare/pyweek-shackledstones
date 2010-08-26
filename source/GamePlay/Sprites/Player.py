class Player:
	def __init__(self):
		self.x = 100
		self.y = 100
		self.layer = 'A'
		self.r = 8
		self.id = 'MC'
		self.dx = 0
		self.dy = 0
		self.is_enemy = False
		self.direction = 'right'
		self.walking = False
		self.state = 'walking'
		self.expired = False
		self.flying = False
		self.state_counter = 0
		self.explode_on_impact = False
	
	def DrawingCoords(self):
	
		coords = (self.x - self.r, self.y - self.r - 13)
		if self.state == 'stabbing':
			if self.direction == 'left':
				coords = (coords[0] - 16, coords[1])
			elif self.direction == 'up':
				coords = (coords[0], coords[1] - 16)
		return coords
	
	def Update(self):
		self.state_counter -= 1
		if self.state_counter <= 0:
			self.state = 'walking'
	
	def Stab(self):
		self.state_counter = 7
		self.state = 'stabbing'
		x = self.x
		y = self.y
		if self.direction == 'left':
			x -= 16
		elif self.direction == 'up':
			y -= 16
		elif self.direction == 'down':
			y += 16
		else:
			x += 16
		game_scene = ActiveGame().GetActiveGameScene()
		
		game_scene.place_death_circle('sword', x, y, 8, 5)
		play_sound('sword')
	def Shoot(self, bullet_type, game_scene):
		self.state_count = 7
		self.state = 'shooting'
		sprite = Projectile(bullet_type, True, self.layer, self.x, self.y, self.direction, game_scene)
		game_scene.sprites.append(sprite)
		play_sound('gunshot')
		
	def CurrentImage(self, render_counter):
		counter = '0'
		if self.state == 'walking':
			if self.walking:
				counter = ('0','1','0','2')[(render_counter // 3) & 3]
			else:
				counter = 0
			counter = str(counter)
			if self.direction == 'right':
				return get_image('sprites/maincharacter/right' + counter)
			if self.direction == 'left':
				return get_image('sprites/maincharacter/left' + counter)
			if self.direction == 'up':
				return get_image('sprites/maincharacter/up' + counter)
			if self.direction == 'down':
				return get_image('sprites/maincharacter/down' + counter)
		elif self.state == 'stabbing':
			counter = ('1','2','2','1','1')[(self.state_counter // 2) % 5]
			counter = str(counter)
			if self.direction == 'right':
				return get_image('sprites/maincharacter/stabright' + counter)
			if self.direction == 'left':
				return get_image('sprites/maincharacter/stableft' + counter)
			if self.direction == 'up':
				return get_image('sprites/maincharacter/stabup' + counter)
			if self.direction == 'down':
				return get_image('sprites/maincharacter/stabdown' + counter)
			
		return get_image('sprites/maincharacter/down' + counter)
		