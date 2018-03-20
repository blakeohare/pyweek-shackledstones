def applyMapScriptFunctions(scriptEngine):

	scriptEngine._addFn('warp', do_warp)
	scriptEngine._addFn('dialog', do_dialog)
	scriptEngine._addFn('remove tile', do_removeTile)
	scriptEngine._addFn('set tile', do_setTile)
	scriptEngine._addFn('sound', do_sound)
	scriptEngine._addFn('music', do_music)
	scriptEngine._addFn('launch cutscene', do_cutscene)
	scriptEngine._addFn('toggle mirror', do_toggle_mirror)
	scriptEngine._addFn('get key', do_getkey)
	scriptEngine._addFn('save', do_save_point)
	scriptEngine._addFn('sign', do_sign_display)
