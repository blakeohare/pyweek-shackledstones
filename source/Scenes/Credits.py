class CreditsScene:
	def __init__(self):
		self.next = self
		self._y = 250
		screen_width = _activeScreen.get_width()
		
		lines = [
			"heading1:%s" % GAME_NAME,
			"heading:Team Nerdparadise",
			"www.nerdparadise.com",
			"",
			"",
			"heading:Programming",
			"Blake O'Hare",
			"Richard Bailey",
			"Adrian Cline",
			"",
			"",
			"",
			"heading:Pixel Art",
			"Angel McLaughlin",
			"",
			"",
			"",
			"heading:Character Art",
			"Chun Y",
			"",
			"",
			"",
			"heading:Music",
			"Adrian Cline",
			"",
			"",
			"",
			"heading:Level Design",
			"Christine Sandquist",
			"Yan Yan",
			"Brett S."
			"",
			"",
			"",
			"heading:Special Thanks...",
			"www.anke-art.de, for Fortunaschwein font",
			"Ray Meadows, for RM Typerighter font",
			"",
			"",
			"",
			"heading:Welcoming To Team",
			"heading:Nerdparadise",
			"Christine Sandquist",
			"Yan Yan",
			"Chun Y",
		]
		
		cSurf = []
		cum_y = 0
		for l in lines:
			sz = 18
			if l.startswith('heading1:'):
				l = l.split(':')[1]
				sz = 45
			if l.startswith('heading:'):
				l = l.split(':')[1]
				sz = 30
			surf = render_text_size(sz, l, WHITE)
			cSurf.append(surf)
			cum_y += surf.get_height()
		
		self.blit_instructions = []
		
		y = 0
		for s in cSurf:
			
			x = (screen_width - s.get_width()) // 2
			self.blit_instructions.append([s, x, y])
			y += s.get_height()
		self.cum_y = cum_y
	
	def processInput(self, events):
		for e in events:
			if e.down:
				if e.Start() or e.A() or e.B():
					mm = MainMenuScene()
					self.next = mm
					mm.next = mm
	
	def update(self, conter):
		pass
	
	def render(self, screen, renderOffset):
		
		sw = SCREEN_WIDTH
		offy = self._y
		
		for instr in self.blit_instructions:
			img = instr[0]
			x = instr[1]
			y = instr[2]
			screen.blit(img, (x, offy + y))
		
		self._y -= 1
		
		if (self.cum_y - abs(self._y)) <= -40:
			mm = MainMenuScene()
			self.next = mm
			mm.next = mm
