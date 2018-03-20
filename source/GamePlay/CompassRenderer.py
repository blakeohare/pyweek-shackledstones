class CompassRenderer:
	
	def __init__(self):
		self.counter = 0
		self.on_temple = False
	
	def render(self, screen, game_scene):
		compass_image = get_image('ui/compass')
		self.counter += 1
		game_scene = getActiveGame().getActiveGameScene()
		if getActiveGame().getVar('is_compass_active') == 1:
			screen.blit(compass_image, (10, 200))
			spin_angle = self.counter * 3.14159 * 2 / 30
			if game_scene != None and game_scene.level.dungeon == 'light':
				angle = spin_angle
			elif game_scene == None or game_scene.name != 'world_W':
				angle = 3.14159 / 2
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
						angle = 3.14159 / 2
					else:
						angle = -3.14159 / 2
				elif dy == 0:
					if dx < 0:
						angle = 0
					else:
						angle = 3.14159
				else:
					angle = math.atan(dy / (0.0+ dx))
					if dx > 0:
						angle += 3.14159
			
			angle -= 3.14159 / 2
			n = (math.cos(angle - 3.14159 / 2), math.sin(angle - 3.14159 / 2))
			s = (math.cos(angle + 3.14159 / 2), math.sin(angle + 3.14159 / 2))
			e = (math.cos(angle) / 3, math.sin(angle) / 3)
			w = (math.cos(angle + 3.14159) / 3, math.sin(angle + 3.14159) / 3)
			
			
			n = (int(n[0] * 20) + 40, int(n[1] * 20) + 230)
			s = (int(s[0] * 20) + 40, int(s[1] * 20) + 230)
			e = (int(e[0] * 20) + 40, int(e[1] * 20) + 230)
			w = (int(w[0] * 20) + 40, int(w[1] * 20) + 230)
			
			pygame.draw.polygon(screen, (180, 0, 0), [n, e, w])
			pygame.draw.polygon(screen, (255, 255, 255), [s, e, w])
			pygame.draw.polygon(screen, (0,0,0), [n, e, s, w], 2)
