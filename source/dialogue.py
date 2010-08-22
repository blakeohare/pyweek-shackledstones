D_NORMAL   = 0
D_SCAN     = 1
D_PAUSE    = 2
D_QUESTION = 3
D_CHECKVAR = 4 

class Dialague:
   # script -- ScriptIter
   def __init__(self, script):
      self._script = script
      self._state = D_NORMAL