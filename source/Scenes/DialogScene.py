class DialogScene:
	def __init__(self, dlg, sourceScene):
		if not isinstance(dlg, Dialog):
			raise Exception("dlg must an object of type Dialog")
		
		self.next = self
		self._source = sourceScene
		self._dlg = dlg
		self._choice = 0
		self._lineHave = 5
		self._more = False
		self._moreDot = True
		self._truncating = True
		self._fastText = False
		self._curLine = 0
		self._curLetter = 0
		self._tick = 0
		
	def processInput(self, events):
		d = self._dlg
		
		if 0 != len(events):
			for e in events:
				if e.down:
					if e.Up() and d.State() == D_QUESTION:
						self._choice -= 1
						self._choice %= len(self._dlg.Choices())
					
					if e.Down() and d.State() == D_QUESTION:
						self._choice += 1
						self._choice %= len(self._dlg.Choices())
				else:
					if e.A() or e.B():
						if self._truncating:
							self._curLetter = 0
							self._fastText = True
							self._truncating = False
						elif self._more:
							self._curLine += self._lineHave
							self._curLetter = 0
							self._fastText = False
							self._truncating = False
							self._more = False
						else:
							if self._dlg.State() == D_QUESTION:
								self._dlg.Answer(self._choice)
							self._curLine = 0
							self._curLetter = 0
							self._fastText = False
							self._truncating = False
							self._dlg.scriptEngine.advance()

	def update(self, game_counter):
		pass

	def render(self, screen, renderOffset):
		self._tick += 1
		self._source
		d = self._dlg
		self._curLetter += 1
		
		if d.State() == D_END:
			self.next = self._source
			self._source.next = self._source

		self._source.render(screen, renderOffset)
		
		p = d.Profile()

		if p:
			isMainCharacter = p == 'mc_portrait'
			pSurf = get_image('portraits/' + p + '.png')
			x = 4 if isMainCharacter else 290
			y = 110
			pSurf.draw(x, y)
			
		df = get_image('ui/dframe.png')
		df.draw(0, SCREEN_HEIGHT - df.height - 4)
		
		lineWidth = df.width - (2 * D_TEXT_OFFSET_X)
		wt = getFontEngine().wrap_text(lineWidth, d.Text())
		
		linesRequired = len(wt)
		
		tSurf = []

		lineNo = 0
		runningTotal = 0

		while lineNo < self._lineHave:
			idx = self._curLine + lineNo
			if idx < len(wt):
				line = wt[idx]
				if not self._fastText:
					if not (runningTotal + len(line) <= self._curLetter):
						delta = self._curLetter - runningTotal
						line = line[0:delta]
						self._truncating = True
					else:
						self._truncating = False
				runningTotal += len(line)
				tSurf.append(render_text(line, BLACK))
				
				if self._truncating:
					break
			lineNo += 1

		if linesRequired > self._lineHave and (lineNo == self._lineHave):
			self._more = True
		if self._curLine + self._lineHave >= linesRequired:
			self._more = False

		fontHeight = getFontEngine().getDefaultFontHeight()
		lineNo = 0
		for t in tSurf:
			t.draw(D_TEXT_OFFSET_X, D_TEXT_OFFSET_Y + lineNo * fontHeight)
			lineNo += 1
		if D_QUESTION == d.State() and not self._truncating:
			cy = Math.floor(D_TEXT_OFFSET_Y + (lineNo + self._choice + .5) * fontHeight)
			cx = D_TEXT_OFFSET_X + 6
			
			# draw choice indicator
			Graphics2D.Draw.ellipse(cx - 4, cy - 4, 8, 8, 0, 0, 255)
			
			# print choice text
			for c in d.Choices():
				cSurf = render_text(c, BLACK)
				cSurf.draw(D_ANSWER_OFFSET_X, D_TEXT_OFFSET_Y + lineNo * fontHeight)
				lineNo += 1
			
		if self._more:
			if (self._tick % 10 == 0):
				self._moreDot = not self._moreDot
			if self._moreDot:
				Graphics2D.Draw.ellipse(370 - 2, 273 - 2, 4, 4, 255, 255, 255)
