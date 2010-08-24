

class TileStore:
	def __init__(self):
		tile_file = 'data' + os.sep + 'tiles.txt'
		c = open(tile_file, 'rt')
		lines = c.read().split('\n')
		c.close()
		
		self.templates = {}
		for line in lines:
			tline = trim(line)
			if len(tline) > 0 and tline[0] != '#':
				parts = tline.split('\t')
				if len(parts) == 4 or len(parts) == 5:
					template = TileTemplate(parts)
					self.templates[template.id] = template
	
	def GetTile(self, id):
		return self.templates.get(id)
			

### STATIC ###

_tileStore = None
def get_tile_store():
	global _tileStore
	if _tileStore == None:
		_tileStore = TileStore()
	return _tileStore
	
	