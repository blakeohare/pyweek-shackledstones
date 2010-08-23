# warp: implement for player warping
# mapFile --------- file path (relative, from base directory)
# tileId ---------- the id of the tile to warp to (alpha numeric)
# transitionStyle - how the warp is displayed, will be one of WARP_X from constants.py
def do_warp(mapFile, tileId, transitionStyle = WARP_INSTANT):
   pass

cr.Register("warp", do_warp, 3)


# dialog: transitions to a dialogue scene using the indicated file as script
# scriptFile - file path (relative, from base directory)
def do_dialog(scriptFile):
   pass
   
cr.Register("dialog", do_dialog, 1)

# remove tile: removes a tile from the map
# tileId ------ the id of the tile to remove
# detailLayer - which layer to remove it from
def do_removeTile(tileId, detailLayer):
   pass
   
cr.Register('remove tile', do_removeTile, 2)

# set tile: updates the tile at a location
# posId ------- id indicating which tile
# detailLayer - which layer we're acting in
# tileTypeId -- I have no idea
def do_setTile(posId, detailLayer, tileTypeId):
   pass
cr.Register('set tile', do_setTile, 3)