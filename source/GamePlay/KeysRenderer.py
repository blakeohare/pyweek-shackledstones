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
				area = pygame.Rect(xoffset,screen.get_clip().bottom - 16, 8, 8)
				if count:
					screen.blit(image, area)
				xoffset += 16
