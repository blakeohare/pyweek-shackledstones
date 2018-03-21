# The world is a happy place

GAME_NAME = "Shackled Stones"

TILE_COLUMN_COUNT = 24
TILE_ROW_COUNT = 18

SCREEN_WIDTH = TILE_COLUMN_COUNT * 16
SCREEN_HEIGHT = TILE_ROW_COUNT * 16

WARP_NSCROLL = "north scroll"
WARP_SSCROLL = "south scroll"
WARP_ESCROLL = "east scroll"
WARP_WSCROLL = "west scroll"
WARP_PIXELATE = "pixelate"
WARP_INSTANT = "instant"
WARP_FADE = "fade"

KEY_LEFT = 'left'
KEY_RIGHT = 'right'
KEY_UP = 'up'
KEY_DOWN = 'down'

WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
BLUE = [0, 0, 255]
RED = [255, 0, 0]

D_TEXT_OFFSET_X = 13
D_ANSWER_OFFSET_X = 25
D_TEXT_OFFSET_Y = 198

# not constants, but globals.
# technically since this is Python, the above aren't constants either.
_gameContext = None
_jukebox = None
_inputManager = None
_temp_screen_for_transitions = None
_temp_screens = { }
_tileStore = None
_key_registry = None
_fontEngine = None

# TODO: this shouldn't be here. It should at least be tied to either the game instance or the current map.
_invincible = False

_defaultMirror = {
	'A' : 'mirror1',
	'B' : 'mirror2',
	'C' : 'mirror3',
	'D' : 'mirror4',
	'E' : 'mirror1',
	'F' : 'mirror2',
	'G' : 'mirror3',
	'H' : 'mirror4',
	'I' : 'mirror1',
	'J' : 'mirror2',
	'K' : 'mirror3',
	'L' : 'mirror4',
	'M' : 'mirror1',
	'N' : 'mirror3'
}

_cutSceneStore = { }

_play_once = {
	'interrogation' : False,
	'at_water_temple' : False,
}

_bulletSwitches = {
	'Fire_Room2' : ['switch'],
	'Fire_Key1' : ['switch_B'],
	'light_rightroom_b1' : ['switch'],
	'light_south_southroom' : ['switch_left','switch_right'],
	'light_southroom_b1' : ['switch'],
	'light_bosshall_f1' : ['left','right'],
	'world_bridge' : ['switch']
}

_grapple_singleton = None

class EmptyObj:
	pass