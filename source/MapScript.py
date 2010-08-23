class MapScript(Scripted):
   # script -- ScriptIter
   def __init__(self, scriptIter):
      Scripted.__init__(self, scriptIter)
   
   # get the next bit of stuff to display
   def Advance(self):
      return Scripted.Advance(self)
   
   # fancy name so it makes more sense
   def Exec(self):
      return self.Advance()
   
   def _parseInternal(self, line):
      print('MapScript._parseInternal(%s)' % line)

   # function implementations
   # return indicates if script execution should continue (True) or stop until
   # the next Advance (False)