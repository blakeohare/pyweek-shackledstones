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
      self._curProfile = None
      self._state = D_NORMAL
      
      # What we should be displaying
      self._buffer = ''
      # when we have a question what are the choices?
      self._choice = []
      
      # perform the initial parse (fill the buffer)
      self._parse()
   
   # Get the path to the current profile
   def GetProfile(self):
      return self._curProfile
   
   # Find out what mode the dialogue is in
   def State(self):
      return self._state
   
   # get the next bit of stuff to display
   def Advance(self):
      sef._parse()
   
   # What we should be displaying if we're in "talk" mode (D_NORMAL)
   def Text(self):
      return self._buffer
   
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
      for line in self._script:
         if Parser.IsCommand(line):
            (cmd, args) = Parser.Segment(line)
            print("command: %s, args: %s" % (cmd, str(args)))
         else:
            print("dialogue: %s" % (line))
      pass
   
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

AddTest('testDialogue', testDialogue)