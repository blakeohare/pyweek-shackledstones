# warp: implement for player warping
# mapFile --------- file path (relative, from base directory)
# tileId ---------- the id of the tile to warp to (alpha numeric)
# transitionStyle - how the warp is displayed, will be one of WARP_X from constants.py
def do_warp(mapFile, tileId, transitionStyle = WARP_INSTANT):
	game_scene = getActiveGame().getActiveGameScene()
	game_scene.next = TransitionScene(game_scene, mapFile, tileId, transitionStyle)

# dialog: transitions to a dialogue scene using the indicated file as script
# scriptFile - file path (relative, from base directory)
def do_dialog(scriptFile):
	pass

# remove tile: removes a tile from the map
# tileId ------ id indicating which position and layer
# detailLayer - which detail layer to remove it from
def do_removeTile(tileId, detailLayer):
	return do_setTile(tileId, detailLayer, '')

# set tile: updates the tile at a location
# posId ------- id indicating which position and layer
# detailLayer - which detail layer we're acting in
# tileTypeId -- ID of the tile to add (can be referenced from the tiles.txt file in /data/)
def do_setTile(posId, detailLayer, tileTypeId):
	game_scene = getActiveGame().getActiveGameScene()
	detailLayer = detailLayer.replace(' ', '').lower()
	if game_scene != None:
		layers = game_scene.level.layers
		ids = game_scene.level.ids
		id = ids.get(posId)
		if id == None:
			print("ERROR: " + posId + ' is not a valid tile ID on this map')
			return
		layers[id.layer].tiles[id.x][id.y].setTile(detailLayer, tileTypeId)
	return True

def do_sound(file):
	play_sound(file)

def do_music(file, loop = False):
	play_music(file)

def do_toggle_mirror(mirror_name):
	current = getActiveGame().getString('mirror_state_' + mirror_name)
	if current == 'mirror1': current = 'mirror2'
	elif current == 'mirror2': current = 'mirror3'
	elif current == 'mirror3': current = 'mirror4'
	else: current = 'mirror1'
	play_sound('mirrorrotate')
	getActiveGame().setSavedVar('mirror_state_' + mirror_name, current)

def do_switch_scene(newScene):
	game_scene = getActiveGame().getActiveGameScene()
	if newScene == 'flyaway':
		game_scene.next = SimpleAnimationScene('flyaway')
	if newScene == 'flyhome':
		game_scene.next = SimpleAnimationScene('flyhome')

def do_cutscene(cutscene):
	game_scene = getActiveGame().getActiveGameScene()
	game_scene.player.walking = False
	game_scene.cutscene = get_cutscene(cutscene)
	return True

def do_getkey(color):
	game_scene = getActiveGame().getActiveGameScene()
	dungeon = game_scene.level.dungeon
	getKeyRegistry().addKey(dungeon, color)
	return True
	
def do_save_point():
	game_scene = getActiveGame().getActiveGameScene()
	do_cutscene('save_point_routine')
	return True

def do_sign_display(text):
	lines = str(text).strip().split('$')
	i = 1
	finLines = []
	finLines.append(lines[0])
	while i < len(lines):
		finLines.append('\\n')
		finLines.append(lines[i])
		i += 1
	game_scene = getActiveGame().getActiveGameScene()
	ds = DialogScene(
		Dialog(ScriptIter(['[profile][]'] + finLines + ['[pause]','','[end]'])),
		game_scene)
	game_scene.next = ds
	game_scene.player.walking = False
	return True
	
def do_buy(item):
	price = 0
	if item == 'life':
		price = 5
		var = '_temp'
	if item == 'compass':
		price = 15
		var = 'item_compass'
	elif item == 'shovel':
		price = 20
		var = 'item_shovel'
	elif item == 'fire':
		price = 30
		var = 'item_cannon_fire'
	elif item == 'ice':
		price = 30
		var = 'item_cannon_ice'
	elif item == 'multi':
		price = 50
		var = 'item_cannon_multi'
	elif item == 'armor':
		price = 50
		var = 'has_armor'
	
	if price == 0:
		return True
	
	if has_money(price):
		getActiveGame().setTempVar('transaction_failed', 0)
		getActiveGame().setSavedVar(var, 1)
		print('set %s to 1' % str(var))
		modify_money(-price)
		if item == 'life':
			heal_damage()
			heal_damage()
			heal_damage()
			
	else:
		print('failure!')
		getActiveGame().setTempVar('transaction_failed', '1')
	
	return True

def do_go_to_credits():
	getActiveGame().getActiveGameScene().gotocredits = True

def do_save_game():
	game = getActiveGame()
	game.setSavedVar('save_map', game_scene.name)
	game.setSavedVar('save_x', game_scene.player.x)
	game.setSavedVar('save_y', game_scene.player.y)
	game.saveToFile()
