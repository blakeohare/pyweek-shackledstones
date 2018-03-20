D_NORMAL = 0
D_SCAN = 1
D_PAUSE = 2
D_QUESTION = 3
D_CHECKVAR = 4 
D_END = 5

class Dialog:
	
	def __init__(self, scriptIter):
		self.scriptEngine = ScriptEngine(scriptIter, self._parseScriptedDialog, self._advancePreCheck, self._endPreCheck)
		self._profile = None
		self._state = D_NORMAL
		
		# What we should be displaying
		self._buffer = ''
		# When we're in question mode
		self._question = None
		# when we have a question what are the choices?
		self._choices = []
		
		self.scriptEngine._addFn('profile', self._setProfile)
		self.scriptEngine._addFn('pause', self._pause)
		self.scriptEngine._addFn('question', self._beginQuestion)
		self.scriptEngine._addFn('choice', self._addChoice)
		self.scriptEngine._addFn('/question', self._poseQuestion)
		self.scriptEngine._addFn('save', self._saveGame)
		
		# perform the initial parse (fill the buffer)
		self.scriptEngine.advance()
	
	# Get the path to the current profile
	def Profile(self):
		return self._profile
	
	# Find out what mode the dialog is in
	def State(self):
		return self._state
	
	# get the next bit of stuff to display
	def _advancePreCheck(self):
		# do not allow resuming if the dialog is finished
		if self.State() == D_END:
			return False
		
		self._buffer = ''
		return True
	
	# What we should be displaying if we're in "talk" mode (D_NORMAL)
	def Text(self):
		return self._buffer.strip()
	
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
		self.scriptEngine._script.FindLabel(c.Label())
	
	def _parseScriptedDialog(self, line):
		name = getActiveGame().getVar('name')
		# TODO: settle on one casing
		line = line.replace('%Name%', name).replace('%NAME%', name)
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
		self._choices.append(DialogChoice(text, label))
		return True
	
	def _saveGame(self):
		game_scene = getActiveGame().getActiveGameScene()
		getActiveGame().setSavedVar('save_map', game_scene.name)
		getActiveGame().setSavedVar('save_x', game_scene.player.x)
		getActiveGame().setSavedVar('save_y', game_scene.player.y)
		getActiveGame().saveToFile()
		return True
	
	def _poseQuestion(self):
		return False
	
	def _setProfile(self, file):
		self._profile = file
		return True
	
	# TODO: why not just set this as the end implementation via addFn? It'll overwrite it in the lookup.
	def _endPreCheck(self):
		self._state = D_END
	
	def _pause(self):
		return False
