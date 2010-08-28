class Scripted:
   def __init__(self, scriptIter):
      if not isinstance(scriptIter, ScriptIter):
         raise Exception("scriptIter must be an object of type ScriptIter")
      self._script = scriptIter
      self._fnTable = {}
      
      self._addFn('comment', self._noop)
      self._addFn('label', self._noop)
      self._addFn('jump', self._jump)
      self._addFn('check', self._checkVar)
      self._addFn('set', self._set)
      self._addFn('end', self._end)
      self._addFn('switch scene', do_switch_scene)
      self._addFn('buy', do_buy)

   def _parse(self):
      for line in self._script:
         print(line)
         if Parser.IsCommand(line):
            (cmd, args) = Parser.Segment(line)
            if self._fnTable.get(cmd):
               c = self._call(cmd, args)
               
               if not c:
                  break
            else:
               print('Unrecognized command: %s' % cmd)
         else:
            self._parseInternal(line)

   def _parseInternal(self, line):
      print('NOT_IMPLEMENTED, dropping %s' % line)
   
   def _addFn(self, name, fn):
      self._fnTable[name] = fn
   
   def _call(self, name, args):
      if name in self._fnTable:
         return self._fnTable[name](*args)
      else:
         print('%s not registered' % name)

   # Move the script on if it's a multi-part deal.  Override this if you want
   # take special actions on script resume
   def Advance(self):
      self._parse()

   # function implementations
   # return indicates if script execution should continue (True) or stop until
   # the next call to Advance(False)
   def _checkVar(self, var, test, val, label, failLabel=None):
      sval = ActiveGame().GetVar(var)
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
      ag = ActiveGame().SetSavedVar(var, val)
      return True

   def _jump(self, label):
      self._script.FindLabel(label)
      return True

   def _noop(self, *args):
      return True
   
   def _end(self):
      return False