
def trim(string):
	if string == None: return ''
	while len(string) > 0 and string[0] in ' \n\r\t':
		string = string[1:]
	while len(string) > 0 and string[-1] in ' \r\n\t':
		string = string[:-1]
	return string

def scriptPath(*path):
   p = os.path.join('data', 'scripts', *path)
   p = '%s.scr' % (p)
   return p