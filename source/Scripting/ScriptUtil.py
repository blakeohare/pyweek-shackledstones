
# Is the input line a command?
# Returns:
#  False if not
#  The command name if so
def ScriptUtil_isCommand(string):
	return len(string) > 0 and string[0] == '[' and string[-1] == ']'

# Parse a script line into a tuple containing cmd and an array of args
# Returns:
#  False if not a command
#  ($cmd, $args), where args is a list
def ScriptUtil_splitCommand(string):
	if not ScriptUtil_isCommand(string):
		return False
	args = string[1:-1].split('][')
	cmd = args[0]
	args = args[1:]
	return [cmd, args]

# Loads a file into a ScriptIter
def ScriptUtil_loadFile(path):
	scr = Resources.readText(path).split('\n')
	return ScriptIter(scr)
