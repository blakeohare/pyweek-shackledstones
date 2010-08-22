# encapsulates information about a script command
class ScriptCommand:
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
         print("ArgMismatch Exception, expecting %d args, got %s" % (self.ArgCount(), str(args)))
         
      if (len(args) == 0):
         return self.FnPtr().__call__()
      if (len(args) == 1):
         return self.FnPtr().__call__(args[0])
      return self.FnPtr().__call__(*args)

class CommandRegistry:
   def __init__(self):
      self._commands = {}
   
   # Registers a new command with the scripting engine
   # cmd ------ text name
   # fn ------- a function pointer
   # argCount - how many args to expect, basic runtime validation
   def Register(self, cmd, fn, argCount):
      self._commands[cmd] = ScriptCommand(cmd, fn, argCount)
   
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
   se = ScriptEngine()
   se.Register("test0", do_test0, 0)
   se.Register("test1", do_test1, 1)
   se.Register("test2", do_test2, 2)
   
   args = []
   se.GetCmd("test0").Call(args)
   args.append(1)
   se.GetCmd("test1").Call(args)
   args.append(3)
   se.GetCmd("test2").Call(args)

# testScript()