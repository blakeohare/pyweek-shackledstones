
_g2dDraw_tempSurf = {}
def Graphics2D_Draw_rectangle(x, y, w, h, r, g, b, a = 255):
	if a >= 255:
		pygame.draw.rect(_activeScreen, (r, g, b), pygame.Rect(x, y, w, h))
	elif a <= 0:
		return
	else:
		k = w * 100000 + h
		t = _g2dDraw_tempSurf.get(k)
		if t == None:
			t = pygame.Surface((w, h)).convert()
			_g2dDraw_tempSurf[k] = t
		t.fill((r, g, b))
		t.set_alpha(a)
		_activeScreen.blit(t, (x, y))

def Graphics2D_Draw_ellipse(x, y, w, h, r, g, b, a = 255):
	pygame.draw.ellipse(_activeScreen, (r, g, b), pygame.Rect(x, y, w, h))
	
def Graphics2D_Draw_line(x1, y1, x2, y2, strokeSize, r, g, b, a = 255):
	pygame.draw.line(_activeScreen, (r, g, b), (x1, y1), (x2, y2), strokeSize)

def Graphics2D_Draw_triangle(x1, y1, x2, y2, x3, y3, r, g, b, a = 255):
	pygame.draw.polygon(_activeScreen, (r, g, b), [(x1, y1), (x2, y2), (x3, y3)])

def Graphics2D_Draw_quad(x1, y1, x2, y2, x3, y3, x4, y4, r, g, b, a = 255):
	pygame.draw.polygon(_activeScreen, (r, g, b), [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])

def Graphics2D_Draw_fill(r, g, b):
	_activeScreen.fill((r, g, b))

Graphics2D = EmptyObj()
Graphics2D.Draw = EmptyObj()
Graphics2D.Draw.rectangle = Graphics2D_Draw_rectangle
Graphics2D.Draw.ellipse = Graphics2D_Draw_ellipse
Graphics2D.Draw.line = Graphics2D_Draw_line
Graphics2D.Draw.triangle = Graphics2D_Draw_triangle
Graphics2D.Draw.quad = Graphics2D_Draw_quad
Graphics2D.Draw.fill = Graphics2D_Draw_fill

class ImageWrapper:
	def __init__(self, nativeImage):
		self.nativeImage = nativeImage
		self.width = nativeImage.get_width()
		self.height = nativeImage.get_height()
	
	def draw(self, x, y):
		_activeScreen.blit(self.nativeImage, (x, y))
	
	def drawStretched(self, x, y, width, height):
		_activeScreen.blit(self.nativeImage, pygame.Rect(x, y, width, height))
	
	# TODO: get rid of these and call the fields directly
	def get_width(self): return self.width
	def get_height(self): return self.height
	def get_size(self): return (self.width, self.height)
