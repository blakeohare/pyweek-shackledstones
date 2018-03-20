class KeyRenderer:
	
	def __init__(self):
		pass
	
	def render(self, screen, game_scene):
		colors="black blue green indigo red white yellow".split()
		images= [get_image('tiles/keys/%s/key.png'%color) for color in colors]
		currentdungeon=game_scene.level.dungeon
		counts= [getKeyRegistry().getKeyCount(currentdungeon,color) for color in colors]
		xoffset=16
		for image, count in zip(images,counts):
			area=pygame.Rect(xoffset,screen.get_clip().bottom-16,8,8)
			if count:
				screen.blit(image, area)
			xoffset+=16
			screen.blit
