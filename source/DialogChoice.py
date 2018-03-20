class DialogChoice:
	def __init__(self, txt, label):
		self._text = txt
		self._label = label
	def __str__(self):
		return '[%s] %s' % (self.Label(), self.Text())
	
	def Text(self):
		return self._text
	def Label(self):
		return self._label
