
def Graphics2D_Draw_rectangle(x, y, w, h, r, g, b, a = 255):
	pygame.draw.rect(_activeScreen, (r, g, b), pygame.Rect(x, y, w, h))

def Graphics2D_Draw_line(x1, y1, x2, y2, strokeSize, r, g, b, a = 255):
	pygame.draw.line(_activeScreen, (r, g, b), (x1, y1), (x2, y2), strokeSize)

Graphics2D = EmptyObj()
Graphics2D.Draw = EmptyObj()
Graphics2D.Draw.rectangle = Graphics2D_Draw_rectangle
Graphics2D.Draw.line = Graphics2D_Draw_line
