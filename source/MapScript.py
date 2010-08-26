class MapScript(Scripted):
   # script -- ScriptIter
   def __init__(self, scriptIter):
      Scripted.__init__(self, scriptIter)
      self._addFn('warp', do_warp)
      self._addFn('dialog', do_dialog)
      self._addFn('remove tile', do_removeTile)
      self._addFn('set tile', do_setTile)
      self._addFn('sound', do_sound)
      self._addFn('music', do_music)
      self._addFn('launch cutscene', do_cutscene)
      self._addFn('toggle mirror', do_toggle_mirror)
      self._addFn('get key', do_getkey)
   
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
   def _end(self):
      # what to do?
      return Scripted._end(self)
   
   