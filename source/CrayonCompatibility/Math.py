import math

def Math_floor(value):
	if type(value) == _STRING_TYPE or value == None:
		raise Exception("Invalid input for Math.floor")
	return int(value)

Math = EmptyObj()
Math.cos = math.cos
Math.sin = math.sin
Math.arctan = math.atan2
Math.abs = abs
Math.floor = Math_floor
Math.max = max
Math.min = min
Math.PI = math.pi
Math.E = math.e
