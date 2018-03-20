class MainMenuScene:
	def clickStartGame(self):
		scene = GameSelectScene(self)
		self.next = scene

	def clickSetup(self):
		self.next = JoystickConfigScene()
	
	def clickCredits(self):
		self.next = CreditsScene()

	def __init__(self):
		self._fc = 0
		self.next = self
		self._selection = 0
		self._frame = 0
		
		self._gears = []
		i = 1
		while i <= 4:
			self._gears.append(get_image('ui/gear' + str(i) + '.png'))
			i += 1
	
	def processInput(self, events):
		for e in events:
			if e.down:
				if e.Down():
					play_sound("menu2")
					self._selection = (self._selection + 1) % 3
				if e.Up():
					play_sound("menu2")
					self._selection = (self._selection - 1) % 3
				if e.A() or e.B() or e.Start():
					if self._selection == 0:
						self.clickStartGame()
					elif self._selection == 1:
						self.clickSetup()
					elif self._selection == 2:
						self.clickCredits()
				if e.X():
					scene = GameOverScene()
					self.next = scene
					scene.next = scene
				if e.Y():
					scene = CreditsScene()
					self.next = scene
					scene.next = scene

	def update(self, conter):
		play_music('title')
	
	def render(self, screen):
		self._fc += 1
		
		frame = self._frame
		if (self._fc % 2 == 0):
			self._frame += 1
			self._frame %= len(self._gears)
		
		title = render_text_size(45, GAME_NAME, WHITE, MENU_FONT)
		start = render_text_size(20, "Start", WHITE, MENU_FONT)
		setup = render_text_size(20, "Setup", WHITE, MENU_FONT) 
		credits = render_text_size(20, "Credits", WHITE, MENU_FONT) 
		art = get_image('misc/mainmenu-bg.png')
		
		titleOffset = (int((screen.get_width() - title.get_width()) / 2), 20)
		startOffset = (100, 100)
		setupOffset = (100, 150)
		creditsOffset = (100, 200)
		artOffset = (190, 20)
		
		screen.blit(art, artOffset)
		screen.blit(title, titleOffset)
		screen.blit(start, startOffset)
		screen.blit(setup, setupOffset)
		screen.blit(credits, creditsOffset)
		
		gx = startOffset[0] - 50
		gy = startOffset[1] - 10 + (self._selection * 50)
		g = self._gears[frame]
		screen.blit(g, (gx, gy))
