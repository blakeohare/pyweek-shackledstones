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
		self.transition_type = transition_type
		play_music(self.to_scene.level.music)
		
		if dest_tile == None:
			self.next = from_scene
		else:
			self.next = self
			self.to_scene.place_player(dest_tile.layer, dest_tile.x, dest_tile.y)
			self.to_scene.player_invisible = True
			self.from_scene.player_invisible = True
			
	def processInput(self, events):
		pass
		
	def update(self, game_counter):
		self.duration -= 1
		if self.duration <= 0:
			self.next = self.to_scene
			self.next.overlayRenderer = self.overlayRenderer
			self.to_scene.player_invisible = False

	def render(self, screen, renderOffset):
		progress = self.duration / self.max_duration
		antiprogress = 1 - progress
		transition = self.transition_type
		h = screen.get_height()
		w = screen.get_width()
		x = int(progress * w)
		y = int(progress * h)
		to_offset = [0, 0]
		from_offset = [0, 0]
		
		callRender = True
		
		if transition == WARP_SSCROLL:
			to_offset[1] = y
			from_offset[1] = y - h
		elif transition == WARP_NSCROLL:
			to_offset[1] = -y
			from_offset[1] = -y + h
		elif transition == WARP_ESCROLL:
			to_offset[0] = x
			from_offset[0] = x - w
		elif transition == WARP_WSCROLL:
			to_offset[0] = -x
			from_offset[0] = -x + w
		elif transition == WARP_PIXELATE or transition == WARP_FADE:
			callRender = False
			rProgress = 1 - progress # original calculations are backwards? 
			if rProgress < .5:
				self.from_scene.render(screen, (0, 0))
				amount = Math.floor(255 * rProgress * 2)
			else:
				self.to_scene.render(screen, (0, 0))
				amount = Math.floor((1 - (rProgress * 2 - 1)) * 255)
			
			alpha = int(max(0,min(255, 255 * (1 - amount))))
			fill_screen_with_alpha(0, 0, 0, amount)
		
		if callRender:
			self.from_scene.render(screen, from_offset)
			self.to_scene.render(screen, to_offset)
			
		self.overlayRenderer.render(screen)
