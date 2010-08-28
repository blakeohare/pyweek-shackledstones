### STATIC ###

def create_sprite(name, id=None):
	if ' ' + name + ' ' in ' blob death eyeball skeleton death snake mechanicalman ':
		sprite = Enemy(name, id)
	else:
		sprite = NPC(name, id)
	return sprite