class FontEngine:

	def __init__(self):
		self.cache = {}
		self.fontCache = {}
		self._defaultFont = self.getFont('default', 13)

	def getFont(self, name, size):
		k = '|'.join([name, str(size)])
		font = self.fontCache.get(k)
		if font == None:
			if name == 'default':
				path = 'rm_typerighter.ttf'
			elif name == 'fancy':
				path = 'fortunaschwein.ttf'
			else:
				raise Exception("Unknown font option")
			path = ('source/fonts/' + path).replace('/', os.sep)
			font = pygame.font.Font(path, size)
			self.fontCache[k] = font
		return font
		
	def wrap_text(self, lineWidth, txt):
		
		words = txt.replace('\n', ' ').replace('  ', ' ').replace('  ', ' ').split(' ') # bleh
		
		lineSet = []
		curLine = ''
		curWidth = 0
		for word in words:
			word = word.strip()
			
			if (curLine != ''):
				renderWord = ' ' + word
			else:
				renderWord = word
			
			# Use black since there's a better chance it'll cause a cache hit
			wordWidth = render_text(renderWord, (0, 0, 0)).width
			
			if (curWidth + wordWidth) < lineWidth:
				curLine += renderWord
				curWidth += wordWidth
			else:
				lineSet.append(curLine)
				curLine = word
				curWidth = wordWidth
		
		if (curLine != ''):
			lineSet.append(curLine)
		
		return lineSet

	def render_text(self, string, color):
		return render_text_size(13, string, color, 'default')

	def render_text_size(self, size, string, color, fontPath):
		
		k = str([string, color, fontPath, size])
		existing = self.cache.get(k)
		if existing != None: return existing
		
		font = self.getFont(fontPath, size)
		img = ImageWrapper(font.render(string, True, color))
		if len(self.cache) > 20:
			self.cache = {}
		
		self.cache[k] = img
		return img

	def getDefaultFontHeight(self):
		return self._defaultFont.get_height()

def render_text_size(size, string, color, fontPath = 'fancy'):
	return getFontEngine().render_text_size(size, string, color, fontPath)

def render_text(string, color):
	return getFontEngine().render_text(string, color)

def getFontEngine():
	global _fontEngine
	if _fontEngine == None:
		_fontEngine = FontEngine()
	return _fontEngine
