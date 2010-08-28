class Goody:
	def __init__(self, name, id=None):
		self.name = name
		self.id = id
		self.x = 100
		self.y = 100
		self.dx = 0
		self.dy = 0
		self.is_enemy = False
		self.layer = 'A'
		self.r = 8
		self.direction = 'right'
		self.flying = False
		self.expired = False
		self.walking = False
		self.state = 'standing'
		self.state_counter = 0
		self.explode_on_impact = False
	
	def DrawingCoords(self):
		return (0,0)
	
	def Update(self):
		pass
		
	def CurrentImage(self, render_counter):
		counter = render_counter / 30
		if counter < 4:
			counter = '1'
		elif counter < 8:
			counter = '2'
		else:
			counter = '0'
		if self.name == 'money':
			return get_image('misc/money' + counter)
		else:
			return get_image('misc/life_refill' + counter)
		