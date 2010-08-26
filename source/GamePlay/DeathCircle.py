
class DeathCircle:
	def __init__(self, x, y, radius, duration, type):
		self.x = x
		self.y = y
		self.r = radius
		self.time_left = duration
		self.type = type
		self.expired = False
	
	def update(self):
		self.time_left -= 1
		if self.time_left < 0:
			self.expired = True
	
	def touches_sprite(self, sprite):
		if sprite.flash_counter < 0:
			dx = sprite.x - self.x
			dy = sprite.y - self.y
			max_distance = self.r + sprite.r
			if dx ** 2 + dy ** 2 < max_distance ** 2:
				return True
		return False
