class NPC:
	def __init__(self, name, id=None):
		self.name = name
		self.id = id
		self.x = 100
		self.y = 100
		self.layer = 'A'
		self.r = 8
		self.direction = 'right'
		self.walking = False
		self.state = 'standing'
		self.state_counter = 0
	
	def DrawingCoords(self):
	
		coords = (self.x - self.r, self.y - self.r - 13)
		return coords
	
	def Update(self):
		self.state_counter -= 1
		if self.state_counter <= 0 and self.state != 'walking' and self.state != 'standing':
			self.state = 'standing'
	
	def CurrentImage(self, render_counter):
		if self.state == 'walking' or self.state == 'standing':
			if self.state == 'walking':
				counter = ('0','1','0','2')[(render_counter // 3) & 3]
			else:
				counter = 0
			counter = str(counter)
			if self.direction == 'right':
				return get_image('sprites/'+self.name+'/right' + counter)
			if self.direction == 'left':
				return get_image('sprites/'+self.name+'/left' + counter)
			if self.direction == 'up':
				return get_image('sprites/'+self.name+'/up' + counter)
			if self.direction == 'down':
				return get_image('sprites/'+self.name+'/down' + counter)
	
		return get_image('sprites/'+self.name+'/down' + counter)
		