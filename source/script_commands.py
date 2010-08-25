# warp: implement for player warping
# mapFile --------- file path (relative, from base directory)
# tileId ---------- the id of the tile to warp to (alpha numeric)
# transitionStyle - how the warp is displayed, will be one of WARP_X from constants.py
def do_warp(mapFile, tileId, transitionStyle = WARP_INSTANT):
   game_scene = ActiveGame().GetActiveGameScene()
   game_scene.next = TransitionScene(game_scene, mapFile, tileId, transitionStyle)

cr.Register("warp", do_warp, 3)


# dialog: transitions to a dialogue scene using the indicated file as script
# scriptFile - file path (relative, from base directory)
def do_dialog(scriptFile):
   pass
   
cr.Register("dialog", do_dialog, 1)

# remove tile: removes a tile from the map
# tileId ------ id indicating which position and layer
# detailLayer - which detail layer to remove it from
def do_removeTile(tileId, detailLayer):
	do_setTile(tileId, detailLayer, '')
   
cr.Register('remove tile', do_removeTile, 2)

# set tile: updates the tile at a location
# posId ------- id indicating which position and layer
# detailLayer - which detail layer we're acting in
# tileTypeId -- ID of the tile to add (can be referenced from the tiles.txt file in /data/)
def do_setTile(posId, detailLayer, tileTypeId):
	game_scene = ActiveGame().GetActiveGameScene()
	detailLayer = detailLayer.replace(' ', '').lower()
	if game_scene != None:
		layers = game_scene.level.layers
		ids = game_scene.level.ids
		id = ids.get(posId)
		if id == None:
			print("ERROR: " + posId + ' is not a valid tile ID on this map')
			return
		layers[id.layer].tiles[id.x][id.y].SetTile(detailLayer, '')

cr.Register('set tile', do_setTile, 3)

def do_sound(file):
   pass

def do_music(file, loop = False):
   pass

def do_switch_scene(newScene):
   pass