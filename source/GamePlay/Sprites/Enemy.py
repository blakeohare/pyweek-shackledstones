class Enemy:
	def __init__(self, name, id=None):
		self.name = name
		self.id = id
		self.is_enemy = True
		self.explode_on_impact = False
		self.x = 100
		self.y = 100
		self.layer = 'A'
		self.r = 8
		self.direction = 'right'
		self.walking = False
		self.expired = False
		self.state = 'standing'
		self.flying = False
		self.frozen = False
		self.is_goody = False
		self.state_counter = 0
		self.dx = 0
		self.dy = 0
		self.life = 0
		self.flash_counter = -1
		self.flying_damage = -42
		self.damage_dx = 0.0
		self.damage_dy = 0.0
		self.game_scene = ActiveGame().GetActiveGameScene()
		if self.name == 'blob':
			self.life = 2
			self.state = 'thinking'
			self.state_counter = int(30 * random.random())
			self.r = 8
		elif self.name == 'eyeball':
			self.life = 2
			self.state = 'walking'
			self.state_counter = int(30 * random.random())
			self.r = 8
		elif self.name == 'mechanicalman':
			self.life = 4
			self.state = 'walking'
			self.state_counter = int(30 * random.random())
			self.r = 8
		elif self.name == 'beetle':
			self.life = 1
			self.state = 'walking'
			self.state_counter = int(30 * random.random())
			self.r = 8
		elif self.name == 'death':
			self.r = 16
			self.life = 15
			self.state = 'walking'
			
			
	
	def DrawingCoords(self):
		offsets = (0,0)
		if self.name == 'mechanicalman':
			offsets = (0, -6)
		elif self.name == 'eyeball':
			offsets = (0, (self.state_counter // 10) & 1)
		elif self.name == 'death':
			offsets = (0, 8)
		coords = (self.x - self.r - offsets[0], self.y - self.r - offsets[1])
		
		return coords
	
	def get_goody(self):
		i = int(random.random() * 10)
		g = None
		if self.name== 'death': return None
		if i < 3:
			g = Goody('life')
		else:
			g = Goody('money')
			
		if g != None:
			g.layer = self.layer
			g.x = self.x
			g.y = self.y
		return g
	
	def Update(self):
		self.dx = 0
		self.dy = 0
		self.state_counter -= 1
		self.flash_counter -= 1
		self.flying_damage -= 1
		player_x = self.game_scene.player.x
		player_y = self.game_scene.player.y
		
		delta_x = self.x - player_x
		delta_y = self.y - player_y
		
		dc = None
		for death_circle in self.game_scene.death_circles:
			if death_circle.touches_sprite(self):
				dc = death_circle
				self.flash_counter = 10
				self.life -= 1
				self.flying_damage = 9
				nv = get_normalized_vector(death_circle.x, death_circle.y, self.x, self.y)
				self.damage_dx = nv[0] * 4
				self.damage_dy = nv[1] * 4
		
		if self.life <= 0:
			self.expired = True
			goody = self.get_goody()
			if goody != None:
				self.game_scene.sprites.append(goody)
			return
		
		if self.flying_damage > 0:
			self.dx = int(self.damage_dx)
			self.dy = int(self.damage_dy)
		elif not self.frozen:
			if self.name == 'death':
				if player_x < self.x:
					self.dx = -1
				elif player_x > self.x:
					self.dx = 1
				if player_y < self.y:
					self.dy = -1
				elif player_y > self.y:
					self.dy = 1
			elif self.name == 'blob':
				if self.state_counter <= 0:
					if self.state == 'thinking':
						self.state = 'approach'
						self.state_counter = 15
					elif self.state == 'approach':
						self.state = 'thinking'
						self.state_counter = 30
				if self.state == 'approach':
					if player_x > self.x:
						self.dx = 1
					elif player_x < self.x:
						self.dx = -1
					if player_y > self.y:
						self.dy = 1
					elif player_y < self.y:
						self.dy = -1
			elif self.name == 'eyeball' or self.name == 'beetle':
				if self.state_counter <= 0:
					self.state_counter = 50
					if self.name == 'beetle':
						self.state_counter = 50
					self.direction = random.choice('right left down up'.split(' '))
					
				if self.direction == 'left':
					self.dx = -1
				elif self.direction == 'right':
					self.dx = 1
				elif self.direction == 'up':
					self.dy = -1
				else:
					self.dy = 1
			
			elif self.name == 'mechanicalman':
				if self.state_counter <= 0:
					if self.state == 'walking':
						self.state = 'standing'
					elif self.state == 'standing':
						self.state = 'walking'
					self.state_counter = 15
				if self.state == 'walking':
					if abs(delta_x) > abs(delta_y):
						if delta_x > 0:
							self.direction = 'left'
							self.dx = -1
						else:
							self.direction = 'right'
							self.dx = 1
					else:
						if delta_y > 0:
							self.direction = 'up'
							self.dy = -1
						else:
							self.direction = 'down'
							self.dy = 1
			
			
	
	def CurrentImage(self, render_counter):
		if self.frozen: render_counter = 0
		if self.flash_counter > 0 and self.flash_counter & 2 == 0:
			return None
			
		if self.name == 'blob':
			counter = str((render_counter // 4) & 1)
			return get_image('sprites/blob/anim' + counter)
		elif self.name == 'death':
			counter = ('0','1','0','2')[render_counter & 3]
			return get_image('sprites/death/' + counter)
		elif self.name == 'eyeball':
			return get_image('sprites/eyeball/' + self.direction)
		elif self.name == 'beetle':
			counter = str(1 + ((render_counter // 4) & 1))
			f = 'horizontal'
			if self.direction == 'up' or self.direction == 'down':
				f = 'vertical'
			return get_image('sprites/beetle/' + f + counter)
		elif self.name == 'mechanicalman':
			if self.state == 'standing':
				counter = '0'
			else:
				counter = ('0','1','0','2')[render_counter & 3]
			return get_image('sprites/mechanicalman/' + self.direction + str(counter))
		return get_image('sprites/blob/anim0')
		