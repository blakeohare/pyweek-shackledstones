def get_normalized_vector(xa, ya, xb, yb):
	dx = xb - xa
	dy = yb - ya
	if dx == 0 and dy == 0:
		dx = Random.randomFloat() * 4 - 2
		dy = random_choice([-2, -1, 1, 2])
		# if the damage is applied from the identical pixel source, 
		# pretend it's some random direction
	d = (dx * dx + dy * dy) ** .5
	dx = dx / d
	dy = dy / d
	return (dx, dy)

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
