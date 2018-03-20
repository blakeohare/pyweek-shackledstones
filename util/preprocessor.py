import os

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

def read_file(file):
	c = open(file, 'rt')
	text = c.read()
	c.close()
	return text

pyweek_root = '.' + os.sep

imports = pyweek_root + 'source' + os.sep + 'imports.py'
main = pyweek_root + 'source' + os.sep + 'main.py'
functions = pyweek_root + 'source' + os.sep + 'functions.py'
constants = pyweek_root + 'source' + os.sep + 'constants.py'
exempt = [imports, main, functions, constants]

root = pyweek_root + 'source'

body = []

files = get_all_files(root)

body.append(read_file(imports))
body.append(read_file(constants))
body.append(read_file(functions))

for file in files:
	body.append('\n### ' + file + "\n\n")
	body.append(read_file(file))
	body.append("\n")

body.append('\n### main.py\n\n')	
body.append(read_file(main))
body.append("\n")

c = open(pyweek_root + 'game.py', 'wt')
c.write('\n'.join(body))
c.close()

