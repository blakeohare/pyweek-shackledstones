
class G2DText_Renderer:
	def __init__(self, resource):
		self.resource = resource
		self.color = (0, 0, 0)
		self.size = 13
		self.activePyGameFont = None
	
	def setColor(self, r, g, b):
		self.color = (r, g, b)
		return self
	
	def setSize(self, size):
		self.size = size
		self.activePyGameFont = None
		return self
	
	def render(self, text):
		if self.activePyGameFont == None:
			self.activePyGameFont = self.resource.getPyGameFont(self.size)
		return ImageWrapper(self.activePyGameFont.render(text, True, self.color))

g2dtext_resources = {}
class G2DText_FontResource:
	def __init__(self, path):
		self.path = ('source/' + path).replace('/', _OS_SEP)
		self.renderersByKey = {}
	
	def getRenderer(self):
		return G2DText_Renderer(self)
	
	def getPyGameFont(self, size):
		output = self.renderersByKey.get(size)
		if output == None:
			output = pygame.font.Font(self.path, size)
			self.renderersByKey[size] = output
		return output
	
def Graphics2DText_FontResource_loadFromResource(path):
	output = g2dtext_resources.get(path)
	if output == None:
		output = G2DText_FontResource(path)
	return output

Graphics2DText = EmptyObj()
Graphics2DText.FontResource = EmptyObj()
Graphics2DText.FontResource.loadFromResource = Graphics2DText_FontResource_loadFromResource
