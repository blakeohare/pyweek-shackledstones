import os

pyweek_root = '.' + os.sep

imports = pyweek_root + 'source' + os.sep + 'imports.py'
main = pyweek_root + 'source' + os.sep + 'main.py'
functions = pyweek_root + 'source' + os.sep + 'functions.py'
exempt = [imports, main, functions]

root = pyweek_root + 'source'

def get_all_files(folder):
	files = []
	for file in os.listdir(folder):
		path = folder + os.sep + file
		if os.path.isdir(path):
			files += get_all_files(path)
		elif path.lower().endswith('.py'):
			if not path in exempt:
				files.append(path)
	return files

body = ''
static = ''

files = get_all_files(root)

def read_file(file):
	c = open(file, 'rt')
	t = c.read()
	c.close()
	
	parts = t.split('### STATIC ###')
	
	body = parts[0]
	static = ''
	if len(parts) > 1:
		static = parts[1]
	return (body, static)

body = read_file(imports)[0]
body += read_file(functions)[0]
static = ''

for file in files:
	code = read_file(file)
	body += '\n### ' + file + "\n\n" + code[0] + "\n"
	static += '\n### ' + file + " statics\n\n" + code[1] + "\n"

body = body + static + "\n\n" + read_file(main)[0]

c = open(pyweek_root + 'game.py', 'wt')
c.write(body)
c.close()

