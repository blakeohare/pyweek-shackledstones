class JukeBox:
	def __init__(self):
		self.now_playing = None
		self.sound_library = {}
		self.current_volume = True
		pygame.mixer.init()
		pygame.mixer.music.set_volume(1.0)
	
	def PlaySong(self, name):
		return
		if not name:
			pygame.mixer.music.stop()
			return
		
		if self.now_playing != name:
			self.MakeMusicLoud()
			self.now_playing = name
			if not name.endswith('.mp3'):
				name=name+".mp3"
			pygame.mixer.music.load('media' + os.sep + 'music' + os.sep + name)
			pygame.mixer.music.play(-1)
	
	def PlaySound(self, name):
		if not name:
			return
		sound = self.sound_library.get(name)
		if sound == None:
			if not name.endswith('.wav'):
				name=name+".wav"
			sound = pygame.mixer.Sound('media' + os.sep + 'sound' + os.sep + name + '.wav')
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
		
### STATIC ###
_jukebox = JukeBox()
def play_sound(name):
	global _jukebox
	_jukebox.PlaySound(name)
def play_music(name):
	global _jukebox
	_jukebox.PlaySong(name)
def reduce_volume():
	global _jukebox
	_jukebox.MakeMusicSoft()
def increase_volume(name):
	global _jukebox
	_jukebox.MakeMusicLoud()
	