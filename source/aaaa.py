testSet = []

class Test:
	def __init__(self, name, fn):
		self._name = name
		self._fn = fn
	
	def __call__(self):
		print('\n%s\n------------------------------------------------------------' % self._name)
		self._fn()

def AddTest(name, fn):
	testSet.append(Test(name, fn))
	
def RunTests():
	for test in testSet:
		test()