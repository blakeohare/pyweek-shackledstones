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
	
	def render(self, screen):
		self._baseScene.render(screen)
		i = self._i
		isurf = self._itemSurf
		sw = screen.get_width()
		
		
		titleSurf = pygame.Surface((200, 25))
		titleSurf.set_alpha(120)
		
		moneySurf = pygame.Surface((140, 25))
		moneySurf.set_alpha(120)
		
		itemSurf = pygame.Surface((140, 60))
		itemSurf.set_alpha(120)
		
		ss = 1 # strokeSize
		vBorder = 7
		
		money_off_x = int((screen.get_width() - moneySurf.get_width()) / 2)
		money_off_y = 150
		draw_rect_stroke(money_off_x - ss, money_off_y - ss, 140 + (2 *ss), 25 + (2 *ss), 255, 255, 255, ss)
		
		item_off_x = int((screen.get_width() - itemSurf.get_width()) / 2)
		item_off_y = money_off_y + titleSurf.get_height() + vBorder
		draw_rect_stroke(item_off_x - ss, item_off_y - ss, 140 + (2 *ss), 60 + (2 *ss), 255, 255, 255, ss)
		
		title_off_x = int((screen.get_width() - titleSurf.get_width()) / 2)
		title_off_y = item_off_y + itemSurf.get_height() + vBorder
		draw_rect_stroke(title_off_x - ss, title_off_y - ss, 200 + (2 *ss), 25 + (2 *ss), 255, 255, 255, ss)
		
		screen.blit(titleSurf, (title_off_x, title_off_y))
		screen.blit(itemSurf, (item_off_x, item_off_y))
		screen.blit(moneySurf, (money_off_x, money_off_y))

		if i.hasAny():
			# TODO: this is ugly and terrible, fix it
			a = render_text_size(17, 'A', WHITE)
			aw = a.get_width()
			ah = a.get_height()
			b = render_text_size(17, 'B', WHITE)
			bw = b.get_width()
			bh = b.get_height()
			x = render_text_size(17, 'X', WHITE)
			xw = x.get_width()
			xh = x.get_height()
			y = render_text_size(17, 'Y', WHITE)
			yw = y.get_width()
			yh = y.get_height()
			eq = pygame.Surface((aw + bw + 40 + 18, 46))
			eq.set_alpha(120)
			eq.fill(BLACK)
			ex = int((sw - eq.get_width()) / 2)
			ey = 50
			screen.blit(eq, (ex, ey))
			draw_rect_stroke(ex - ss, ey - ss, eq.get_width() + (2 * ss), eq.get_height() + (2 * ss), 255, 255, 255, ss)
			'''
			a	 x
			b	 y
			'''
			surf = i.getItemIcon('a')
			screen.blit(a, (ex + 3, ey + 0))
			if surf:
				screen.blit(surf, (ex + aw + 6, ey))
			
			surf = i.getItemIcon('b')
			screen.blit(b, (ex + 3, ey + 23))
			if surf:
				screen.blit(surf, (ex + bw + 6, ey + 23))
			
			surf = i.getItemIcon('x')
			screen.blit(x, (ex + aw + 26, ey + 0))
			if surf:
				screen.blit(surf, (ex + xw + aw + 26 + 3, ey))
			
			surf = i.getItemIcon('y')
			screen.blit(y, (ex + bw + 26, ey + 23)) 
			if surf:
				screen.blit(surf, (ex + bw + yw + 26 + 3, ey + 23))

		# draw player money:
		coinSurf = get_image('misc/money0.png')
		cx = money_off_x + 4
		cy = money_off_y + int((moneySurf.get_height() - coinSurf.get_height()) / 2)
		screen.blit(coinSurf, (cx, cy))
		
		amt = render_number(get_money(), WHITE)
		mx = money_off_x + moneySurf.get_width() - 5 - amt.get_width()
		my = money_off_y + int((moneySurf.get_height() - amt.get_height()) / 2)
		screen.blit(amt, (mx, my))

		# draw all items the player has:
		col = 0
		while col < 5:
			row = 0
			while row < 2:
				item = self._layout[row][col]
				if isurf[item] and i.check(item):
					screen.blit(isurf[item], (item_off_x + 4 + (28 * col), item_off_y + 4 + (28 * row)))
				
				row += 1
			col += 1
		
		# deal with selected item label:
		item = self._layout[self._selection[1]][self._selection[0]]
		if i.check(item):
			text = render_text_size(17, i.description(item), WHITE)
			
			if text:
				txt_off_x = title_off_x + int((titleSurf.get_width() - text.get_width()) / 2)
				txt_off_y = title_off_y + 2
				
				screen.blit(text, (txt_off_x, txt_off_y))
		
		# draw cannon overlay
		try:
			idx = self._layout[1].index(i.whichCannonEquipped())
			cannonSurf = self._itemSurf['cannon-icon']
			cannon_off_x = item_off_x + (28 * idx) + 8
			cannon_off_y = item_off_y + 28 + 10
			screen.blit(cannonSurf, (cannon_off_x, cannon_off_y))
		except:
			pass
		
		if i.hasAny():
			# draw selection box
			sel_off_x = item_off_x + 2 + (28 * self._selection[0])
			sel_off_y = item_off_y + 2 + (28 * self._selection[1])
			draw_rect_stroke(sel_off_x, sel_off_y, 24, 24, 255, 0, 0, 1)
