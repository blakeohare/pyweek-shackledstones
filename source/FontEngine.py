class FontEngine:

	def __init__(self):
		self.cache = {}
		self.fontResources = {}
		self.fontRenderers = {}
		self._defaultFont = self.getFont('default', 13, (0, 0, 0))

	def getFontResource(self, name):
		output = self.fontResources.get(name)
		if output == None:
			if name == 'default':
				path = 'fonts/rm_typerighter.ttf'
			elif name == 'fancy':
				path = 'fonts/fortunaschwein.ttf'
			else:
				raise Exception("Unknown font option")
			output = Graphics2DText.FontResource.loadFromResource(path)
			self.fontResources[name] = output
		return output
	
	def getFont(self, name, size, color):
		k = '|'.join([name, str(size), str(color)])
		font = self.fontRenderers.get(k)
		if font == None:
			fontResource = self.getFontResource(name)
			font = fontResource.getRenderer().setColor(color[0], color[1], color[2]).setSize(size)
			self.fontRenderers[k] = font
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
		
		font = self.getFont(fontPath, size, color)
		img = font.render(string)
		if len(self.cache) > 20:
			self.cache = {}
		
		self.cache[k] = img
		return img

	def getDefaultFontHeight(self):
		return 18

def render_text_size(size, string, color, fontPath = 'fancy'):
	return getFontEngine().render_text_size(size, string, color, fontPath)

def render_text(string, color):
	return getFontEngine().render_text(string, color)

def getFontEngine():
	global _fontEngine
	if _fontEngine == None:
		_fontEngine = FontEngine()
	return _fontEngine
