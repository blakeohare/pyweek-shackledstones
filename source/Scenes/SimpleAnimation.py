class SimpleAnimationScene:
	def __init__(self, name):
		self.next = self
		self.name = name
		self.render_counter = 0
		if name == 'flyaway':
			play_sound("flying")
			self.expiration = 60
		else:
			self.expiration = 0

	def ProcessInput(self, events):
		pass

	def Update(self, conter):
		self.expiration -= 1
		if self.expiration <= 0:
			if self.name == 'flyaway':
				self.next = GamePlayScene('escape_pod', 30, 30)

	def Render(self, screen):
		if self.name == 'flyaway':
			x = (4 * self.render_counter) % 384
			y = self.render_counter % 288
			sky = get_image('misc/sky')
			transport = get_image('misc/transport' + str(self.render_counter & 1))
			pod = get_image('misc/escapepod' + str(self.render_counter & 1))
			screen.blit(sky, (x, y))
			screen.blit(sky, (x - 384, y))
			screen.blit(sky, (x, y - 288))
			screen.blit(sky, (x - 384, y - 288))
			
			screen.blit(transport, (200, 50))
			screen.blit(pod, (220 + 3 *  - self.render_counter, 70 + self.render_counter))
			
		self.render_counter += 1
