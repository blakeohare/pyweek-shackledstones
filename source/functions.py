
def trim(string):
	if string == None: return ''
	while len(string) > 0 and string[0] in ' \n\r\t':
		string = string[1:]
	while len(string) > 0 and string[-1] in ' \r\n\t':
		string = string[:-1]
	return string

def min(a, b):
	if a < b: return a
	return b
def max(a, b):
	if a < b: return b
	return a

def go_script_go(script_contents):
	MapScript(ScriptIter(script_contents.split('\n'))).Exec()

def scriptPath(*path):
   p = os.path.join('data', 'scripts', *path)
   p = '%s.scr' % (p)
   return p

def portraitPath(*path):
   p = os.path.join('images', 'portraits', *path)
   p = '%s.png' % p
   return p

def uiImgPath(*path):
   p = os.path.join('images', 'ui', *path)
   p = '%s.png' % p
   return p

def render_text(string, color = BLACK):
   return _font.render(string, True, color)

_fontBucket = {}
def render_text_size(size, string, color = BLACK, fontPath = MENU_FONT):
   fontKey = '%s-%s' % (fontPath, str(size))
   f = _fontBucket.get(fontKey)
   
   if not f:
      f = pygame.font.Font(fontPath, size)
      _fontBucket[fontKey] = f
   return f.render(string, True, color)

	
def make_list(size):
	return [None] * size

def make_table(width, height):
	cols = make_list(width)
	i = 0
	while i < width:
		cols[i] = make_list(height)
		i += 1
	return cols
	