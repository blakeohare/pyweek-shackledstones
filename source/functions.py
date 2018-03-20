def read_text_file(path):
	realPath = path.replace('/', os.sep)
	c = open(realPath, 'rt')
	text = c.read()
	c.close()
	return text

def write_text_file(path, content):
	realPath = path.replace('/', os.sep)
	c = open(realPath, 'wt')
	c.write(content)
	c.close()

def file_exists(path):
	realPath = path.replace('/', os.sep)
	return os.path.exists(realPath)

def get_image(path):
	img = _imageLibrary.get(path)
	if img == None:
		file_path = 'images' + os.sep + path.replace('/', os.sep).replace('\\', os.sep)
		if not file_path.endswith('.png'):
			file_path += '.png'
		
		_imageLibrary[path] = pygame.image.load(file_path)
	return _imageLibrary[path]

def run_script(script_contents):
	script_contents = script_contents.replace('\\n', '\n') # TODO: fix this
	scriptIter = ScriptIter(script_contents.split('\n'))
	scriptEngine = ScriptEngine(scriptIter)
	applyMapScriptFunctions(scriptEngine)
	scriptEngine.advance()

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

def render_number(num, color=BLACK, sz=15):
	return render_text_size(sz, str(num), color, TEXT_FONT)

def make_list(size):
	return [None] * size

def make_table(width, height):
	cols = make_list(width)
	i = 0
	while i < width:
		cols[i] = make_list(height)
		i += 1
	return cols

def get_money():
	value = getActiveGame().getVar('money_amount')
	if value == None:
		return 0
	else:
		return int(value)

def set_money(amount):
	getActiveGame().setSavedVar('money_amount', int(amount))

def modify_money(amount):
	set_money(max(0, get_money() + amount))

def has_money(amount):
	return get_money() >= amount

def get_life():
	value = getActiveGame().getVar('life_meter')
	if value == None:
		return 3
	else:
		return max(0, int(value))

def get_max_life():
	value = getActiveGame().getVar('has_armor')
	if value == None or value == 0:
		return 10
	else:
		return 20

def set_life(amount):
	getActiveGame().setTempVar('life_meter', min(10, amount))

def take_damage(amount):
	set_life(get_life() - amount)
	return get_life() <= 0

def heal_damage():
	set_life(get_life() + 1)

def wrap_text(surf, txt, fnt):
	lineWidth = surf.get_width()
	words = re.split("\s", txt)
	clr = pygame.Color('#ffffff')
	
	lineSet = []
	curLine = ''
	curWidth = 0
	for word in words:
		word = word.strip()
		
		if (curLine != ''):
			renderWord = ' %s' % word
		else:
			renderWord = word
		
		wSurf = fnt.render(renderWord, True, clr)
		wordWidth = wSurf.get_width()
		
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

def lines_visible(surf, fnt):
	return int(surf.get_height() / fnt.get_height())

def draw_rect_stroke(x, y, w, h, r, g, b, strokeSize):
	right = x + w
	bottom = y + h
	Graphics2D.Draw.line(x, y, right, y, strokeSize, r, g, b)
	Graphics2D.Draw.line(x, bottom, right, bottom, strokeSize, r, g, b)
	Graphics2D.Draw.line(x, y, x, bottom, strokeSize, r, g, b)
	Graphics2D.Draw.line(right, y, right, bottom, strokeSize, r, g, b)
