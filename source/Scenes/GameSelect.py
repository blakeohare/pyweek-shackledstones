class GameSelectScene:
	def __init__(self, prevScene):
		self._prevScene = prevScene
		self.next = self
		
		self._eraseMode = False
		self._erase = False
		self._cancel = False
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
				if self._erase or self._cancel:
					if e.Up():
						play_sound("menu2")
						self._erase = False
						self._cancel = False
						self._selection = 2
						return
					if e.Down():
						play_sound("menu2")
						self._erase = False
						self._cancel = False
						self._selection = 0
						return
					if e.Right() or e.Left():
						self._erase = not self._erase
						self._cancel = not self._cancel
						return
				elif e.Up():
					play_sound("menu2")
					self._selection -= 1
					self._selection %= 4
					
				elif e.Down():
					play_sound("menu2")
					self._selection += 1
					self._selection %= 4
				
				if (e.Up() or e.Down()) and self._selection == 3:
					self._erase = True

				if e.A() or e.B() or e.Start():
					if self._cancel:
						self.next = self._prevScene
						self._prevScene.next = self._prevScene
						return
					
					if self._erase:
						self._eraseMode = True
						return
					
					if self._eraseMode:
						getGameContext().deletePlayer(self._selection + 1)
						self._eraseMode = False
						return
					
					newGame = not getGameContext().getPlayerName(self._selection + 1)
					getGameContext().setActiveGame(self._selection + 1)
					
					if newGame:
						self.next = NameEntryScene()
					else:
						#print('TODO: set up to resume gameplay')
						m = getActiveGame().getVar('save_map')
						if m == None:
							m = 'transport_1'
							x = 64
							y = 56
						x = getActiveGame().getVar('save_x')
						y = getActiveGame().getVar('save_y')
						if x == None: x = 64
						if y == None: y = 56
						self.next = GamePlayScene(m, x, y + 16)
						self.next.level.update_tile_standing_on(self.next.player.layer, self.next.player.x, self.next.player.y)
						self.next.prevTile = self.next.level.playerStandingOn
						self.next.firstTimeOnTile = False
						self.next.disable_save = True
						
	def update(self, conter):
		play_music("menuwaitingroom")
	
	def render(self, screen, renderOffset):
		# what color is used for everything else
		txtColor = WHITE
		# what color is in the game select thing
		descColor = BLACK
		# game selection block
		gameSelColor = WHITE
		
		self._fc += 1
		frame = self._frame
		if (self._fc % 2 == 0):
			self._frame += 1
			self._frame %= len(self._gears)
		g = self._gears[frame]

		gc = getGameContext()
		
		sw = screen.get_width()
		gameSel_y = 20
		
		gameTxt = "Game Select"
		if self._eraseMode:
			gameTxt = 'Erase Game'
		gameSel = render_text_size(23, gameTxt, txtColor)
		screen.blit(gameSel, (int((sw - gameSel.get_width()) / 2), gameSel_y))
	
		post_title_y = gameSel_y + gameSel.get_height() + 10
	
		# game sel width
		sel_w = int(.7 * sw)
		# game sel height
		sel_h = 45
		# separation between game sel blocks
		gameSel_sep = 15
		selSurf = pygame.Surface((sel_w, sel_h))
		selSurf.set_alpha(ALPHA)
		selSurf.fill(gameSelColor)
		
		i = 0
		while i < 3:
			sx = int(sw * .2)
			sy = i * (gameSel_sep + sel_h) + post_title_y

			if i == self._selection:
				screen.blit(g, (sx - 50, sy))
	
			screen.blit(selSurf, (sx, sy))
			
			slot_num = i + 1
			name = gc.getPlayerName(slot_num)
			if name:
				nameSurf = render_text_size(17, name, descColor)
			else:
				nameSurf = render_text_size(17, 'New Game', descColor)
			
			nx = sx + 10
			ny = int((selSurf.get_height() - nameSurf.get_height()) / 2) + sy
			screen.blit(nameSurf, (nx, ny))

			if name:
				stones = gc.getStones(slot_num)
				j = 0
				stones.reverse()
				for st in stones:
					stSurf = get_image('ui/stones/' + st + '.png')
					stx = sx + selSurf.get_width() - 10 - ((1 + j) * 20)
					sty = sy + int((selSurf.get_height() - stSurf.get_height()) / 2)
					
					screen.blit(stSurf, (stx, sty))
					j += 1

			i += 1
		
		erase = render_text_size(20, 'Erase', txtColor)
		cancel = render_text_size(20, 'Cancel', txtColor)
		
		screen.blit(erase, (75, 240))
		cx = 230
		screen.blit(cancel, (cx, 240))
		
		gy = 230
		if self._erase:
			screen.blit(g, (sx - 50, gy))
		if self._cancel:
			screen.blit(g, (cx + 10 + cancel.get_width(), gy))
			
		# stone badges
