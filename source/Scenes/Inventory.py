class InventoryScene:
	def __init__(self, overlay):
		self.next = self
		
		i = Inventory()
		self._layout = ([i.Sabre(), i.Hammer(), i.Drill(), i.Hook(), i.Compass()],
							 [i.Cannon(), i.CannonFire(), i.CannonIce(), i.CannonMulti(), i.Shovel()])
		
		self._i = i
		self._baseScene = overlay
		self._itemSurf = {}
		self._selection = [0, 0]
		
		il = ImageLib
		isurf = self._itemSurf
		
		isurf['cannon-icon'] = il.FromFile(uiImgPath('cannon-icon'))
		isurf[i.Cannon()] = il.FromFile(uiImgPath('ammo-sshot'))
		isurf[i.CannonFire()] = il.FromFile(uiImgPath('ammo-fire'))
		isurf[i.CannonIce()] = il.FromFile(uiImgPath('ammo-ice'))
		isurf[i.CannonMulti()] = il.FromFile(uiImgPath('ammo-multi'))
		isurf[i.Sabre()] = il.FromFile(uiImgPath('sabre-have'))
		isurf[i.Hammer()] = il.FromFile(uiImgPath('hammer-have'))
		isurf[i.Drill()] = il.FromFile(uiImgPath('drill-have'))
		isurf[i.Hook()] = il.FromFile(uiImgPath('hook-have'))
		isurf[i.Compass()] = il.FromFile(uiImgPath('compass-have'))
		isurf[i.Shovel()] = il.FromFile(uiImgPath('shovel-have'))
	
	def ProcessInput(self, events):
		for e in events:
			if e.down and e.key == 'start':
				self._baseScene.next = self._baseScene
				self.next = self._baseScene
				# self._i.PrintEquipped()
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
		if not i.Check(item):
			print('player does not have %s' % item)
		else:
			i.Equip(key.lower(), item)

	def Update(self, conter):
		pass
	
	def Render(self, screen):
		self._baseScene.Render(screen)
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
		pygame.draw.rect(screen, WHITE, pygame.Rect(money_off_x - ss, money_off_y - ss, 140 + (2 *ss), 25 + (2 *ss)), ss)
		
		item_off_x = int((screen.get_width() - itemSurf.get_width()) / 2)
		item_off_y = money_off_y + titleSurf.get_height() + vBorder
		pygame.draw.rect(screen, WHITE, pygame.Rect(item_off_x - ss, item_off_y - ss, 140 + (2 *ss), 60 + (2 *ss)), ss)
		
		title_off_x = int((screen.get_width() - titleSurf.get_width()) / 2)
		title_off_y = item_off_y + itemSurf.get_height() + vBorder
		pygame.draw.rect(screen, WHITE, pygame.Rect(title_off_x - ss, title_off_y - ss, 200 + (2 *ss), 25 + (2 *ss)), ss)
		
		screen.blit(titleSurf, (title_off_x, title_off_y))
		screen.blit(itemSurf, (item_off_x, item_off_y))
		screen.blit(moneySurf, (money_off_x, money_off_y))

		if i.HasAny():
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
			eq = pygame.Surface((aw+bw+40+18, 46))
			eq.set_alpha(120)
			eq.fill(BLACK)
			ex = int((sw - eq.get_width())/2)
			ey = 50
			screen.blit(eq, (ex, ey))
			pygame.draw.rect(screen, WHITE, pygame.Rect(ex - ss, ey - ss, eq.get_width() + (2 * ss), eq.get_height() + (2 * ss)), ss)
			'''
			a	 x
			b	 y
			'''
			surf = i.Surf('a')
			screen.blit(a, (ex + 3, ey + 0))
			if surf:
				screen.blit(surf, (ex + aw + 6, ey))
			
			surf = i.Surf('b')
			screen.blit(b, (ex + 3, ey + 23))
			if surf:
				screen.blit(surf, (ex + bw + 6, ey + 23))
			
			surf = i.Surf('x')
			screen.blit(x, (ex + aw + 26, ey + 0))
			if surf:
				screen.blit(surf, (ex + xw + aw + 26 + 3, ey))
			
			surf = i.Surf('y')
			screen.blit(y, (ex + bw + 26, ey + 23)) 
			if surf:
				screen.blit(surf, (ex + bw + yw + 26 + 3, ey + 23))

		# draw player money:
		coinSurf = ImageLib.FromFile(os.path.join('images', 'misc', 'money0.png'))
		cx = money_off_x + 4 # moneySurf.get_width() - coinSurf.get_width() - 5
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
				if isurf[item]:
				 if i.Check(item):
					screen.blit(isurf[item], (item_off_x + 4 + (28 * col),
														item_off_y + 4 + (28 * row)))
				
				row += 1
			col += 1
		
		# deal with selected item label:
		item = self._layout[self._selection[1]][self._selection[0]]
		if i.Check(item):
			text = render_text_size(17, i.Description(item), WHITE)
			
			if text:
				txt_off_x = title_off_x + int((titleSurf.get_width() - text.get_width()) / 2)
				txt_off_y = title_off_y + 2
				
				screen.blit(text, (txt_off_x, txt_off_y))
		
		# draw cannon overlay
		try:
			idx = self._layout[1].index(i.WhichCannonEquipped())
			cannonSurf = self._itemSurf['cannon-icon']
			cannon_off_x = item_off_x + (28 * idx) + 8
			cannon_off_y = item_off_y + 28 + 10
			screen.blit(cannonSurf, (cannon_off_x, cannon_off_y))
		except:
			pass
		
		if i.HasAny():
			# draw selection box
			sel_off_x = item_off_x + 2 + (28 * self._selection[0])
			sel_off_y = item_off_y + 2 + (28 * self._selection[1])
			pygame.draw.rect(screen, RED, pygame.Rect(sel_off_x, sel_off_y, 24, 24), 1)
	
	
	
class Inventory:
	def __init__(self):
		self._ag = ActiveGame()
	
	def Surf(self, slot):
		i = self._Equipped(slot)
		if i:
			return ImageLib.FromFile(uiImgPath('%s' % i))
		else:
			return None
	
	def HasAny(self):
		i = self
		items = (i.Sabre(), i.Hammer(), i.Drill(), i.Hook(), i.Compass(), i.Cannon(), i.CannonFire(), i.CannonIce(), i.CannonMulti(), i.Shovel())
		for it in items:
			if self.Check(it):
				return True
	
	def Check(self, item):
		return str(self._ag.GetVar(item)) == '1'
	
	def HasSabre(self):
		return self.Check('item_sabre')
	
	def HasHammer(self):
		return self.Check('item_hammer')
	
	def HasDrill(self):
		return self.Checu('item_drill')
	
	def HasHook(self):
		return self.Check('item_hook')
	
	def HasCannon(self):
		return self.Check('item_cannon')
	
	def HasCannonFire(self):
		return self.Check('item_cannon_fire')
	
	def HasCannonIce(self):
		return self.Check('item_cannon_ice')
	
	def HasCannonMulti(self):
		return self.Check('item_cannon_multi')
	
	def HasCompass(self):
		return self.Check('item_compass')
		
	def HasShovel(self):
		return self.Check('item_shovel')
	
	def HasAnyCannon(self):
		return self.HasCannon() or self.HasCannonFire() or self.HasCannonIce() or self.HasCannonMulti()
	
	def Equip(self, button, item):
		slots = ['a', 'b', 'x', 'y']
		
		if not (button == 'a' or button == 'b' or button == 'x' or button == 'y'):
			print('Could not equip to slot "%s"' % str(key))
			return False

		for s in slots:
			if self._Equipped(s) == item:
				self._ag.SetSavedVar('equipped_%s' % s, '')
			if item.startswith('item_cannon') and self._Equipped(s).startswith('item_cannon'):
				self._ag.SetSavedVar('equipped_%s' % s, '')
	
		self._ag.SetSavedVar('equipped_%s' % button, item)
		return True
	
	def EquipA(self, val):
		return self.Equip('a', val)
	def EquipB(self):
		return self.Equip('b', val)
	def EquipX(self, val):
		return self.Equip('x', val)
	def EquipY(self, val):
		return self.Equip('y', val)
	
	def EquippedA(self):
		return self._Equipped('a')
	def EquippedB(self):
		return self._Equipped('b')
	def EquippedX(self):
		return self._Equipped('x')
	def EquippedY(self):
		return self._Equipped('y')
	def _Equipped(self, button):
		i = self._ag.GetVar('equipped_%s' % button) or ''
		return i
	def WhichCannonEquipped(self):
		for l in ['a', 'b', 'x', 'y']:
			item = self._Equipped(l)
			if item and item.startswith('item_cannon'):
				return item
		return False
	
	def Sabre(self):
		return 'item_sabre'
	def Hammer(self):
		return 'item_hammer'
	def Drill(self):
		return 'item_drill'
	def Hook(self):
		return 'item_hook'
	def Cannon(self):
		return 'item_cannon'
	def CannonFire(self):
		return 'item_cannon_fire'
	def CannonIce(self):
		return 'item_cannon_ice'
	def CannonMulti(self):
		return 'item_cannon_multi'
	def Compass(self):
		return 'item_compass'
	def Shovel(self):
		return 'item_shovel'
	
	def Description(self, item):
		table = {}
		table[self.Sabre()] = 'Sabre'
		table[self.Hammer()] = 'Power Hammer'
		table[self.Drill()] = 'Steam Drill'
		table[self.Hook()] = 'Magnetic Gappling Hook'
		table[self.Cannon()] = 'Basic Ammo'
		table[self.CannonFire()] = 'Flame Ammo'
		table[self.CannonIce()] = 'Frost Ammo'
		table[self.CannonMulti()] = 'Multi-shot Ammo'
		table[self.Compass()] = 'Compass'
		table[self.Shovel()] = 'Shovel'
		return table.get(item, '')
	
	def PrintEquipped(self):
		for s in ['a', 'b', 'x', 'y']:
			print('%s => %s' % (s, self._Equipped(s)))