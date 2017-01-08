# Graphic-related code for the Dungeon game.

import os

def clear():
	os.system("clear")

# print(chr(27) + "[2J") #clears screen up to this line

def print_map(m):
	for line in m:
		for c in line:
			print c,

# Todo: move this to grahp.py
def render_map_dict(m_dict):
	print '>g.render_map_dict'
	(x,y) = (0,0)
	#x = 0
	#y = 0
	for (xi,yi) in m_dict:
		if x < xi:
			x = xi
		if y < yi:
			y = yi
	for xi in range(x+1):
		for yi in range(y+1):
			print m_dict[(xi,yi)],
		print ''

