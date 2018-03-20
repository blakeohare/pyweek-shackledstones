class Inventory:
	def __init__(self):
		self._ag = getActiveGame()
	
	def Surf(self, slot):
		i = self._Equipped(slot)
		if i:
			return get_image('ui/' + i + '.png')
		else:
			return None
	
	def HasAny(self):
		i = self
		items = (i.Sabre(), i.Hammer(), i.Drill(), i.Hook(), i.Compass(), i.Cannon(), i.CannonFire(), i.CannonIce(), i.CannonMulti(), i.Shovel())
		for it in items:
			if self.Check(it):
				return True
	
	def Check(self, item):
		return str(self._ag.getVar(item)) == '1'
	
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
				self._ag.setSavedVar('equipped_%s' % s, '')
			if item.startswith('item_cannon') and self._Equipped(s).startswith('item_cannon'):
				self._ag.setSavedVar('equipped_%s' % s, '')
	
		self._ag.setSavedVar('equipped_%s' % button, item)
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
		i = self._ag.getVar('equipped_%s' % button) or ''
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
