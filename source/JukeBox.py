class JukeBox:
	def __init__(self):
		self.now_playing = None
		self.sound_library = {}
		self.current_volume = True
		pygame.mixer.init()
		pygame.mixer.music.set_volume(1.0)
	
	def PlaySong(self, name):
		#return
		if name == 'STOP': name = None
		if not name:
			pygame.mixer.music.stop()
			return
		
		if self.now_playing != name:
			self.MakeMusicLoud()
			self.now_playing = name
			if not name.endswith('.ogg'):
				name = name + '.ogg'
			pygame.mixer.music.load('source' + os.sep + 'music' + os.sep + name)
			pygame.mixer.music.play(-1)
	
	def PlaySound(self, name):
		if not name:
			return
		sound = self.sound_library.get(name)
		if sound == None:
			if not name.endswith('.ogg'):
				name=name + '.ogg'
			sound = pygame.mixer.Sound('source' + os.sep + 'sound' + os.sep + name)
			self.sound_library[name] = sound
		sound.play()
	
	def MakeMusicSoft(self):
		if self.current_volume:
			pygame.mixer.music.set_volume(0.5)
			self.current_volume = False
	
	def MakeMusicLoud(self):
		if not self.current_volume:
			pygame.mixer.music.set_volume(1.0)
			self.current_volume = True

def getJukebox():
	global _jukebox
	if _jukebox == None:
		_jukebox = JukeBox()
	return _jukebox

def play_sound(name):
	getJukebox().PlaySound(name)

def play_music(name):
	getJukebox().PlaySong(name)

def reduce_volume():
	getJukebox().MakeMusicSoft()

def increase_volume(name):
	getJukebox().MakeMusicLoud()
	