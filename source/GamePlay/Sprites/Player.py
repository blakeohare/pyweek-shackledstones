_invincible = False

class Player:
	def __init__(self):
		self.x = 100
		self.y = 100
		self.layer = 'A'
		self.r = 8
		self.id = 'MC'
		self.dx = 0
		self.is_goody = False
		self.dy = 0
		self.is_enemy = False
		self.direction = 'right'
		self.walking = False
		self.state = 'walking'
		self.expired = False
		self.flying = False
		self.flash_counter = -1
		self.state_counter = 0
		self.flying_damage = -42
		self.damage_dx = 0
		self.damage_dy = 0
		self.explode_on_impact = False
	
	def drawingCoords(self):
	
		coords = (self.x - self.r, self.y - self.r - 13)
		if self.state == 'stabbing' or self.state == 'hammering' or self.state == 'drilling':
			if self.direction == 'left':
				coords = (coords[0] - 16, coords[1])
			elif self.direction == 'up':
				coords = (coords[0], coords[1] - 16)
		return coords
	
	def update(self):
		global _invincible
		self.state_counter -= 1
		self.flash_counter -= 1
		self.flying_damage -= 1
		if self.state_counter <= 0:
			self.state = 'walking'
			
		if self.flash_counter < 0:
			if not _invincible:
				game_scene = getActiveGame().getActiveGameScene()
				for sprite in game_scene.sprites:
					if sprite.is_enemy:
						if sprite.layer == self.layer:
							dx = sprite.x - self.x
							dy = sprite.y - self.y
							if dx ** 2 + dy ** 2 < (self.r + sprite.r) ** 2:
								self.flash_counter = 30
								take_damage(1)
								if get_life() == 0:
									set_life(3)
									getActiveGame().getActiveGameScene().next = GameOverScene()
								else:
									self.flying_damage = 5
									nv = get_normalized_vector(sprite.x, sprite.y, self.x, self.y)
									self.damage_dx = nv[0] * 7
									self.damage_dy = nv[1] * 7
	
	def stab(self):
		if self.is_submerged(): return
		self.state_counter = 7
		self.state = 'stabbing'
		x = self.x
		y = self.y
		if self.direction == 'left':
			x -= 16
		elif self.direction == 'up':
			y -= 16
		elif self.direction == 'down':
			y += 16
		else:
			x += 16
		game_scene = getActiveGame().getActiveGameScene()
		
		game_scene.place_death_circle('sword', x, y, 8, 5)
		play_sound('sword')

	def shoot(self, bullet_type, game_scene):
		if self.is_submerged(): return
		self.state_count = 7
		self.state = 'shooting'
		
		sprites = []
		if bullet_type == 'multi':
			also = []
			if self.direction == 'left' or self.direction == 'right':
				also = ['up','down']
			if self.direction == 'down' or self.direction == 'up':
				also = ['left','right']
			for b in also:
				sprites.append(Projectile(bullet_type, True, self.layer, self.x, self.y, b, game_scene))
		sprites.append(Projectile(bullet_type, True, self.layer, self.x, self.y, self.direction, game_scene))
		for s in sprites:
			game_scene.sprites.append(s)
		play_sound('gunshot')
		
	def dig(self):
		if self.is_submerged(): return
		self.state_counter = 20
		self.state = 'shovelling'
		play_sound('dig')
	
	def drill(self):
		if self.is_submerged(): return
		self.state_counter = 15
		self.state = 'drilling'
		x = self.x
		y = self.y
		if self.direction == 'left':
			x -= 16
		elif self.direction == 'up':
			y -= 16
		elif self.direction == 'down':
			y += 16
		else:
			x += 16
		game_scene = getActiveGame().getActiveGameScene()
		
		game_scene.place_death_circle('drill', x, y, 8, 5)
		play_sound('drill')
	
	def hammer(self):
		if self.is_submerged(): return
		self.state_counter = 15
		self.state = 'hammering'
		x = self.x
		y = self.y
		if self.direction == 'left':
			x -= 16
		elif self.direction == 'up':
			y -= 16
		elif self.direction == 'down':
			y += 16
		else:
			x += 16
		game_scene = getActiveGame().getActiveGameScene()
		
		game_scene.place_death_circle('hammer', x, y, 8, 5)
		play_sound('hammer')
	
	def Grapple(self):
		if self.is_submerged(): return
		game_scene = getActiveGame().getActiveGameScene()
		if game_scene.grapple == None:
			start_x = self.x
			start_y = self.y
			end_x = start_x
			end_y = start_y
			if self.direction == 'up':
				end_y -= 16 * 6
			elif self.direction == 'down':
				end_y += 16 * 6
			elif self.direction == 'left':
				end_x -= 16 * 6
			elif self.direction == 'right':
				end_x += 16 * 6
			
			grapple = Projectile('grapple', True, self.layer, self.x, self.y, self.direction, game_scene)
			grapple.end_x = end_x
			grapple.end_y = end_y
			game_scene.sprites.append(grapple)
			game_scene.grapple = grapple
	
	def is_submerged(self):
		gs = getActiveGame().getActiveGameScene()
		if gs != None:
			layer = gs.level.layers[self.layer]
			x = self.x >> 4
			y = self.y >> 4
			if x >= 0 and x < layer.width and y >= 0 and y < layer.height:
				value = layer.tiles[x][y].submerged
				return value
	
	def currentImage(self, render_counter):
		if self.flash_counter > 0 and (self.flash_counter & 1) == 0:
			return None
		
		counter = '0'
		if self.is_submerged():
			if self.direction == 'right':
				return get_image('sprites/maincharacter/sinkright2')
			if self.direction == 'left':
				return get_image('sprites/maincharacter/sinkleft2')
			if self.direction == 'up':
				return get_image('sprites/maincharacter/sinkup2')
			if self.direction == 'down':
				return get_image('sprites/maincharacter/sinkdown2')
		elif self.state == 'walking':
			if self.walking:
				counter = ('0','1','0','2')[(render_counter // 3) & 3]
			else:
				counter = 0
			counter = str(counter)
			if self.direction == 'right':
				return get_image('sprites/maincharacter/right' + counter)
			if self.direction == 'left':
				return get_image('sprites/maincharacter/left' + counter)
			if self.direction == 'up':
				return get_image('sprites/maincharacter/up' + counter)
			if self.direction == 'down':
				return get_image('sprites/maincharacter/down' + counter)
		elif self.state == 'stabbing' or self.state == 'hammering' or self.state == 'drilling' or self.state == 'shovelling':
			if self.state == 'stabbing':
				img_name = 'stab'
				counter = ('1','2','2','1','1')[(self.state_counter // 2) % 5]
			if self.state == 'drilling':
				img_name = 'drill'
				counter = ((self.state_counter // 2) % 3) + 1
			if self.state == 'hammering':
				img_name = 'hammer'
				counter = ('1','1','2','3','3','3','3','3','3','3','3','3','2','1','1')[self.state_counter % 15]
			if self.state == 'shovelling':
				img_name = 'shovel'
				counter = 2 - ((self.state_counter // 11) % 2)
				self.direction = 'right'
			counter = str(counter)
			if self.direction == 'right':
				return get_image('sprites/maincharacter/'+img_name+'right' + counter)
			if self.direction == 'left':
				return get_image('sprites/maincharacter/'+img_name+'left' + counter)
			if self.direction == 'up':
				return get_image('sprites/maincharacter/'+img_name+'up' + counter)
			if self.direction == 'down':
				return get_image('sprites/maincharacter/'+img_name+'down' + counter)
			
		return get_image('sprites/maincharacter/down' + counter)
