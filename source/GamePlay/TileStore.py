class TileStore:
	def __init__(self):
		self.templates = {}
		
		lines = Resources.readText('data/tiles.txt').split('\n')
		for line in lines:
			tline = line.strip()
			if len(tline) > 0 and tline[0] != '#':
				parts = tline.split('\t')
				if len(parts) == 4 or len(parts) == 5:
					template = TileTemplate(parts)
					self.templates[template.id] = template
	
	def getTile(self, id):
		return self.templates.get(id)

def get_tile_store():
	global _tileStore
	if _tileStore == None:
		_tileStore = TileStore()
	return _tileStore
