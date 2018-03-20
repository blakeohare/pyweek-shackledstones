
# Abstration for the varying sources a script could come from
class ScriptIter:
		# script - an array of strings from any source
		def __init__(self, script):
			self._i = 0
			self._script = script

		# Utility to scan the script for a label.
		# Return:
		#  True - If the label is found, sets index such that Next 
		#			or __next__ will return the label
		#  False - If there is no label
		def FindLabel(self, label):
			idx = 0
			
			tgt = '\s*\[label\]\s*\[%s\]\s*' % (label)
			
			while (idx < len(self._script)):
				if re.match(tgt, self._script[idx]):
					self._i = idx
					return True
				idx += 1
			
			return False

		# Return the next line and step through the script
		def Next(self):
			return self.__next__()

		# Reset the script to the top
		def Reset(self):
			self._i = 0

		def __iter__(self):
			return self
		
		def next(self):
			return self.__next__()

		def __next__(self):
			idx = self._i
			if (idx >= len(self._script)):
				raise StopIteration
			
			self._i += 1
			return self._script[idx]
