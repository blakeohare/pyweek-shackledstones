
# Abstration for the varying sources a script could come from
class ScriptIter:
	# script - an array of strings from any source
	def __init__(self, script):
		lines = []
		# TODO: parse the entire script
		self.labels = {}
		for line in script:
			line = line.strip()
			if line != '' and not line.startswith('[comment]'):
				if ScriptUtil_isCommand(line):
					t = ScriptUtil_splitCommand(line)
					if t[0] == 'label':
						self.labels[t[1][0]] = len(lines)
				
				lines.append(line)
		
		self._i = 0
		self._script = lines

	# Utility to scan the script for a label.
	# Returns True if the label is found, sets index such that next() will return the label.
	# Returns False if there is no label.
	def FindLabel(self, label):
		index = self.labels.get(label)
		if index == None:
			return False
		self._i = index
		return True
	
	def next(self):
		idx = self._i
		if (idx >= len(self._script)):
			return None
		
		self._i += 1
		return self._script[idx]
