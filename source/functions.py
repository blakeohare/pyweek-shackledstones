
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