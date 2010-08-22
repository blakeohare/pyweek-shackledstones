D_NORMAL   = 0
D_SCAN     = 1
D_PAUSE    = 2
D_QUESTION = 3
D_CHECKVAR = 4 
D_END      = 5

class Dialogue:
   # script -- ScriptIter
   def __init__(self, script):
      self._script = script
      self._profile = None
      self._state = D_NORMAL
      
      # What we should be displaying
      self._buffer = ''
      # when we have a question what are the choices?
      self._choice = []
      
      self._fnTable = {}
      self._addFn('comment', self._comment) # this should be a lambda
      self._addFn('profile', self._setProfile)
      self._addFn('pause', self._pause)
      
      # perform the initial parse (fill the buffer)
      self._parse()
   
   # Get the path to the current profile
   def Profile(self):
      return self._profile
   
   # Find out what mode the dialogue is in
   def State(self):
      return self._state
   
   # get the next bit of stuff to display
   def Advance(self):
      self._parse()
   
   # What we should be displaying if we're in "talk" mode (D_NORMAL)
   def Text(self):
      return trim(self._buffer)
   
   # what choices are available
   def Choices(self):
      if self.State() != D_QUESTION:
         print("ERR: Not in Question mode")
      options = []
      for a in self._choices:
         options.append(a.Text())
      return options
   
   # Answer a question
   # resp - which choice the user went with
   def Answer(self, resp):
      pass
   
   def _parse(self):
      self._buffer = ''
      for line in self._script:
         if Parser.IsCommand(line):
            (cmd, args) = Parser.Segment(line)
            c = self._call(cmd, args)
            print("command: %s\n   args: %s\n   returns: %s" % (cmd, str(args), str(c)))
            
            if not c:
               break
         else:
            if len(line) == 0:
               continue
            if line == '\\n':
               line = '\n'
            self._buffer += line + '\n'

   def _addFn(self, name, fn):
      self._fnTable[name] = fn
   
   def _call(self, name, args):
      if name in self._fnTable:
         return self._fnTable[name](*args)
      else:
         print('%s not registered' % name)

   # function implementations
   # return indicates if script execution should continue (True) or stop until
   # the next Advance (False)
   def _setProfile(self, file):
      self._profile = file
      return True
   
   def _pause(self):
      return False

   def _comment(self):
      return True

class Choice:
   def __init__(self, txt, label):
      self._text = txt
      self._label = label
   def __str__(self):
      return '[%s] %s' % (self.Label(), self.Text())
   
   def Text(self):
      return self._text
   def Label(self):
      return self._label
   
###############################################################################
# Testing Code

def testDialogue():
   si = Parser.LoadFile(scriptPath('test'))
   d = Dialogue(si)
   
   print('----------------------')
   print('current dialogue text:')
   print("'%s'" % d.Text())
   print('----------------------')
   
   d.Advance()
   print('----------------------')
   print('current dialogue text:')
   print("'%s'" % d.Text())
   print('----------------------')
   
AddTest('testDialogue', testDialogue)