class CompassRenderer:
	
	def __init__(self):
		self.counter = 0
		self.on_temple = False
	
	def render(self, screen, game_scene):
		compass_image = get_image('ui/compass')
		self.counter += 1
		game_scene = getActiveGame().getActiveGameScene()
		if getActiveGame().getBool('is_compass_active'):
			compass_image.draw(10, 200)
			spin_angle = self.counter * Math.PI * 2 / 30
			if game_scene != None and game_scene.level.dungeon == 'light':
				angle = spin_angle
			elif game_scene == None or game_scene.name != 'world_W':
				angle = Math.PI / 2
			else:
				tile = game_scene.level.ids['temple']
				x = (tile.x << 4) + 8
				y = (tile.y << 4) + 8
				player_x = game_scene.player.x 
				player_y = game_scene.player.y
				
				dx = x - player_x
				dy = y - player_y
				
				if abs(dx) < 5 and abs(dy) < 5:
					angle = spin_angle
				elif dx == 0:
					if dy < 0:
						angle = Math.PI / 2
					else:
						angle = -Math.PI / 2
				elif dy == 0:
					if dx < 0:
						angle = 0
					else:
						angle = Math.PI
				else:
					angle = Math.arctan(dy, dx)
					if dx > 0:
						angle += Math.PI
			
			angle -= Math.PI / 2
			n = (Math.cos(angle - Math.PI / 2), Math.sin(angle - Math.PI / 2))
			s = (Math.cos(angle + Math.PI / 2), Math.sin(angle + Math.PI / 2))
			e = (Math.cos(angle) / 3, Math.sin(angle) / 3)
			w = (Math.cos(angle + Math.PI) / 3, Math.sin(angle + Math.PI) / 3)
			
			
			n = (Math.floor(n[0] * 20) + 40, Math.floor(n[1] * 20) + 230)
			s = (Math.floor(s[0] * 20) + 40, Math.floor(s[1] * 20) + 230)
			e = (Math.floor(e[0] * 20) + 40, Math.floor(e[1] * 20) + 230)
			w = (Math.floor(w[0] * 20) + 40, Math.floor(w[1] * 20) + 230)
			
			Graphics2D.Draw.triangle(n[0], n[1], e[0], e[1], w[0], w[1], 180, 0, 0)
			Graphics2D.Draw.triangle(s[0], s[1], e[0], e[1], w[0], w[1], 255, 255, 255)
			
			for segment in ((n, e), (e, s), (s, w), (w, n)):
				a = segment[0]
				b = segment[1]
				Graphics2D.Draw.line(a[0], a[1], b[0], b[1], 2, 0, 0, 0)
