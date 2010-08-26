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
		self.state_counter = 0
		self.dx = 0
		self.dy = 0
		self.game_scene = ActiveGame().GetActiveGameScene()
		if self.name == 'blob':
			self.state = 'thinking'
			self.state_counter = 30
			self.r = 8
	
	def DrawingCoords(self):
		offsets = (0,0)
		coords = (self.x - self.r - offsets[0], self.y - self.r - offsets[1])
		return coords
	
	def Update(self):
		self.state_counter -= 1
		player_x = self.game_scene.player.x
		player_y = self.game_scene.player.y
		
		if self.name == 'blob':
			if self.state_counter == 0:
				if self.state_counter == 'thinking':
					self.state = 'approach'
				elif self.state_counter == 'approach':
					self.state = 'thinking'
				self.state_counter = 30
			if self.state == 'approach':
				if player_x > self.x:
					self.dx = 2
				elif player_x < self.x:
					self.dx = -2
				if player_y > self.y:
					self.dy = 2
				elif player_y < self.y:
					self.dy = -2
			
	
	def CurrentImage(self, render_counter):
		if self.name == 'blob':
			counter = str(render_counter & 1)
			return get_image('sprites/blob/anim' + counter)
		return get_image('sprites/blob/anim0')
		