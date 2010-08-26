### STATIC ###

def create_sprite(name, id=None):
	if ' ' + name + ' ' in ' blob ':
		sprite = Enemey(name, id)
	else:
		sprite = NPC(name, id)
	return sprite