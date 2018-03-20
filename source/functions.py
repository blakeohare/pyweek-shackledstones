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

def go_script_go(script_contents):
	script_contents = script_contents.replace('\\n', '\n') # -_-
	MapScript(ScriptIter(script_contents.split('\n'))).Exec()

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
	value = ActiveGame().GetVar('money_amount')
	if value == None:
		return 0
	else:
		return int(value)

def set_money(amount):
	ActiveGame().SetSavedVar('money_amount', int(amount))

def modify_money(amount):
	set_money(max(0, get_money() + amount))

def has_money(amount):
	return get_money() >= amount

def get_life():
	value = ActiveGame().GetVar('life_meter')
	if value == None:
		return 3
	else:
		return max(0, int(value))

def get_max_life():
	value = ActiveGame().GetVar('has_armor')
	if value == None or value == 0:
		return 10
	else:
		return 20
		
def set_life(amount):
	ActiveGame().SetTempVar('life_meter', min(10, amount))
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
		
		if (word == '$nl$'):
			if curLine != '':
				lineSet.append(curLine)
				curLine = ''
				curWidth = 0
			lineSet.append('')
			continue

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
