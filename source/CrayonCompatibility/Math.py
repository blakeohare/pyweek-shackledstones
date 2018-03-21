import math

Math = EmptyObj()
Math.cos = math.cos
Math.sin = math.sin
Math.arctan = lambda y, x: math.atan2(y, x)
Math.abs = abs
Math.floor = int
Math.max = max
Math.min = min
Math.PI = math.pi
Math.E = math.e
