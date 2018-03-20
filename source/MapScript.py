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
		self._addFn('save', do_save_point)
		self._addFn('sign', do_sign_display)
	
	# get the next bit of stuff to display
	def advance(self):
		return Scripted.advance(self)
	
	# fancy name so it makes more sense
	def execute(self):
		return self.advance()
	
	def _parseInternal(self, line):
		print('MapScript._parseInternal(%s)' % line)

	# function implementations
	# return indicates if script execution should continue (True) or stop until
	# the next Advance (False)
	def _end(self):
		# what to do?
		return Scripted._end(self)
