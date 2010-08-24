class TransitionScene:

	def __init__(self, from_scene, to_level, to_tile, transition_type):
		self.from_scene = from_scene
		self.to_scene = GamePlayScene(to_level, 1, 1)
		dest_tile = self.to_scene.level.ids.get(to_tile)
		self.duration = 30
		self.temp_screen = None
		self.transition_type = transition_type
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
		progress = self.duration / 30.0
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
			x = -x
			y = 0
			screen.blit(self.get_from_screen(), (x, y))
			screen.blit(self.get_to_screen(), (x + w, y))
		elif transition == WARP_WSCROLL:
			x = x
			y = 0
			screen.blit(self.get_from_screen(), (x, y))
			screen.blit(self.get_to_screen(), (x - w, y))
		elif transition == WARP_PIXELATE:
			pass
			#TODO: Pixelate
		elif transition == WARP_FADE:
			#TODO: Fade
			pass
		
		
			
		
	
	

### STATIC ###
_temp_screen_for_transitions = None
def GetTempScreen(real_screen):
	global _temp_screen_for_transitions
	if _temp_screen_for_transitions == None:
		w = real_screen.get_width()
		h = real_screen.get_height()
		_temp_screen_for_transitions = pygame.Surface((w, h))
	return _temp_screen_for_transitions
