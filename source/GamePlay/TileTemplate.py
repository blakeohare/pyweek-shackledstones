class TileTemplate:
	def __init__(self, parts):
		self.id = parts[0]
		self.physics = parts[2]
		self.imagefiles = parts[3].split('|')
		
		images = []
		for img in self.imagefiles:
			images.append(get_image('tiles/' + img.strip()))
		self.images = images
		
		if len(parts) == 5:
			self.anim_delay = int(parts[4])
		else:
			self.anim_delay = 4
		self.num_images = len(self.images)
		
	def Render(self, screen, x, y, render_counter):
		if self.num_images == 1:
			screen.blit(self.images[0], (x, y))
		else:
			screen.blit(
				self.images[(render_counter // self.anim_delay) % self.num_images],
				(x, y))
