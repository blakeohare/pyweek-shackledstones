class JukeBox:
	def __init__(self):
		self.now_playing = None
		self.sound_library = {}
		self.music_library = {}
		self.current_volume = True
	
	def playSong(self, name):
		if name == 'STOP': name = None
		if name == None:
			Audio.Music.stop()
			return
		
		if self.now_playing != name:
			self.now_playing = name
			if not name.endswith('.ogg'):
				name = name + '.ogg'
			
			mus = self.music_library.get(name)
			if mus == None:
				mus = Audio.Music.loadFromResource('music/' + name)
				self.music_library[name] = mus
			
			mus.play(True)
	
	def playSound(self, name):
		if not name:
			return
		soundRes = self.sound_library.get(name)
		if soundRes == None:
			if not name.endswith('.ogg'):
				name = name + '.ogg'
			soundRes = Audio.SoundResource.loadFromResource('sound/' + name)
			self.sound_library[name] = soundRes
		soundRes.play()
	
def getJukebox():
	global _jukebox
	if _jukebox == None:
		_jukebox = JukeBox()
	return _jukebox

def play_sound(name):
	getJukebox().playSound(name)

def play_music(name):
	getJukebox().playSong(name)
