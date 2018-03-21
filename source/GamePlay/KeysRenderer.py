class KeyRenderer:
	
	def __init__(self):
		self.colors = "black blue green indigo red white yellow".split()
	
	def render(self, screen, game_scene):
		currentdungeon = game_scene.level.dungeon
		if currentdungeon != '':
			items = []
			for color in self.colors:
				img = get_image('tiles/keys/' + color + '/key.png')
				count = getKeyRegistry().getKeyCount(currentdungeon, color)
				items.append([img, count])
			
			xoffset = 16
			for item in items:
				image = item[0]
				count = item[1]
				if count > 0:
					screen.blit(image, pygame.Rect(xoffset, SCREEN_HEIGHT - 16, 8, 8))
				xoffset += 16
