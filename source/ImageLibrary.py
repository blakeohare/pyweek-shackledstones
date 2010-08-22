class Image:
	def __init__(self, img, x_offset = 0, y_offset = 0):
		self.img = img
		self.x_offset = x_offset
		self.y_offset = y_offset
	
	def blit(self, image, coords):
		self.img.blit(image, (coords[0] + image.x_offset, coords[1] + image.y_offset))

_image_offset_lookup = {
#none

}

class ImageLibrary:

	def __init__(self):
		self.images = {}
	
	def get_image(self, path):
		if not self.images.has_key(path):
			file_path = 'images' + os.sep + path.replace('/', os.sep).replace('\\', os.sep)
			if not file_path.endswith('.png'):
				file_path += '.png'
			
			img = pygame.image.load(file_path)
			x = 0
			y = 0
			if _image_offset_lookup.has_key(path):
				image = Image(img, _image_offset_lookup[path][0], _image_offset_lookup[path][1])
			else:
				image = Image(img, 0, 0)
			self.images[path] = image
		return self.images[path]

### STATIC ###

_imageLibrary = ImageLibrary()
def get_image(path):
	return _imageLibrary.get_image(path)
