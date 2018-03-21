
def get_image(path):
	img = _imageLibrary.get(path)
	if img == None:
		file_path = os.path.join('source', 'images', path.replace('/', os.sep).replace('\\', os.sep))
		if not file_path.endswith('.png'):
			file_path += '.png'
		
		_imageLibrary[path] = ImageWrapper(pygame.image.load(file_path))
	return _imageLibrary[path]

def run_script(script_contents):
	script_contents = script_contents.replace('\\n', '\n') # TODO: fix this
	scriptIter = ScriptIter(script_contents.split('\n'))
	scriptEngine = ScriptEngine(scriptIter)
	applyMapScriptFunctions(scriptEngine)
	scriptEngine.advance()

def make_table(width, height):
	cols = []
	t = [None]
	while width > 0:
		cols.append(t * height)
		width -= 1
	return cols

def get_money():
	return getActiveGame().getInt('money_amount')

def set_money(amount):
	getActiveGame().setSavedVar('money_amount', int(amount))

def modify_money(amount):
	set_money(max(0, get_money() + amount))

def has_money(amount):
	return get_money() >= amount

def get_life():
	return max(0, getActiveGame().getInt('life_meter', 3))

def get_max_life():
	return 20 if getActiveGame().getBool('has_armor') else 10

def set_life(amount):
	getActiveGame().setTempVar('life_meter', min(10, amount))

def take_damage(amount):
	set_life(get_life() - amount)
	return get_life() <= 0

def heal_damage():
	set_life(get_life() + 1)

def draw_rect_stroke(x, y, w, h, r, g, b, strokeSize):
	right = x + w - 1
	bottom = y + h - 1
	Graphics2D.Draw.line(x, y, right, y, strokeSize, r, g, b)
	Graphics2D.Draw.line(x, bottom, right, bottom, strokeSize, r, g, b)
	Graphics2D.Draw.line(x, y, x, bottom, strokeSize, r, g, b)
	Graphics2D.Draw.line(right, y, right, bottom, strokeSize, r, g, b)

def fill_screen_with_alpha(r, g, b, a):
	Graphics2D.Draw.rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, r, g, b, a)
	
def draw_circle_stroke(x, y, radius, strokeSize, r, g, b):
	m = Math.PI * 2 / 20.0
	for i in range(20):
		aAng = m * i
		bAng = m * (i + 1)
		x1 = Math.floor(Math.cos(aAng) * radius + x)
		y1 = Math.floor(Math.sin(aAng) * radius + y)
		x2 = Math.floor(Math.cos(bAng) * radius + x)
		y2 = Math.floor(Math.sin(bAng) * radius + y)
		Graphics2D.Draw.line(x1, y1, x2, y2, strokeSize, r, g, b)

def random_choice(list):
	return list[Random.randomInt(len(list))]