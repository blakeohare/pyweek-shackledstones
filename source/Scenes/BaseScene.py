class BaseScene:
	def __init__(self):
		self.next = self
	
	def processInput(self, events):
		pass
	
	def update(self, conter):
		pass
	
	def render(self, screen):
		pass
