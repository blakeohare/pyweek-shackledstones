class InventoryScene:
	def __init__(self, overlay):
		self.next = self
		
		i = Inventory()
		self._layout = ([i.sabre(), i.hammer(), i.drill(), i.hook(), i.compass()],
						[i.cannon(), i.cannonFire(), i.cannonIce(), i.cannonMulti(), i.shovel()])
		
		self._i = i
		self._baseScene = overlay
		self._itemSurf = {}
		self._selection = [0, 0]
		
		isurf = self._itemSurf
		
		isurf['cannon-icon'] = get_image('ui/cannon-icon.png')
		isurf[i.cannon()] = get_image('ui/ammo-sshot.png')
		isurf[i.cannonFire()] = get_image('ui/ammo-fire.png')
		isurf[i.cannonIce()] = get_image('ui/ammo-ice.png')
		isurf[i.cannonMulti()] = get_image('ui/ammo-multi.png')
		isurf[i.sabre()] = get_image('ui/sabre-have.png')
		isurf[i.hammer()] = get_image('ui/hammer-have.png')
		isurf[i.drill()] = get_image('ui/drill-have.png')
		isurf[i.hook()] = get_image('ui/hook-have.png')
		isurf[i.compass()] = get_image('ui/compass-have.png')
		isurf[i.shovel()] = get_image('ui/shovel-have.png')
	
	def processInput(self, events):
		for e in events:
			if e.down and e.key == 'start':
				self._baseScene.next = self._baseScene
				self.next = self._baseScene
				return

			if e.down:
				if e.key == 'up':
					self._selection[1] -= 1
					self._selection[1] %= 2
				elif e.key == 'down':
					self._selection[1] += 1
					self._selection[1] %= 2
				elif e.key == 'right':
					self._selection[0] += 1
					self._selection[0] %= 5
				elif e.key =='left':
					self._selection[0] -= 1
					self._selection[0] %= 5
				else:
					self._select(e.key, self._selection[0], self._selection[1])

	def _select(self, key, row, col):
		item = self._layout[col][row]

		i = self._i
		if not i.check(item):
			print('player does not have ' + item)
		else:
			i.equip(key.lower(), item)

	def update(self, conter):
		pass
	
	def render(self, screen, renderOffset):
		self._baseScene.render(screen, renderOffset)
		i = self._i
		isurf = self._itemSurf
		sw = SCREEN_WIDTH
		
		title_w = 200
		title_h = 25
		
		money_w = 140
		money_h = 25
		
		item_w = 140
		item_h = 60
		
		ss = 1 # strokeSize
		vBorder = 7
		
		money_off_x = (SCREEN_WIDTH - money_w) // 2
		money_off_y = 150
		draw_rect_stroke(money_off_x - ss, money_off_y - ss, 140 + (2 *ss), 25 + (2 *ss), 255, 255, 255, ss)
		
		item_off_x = (SCREEN_WIDTH - item_w) // 2
		item_off_y = money_off_y + title_h + vBorder
		draw_rect_stroke(item_off_x - ss, item_off_y - ss, 140 + (2 *ss), 60 + (2 *ss), 255, 255, 255, ss)
		
		title_off_x = (SCREEN_WIDTH - title_w) // 2
		title_off_y = item_off_y + item_h + vBorder
		draw_rect_stroke(title_off_x - ss, title_off_y - ss, 200 + (2 *ss), 25 + (2 *ss), 255, 255, 255, ss)
		
		Graphics2D.Draw.rectangle(title_off_x, title_off_y, title_w, title_h, 0, 0, 0, 120)
		Graphics2D.Draw.rectangle(item_off_x, item_off_y, item_w, item_h, 0, 0, 0, 120)
		Graphics2D.Draw.rectangle(money_off_x, money_off_y, money_w, money_h, 0, 0, 0, 120)

		if i.hasAny():
			a = render_text_size(17, 'A', WHITE)
			aw = a.width
			ah = a.height
			b = render_text_size(17, 'B', WHITE)
			bw = b.width
			bh = b.height
			x = render_text_size(17, 'X', WHITE)
			xw = x.width
			xh = x.height
			y = render_text_size(17, 'Y', WHITE)
			yw = y.width
			yh = y.height
			eq_w = aw + bw + 40 + 18
			eq_h = 46
			ex = (sw - eq_w) // 2
			ey = 50
			Graphics2D.Draw.rectangle(ex, ey, eq_w, eq_h, 0, 0, 0, 120)
			draw_rect_stroke(ex - ss, ey - ss, eq_w + (2 * ss), eq_h + (2 * ss), 255, 255, 255, ss)
			'''
			a	 x
			b	 y
			'''
			surf = i.getItemIcon('a')
			a.draw(ex + 3, ey + 0)
			if surf:
				surf.draw(ex + aw + 6, ey)
			
			surf = i.getItemIcon('b')
			b.draw(ex + 3, ey + 23)
			if surf:
				surf.draw(ex + bw + 6, ey + 23)
			
			surf = i.getItemIcon('x')
			x.draw(ex + aw + 26, ey + 0)
			if surf:
				surf.draw(ex + xw + aw + 26 + 3, ey)
			
			surf = i.getItemIcon('y')
			y.draw(ex + bw + 26, ey + 23)
			if surf:
				surf.draw(ex + bw + yw + 26 + 3, ey + 23)

		# draw player money:
		coinSurf = get_image('misc/money0.png')
		cx = money_off_x + 4
		cy = money_off_y + (money_h - coinSurf.height) // 2
		coinSurf.draw(cx, cy)
		
		amt = render_text_size(15, str(get_money()), WHITE, TEXT_FONT)
		mx = money_off_x + money_w - 5 - amt.width
		my = money_off_y + (money_h - amt.height) // 2
		amt.draw(mx, my)

		# draw all items the player has:
		col = 0
		while col < 5:
			row = 0
			while row < 2:
				item = self._layout[row][col]
				if isurf[item] and i.check(item):
					isurf[item].draw(item_off_x + 4 + (28 * col), item_off_y + 4 + (28 * row))
				
				row += 1
			col += 1
		
		# deal with selected item label:
		item = self._layout[self._selection[1]][self._selection[0]]
		if i.check(item):
			text = render_text_size(17, i.description(item), WHITE)
			
			if text:
				txt_off_x = title_off_x + (title_w - text.width) // 2
				txt_off_y = title_off_y + 2
				
				text.draw(txt_off_x, txt_off_y)
		
		# draw cannon overlay
		try:
			idx = self._layout[1].index(i.whichCannonEquipped())
			cannonSurf = self._itemSurf['cannon-icon']
			cannon_off_x = item_off_x + (28 * idx) + 8
			cannon_off_y = item_off_y + 28 + 10
			cannonSurf.draw(cannon_off_x, cannon_off_y)
		except:
			pass
		
		if i.hasAny():
			# draw selection box
			sel_off_x = item_off_x + 2 + (28 * self._selection[0])
			sel_off_y = item_off_y + 2 + (28 * self._selection[1])
			draw_rect_stroke(sel_off_x, sel_off_y, 24, 24, 255, 0, 0, 1)
