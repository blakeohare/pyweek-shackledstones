class GameOverScene:
	def _LastSave(self):
		getActiveGame().parse()
		m = getActiveGame().getString('save_map')
		if m == '':
			m = 'transport_1'
			x = 64
			y = 64
		x = getActiveGame().getInt('save_x', None)
		y = getActiveGame().getInt('save_y', None)
		if x == None: x = 0
		if y == None: y = 0
		self.next = GamePlayScene(m, x, y + 16)
		self.next.level.update_tile_standing_on(self.next.player.layer, self.next.player.x, self.next.player.y)
		self.next.prevTile = self.next.level.playerStandingOn
		self.next.firstTimeOnTile = False
		self.next.disable_save = True
	
	def _MainMenu(self):
		mm = MainMenuScene()
		self.next = mm
		mm.next = mm
	
	def _Quit(self):
		self.next = None

	def __init__(self):
		self.next = self
		
		self._selection = 0
		self._fc = 0
		self._frame = 0
	
		self._gears = []
		i = 1
		while i <= 4:
			self._gears.append(get_image('ui/gear' + str(i) + '.png'))
			i += 1

	
	def processInput(self, events):
		for e in events:
			if e.down:
				if e.Up():
					self._selection -= 1
					self._selection %= 3
				if e.Down():
					self._selection += 1
					self._selection %= 3
				if e.A() or e.B() or e.Start():
					if self._selection == 0:
						self._LastSave()
					if self._selection == 1:
						self._MainMenu()
					if self._selection == 2:
						self._Quit()
	
	def update(self, conter):
		pass
	
	def render(self, screen, renderOffset):
		self._fc += 1
		
		frame = self._frame
		if (self._fc % 2 == 0):
			self._frame += 1
			self._frame %= len(self._gears)

		Graphics2D.Draw.fill(0, 0, 0)
		sw = SCREEN_WIDTH
		
		death = render_text_size(23, "You Have Perished", WHITE)
		death_sub = render_text_size(15,  "The empire has lost its best hope", WHITE)
		death_sub2 = render_text_size(15, "for salvation. Are there any that", WHITE)
		death_sub3 = render_text_size(15, "may hope to fill your place?", WHITE)

		death_x = int((sw - death.width) / 2)
		death_y = 23
		death.draw(death_x, death_y)
		death_x = int((sw - death_sub.width) / 2)
		death_y = death_y + death.height + 4
		death_sub.draw(death_x, death_y)
		death_x = int((sw - death_sub2.width) / 2)
		death_y = death_y + death_sub.height
		death_sub2.draw(death_x, death_y)
		death_x = int((sw - death_sub3.width) / 2)
		death_y = death_y + death_sub2.height
		death_sub3.draw(death_x, death_y)
		
		cont = render_text_size(23, "Go to Last Save", WHITE)
		main = render_text_size(23, "Main Menu", WHITE)
		quit = render_text_size(23, "Quit", RED)
		
		cx = 135
		cy = death_y + death_sub3.height + 20
		mx = cx
		my = cy + cont.height + 15
		qx = cx
		qy = my + main.height + 13
		
		cont.draw(cx, cy)
		main.draw(mx, my)
		quit.draw(qx, qy)
		
		gx = cx - 50
		gy = cy + (43 * self._selection) - 7
		g = self._gears[frame]
		g.draw(gx, gy)
