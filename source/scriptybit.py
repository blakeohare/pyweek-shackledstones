# uncomment for testing

class ParserClass:
   def __init__(self):
      self._re_bracket = re.compile('\s*\[(.*?)\]')
   
   # Is the input line a command?
   # Returns:
   #  False if not
   #  The command name if so
   def IsCommand(self, string):
      m = self._re_bracket.match(string)
      if m:
         return m.group(1)
      return False
   
   # Parse a script line into a tuple containing cmd and an array of args
   # Returns:
   #  False if not a command
   #  ($cmd, $args), where args is a list
   def Segment(self, string):
      if not self.IsCommand(string):
         return False
      
      p = self._re_bracket
      m = p.match(string)
      cmd = trim(m.group(1))
      args = []
      
      while True:
         m = p.match(string, m.end())
         if not m:
            break
         args.append(trim(m.group(1)))
      
      return (cmd, args)
Parser = ParserClass()

# Abstration for the varying sources a script could come from
class ScriptIter:
      # script - an array of strings from any source
      def __init__(self, script):
         self._i = 0
         self._script = script

      # Utility to scan the script for a label.
      # Return:
      #  True - If the label is found, sets index such that Next 
      #         or __next__ will return the label
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


# encapsulates information about a script command
class Command:
   # cmd ------ text name
   # fn ------- a function pointer
   # argCount - how many args to expect, basic runtime validation
   def __init__(self, cmd, fn, argCount):
      self._name = cmd
      self._fnPtr = fn
      self._argCount = argCount
   
   def Name(self):
      return self._name
   
   def FnPtr(self):
      return self._fnPtr
   
   def ArgCount(self):
      return self._argCount

   # Call this function
   # args - a list of the arguments to call the function with
   def Call(self, args):
      if (len(args) != self.ArgCount()):
         print("ArgMismatch Exception...")
         print("    %s expects %d args" % (self.Name(), self.ArgCount()))
         print("    got '%s'" % (str(args)))
         
      return self.FnPtr().__call__(*args)


# associates strings with function pointers
class CommandRegistry:
   def __init__(self):
      self._commands = {}
   
   # Registers a new command with the scripting engine
   # cmd ------ text name
   # fn ------- a function pointer
   # argCount - how many args to expect, basic runtime validation
   def Register(self, cmd, fn, argCount):
      self._commands[cmd] = Command(cmd, fn, argCount)
   
   # Get a ScriptCommand based on it's name or None if we can't find it
   # cmd - the command to retrieve
   def GetCmd(self, cmd):
      if cmd in self._commands:
         return self._commands[cmd]
      else:
         print("Could not find command %s" % (str(cmd)))
         return None

class ScriptEngine:
   def __init__(self):
      pass
   
# declare globals
cr = CommandRegistry()
se = ScriptEngine()

###############################################################################
# Testing code

def do_test0():
   print("test0")

def do_test1(a):
   print("test1 arg: %s" % (str(a)))

def do_test2(a, b):
   print("test2 arg: %s and %s" % (str(a), str(b)))

def testScript():
   c = CommandRegistry()
   c.Register("test0", do_test0, 0)
   c.Register("test1", do_test1, 1)
   c.Register("test2", do_test2, 2)
   
   args = []
   c.GetCmd("test0").Call(args)
   args.append(1)
   c.GetCmd("test1").Call(args)
   args.append(3)
   c.GetCmd("test2").Call(args)
if testCode:
   testScript()

def testScriptIter():
   scr = ['aoeu1', 'aoeu2', 'aoeu3', '[label]  [testing]    ', 'aoeu4', 'aoeu5', 'aoeu6', 'aoeu7']
   si = ScriptIter(scr)
   
   for a in si:
      print(a)
   
   print("---------------------------")
   
   si.FindLabel('testing')
   print(si.Next())
   print(si.Next())
   print(si.Next())
   print("---------------------------")
   si.FindLabel('aoeuaoeu')
   
   for a in si:
      print(a)
if testCode:
   testScriptIter()

def testParser():
   tests = ['[jump][fin]', '[check][script-state][eq][done][script-code-done]', 'test', '[end]']
   for a in tests:
      ret = Parser.Segment(a)
      print(ret)

if testCode:
   testParser()