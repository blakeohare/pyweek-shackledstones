
class ImageLibrary:

	def __init__(self):
		self.images = {}
	
	def get_image(self, path):
		img = self.images.get(path)
		if img == None:
			file_path = 'images' + os.sep + path.replace('/', os.sep).replace('\\', os.sep)
			if not file_path.endswith('.png'):
				file_path += '.png'
			
			self.images[path] = pygame.image.load(file_path)
		return self.images[path]

### STATIC ###

_imageLibrary = ImageLibrary()
def get_image(path):
	return _imageLibrary.get_image(path)