
# Is the input line a command?
# Returns:
#  False if not
#  The command name if so
def ScriptUtil_isCommand(self, string):
	m = _re_bracket.match(string)
	if m:
		return m.group(1)
	return False

# Parse a script line into a tuple containing cmd and an array of args
# Returns:
#  False if not a command
#  ($cmd, $args), where args is a list
def ScriptUtil_splitCommand(string):
	if not ScriptUtil_isCommand(string):
		return False
	
	p = _re_bracket
	m = p.match(string)
	cmd = m.group(1).strip()
	args = []
	
	while True:
		m = p.match(string, m.end())
		if not m:
			break
		args.append(m.group(1).strip())
	
	return [cmd, args]

# Loads a file into a ScriptIter
def ScriptUtil_loadFile(path):
	scr = read_text_file(path).split('\n')
	return ScriptIter(scr)
