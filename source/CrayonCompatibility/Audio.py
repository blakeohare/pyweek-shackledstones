
Audio = EmptyObj()
Audio.Music = EmptyObj()
Audio.SoundResource = EmptyObj()
Audio.is_initialized = False

def Audio_Music_stop():
	pygame.mixer.music.stop()

_audio_music_cache = {}
def Audio_Music_loadFromResource(path):
	m = _audio_music_cache.get(path)
	if m == None:
		m = MusicInstance(path)
	return m

def Audio_SoundResource_loadFromResource(path):
	return SoundResourceInstance(path)
	
def _audio_ensure_initialized():
	if not Audio.is_initialized:
		pygame.mixer.init()
		pygame.mixer.music.set_volume(1.0)
		Audio.is_initialized = True

class MusicInstance:
	def __init__(self, path):
		path = 'source/' + path
		path = path.replace('/', os.sep)
		self.file_path = path
	
	def play(self, loop):
		_audio_ensure_initialized()
		pygame.mixer.music.load(self.file_path)
		pygame.mixer.music.play(-1 if loop else 1)

class SoundResourceInstance:
	def __init__(self, path):
		path = 'source/' + path
		path = path.replace('/', os.sep)
		_audio_ensure_initialized()
		self.nativeSound = pygame.mixer.Sound(path)
	
	def play(self):
		self.nativeSound.play()
	
Audio.Music.loadFromResource = Audio_Music_loadFromResource
Audio.Music.stop = Audio_Music_stop
Audio.SoundResource.loadFromResource = Audio_SoundResource_loadFromResource
