
def Graphics2D_Draw_rectangle(x, y, w, h, r, g, b, a = 255):
	pygame.draw.rect(_activeScreen, (r, g, b), pygame.Rect(x, y, w, h))

def Graphics2D_Draw_line(x1, y1, x2, y2, strokeSize, r, g, b, a = 255):
	pygame.draw.line(_activeScreen, (r, g, b), (x1, y1), (x2, y2), strokeSize)

def Graphics2D_Draw_triangle(x1, y1, x2, y2, x3, y3, r, g, b, a = 255):
	pygame.draw.polygon(_activeScreen, (r, g, b), [(x1, y1), (x2, y2), (x3, y3)])

def Graphics2D_Draw_quad(x1, y1, x2, y2, x3, y3, x4, y4, r, g, b, a = 255):
	pygame.draw.polygon(_activeScreen, (r, g, b), [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])

Graphics2D = EmptyObj()
Graphics2D.Draw = EmptyObj()
Graphics2D.Draw.rectangle = Graphics2D_Draw_rectangle
Graphics2D.Draw.line = Graphics2D_Draw_line
Graphics2D.Draw.triangle = Graphics2D_Draw_triangle
Graphics2D.Draw.quad = Graphics2D_Draw_quad
