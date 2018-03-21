import os

import pygame
from pygame.locals import *

_STRING_TYPE = type('')
_OS_SEP = os.sep
_OS_PATH_JOIN = os.path.join

def Core_parseInt(value):
	if type(value) == _STRING_TYPE:
		return int(value)
	raise Exception("Invalid input for Core.parseInt")

Core = EmptyObj()
Core.parseInt = Core_parseInt
Core.isString = lambda x: type(x) == _STRING_TYPE

# file IO helpers used by both UserData and Resources
def read_text_file(path):
	realPath = path.replace('/', _OS_SEP)
	c = open(realPath, 'rt')
	text = c.read()
	c.close()
	return text

def write_text_file(path, content):
	realPath = path.replace('/', _OS_SEP)
	c = open(realPath, 'wt')
	c.write(content)
	c.close()

def file_exists(path):
	realPath = path.replace('/', _OS_SEP)
	return os.path.exists(realPath)

