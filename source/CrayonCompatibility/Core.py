
_STRING_TYPE = type('')

Core = EmptyObj()
Core.parseInt = int
Core.isString = lambda x: type(x) == _STRING_TYPE

# file IO helpers used by both UserData and Resources
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
