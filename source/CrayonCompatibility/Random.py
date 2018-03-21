import random

def Random_randomInt(m): # randomInt(min, max) call pattern is not used
	return int(random.random() * m)

Random = EmptyObj()
Random.randomFloat = random.random
Random.randomInt = Random_randomInt
