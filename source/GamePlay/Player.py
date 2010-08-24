class Player:
	def __init__(self):
		self.x = 100
		self.y = 100
		self.layer = 'A'
		self.r = 8
		self.direction = 'right'
		self.walking = False
	
	def DrawingCoords(self):
		return (self.x - self.r, self.y - self.r - 13)
	
	def CurrentImage(self, render_counter):
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
		return get_image('sprites/maincharacter/down' + counter)
		