# warp: implement for player warping
# mapFile --------- file path (relative, from base directory)
# tileId ---------- the id of the tile to warp to (alpha numeric)
# transitionStyle - how the warp is displayed, will be one of WARP_X from constants.py
def do_warp(mapFile, tileId, transitionStyle = WARP_INSTANT):
   pass

cr.Register("warp", do_warp, 3)


# dialogue: transitions to a dialogue scene using the indicated file as script
# scriptFile - file path (relative, from base directory)
def do_dialogue(scriptFile):
   pass
   
cr.Register("dialogue", do_dialogue, 1)