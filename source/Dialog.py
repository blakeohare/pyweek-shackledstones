D_NORMAL   = 0
D_SCAN     = 1
D_PAUSE    = 2
D_QUESTION = 3
D_CHECKVAR = 4 
D_END      = 5

class Dialog(Scripted):
   # script -- ScriptIter
   def __init__(self, script):
      Scripted.__init__(self, script)
      self._profile = None
      self._state = D_NORMAL
      
      # What we should be displaying
      self._buffer = ''
      # When we're in question mode
      self._question = None
      # when we have a question what are the choices?
      self._choices = []
      
      self._addFn('profile', self._setProfile)
      self._addFn('pause', self._pause)
      self._addFn('question', self._beginQuestion)
      self._addFn('choice', self._addChoice)
      self._addFn('/question', self._poseQuestion)
      
      # perform the initial parse (fill the buffer)
      self.Advance()
   
   # Get the path to the current profile
   def Profile(self):
      return self._profile
   
   # Find out what mode the dialog is in
   def State(self):
      return self._state
   
   # get the next bit of stuff to display
   def Advance(self):
      # do not allow resuming if the dialog is finished
      if self.State() == D_END:
         return
      
      self._buffer = ''
      Scripted.Advance(self)
   
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
      c = self._choices[resp]
      self._choices = []
      self._state = D_NORMAL
      self._script.FindLabel(c.Label())
   
   def _parseInternal(self, line):
      if len(line) == 0:
         return
         
      if line == '\\n':
         line = '$nl$'
      self._buffer += line + '\n'

   # function implementations
   # return indicates if script execution should continue (True) or stop until
   # the next Advance (False)
   def _beginQuestion(self, text):
      self._state = D_QUESTION
      self._choices = []
      self._buffer = text
      return True
   
   def _addChoice(self, label, text):
      self._choices.append(Choice(text, label))
      return True
   
   def _poseQuestion(self):
      return False
   
   def _setProfile(self, file):
      self._profile = file
      return True
   
   def _end(self):
      self._state = D_END
      return Scripted._end(self)
   
   def _pause(self):
      return False

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

def testDialog():
   si = Parser.LoadFile(scriptPath('test'))
   d = Dialog(si)
   
   print('----------------------')
   print('current dialog text:')
   print("'%s'" % d.Text())
   print('----------------------')
   
   d.Advance()
   print('----------------------')
   print('current dialog text:')
   print("'%s'" % d.Text())
   print('----------------------')
   
AddTest('testDialog', testDialog)