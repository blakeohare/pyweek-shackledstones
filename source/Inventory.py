# Inventory is mostly stateless as it dirctly queries the active game.

class Inventory:
	def __init__(self):
		self._ag = getActiveGame()
	
	def getItemIcon(self, slot):
		i = self._equipped(slot)
		if i:
			return get_image('ui/' + i + '.png')
		else:
			return None
	
	def hasAny(self):
		i = self
		items = (i.sabre(), i.hammer(), i.drill(), i.hook(), i.compass(), i.cannon(), i.cannonFire(), i.cannonIce(), i.cannonMulti(), i.shovel())
		for it in items:
			if self.check(it):
				return True
	
	def check(self, item):
		return self._ag.getBool(item)
	
	def equip(self, button, item):
		slots = ['a', 'b', 'x', 'y']
		
		if not (button == 'a' or button == 'b' or button == 'x' or button == 'y'):
			print('Could not equip to slot "%s"' % str(key))
			return False

		for s in slots:
			if self._equipped(s) == item:
				self._ag.setSavedVar('equipped_%s' % s, '')
			if item.startswith('item_cannon') and self._equipped(s).startswith('item_cannon'):
				self._ag.setSavedVar('equipped_%s' % s, '')
	
		self._ag.setSavedVar('equipped_%s' % button, item)
		return True
	
	def equipA(self, val):
		return self.equip('a', val)
	def equipB(self):
		return self.equip('b', val)
	def equipX(self, val):
		return self.equip('x', val)
	def equipY(self, val):
		return self.equip('y', val)
	
	def equippedA(self):
		return self._equipped('a')
	def equippedB(self):
		return self._equipped('b')
	def equippedX(self):
		return self._equipped('x')
	def equippedY(self):
		return self._equipped('y')
	def _equipped(self, button):
		i = self._ag.getString('equipped_' + button)
		return i
	def whichCannonEquipped(self):
		for l in ['a', 'b', 'x', 'y']:
			item = self._equipped(l)
			if item and item.startswith('item_cannon'):
				return item
		return False
	
	def sabre(self):
		return 'item_sabre'
	def hammer(self):
		return 'item_hammer'
	def drill(self):
		return 'item_drill'
	def hook(self):
		return 'item_hook'
	def cannon(self):
		return 'item_cannon'
	def cannonFire(self):
		return 'item_cannon_fire'
	def cannonIce(self):
		return 'item_cannon_ice'
	def cannonMulti(self):
		return 'item_cannon_multi'
	def compass(self):
		return 'item_compass'
	def shovel(self):
		return 'item_shovel'
	
	def description(self, item):
		table = {}
		table[self.sabre()] = 'Sabre'
		table[self.hammer()] = 'Power Hammer'
		table[self.drill()] = 'Steam Drill'
		table[self.hook()] = 'Magnetic Gappling Hook'
		table[self.cannon()] = 'Basic Ammo'
		table[self.cannonFire()] = 'Flame Ammo'
		table[self.cannonIce()] = 'Frost Ammo'
		table[self.cannonMulti()] = 'Multi-shot Ammo'
		table[self.compass()] = 'Compass'
		table[self.shovel()] = 'Shovel'
		return table.get(item, '')
