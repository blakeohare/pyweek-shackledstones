class Scripted:
   def __init__(self, scriptIter):
      self._script = scriptIter
      self._fnTable = {}
      
      self._addFn('comment', self._noop)
      self._addFn('label', self._noop)
      self._addFn('jump', self._jump)
      self._addFn('check', self._checkVar)
      self._addFn('set', self._set)

   def _parse(self):
      for line in self._script:
         if Parser.IsCommand(line):
            (cmd, args) = Parser.Segment(line)
            c = self._call(cmd, args)
            
            if not c:
               break
         else:
            self._parseInternal(line)

   def _parseInternal(self, line):
      print('NOT_IMPLEMENTED')
   
   def _addFn(self, name, fn):
      self._fnTable[name] = fn
   
   def _call(self, name, args):
      if name in self._fnTable:
         return self._fnTable[name](*args)
      else:
         print('%s not registered' % name)

   # Move the script on it it's a multi-part deal.  Override this if you want
   # take special actions on script resume
   def Advance(self):
      self._parse()

   # function implementations
   # return indicates if script execution should continue (True) or stop until
   # the next call to Advance(False)
   def _checkVar(self, var, test, val, label, failLabel=None):
      sval = globalState.get(var)
      if test == 'eq':
         ret = (sval == val)
      elif test == 'lt':
         ret = (sval < val)
      elif test == 'lte.':
         ret = (sval <= val)
      elif test == 'gt':
         ret = (sval > val)
      elif test == 'gte':
         ret = (sval >= val)
      if ret:
         self._script.FindLabel(label)
      else:
         if failLabel:
            self._script.FindLabel(failLabel)
      return True
   
   def _set(self, var, val):
      globalState[var] = val
      return True

   def _jump(self, label):
      self._script.FindLabel(label)
      return True

   def _noop(self, *args):
      return True