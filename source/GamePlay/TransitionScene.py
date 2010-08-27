class TransitionScene:

	def __init__(self, from_scene, to_level, to_tile, transition_type):
		self.from_scene = from_scene
		self.to_scene = GamePlayScene(to_level, 1, 1)
		self.to_scene.overlayRenderer = None
		self.from_scene.overlayRenderer = None
		self.overlayRenderer = OverlayRenderer()
		dest_tile = self.to_scene.level.ids.get(to_tile)
		self.duration = 30
		if transition_type == WARP_PIXELATE:
			self.duration = 80
		self.max_duration = self.duration + 0.0
		self.temp_screen = None
		self.transition_type = transition_type
		play_music(self.to_scene.level.music)
		
		if dest_tile == None:
			self.next = from_scene
		else:
			self.next = self
			self.to_scene.place_player(dest_tile.layer, dest_tile.x, dest_tile.y)
			self.to_scene.player_invisible = True
			self.from_scene.player_invisible = True
			
	def ProcessInput(self, events):
		pass
		
	def Update(self, game_counter):
		self.duration -= 1
		if self.duration <= 0:
			self.next = self.to_scene
			self.next.overlayRenderer = self.overlayRenderer
			self.to_scene.player_invisible = False
		
	def get_to_screen(self):
		temp = GetTempScreen(self.screen)
		temp.fill((0,0,0))
		self.to_scene.Render(temp)
		return temp
		
	def get_from_screen(self):
		temp = GetTempScreen(self.screen)
		temp.fill((0,0,0))
		self.from_scene.Render(temp)
		return temp
		
	def Render(self, screen):
		self.screen = screen
		temp = GetTempScreen(screen)
		progress = self.duration / self.max_duration
		antiprogress = 1 - progress
		transition = self.transition_type
		h = temp.get_height()
		w = temp.get_width()
		x = int(progress * w)
		y = int(progress * h)
		if transition == WARP_SSCROLL:
			x = 0
			screen.blit(self.get_to_screen(), (x, y))
			screen.blit(self.get_from_screen(), (x, y - h))
		elif transition == WARP_NSCROLL:
			x = 0
			y = -y
			screen.blit(self.get_to_screen(), (x, y))
			screen.blit(self.get_from_screen(), (x, y + h))
		elif transition == WARP_ESCROLL:
			x = x
			y = 0
			screen.blit(self.get_to_screen(), (x, y))
			screen.blit(self.get_from_screen(), (x - w, y))
		elif transition == WARP_WSCROLL:
			x = -x
			y = 0
			screen.blit(self.get_to_screen(), (x, y))
			screen.blit(self.get_from_screen(), (x + w, y))
		elif transition == WARP_PIXELATE or transition == WARP_FADE:
			if progress < .5:
				image = self.get_to_screen()
				amount = progress * 2
			else:
				amount = antiprogress * 2
				image = self.get_from_screen()
			
			if transition == WARP_PIXELATE:
				image = self.pixelate_this(image, 1 - ((1 - amount) ** 2))
			
			screen.fill((0,0,0))
			
			alpha = int(max(0,min(255, 255 * (1 - amount))))
			
			image.set_alpha(alpha)
			screen.blit(image, (0,0))
		self.overlayRenderer.Render(screen)
		
			
	def pixelate_this(self, image, amount):
		minimum_w = 10
		maximum_w = image.get_width()
		minimum_h = 7
		maximum_h = image.get_height()
		
		width = int(minimum_w * amount + maximum_w * (1.0 - amount))
		height = int(minimum_h * amount + maximum_h * (1.0 - amount))
		
		tempScreen = GetTempScreenSize(width, height)
		pygame.transform.scale(image, (width, height), tempScreen)
		
		pygame.transform.scale(tempScreen, (image.get_width(), image.get_height()), image)
		return image
		
		
			
		
	
	

### STATIC ###
_temp_screen_for_transitions = None
_temp_screens = { }
def GetTempScreen(real_screen):
	global _temp_screen_for_transitions
	if _temp_screen_for_transitions == None:
		w = real_screen.get_width()
		h = real_screen.get_height()
		_temp_screen_for_transitions = pygame.Surface((w, h))
	return _temp_screen_for_transitions
def GetTempScreenSize(width, height):
	global _temp_screens
	index = str(width) + '.' + str(height)
	image = _temp_screens.get(index)
	if image == None:
		image = pygame.Surface((width, height))
		_temp_screens[index] = image
	return image